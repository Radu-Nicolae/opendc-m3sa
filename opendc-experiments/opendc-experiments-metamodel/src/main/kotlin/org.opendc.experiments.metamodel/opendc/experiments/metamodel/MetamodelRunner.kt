/*
 * Copyright (c) 2022 AtLarge Research
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package org.opendc.experiments.metamodel

import org.opendc.compute.service.ComputeService
import org.opendc.experiments.metamodel.model.Scenario
import org.opendc.experiments.metamodel.topology.clusterTopology
import org.opendc.experiments.compute.ComputeWorkloadLoader
import org.opendc.experiments.compute.createComputeScheduler
import org.opendc.experiments.compute.export.parquet.ParquetComputeMonitor
import org.opendc.experiments.compute.grid5000
import org.opendc.experiments.compute.registerComputeMonitor
import org.opendc.experiments.compute.replay
import org.opendc.experiments.compute.setupComputeService
import org.opendc.experiments.compute.setupHosts
import org.opendc.experiments.compute.topology.HostSpec
import org.opendc.experiments.provisioner.Provisioner
import org.opendc.experiments.provisioner.ProvisioningStep
import org.opendc.simulator.kotlin.runSimulation
import java.io.File
import java.time.Duration
import java.util.Random
import kotlin.math.roundToLong

/**
 * Helper class for running the Metamodel experiments.
 *
 * @param envPath The path to the directory containing the environments.
 * @param tracePath The path to the directory containing the traces.
 * @param outputPath The path to the directory where the output should be written (or `null` if no output should be generated).
 */
