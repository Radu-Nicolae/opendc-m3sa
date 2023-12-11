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

package org.opendc.experiments.metamodel.portfolio

import org.opendc.experiments.metamodel.model.OperationalPhenomena
import org.opendc.experiments.metamodel.model.Scenario
import org.opendc.experiments.metamodel.model.Topology
import org.opendc.experiments.metamodel.model.Workload
import org.opendc.experiments.compute.sampleByLoad
import org.opendc.experiments.compute.trace

/**
 * A [Portfolio] that explores the difference between horizontal and vertical scaling.
 */
public class MetamodelPortfolio : Portfolio {
    private val topologies = listOf(
        Topology("single"),
        Topology("multi"),
    )

    private val workloads = listOf( // bitbrains small is a short trace collected from bitbrains (now Solvinity)
        Workload("bitbrains-small", trace("trace").sampleByLoad(1.0)),
    )
    private val operationalPhenomena = OperationalPhenomena(0.0, false)
    private val allocationPolicy = "active-servers"

    private val energyModel = "linear"
    private val energyModel1 = "quadratic"
    private val idleEnergy = 150;  // should be actually gotton from "somewhere reliable"
    private val maxEnergy = 250; //ish


    // sub-sub model here
    override val scenarios: Iterable<Scenario> = topologies.flatMap { topology ->
        workloads.map { workload ->
            Scenario(
                topology,
                energyModel,
                workload,
                operationalPhenomena,
                allocationPolicy,
                mapOf("topology" to topology.name, "workload" to workload.name)
            )
        }
    }

    // a model in OpenDC is composed of multiple of these models
    // model = scenario + workload + topology + operationalPhenomena + allocationPolicy + energyModel
    // each of them is a model that lead to a big hierarchical model

    // todo: find the "big" model, that merges all of these models together
    // 1. Identify which would be these OpenDC models (the big models) and idenfitfy / explain what it is comprised of (the sub-models)
    // 2. During 1 - look at topologies (keep the scenarios and workload as "given data"), keep the operationalPhenomena and allocationPolicy as
    // experimental data (which might set with different values from experiment to experiment)

    // Topology
    // Level 1 hierarchy: datacenter = 1 up to n multiple clusters //todo check if there is any networking handled
    // Level 2: cluster is 1 up to n homogenous servers
    // Level 3: a server is 1 up to n components (I can add a model here)
    // Level 4: components are 1 up to n CPUs, or GPUs, or... //todo check which are currently supported
    // clusters of homogeonous resources and we support multiple clusters in the same dataset

    // Energy model - the focus of the work
    // Also a hierarchy
    // Level 4: a simple piece-wise model resource-by-resource where for each resource we can use a workload/load
    // dependent energy model one of ... (linear, quadratic, square...) (I can add a model here)
    // conceptual improval: look at the family of energy models, and decide if you want to extend the family (e.g., make new energy models)

    // In level 3 & 2 & 1: (focus on level 3): look for Andrew Chien & Ricardo Bianchini 's energy uses in datacenters (survey their work
    // and identify possible things / options that can be integrated in openDC) - enumerate those options, and synthesise later with @Alexandru

    // Energy metamodel
    // combines multiple energy models, at each step in time, predicts the energy use, but not for a specific situation
    // rather as a summary (for a range)
    // ultimately, multiple metamodels, e.g., one computing quartiles, one means, etc. and make statistics with these

    // Topology
    // Level 1 hierarchy: will describe this (understand better and provide a background), but not change it



}
