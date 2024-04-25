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

@file:JvmName("ScenarioCli")

package org.opendc.experiments.scenario

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.options.default
import com.github.ajalt.clikt.parameters.options.defaultLazy
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.types.file
import com.github.ajalt.clikt.parameters.types.int
import org.opendc.experiments.base.models.scenario.getScenario
import org.opendc.experiments.base.models.scenario.getScenarioSpec
import org.opendc.experiments.base.runner.runScenario
import java.io.File
import kotlin.io.path.Path

/**
 * Main entrypoint of the application.
 */
public fun main(args: Array<String>): Unit = ScenarioCommand().main(args)

/**
 * Represents the command for the Scenario experiments.
 */
internal class ScenarioCommand : CliktCommand(name = "scenario") {
    /**
     * The path to the environment directory.
     */
    private val scenarioPath by option("--scenario-path", help = "path to scenario file")
        .file(canBeDir = false, canBeFile = true)
        .defaultLazy { File("resources/scenario.json") }

    /**
     * The number of threads to use for parallelism.
     */
    private val parallelism by option("-p", "--parallelism", help = "number of worker threads")
        .int()
        .default(Runtime.getRuntime().availableProcessors() - 1)

    override fun run() {
        // TODO: clean the simulation-results folder?

        val scenarios = getScenario(scenarioPath)

        // create an output folder with the simulationName

        setupOutputFolder()
        for (scenario in scenarios) {
            scenario.outputFolder = "output/${getScenarioSpec(scenarioPath.toString()).name}/"
        }

        runScenario(scenarios, parallelism)
        // TODO: implement outputResults(scenario) // this will take the results, from a folder, and output them visually

        analyzeResults()
    }

    private fun setupOutputFolder(){
        val scenarioSpecName = getScenarioSpec(scenarioPath.toString()).name
        val folderPath = "output/${scenarioSpecName}"
        val trackrPath = folderPath + "/trackr.json"
        val simulationAnalysisPath = folderPath + "/simulation-analysis/"
        val energyAnalysisPath = simulationAnalysisPath + "/energy-analysis/"
        val emissionsAnalysisPath = simulationAnalysisPath + "/emissions-analysis/"

        File(folderPath).mkdir()
        File(trackrPath).createNewFile()
        File(simulationAnalysisPath).mkdir()
        File(energyAnalysisPath).mkdir()
        File(emissionsAnalysisPath).mkdir()
    }

    private fun analyzeResults() {
        // Define the path to the 'analyzr.py' script
        val pythonScriptPath = Path("../opendc-analyzr/src/main.py").toAbsolutePath().normalize()

        // The project root should be two levels up from the 'main.py' script
        val projectRootPath = pythonScriptPath.parent.parent.toFile()

        // Start the process with the project root as the working directory
        val process = ProcessBuilder("python3", pythonScriptPath.toString())
            .directory(projectRootPath)
            .start()

        // Wait for the process to complete and check for errors
        val exitCode = process.waitFor()
        if (exitCode != 0) {
            val errors = process.errorStream.bufferedReader().readText()
            println("Errors: $errors")
        }
    }



}