public class MetamodelRunner(
    private val envPath: File,
    tracePath: File,
    private val outputPath: File?
) {
    /**
     * The [ComputeWorkloadLoader] to use for loading the traces.
     */
    private val workloadLoader = ComputeWorkloadLoader(tracePath)
    private val SERVICE_DOMAIN = "compute.opendc.org"

    /**
     * Run a single [scenario] with the specified seed.
     */
    fun runScenario(scenario: Scenario, seed: Long) = runSimulation {
        val childName = "${scenario.topology.name}.txt" // name of the file with experiment config
        val fileTopology = File(
            envPath,
            childName
        ) // from name to path - for now, just single.txt and multi.txt, with configuration in the file

        /*
        Here, we ===CONFIGURE THE TOPOLOGY===, we are basically setting up the experiment in this case, our topology
        has (by default) 8 CPUs, with frequency 3200, one memory with 128000 size and no storage/net (is net = network?)
        all of these, we take from the configuration file, aforementioned
         */
        val topology = clusterTopology(fileTopology) // using the data from the file, we create the topology
        val allocationPolicy = scenario.allocationPolicy // the policy used to allocate resources e.g., active-servers

        /*
        a provisioner is a helper class to set up the experimental environment, using a simulation dispatcher (see below),
        a seeder, and a service registry (i.e. a map of services)

        A {@link Dispatcher} is used in OpenDC to schedule the execution of future tasks over potentially multiple threads.
         */
        Provisioner(dispatcher, seed).use { provisioner ->
            val experimentSetup = setupExperiment(allocationPolicy, topology)
            val computeService = experimentSetup.first
            val hosts = experimentSetup.second

            // this is the place where we run the steps to configure the experiment
            provisioner.runSteps(computeService, hosts)

            // configuring the model
            if (outputPath != null) {
                // we append to the partition map, we set the topology, the workload, and the seed
                val partitions = scenario.partitions + ("seed" to seed.toString())

                // we create a path for the partition (e.g., "topology=single/workload=bitbrains-small/seed=0")
                val partition = partitions.map { (k, v) -> "$k=$v" }.joinToString("/")

                val parquetComputeMonitor = ParquetComputeMonitor(
                    outputPath,
                    partition,
                    bufferSize = 4096
                )

                val registerComputeMonitor = registerComputeMonitor(
                    SERVICE_DOMAIN,
                    parquetComputeMonitor
                )
                provisioner.runStep(registerComputeMonitor)
            }

            val service = provisioner.registry.resolve(SERVICE_DOMAIN, ComputeService::class.java)!!

            // we are still configuring here
            val vms = scenario.workload.source.resolve(workloadLoader, Random(seed))
            val operationalPhenomena = scenario.operationalPhenomena
            val failureModel =
                if (operationalPhenomena.failureFrequency > 0) {
                    grid5000(Duration.ofSeconds((operationalPhenomena.failureFrequency * 60).roundToLong()))
                } else {
                    null
                }


            /*
            the following chunk of code was written for debugging purposes and understanding the code
             */

            // CODE CHUNK START
            val vm1 = vms.first()

            println("ID: " + vm1.uid + "CPU Count: " + vm1.cpuCount)
            println("CPU Capacity: " + vm1.cpuCapacity)
            println("Memory Capacity: " + vm1.memCapacity)
            println("Total Load: " + vm1.totalLoad)
            println("Start Time: " + vm1.startTime)
            println("Stop Time: " + vm1.stopTime)
            println("Trace: " + vm1.trace)
            println("Interference Profile: " + (vm1.interferenceProfile ?: "None"))

            val usageCol = vm1.trace.usageCol // todo: review!
            val deadlineCol = vm1.trace.deadlineCol // when does the experiment end
            val coresCol = vm1.trace.coresCol // how many cores are used at a given time

            //val file = File("output/trace-${Math.random().toString()}-${vm1.uid}.csv").bufferedWriter() // prevents writing on the same file
            val file = File("output/trace.csv").bufferedWriter()
            file.write("Usage,Deadline,Cores\n")
            for (i in usageCol.indices) {
                file.write("${usageCol[i]}, ${deadlineCol[i]}, ${coresCol[i]}\n")
            }
            file.close()
            // CODE CHUNK END



            // up until now, all we did was configuration, now we are actually running the experiment
            service.replay( // replay launches the servers
                timeSource, // used to align the running jobs~, we use this to make sure everything stars at the same time, and we can compare (we use the same clock - like the CPU)
                vms, // all the jobs that need to be run
                seed, // a seed
                failureModel = failureModel, //
                interference = operationalPhenomena.hasInterference
            )
        }
    }

    fun setupExperiment(allocationPolicy: String, topology: List<HostSpec>): Pair<ProvisioningStep, ProvisioningStep> {
        /*
            after executing compute service will have
            - the service domain (compute.opendc.org)
            - the scheduler (configured with the allocation policy)
            - the scheduling quantum (i.e. the time interval / quantum / granularity of the scheduler) (e.g., PT5M = 300s)
             */
        val computeService = setupComputeService(
            SERVICE_DOMAIN,
            {
                createComputeScheduler( // this function configures the scheduler,
                    allocationPolicy, //taking the allocation policy as filters,
                    Random(it.seeder.nextLong()) // and the random as weighers
                    // we do not give any placement policy, so it is empty (placement = where to put the VMs?)
                )
            }
        )
        println("Compute Service: $computeService")

        /*
        after executing setupHosts will have:
        - a service domain (same as above - "compute.opendc.org")
        - specs (a list of HostSpec - with only one element??) containing:
            - uid (a unique identifier for the host)
            - name (e.g., node-A01-0)
            - meta (a map of key-values, e.g., "cluster" -> "A01")
            - model (basically what we setted up earlier, with direct linking to a files like "single.txt")
            - a "psuFactory" (psu = power supply unit?) - with the idlePower, the maxPower, and the factor (factor depends on model type? linear/quadratic/sqrt/etc??)
            - a "multiplexerFactory" (but the class has no field? why do we need it?)
         */

        val hosts = setupHosts(SERVICE_DOMAIN, topology, optimize = true)

        // return both the compute service and hosts
        return Pair(computeService, hosts)
    }
}
