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
import org.opendc.experiments.provisioner.Provisioner
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
        val childName = "${scenario.topology.name}.txt"
        val fileTopology = File(envPath, childName)

        /*
        Here, we ===CONFIGURE THE TOPOLOGY===, we are basically setting up the experiment
        in this case, our topology has (by default) 8 CPUs, with frequency 3200,
        one memory with 128000 size and no storage/net (is net = network?)
         */
        val topology = clusterTopology(fileTopology)
        val allocationPolicy = scenario.allocationPolicy

        Provisioner(dispatcher, seed).use { provisioner ->

            val computeService = setupComputeService(
                SERVICE_DOMAIN,
                {
                    createComputeScheduler(
                    allocationPolicy,
                    Random(it.seeder.nextLong())
                )}
            )
            val hosts = setupHosts(SERVICE_DOMAIN, topology, optimize = true)
            provisioner.runSteps(computeService, hosts)

            if (outputPath != null) {
                val partitions = scenario.partitions + ("seed" to seed.toString())
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
            val vms = scenario.workload.source.resolve(workloadLoader, Random(seed))
            val operationalPhenomena = scenario.operationalPhenomena
            val failureModel =
                if (operationalPhenomena.failureFrequency > 0) {
                    grid5000(Duration.ofSeconds((operationalPhenomena.failureFrequency * 60).roundToLong()))
                } else {
                    null
                }

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

            //val file = File("output/trace-${Math.random().toString()}-${vm1.uid}.csv").bufferedWriter()
            val file = File("output/trace.csv").bufferedWriter()
            file.write("Usage,Deadline,Cores\n")
            for (i in usageCol.indices) {
                file.write("${usageCol[i]}, ${deadlineCol[i]}, ${coresCol[i]}\n")
            }
            file.close()

            service.replay(timeSource, vms, seed, failureModel = failureModel, interference = operationalPhenomena.hasInterference)
        }
    }
}
