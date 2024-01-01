# <span style="color:lime">TODO</span>

## <span style="color:green">Input configuration</span>
### 1. Workload class
Update the workload class such that it takes also the allocation policy, update the scenario data structure too
<br>1.1 Results: will make it easier to create a list of running workloads

### 2. Txt files
2.1 Create an input-single.txt file that takes the configuration of the single experiment
2.2 Create an multi-single.txt file that takes the configuration of the multi experiment

### 3. Input integration
3.1 Integrate the txt files as input for the actual code (hint in MetamodelPortfolio.kt)
3.2 Add some duktape and link the new integration with the actual process running  


<br>
<hr>

## <span style="color:green">Output configuration</span>
### 4. Output file name
4.0 Find a good, suitable naming schema
<br>
4.1 Seek where we define data.parquet as name, and update the name accordingly

### 5. Link to notebook
5.1 Link to notebook such that the notebook handles a static number of output files
5.2 Handle a dynamic number of files
