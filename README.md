[![Snakemake](https://img.shields.io/badge/snakemake-≥9.11.4-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)

# Welcome to TE_Bench
## A Snakemake workflow associated with the manuscript *TE_Bench: A Foundational Benchmarking Workflow for Transposable Element Discovery Pipelines* (submitted).

![All](https://github.com/hkania/TE_Bench/blob/8ab2e67c1f3254b358f0668d886f99d07e4c8616/.images/Full_WorkflowMay18.png?raw=true)
# Guides
The [Quickstart Guide](https://github.com/hkania/TE_Bench/blob/main/README.md#quick-start-guide) details how to download and test the associated Snakemake workflows. 

The [User Guide](https://github.com/hkania/TE_Bench#user-guide) details how to run the workflows with non-test data.

The [TE Discovery Illustrative Example](https://github.com/hkania/TE_Bench#te-discovery) shows how to use three TE annotation pipelines with TE_Bench.

* We regret we are unable to provide specific download instructions beyond those below. There are many resources available online if you run into computing environments beyond those described here.

# Quick Start Guide
## TE_Bench Installation
_We recommend cloning TE_Bench to a cluster environment with SLURM, as Simulation and Annotation Generation (Stages 1 & 2) are configured to work with the SLURM job manager on HPC. You can use other executors/plugins, but we **do not** provide instructions to do so. More information can be found [here](https://snakemake.github.io/snakemake-plugin-catalog/index.html) _(external, unmonitored link)_._

1. Clone the repository to your cluster _**HIGHLY RECOMMENDED**_ or your local computer
* If you have git installed (recommended)
> ```
> git clone https://github.com/hkania/TE_Bench.git
> ```

* If you do not have git installed, you can also use wget
> ```
> wget https://github.com/hkania/TE_Bench/archive/refs/heads/main.zip
> gunzip TE_Bench
> ```

* Or you can perform a basic download on your local computer or cluster (_**least recommended**_)
  * Click the down arrow next to the 'Code' button at the top of this repository and downlaod the zip file.

2. Generate the TE_Bench Snakemake conda environment
* We use Snakemake version 9.11.4 with the provided snakemake.yml file.

* Navigate into your unzipped TE_Bench repository and type the following command that assumes you have a miniconda installation.
> ```
> conda env create -f snakemake.yaml
> ```
> This command will create an environment called TE_Bench.

3. Download the test data while in your TE_Bench folder.

  _Since GitHub does not include files >50MB in clones, these are the steps to acquire the input files necessary for Quickstart!_

* If you have git LFS (large file storage) installed
> ```
> git lfs pull
> tar -xvf input.tar.gz
> ```

* If you do not have git LFS, you can still wget the input file.

> ```
> wget https://github.com/hkania/TE_Bench/raw/refs/heads/main/input.tar.gz
> tar -xvf input.tar.gz
> ```

* If both the above do not work for you, download `input.tar.gz` from the Duke Research Data Repository [doi.org/10.7924/r4r509](https://doi.org/10.7924/r4r509)
  * If you get a 403 Forbidden Error when trying to access the above link, try to manually paste `https://doi.org/10.7924/r4r509` into your browser. The server may be experiencing a security block.
  * We HIGHLY recommend one of the other two download options. But, if necessary, this option will download the `input.tar.gz` file to your local computer. Then, you will need to move `input.tar.gz` to the TE_Bench repository. If TE_Bench was cloned to a cluster, you can use a command like `scp`.

4. Activate your TE_Bench environment
> ```
> conda activate TE_Bench
> ```

5. Run the Install_Snakefile to complete installation and configuration of scripts with TE databases.
* [**Install_Snakefile**](https://github.com/hkania/TE_Bench/blob/main/Install_Snakefile) aids in installing the required TE Dfam database and altering TE_Bench scripts to work with the Dfam database.

* By default, Install_Snakefile will download and unzip Dfam-curated_only-1.embl.gz from Dfam using wget or curl.
    
  * To run with defaults, make sure your TE_Bench environment is activated then you can run the following.
    
    > ```
    > snakemake -s Install_Snakefile --cores 1
    > ```
 
    > Note you can add `--config help=true` to the `snakemake` command above to see user configuration options.
    
    * You should see the following once it starts running. It will complete in ~5-10 minutes depending on your download speed.
    
    > ```
    > Job stats:
    > job                     count
    > --------------------  -------
    > all                         1
    > dfam_script_patch           1
    > download_dfam               1
    > total                       3
    > ```
    
  * Non-default User Options
    * If you want to use a different Dfam .embl file, you can do the following:
      * Before running the `snakemake` command, add `--config dfam_version=FULL_URL` to the command. Or you can alter the dfam_version key in `config_install.yaml` with your compressed embl URL of choice.
  
  
    * If you want to use RepBase, which is only available to paid RepBase users as of the publication of this manuscript, you can do the following:
      > _Please note we provide very minimal instructions!!_
        * Upload the RepBaseXX.XX.embl.tar.gz file to the `/output/model_data/RepBase/` directory
        * Fill in the `XX` areas in the commands below with your specific RepBase edition and URL
      > ```
      > gunzip RepbaseXX.XX.embl.tar.gz
      > 
      > tar -xvf RepbaseXX.XX.embl.tar
      > 
      > cd RepbaseXX.XX.embl
      > 
      > cat *.ref > RepBase.embl
      > ```
      * Then, before running the `snakemake` command, add `--config repbase_version=RepBaseXX.XX` to the command. Or you can alter the repbase_version key in `config_install.yaml`.

## TE_Bench Testing
You will want to test that all three TE_Bench workflow Snakefiles work with your computing environment. 
> Note that the first two stages are configured to run within a SLURM job manager. We regret that we are unable to provide installation instructions for other executor pluggins, but you may see [here](https://snakemake.github.io/snakemake-plugin-catalog/index.html) for Snakemake's advice on executors beyond the SLURM pluggin.

### 1. Test [**Simulation_Snakefile**](https://github.com/hkania/TE_Bench/blob/main/Simulation_Snakefile), **Workflow Stage 1**

This stage allows you to generate simulated sequences using GARLIC with the Dfam or RepBase databases to use as 'ground truth' in a benchmarking effort.
  
  * By default, Simulation_Snakefile will run a simulation using Dfam to generate 2 1000bp sequences using the _Drosophila melanogaster_ genome release 6 as its model.
  * By default, Simulation_Snakefile is configured to run with a SLURM job manager.
  
    * To run with defaults, make sure your TE_Bench environment is activated then you can run the following.
    
    > ```
    > snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Simulation_Snakefile --config test=true
    > ```

    > You can always add -n to your command to perform a dry-run prior to actually running the workflow.
    > You can also add `help=true` to the end of the `snakemake` command to see user configuration options prior to running the workflow.
    > `-p` and `--verbose` flags are recommended for clarity and potential debugging

    * You should see the following once it starts running. It will complete in ~5 minutes.
    
    > ```
    > Job stats:
    > job                           count
    > --------------------------  -------
    > all                               1
    > garlic_model_build                1
    > garlic_sequence_generation        1
    > seqkit_split                      1
    > split_inserts                     1
    > total                             5
    > ```

  * Non-default User Options
    * If you chose to use RepBase, simply add `repbase=true` to the end of the snakemake command above. It will still work with the test data, and will invoke a different sequence generation script configured for RepBase.

* **Test data Run Times:**
  * `garlic_model_build` uses ~800 Mb on one core and takes ~3 minutes
  * `garlic_sequence_generation` uses ~660 Mb on one core and takes ~1 minute
  * `seqkit_split` uses ~220 Mb on 1 core and takes <1 min

*IMPORTANT:* There is nothing to compare the outputs from testing Simulation_Snakefile to. Garlic sequence generation does not follow a given seed. You can double check that it ran correctly in the resulting log file. The log file can be located in `log/rule_garlic_sequence_generation/droMelTEST`. Use the command below to check that a value of 2 returned as expected (you will need to fill in XX with the corresponding slurm job number that snakemake generated for your rule_garlic_sequence_generation step).

> ```
> `grep -c 'Generated a sequence' log/rule_garlic_sequence_generation/droMelRBTEST/XX.log`
> ```

### 2. Test [**AnnotationGen_Snakefile**](https://github.com/hkania/TE_Bench/blob/main/AnnotationGen_Snakefile), **Workflow Stage 2**

This stage allows you to generate a GFF file to use as your reference GFF, or 'ground truth', after obtaining GARLIC sequences from the simulation stage above.

> _Note: Stage 2 is NOT compatible with other reference file types. You must have ran Stage 1 to generate your simulated reference sequence(s)._

  * By default, AnnotationGen_Snakefile will generate 2 GFF and CSV files for 100Mb sequences simulated with Garlic and the _Drosophila melanogaster_ genome release 6.
  * By default, AnnotationGen_Snakefile is configured to run with a SLURM job manager.
  
    * To run with defaults, make sure your TE_Bench environment is activated then you can run the following.
    
    > ```
    > snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s AnnotationGen_Snakefile --config test=true
    > ```
    > Note: we recommended to use a screen or nohup, as this will take hours to complete.
    
    > You can always add -n to your command to perform a dry-run prior to actually running the workflow.
    > You can also add `help=true` to the end of the `snakemake` command to see user configuration options prior to running the workflow.
    > `-p` and `--verbose` flags are recommended for clarity and potential debugging
   
    * You should see the following once it starts running. It will complete in ~5 minutes.
    
    > ```
    > Job stats:
    > job                          count
    > -------------------------  -------
    > all                              1
    > garlic_to_csv                    2
    > run_garlic_gff_generation        1
    > total                            4
    > ```

* **Test data Run Times:**
  * `run_garlic_gff_generation` uses ~2.5 G on one node with 4 cores and takes ~6 hours
  
### 3. Test [**Benchmark_Snakefile**](https://github.com/hkania/TE_Bench/blob/main/Benchmark_Snakefile), **Workflow Stage 3**

This stage allow you to generate statistics and data visualizations for a given set of annotation GFF files. You can choose to set either the GARLIC file as the reference or a correctly formatted CSV file from another source as the reference.

  * By default, Benchmark_Snakefile will run both Stage 3a (comprehensive benchmarking of all TEs) and Stage 3b (selective benchmarking of select TEs, default LTRs in column V5). 
    * It will run scripts to clean annotation files from earlGrey, EDTA, and RepeatModeler2.
    * Benchmark_Snakefile will calculate benchmark statistics and visualize benchmark data.
    * The default for testing is to run the above with annotation files corresponding to Garlic-simulated 100 Mb _Arabidopsis thaliana_ and _Saccharomyces cerevisiae_ sequences.

    * To run with defaults, make sure your TE_Bench environment is activated then you can run the following.

    > ```
    > snakemake -s Benchmark_Snakefile --config test=true --cores 1 --rerun-incomplete
    > ```

    > You can always add -n to your command to perform a dry-run prior to actually running the workflow.
    > You can also add `help=true` to the end of the `snakemake` command to see user configuration options prior to running the workflow.
    
    * You should see the following once it starts running. It will complete in ~5 minutes.

    > ```  
    > Job stats:
    > job                                        count
    > ---------------------------------------  -------
    > all                                            1
    > comprehensive_calculate_statistics             2
    > comprehensive_coverage_analysis                6
    > comprehensive_garlic_perc_identity             2
    > comprehensive_garlic_plot_perc_identity        6
    > comprehensive_nest_csvs                        2
    > comprehensive_nesting_plot                     2
    > edta_to_csv                                    2
    > eg_to_csv                                      2
    > move_ref_csv_test                              2
    > redundancy_heatmaps                            6
    > redundancy_summaries                           6
    > rm_to_csv                                      2
    > selective_calculate_statistics                 2
    > selective_coverage_analysis                    6
    > selective_filter_csvs                          8
    > selective_nest_csvs                            2
    > selective_nesting_plot                         2
    > total                                         61
    > ```
    
* **Test data Run Times:**
  * All jobs in the test run take ~6 minutes collectively when using 1 core.
  * You may need to submit the same command if the system does not complete the first time around. Do not worry, it should complete remaining jobs the second time.

### 4. Compare the files in TE_Bench/output with the provided [test_outputs](https://github.com/hkania/TE_Bench/tree/main/test_outputs) to ensure everything generated correctly

# User Guide
After following the Quickstart Guide to set up and test TE_Bench, users are able to use the snakemake workflows on publicly available data or their own data.

* [Stage 1 - GARLIC Sequence Simulation](https://github.com/hkania/TE_Bench/tree/main#1-simulation_snakefile-workflow-stage-1)
* [Stage 2 - Annotation Generation](https://github.com/hkania/TE_Bench/tree/main#2-annotationgen_snakefile-workflow-stage-2)
* [Stage 3 - Benchmarking](https://github.com/hkania/TE_Bench/tree/main#3-benchmark_snakefile-workflow-stage-3)

## 1. [**Simulation_Snakefile**](https://github.com/hkania/TE_Bench/blob/main/Simulation_Snakefile), **Workflow Stage 1**
![Sim](https://github.com/hkania/TE_Bench/blob/ea986de5faff60d6383795668fb87652921b319c/.images/Simulation_Workflow.png?raw=true)
This stage allows you to generate simulated sequences using GARLIC with the Dfam or RepBase databases to use as 'ground truth' in a benchmarking effort.
  
  * By default, Simulation_Snakefile will run a simulation using Dfam to generate 2 1000bp sequences and is configured to run with a SLURM job manager.
  
### Inputs:
Simulation_Snakefile requires four files per genome you wish to model and simulate.
> All of the files can be downloaded for multiple genomes from the [UCSC Genome Browser](https://genome.ucsc.edu/). If you wish to use a genome not available from the Genome Browser, make sure the four files above match the formatting of those on the UCSC Genome Browser: [TRF Formatting Guide](https://genome.ucsc.edu/cgi-bin/hgTables?db=hg38&hgta_group=rep&hgta_track=simpleRepeat&hgta_table=simpleRepeat&hgta_doSchema=describe+table+schema&token=1.zfmMHFcH75U0Pr7sJNRM7SCCSmzxCvLNvm8EZ-GhOfrkKFwZXuKO0Se2xyRp52lH-UGbCP4WybzElxThL8EgTFNX4jzuYy3iBQId5xeRswUeLp_8ryMnVcKNbjm6VtAQt_Cpj7a5QDDYjaMFc-EdCOolyWFYwwf9SvA6dwQJs9TCot1s34EiwbgVIwO3Y0tDq5iOFb9NjZnFkqYDdRTcYc6DYTtn2EvxfjRwNCJNRBOVrDZCG1LKmuOvHv-_HkGTpMBFP9kfjDFZMbqtl4ThbCMhslgdOoA9LuhneGLH0b5q6b4ji0ApO0KHDjBXX5Nj22_EWsyX4acUZYmvnh_jpbdZ4kv2SBWPqmRR8671MR7hXck-xcTq77WSIW-iGq8J03znnQhSDkS0KwUh7T1nIdvW2vavIL59i-rVwEwfcXlItPBfIHFLqFurhg7ch5uc4HA-qfePNOR9IL2CFjhHag.ds134MIIw7nx2_Mok5ivJQ.31447100c014bf66dfa95b77be36988095597d92727b4648ed79c7f37ed8a2f1) & [ensGene Formatting Guide](https://genome.ucsc.edu/cgi-bin/hgTables?db=fr3&hgta_group=genes&hgta_track=ensGene&hgta_table=ensGene&hgta_doSchema=describe+table+schema)
          
1. FASTA file with `.fa` file extension
> If you have a `.fasta` file extension, you should modify the filename for Garlic to run properly.
2. RepeatMasker .align file generated from the FASTA above
3. TRF .bed file
4. GTF file (ensGene format) with `ensGene.gtf` file extension
> If you do not have this file extension, but your GTF follows the UCSC formatting guide for ensGene, you can modify the filename and Garlic will run properly.

**Place these genome files within `input/modeldata`.**

### Non-default User Configuration Options
* RepBase: If you configured TE_Bench with RepBase, simply add `--config repbase=true` to the end of the snakemake command, or edit the size key in the `config_simulation.yaml`.
* Size: If you want to run a simulation to generate a sequence >1000bp in length, simply add `--config size=N` to the end of the snakemake command, or edit the size key in the `config_simulation.yaml`.
  > For 100 Mb, use 100000000
* Number of Sequences: If you want to run a simulation to generate more than 2 sequences for a model genome, simply add `--config num_seqs=N` to the end of the snakemake command, or edit the size key in the `config_simulation.yaml`.
* To invoke multiple config changes in the commandline, use this format `--config size=N num_seq=N`
    
* To see a description of configuration options and defaults, run the following command in an active TE_Bench environment.
    > ```
    > snakemake -s Simulation_Snakefile --config help=true
    > ```
    
### Additional considerations
* Depending on the size you want your simulated sequence(s) to be and the TE content of the model(s) you are using, you may need to vary the allocated resources to get the job(s) to complete. To do so, you will need to edit `Simulation_Snakefile` at lines 235 **AND** either 282-283 if using RepBase or 307-308 if using Dfam. You can use a text editor, or a command such as `nano`.
    > ```
    > 234 resources:
    > 235    mem_mb = 5000 # edit value here for more or less memory for the model build step
    > 281 resources:
    > 282    mem_mb = 5000, # edit value here for more or less memory for the sequence simulation step w/RepBase
    > 283    runtime = 1440 # edit value here for more or less time for the sequence simulation step w/RepBase
    > 
    > 306 resources:
    > 307   mem_mb = 30000, # edit value here for more or less memory for the sequence simulation step w/Dfam
    > 308   runtime = 1440 # edit value here for more or less time for the sequence simulation step w/Dfam
    > ```

* If you want more control in your SLURM jobs, you can add a `slurm_extra =` line under the `resources:` option of a Snakemake rule with flags like `--mail-type=ALL`. See the [Snakemake executor plugin: slurm](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html) page for more details _(external, unmonitored link)._

* This job can take hours to days to complete. As such, we recommend running on a screen or use `nohup` to ensure it can run in the background. If you are unfamiliar with these, there are plenty of online resources to help.
    
### Job Submission
* Once you are ready, use the following command to run your simulation(s).
    
    > ```
    > snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Simulation_Snakefile
    > ```

    > You can always add -n to your command to perform a dry-run prior to actually running the workflow.
    > You can also add `help=true` to the end of the `snakemake` command to see user configuration options prior to running the workflow.
    > `-p` and `--verbose` flags are recommended for clarity and potential debugging

    * You should see the following once it starts running.
    
    > ```
    > Job stats:
    > job                           count
    > --------------------------  -------
    > all                               1
    > garlic_model_build                X (number of models you are building)
    > garlic_sequence_generation        X (number of models you are building)
    > seqkit_split                      X (number of models you are building)
    > split_inserts                     X (number of models you are building)
    > total                             X5 (number of models you are building x 5)
    > ```

    * To make sure it ran correctly, check the resulting log file to see that the sequence(s) was(were) generated using the command below. You will need to fill in `XX` with the corresponding slurm job number(s) that snakemake generated for your `rule_garlic_sequence_generation` step(s).
> This should return a value that matches the num_seqs variable, and you will need to repeat this step for each model (seq_name) you are using as snakemake will create separate log files for each `rule_garlic_sequence_generation` step.

   > ```
   > grep -c 'Generated a sequence' log/rule_garlic_sequence_generation/{seq_name}/XX.log
   > ```

### [Outputs](https://github.com/hkania/TE_Bench/blob/3f3acf94288610391ea92eac1b75e04299384049/.images/Simulation_Scripts.png)
![SimOutput](https://github.com/hkania/TE_Bench/blob/3f3acf94288610391ea92eac1b75e04299384049/.images/Simulation_Scripts.png?raw=true)
Once Simulation_Snakefile completes, you will have the following outputs **PER MODEL**
> model = {seq_name}
  
1. Model build files:  
      * output/model_data/{seq_name}/{seq_name}
        * .kmer.K4.W1000.data -- _Contains information on kmers built with default Garlic parameter k-mer size 4._

        * .inserts.W1000.data -- _Contains information on TE-inserts built with default Garlic parameter window size 1000._
        
        * .repeats.W1000.data -- _Contains information on Tandem Repeats built with default Garlic parameter window size 1000._
  
        * .GCt.W1000.data -- _Contains information on kmers built with default Garlic parameters bin size 10000 and number of GC bins 25._
      
2. Full simulation files:

      * output/sim_fastas/{seq_name}/{seq_name}
        * _sim.fasta -- _This is a multiFASTA file will all simulated sequences from a Garlic simulation run on one model._

        
        * _sim.inserts -- _This is a log file outlinging all of the inserted TE sequences for each simulated sequence from a Garlic simulation run on one model._ 
  
 
        * _sim.base.fasta -- _This is a multiFASTA file containing the background sequences from a Garlic simulation run on one model. (ie. sequences with no TEs for negative controls)._
      
3. Separated sequence files (x the number of sequences you specified to generate per model:

   > If num_seqs = 2, then you will have 2x these files with _1 and _2 appended to the seq_name)

      * output/sim_fastas/{seq_name}/{seq_name}_split/{seq_name}_base _{num}.fasta -- _These are split FASTA sequences with *NO* TEs._
   
      * output/sim_fastas/{seq_name}/{seq_name}_ split/{seq_name}_{num}
        * .inserts -- _This file outlines sequence-specific inserts and associated metadata._
  
        * .fasta -- _These are split FASTA sequences with TE inserts.__

## 2. [**AnnotationGen_Snakefile**](https://github.com/hkania/TE_Bench/blob/main/AnnotationGen_Snakefile), **Workflow Stage 2**
![Annotate](https://github.com/hkania/TE_Bench/blob/7ed894260b9b84e4ef213c2868f338a29e99a9a7/.images/Annotation_Workflow.png?raw=true)
This stage allows you to generate a GFF file to use as your reference GFF, or 'ground truth', after obtaining GARLIC sequences from the simulation stage above.

> _Note: Stage 2 is NOT compatible with other reference file types. You must have ran Stage 1 to generate your simulated reference sequence(s)._

  * By default, AnnotationGen_Snakefile will generate 2 GFF and CSV files for 100Mb sequences simulated with Garlic and is configured to run with a SLURM job manager.

### Inputs:
AnnotationGen_Snakefile requires three file types to generate GFF and CSV annotations from Garlic-simulated reference sequences produced via Simulation_Snakefile.

1. Simulated, split FASTA sequences in `output/sim_fastas/{seq_name}/{seq_name}_split`
2. Simulated, split .inserts files in `output/sim_fastas/{seq_name}/{seq_name}_split`
3. The snakemake log file produced from rule run_garlic_gff_generation in Simulation_Snakefile
> This can be found in `log/rule_garlic_sequence_generation/{seq_name}/XX.log`, where XX is your SLURM job number generated from snakemake.

**AnnotationGen_Snakefile, assumes that you ran Simulation_Snakefile and thus have a .fa fasta file in `input/modeldata`.** If you do not have a `.fa` file in `input/modeldata` for the model you want to run annotation generation for, the snakefile will not run.

### Non-default User Configuration Options
* Number of Sequences: If you ran a simulation to generate more than 2 sequences for your model, simply add `--config num_seqs=N` to the end of the snakemake command, or edit the num_seqs key in the `config_annotationgen.yaml`.
* GARLIC_LOG_FILE: You **MUST** alter this config to point toward your snakemake log file. Otherwise, the GFF generation will break, as the log file will not correspond to your simulated sequences. Simply add `--config GARLIC_LOG_FILE=YOUR_PATH` to the end of the snakemake command, or edit the GARLIC_LOG_FILE key in the `config_annotationgen.yaml`.
* To invoke multiple config changes in the commandline, use this format `--config size=N num_seq=N`
    
* To see a description of configuration options and defaults, run the following command in an active TE_Bench environment.
    > ```
    > snakemake -s Simulation_AnnotationGen --config help=true
    > ```

### Additional considerations
* We **HIGHLY** recommend running this step directly after each simulation. This will ensure its performance on one model at a time. Otherwise, the steps involving the Garlic log files will become disrupted.

* Depending on the size of your simulated sequence(s) and the TE content of the model(s) you are using, you may need to vary the allocated resources to get the job(s) to complete. To do so, you will need to edit `AnnotationGen_Snakefile` at lines 115-116.
    > ```
    > 114 resources:
    > 115   mem_mb = 30000, # edit value here for more or less memory for the sequence simulation step w/Dfam
    > 116   runtime = 1440 # edit value here for more or less time for the sequence simulation step w/Dfam
    > ```

* If you want more control in your SLURM jobs, you can add a `slurm_extra =` line under the `resources:` option of a Snakemake rule with flags like `--mail-type=ALL`. See the [Snakemake executor plugin: slurm](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html) page for more details _(external, unmonitored link)._

* This job can take hours to days to complete. As such, we recommend running on a screen or use `nohup` to ensure it can run in the background. If you are unfamiliar with these, there are plenty of online resources to help.

### Job Submission
* Once you are ready, use the following command to run your Garlic reference annotation generation.
    
    > ```
    > snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s AnnotationGen_Snakefile
    > ```

    > You can always add -n to your command to perform a dry-run prior to actually running the workflow.
    > You can also add `help=true` to the end of the `snakemake` command to see user configuration options prior to running the workflow.
    > `-p` and `--verbose` flags are recommended for clarity and potential debugging

    * You should see the following once it starts running.
    
    > ```
    > Job stats:
    > job                           count
    > --------------------------  -------
    > all                               1
    > garlic_to_csv                     X (number of sequences you simulated)
    > run_garlic_gff_generation         1
    > total                             2+X
    > ``` 
    
### [Outputs](https://github.com/hkania/TE_Bench/blob/7ed894260b9b84e4ef213c2868f338a29e99a9a7/.images/Annotation_Scripts.png)
![AnnotatOutput](https://github.com/hkania/TE_Bench/blob/da470f95900241acae2dd2966aa0da780b48b4a5/.images/Annotation_Scripts.png?raw=true)
Once AnnotationGen_Snakefile completes, you will have the following outputs

1. Model build files:  
      * output/garlic_gff_generation/{seq_name}/gffs/{seq_name}_{num}_Garlic.gff -- _GFF TE annotation files for every simulated sequence from the provided genomic model._
      
      * output/cleaned_csvs/{seq_name}_ {num}/full/comprehensive/{seq_name}_{num}_Garlic.csv-- _CSV TE annotation files for every simulated sequence from the provided genomic model._

2. Intermediate files (may delete if you don't want them):  
      * output/garlic_gff_generation/rep.inserts.tar.gz -- _Contains all the NCBI Blast+ intermediate files for defining start and stop positions of nested elements._
      
      * output/garlic_gff_generation/logs -- _Contains separated sections of the Garlic simulation log file, one per sequence_
      
      * output/garlic_gff_generation/{seq_name}/gffs/int/{seq_name}
        * _sing -- _GFF of only not nested, 'sing' for single, TE elements._
        * _nest -- _GFF of only host and nested, 'nest', TE elements._


## 3. [**Benchmark_Snakefile**](https://github.com/hkania/TE_Bench/blob/main/Benchmark_Snakefile), **Workflow Stage 3**
![Benchmark](https://github.com/hkania/TE_Bench/blob/a148bfe997f82e35604b5951e1aed46ac919f5e8/.images/Benchmark_Workflow_May22.png?raw=true)
This stage allow you to generate statistics and data visualizations for a given set of annotation GFF files. You can choose to set either the GARLIC file as the reference or a correctly formatted CSV file from another source as the reference.

  * By default, Benchmark_Snakefile will run both Stage 3a (comprehensive benchmarking of all TEs) and Stage 3b (selective benchmarking of select TEs, default LTRs in column V5). 
    * It will run scripts to clean annotation files from earlGrey, EDTA, and RepeatModeler2.
    * Benchmark_Snakefile will calculate benchmark statistics and visualize benchmark data for 100Mb sequences.
      
### Inputs:
Benchmark_Snakefile requires these files regardless of what tool(s) you used for TE annotation

1. A reference TE annotation CSV file
> Follow the 8-column expected format below if your reference file is not from TE_Bench Workflow Stage 1 with Simulation_Snakefile.
2. Tool TE annotation CSV file(s)
* If you used earlGrey, RepeatModeler2, and/or EDTA, Benchmark_Snakefile can run query cleaning to generate the cleaned CSV files for downstream benchmarking (see below for TE Discovery guidance).
> If you used a different tool, follow the 8-column expected format below to generate a compatible CSV file and be sure to set the clean_eg, clean_rm2, and clean_edta params to false.

* The following inputs are reference data-specific, and are not required for Benchmark_Snakefile to run.
3. Garlic .inputs file
> If you used Simulation_Snakefile to generate your sequences, you can do an identity regression analysis using the split .inserts files generated in Stage 2 AnnotationGen.

**Place CSV files within `output/cleaned_csvs/{seq_name}/full/comprehensive`.** This indicates that CSV files with full (whole sequence) TE annotation are ready for snakemake comprehensive benchmarking.

**If performing query cleaning with TE_Bench, you will want to place the respective TE annotation data files in `input/annotationdata`.** See our [TE Discovery Illustrative Example](https://github.com/hkania/TE_Bench#te-discovery) below for assistance, especially with regard to file extensions.

#### BENCHMARK_SNAKEFILE EXPECTED CSV FORMAT
| Col1  | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 | Col8
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Sequence Name  | Program (what generated the sequence) | Start Position | End Position | TE Class/Subclass (Non-specific, ie. Line-dependent) | TE Family (ie. Alu) | TE Name (ie. AluY) | TE Superfamily (Specific, ie. SINE)

### Non-default User Configuration Options
* Comprehensive and selective benchmarking: By default both comprehensive and selective benchmarking are performed. Please add `--config stg3a=false` to exclude comprehensive benchmarking or `--config stg3b=false` to exclude selective benchmarking.
* File extensions: Please make careful note of the extensions of your annotation files. Edit `--config ref_ext=XX` or the ref_ext key in the `config_benchmark.yaml` to match your reference CSV suffix.
> See our TE Discovery Illustrative Example for help with the `RM2_gff_ext`, `RM2_fasta_ext`, `EG_gff_ext`, and `EDTA_gff_ext` flags if you ran RepeatModeler2, earlGrey, and/or EDTA to generate your TE annotation(s).
* Data cleaning: If you **did not** use earlGrey, RepeatModeler2, and/or EDTA to generate your TE annotation, please add `--config clean_eg=false clean_rm=false clean_edta=false` to the end of the snakemake command, or edit the keys in the `config_benchmark.yaml`.
> These flags invoke R scripts which clean the outputs produced by these annotation tools. If you have a tool which produces an output formatted like one of these tools, you can leverage the bones of our scripts to prepare your files for TE_Bench.
* Overall benchmark visualizations: By default, Benchmark_Snakefile will generate visualizations. If you do not want any, or some subset of these, please specify with `--config radar=false pie=false nest=false` and only include those you are not interested in running, or edit the keys in the `config_benchmark.yaml`.
* Identity regression visualization: By default, Benchmark_Snakefile assumes the reference annotation was produced by Garlic and a `.inserts` file is available. Please specify the directory containing the .inserts file(s), which should be `output/sim_fastas/{seq_name}/{seq_name}_split`
> If your reference is not from Garlic, please add please add `--config iden=false` to the end of the snakemake command, or edit the keys in the `config_benchmark.yaml`.
* Sequence length: If you want ran a simulation to generate a sequence that is **NOT** 100Mb in length, simply add `--config seq_len=N` to the end of the snakemake command, or edit the seq_len key in the `config_benchmark.yaml`.
* Extra TE categories: If you have TEs that are not LINEs, SINEs, LTRs, or DNA elements, you can choose to include them as a category for visualizations. Please add `--config extras=CATEGORY1,CATEGORY2,...` to the end of the snakemake command, or edit the extras key in the `config_benchmark.yaml`.
* Selective benchmarking column: By deafult, filters on Col5 (`V5`) of the Benchmark_Snakefile expected CSV format. If you'd like to filter on a different column to investigate a separate TE variable, please specify `--config column=V#` to the end of the snakemake command, or edit the column key in the `config_benchmark.yaml`.
* Selective benchmarking target types: If you want to specify which types within the selective benchmarking column to perform selective benchmarking and visualizations on, please add `--config target_types=TYPE1,TYPE2,...` to the end of the snakemake command, or edit the target_types key in the `config_benchmark.yaml`.
* Misclassification and Redundancy: By default, Benchmark_Snakefile will run a misclassification and redundancy analysis for test annotation CSV files and assumes column V5 specifies TE class. If you do not want to run these analyses, please add `--config redundancy=false` to the end of the snakemake command, or edit the redundancy key in the `config_benchmark.yaml`.

* To see a description of configuration options and defaults, run the following command in an active TE_Bench environment.
    > ```
    > snakemake -s Benchmark_Snakefile --config help=true
    > ```

### Additional considerations
* We **HIGHLY** recommend running this step directly after each annotation generation step if running with Garlic simulations. This will ensure its performance on one model at a time. Otherwise, the steps involving the Garlic .inserts files will become disrupted.

* Cores: The number of cores you use to run Benchmark_Snakefile on will determine how quick the results are generated. It will work on 1 core, but increasing the cores if you can will help speed things up if you need!

### Job Submission
* Once you are ready, use the following command to run your benchmarking analysis.
    
    > ```
    > snakemake -s Benchmark_Snakefile --cores N --rerun-incomplete
    > ```

    > You can always add -n to your command to perform a dry-run prior to actually running the workflow.
    > You can also add `help=true` to the end of the `snakemake` command to see user configuration options prior to running the workflow.

    * You should see the following once it starts running.
    
    > ```
    > Job stats:
    > job                           count
    > --------------------------  -------
    > all                                            1
    > comprehensive_calculate_statistics             X (number of sequences you are analyzing annotation for)
    > comprehensive_coverage_analysis                #X (number of sequences times the number of annotation tools being compared)
    > comprehensive_garlic_perc_identity             X * Note, only applies if using GARLIC simulated sequences and the iden=true flag
    > comprehensive_garlic_plot_perc_identity        #X  * Note, only applies if using GARLIC simulated sequences and the iden=true flag
    > comprehensive_nest_csvs                        X
    > comprehensive_nesting_plot                     X
    > comprehensive_statistics_radar_plot            X
    > redundancy_heatmaps                            #X
    > redundancy_summaries                           #X    
    > selective_calculate_statistics                 ^X (number of sequences you are analyzing annotation for x number of element types)
    > selective_coverage_analysis                    #^X
    > selective_filter_csvs                          #^X (number of sequences times number of annotation tools being compared +1 for GARLIC)
    > selective_nest_csvs                            ^X
    > selective_nesting_plot                         ^X
    > selective_statistics_radar_plot                ^X
    > total                                          $ (sum of the counts above)
    > ```

### Outputs
![BenchOutputA](https://github.com/hkania/TE_Bench/blob/94db6f3cfaa349e750f9fc6355fc0571ce3001e9/.images/Bench_A_Scripts_May22.png?raw=true)
Once Benchmark_Snakefile completes, you will have some subset of the following outputs, or all if you ran Garlic simulations with complete comprehensive benchmarking.
> model = {seq_name}, program = {prog}

1. Query Data Cleaning:  
      * output/cleaned_csvs/{seq_name}/full/comprehensive/{seq_name}
        * _EG.csv -- _Cleaned CSV TE annotation file from an earlGrey run._

        * _EDTA.csv -- _Cleaned CSV TE annotation file from an EDTA run._
        
        * _RM2.csv -- _Cleaned CSV TE annotation file from a RepeatModeler2 + RepeatMasker run._
        
2. Benchmark Statistics:
      * output/stats/{seq_name}/comprehensive/{seq_name}_stats.txt -- _A text file with whole sequence metric scores from all tested TE annotation pipelines._
      
      * output/stats/{seq_name}/comprehensive/plots/{seq_name}_plot_stats.pdf -- _A radar plot visualizing the whole sequence metric scores from all tested TE annotation pipelines._
      
3. Coverage Analysis
    * output/cleaned_csvs/{seq_name}/coverage_csvs/comprehensive/{seq_name}_{prog}_cov.csv -- _One CSV file per tested TE annotation with a new column specifying the coverage of the reference element (in terms of percentage of base pairs identified as TP)._
    
    * output/stats/{seq_name}/comprehensive/plots/{seq_name}_{prog}_coverage_piechart.pdf -- _A piechart with an outer ring summarizing the percent of TEs within the sequence attributed to each major TE classification and and inner ring summarizing how many elements are covered by the test annotation at 80% or more._
        
4. Identity Analysis
    * output/cleaned_csvs/{seq_name}/identity_csvs/comprehensive/{seq_name}_ref_perc_iden.csv -- _One CSV file per model sequence specifying the percent identity of each element of the reference to its consensus element._

    * output/stats/{seq_name}/comprehensive/{seq_name}_{prog}_perc.id.csv -- _One set of regressions divided by major TE classification plotting percent identity of refernce to consensus by test TE annotation coverage._

5. Nested TE Analysis
    * output/cleaned_csvs/{seq_name}/nest_csvs/comprehensive/{seq_name}_host.csv -- _One CSV file per model sequence specifying the host TEs within the reference sequence._

    * output/cleaned_csvs/{seq_name}/nest_csvs/comprehensive/{seq_name}_nest.csv -- _One CSV file per model sequence specifying the nested TEs within the reference sequence._

    * output/cleaned_csvs/{seq_name}/nest_csvs/comprehensive/{seq_name}_nonest.csv -- _One CSV file per model sequence specifying the TEs not involved in nesting within the reference sequence._

    * output/stats/{seq_name}/comprehensive/plots/{seq_name}_nesting.pdf -- _One three-panel barplot per model sequence showing the distribution of coverage across the nested TE status categories for all tested TE annotations._

6. Misclassification and Redundancy Analysis
    * output/stats/{seq_name}/comprehensive/{seq_name}_{prog}_partialoverlaps.tsv -- _One TSV file per test TE annotation specifying TEs and associated bps within the test annotation that have partial (<95%) overlap._

    * output/stats/{seq_name}/comprehensive/{seq_name}_{prog}_redundantoverlaps.tsv -- _One TSV file per test TE annotation specifying TEs and associated bps within the test annotation that have redundant (>95%) overlap. Note that nested TEs (100% overlap) are not included._

    * output/stats/{seq_name}/comprehensive/{seq_name}_{prog}_redundancysummary.txt -- _One text file per TE annotation specifying details about overlapping base pairs and categorizations within the test annotation._

    * output/stats/{seq_name}/comprehensive/plots/{seq_name}_redundancyheatmap_{prog}.pdf -- _One dual heatmap per TE annotation showing reference-test annotation class correspondence and misclassification on the righthand side and signals of within-annotation redundancy/fragmentation on the lefthandside._

![BenchOutputB](https://github.com/hkania/TE_Bench/blob/609da477fe405277c63ccd86be62aa7985b0fa10/.images/Bench_B_Scripts.png?raw=true)
Once Benchmark_Snakefile completes, you will have some subset of the following outputs, or all if you ran Garlic simulations with complete selective benchmarking.
> model = {seq_name}, program = {prog}, type = {type} where it can be any number of tested TE types within the specified filtered column.
        
1. CSV Filtering:
      * output/leaned_csvs/{seq_name}/full/{type}/{seq_name}_ {prog}_{type}.csv -- _One CSV file per tested TE annotation and TE type combo, ie. a CSV file with all the LTR elements found by earlGrey._
      
2. Selective Benchmark Statistics:
      * output/stats/{seq_name}/{type}/{seq_name}/{type}_stats.txt -- _A text file with type-filtered sequence metric scores from all tested TE annotation pipelines._
      
      * output/stats/{seq_name}/{type}/plots/{seq_name}_{type}_plot_stats.pdf -- _A radar plot visualizing the type-filtered sequence metric scores from all tested TE annotation pipelines._
      
3. Selective Coverage Analysis
    * output/cleaned_csvs/{seq_name}/coverage_csvs/{type}/{seq_name}_ {prog}_{type}_cov.csv -- _One CSV file per tested TE annotation with a new column specifying the coverage of the reference element (in terms of percentage of base pairs identified as TP) filtered by TE type._
            
4. Nested TE Analysis
    * output/cleaned_csvs/{seq_name}/nest_csvs/{type}/{seq_name}_{type}_host.csv -- _One CSV file per model sequence specifying the host TEs within the reference sequence._

    * output/cleaned_csvs/{seq_name}/nest_csvs/{type}/{seq_name}_{type}_nest.csv -- _One CSV file per model sequence specifying the nested TEs within the reference sequence._

    * output/cleaned_csvs/{seq_name}/nest_csvs/{type}/{seq_name}_{type}_nonest.csv -- _One CSV file per model sequence specifying the TEs not involved in nesting within the reference sequence._

    * output/stats/{seq_name}/{type}/plots/{seq_name}_{type}_nesting.pdf -- _One three-panel barplot per model sequence showing the distribution of coverage across the nested TE status categories for all tested TE annotations._


### Further considerations
* If you used Garlic, pay attention to the minimum percent identity to TE consensus in your sequence of interest (the default minimum in this workflow is 50%, which is typical of mammalian models). You can check your GARLIC reference percent identity CSV file using the following terminal command:
> ```
> cut -d, -f 9 {seq_name}_ref_perc_iden.csv | sort -n | head
> ```

> If you need to edit the minimum value to be plotted by the `plot_identity_vs_coverage.py` script, you can edit line 132 and re-run that script.
> ```
> 132 ax.set_xlim(50, 100)
> ```

* It is still a good idea to double check your files, as sometimes GARLIC can generate unexpected categories (which is the case for the Y' element in yeast which is classifies as `Other` as its Class in column V5).

*If you have a non-GARLIC reference and/or ran a program that is not EarlGrey, EDTA, or RepeatModeler2 and/or a newer version of any of those three pipelines you need to investigate your data and check that the values you want to consider in selective benchmarking match across the CSV files.

# TE Discovery
![TE_DISCOVER](https://github.com/hkania/TE_Bench/blob/6079be2d0bc61241172d215a05ba5e7f935933fb/.images/TE_Discovery_Illustration.png?raw=true)

_Here we describe an illustrative example of the three TE Discovery tools used in TE_Bench's manuscript case-study. Please note that we use default states of these tools. Each tool has its own installation guide, set of optional parameters, and more, that can be modified and tested using TE_Bench._

## earlGrey
An installation guide and user guide are provided within [earlGrey's official documentation](https://github.com/TobyBaril/EarlGrey).

### 1. Inputs

* earlGrey expects a FASTA file as input. 
  * When using TE_Bench, you can use the .fasta file(s) found in `output/sim_fastas/SAMPLE_NAME/SAMPLE_NAME_split/` as reference FASTAs for benchmarking after you run Stage 1 of TE_Bench.
  * Doing so will allow you to compare the output annotation(s) from earlGrey to the output annotation(s) from Stage 2 of TE_Bench: `output/cleaned_csvs/SAMPLE_NAME/full/comprehensive/SAMPLE_NAME*_Garlic.csv`

* When you have earlGrey configured to run, here is a sample command ran with 16 threads. We recommend consulting earlGrey's official documentation for more information to better decide your commands!
  
> ```
> earlGrey -g FASTA_PATH -s SAMPLE_NAME -t 16
> ```
> * _Keep SAMPLE_NAME consistent, so if you ran Stage 1 of TE_Bench with a model called `homSap`, you would want to have SAMPLE_NAME be homSap. That way snakemake can fill wildcards correctly._
    
### 2. Relevant Outputs for TE_Bench
* Once earlGrey has completed, it will have created a parent directory `SAMPLE_NAME_EarlGrey` with subdirectories. The subdirectory of interest is `SAMPLE_NAME_summaryFiles`.

* The relevant file `SAMPLE_NAME.filteredRepeats.gff` for TE_Bench is within `SAMPLE_NAME_summaryFiles`. 

### 3. Preparing the Output for TE_Bench
* We recommend first renaming the output file to `SAMPLE_NAME_EG.gff`. This nomenclature matches the default file extension expected by TE_Bench.

* Then, move or copy the renamed GFF file to TE_Bench's `input/annotationdata` directory.

* Then, prior to running Benchmark_Snakefile, make sure you have the correct file extension specified within `config_benchmark.yaml` or overwrite with `--config EG_gff_ext={XXX}` if you chose not to rename the file.

* This will permit TE_Bench to clean the GFF file prior to performing benchmark calculations and visualization steps.

### 4. Other Considerations
* TE_Bench is configured to run on any number of test annotation files. If you want to run the earlGrey annotation against another program's annotation, be sure the basenames (SAMPLE_NAME) match.
  * For example, `droMel_EG.gff` will be compared with `droMel_RM2.gff` but not `droMel_2_RM2.gff`.
  
  * As another example, if you want to trial different parameters of earlGrey, you could name one gff `droMel_EG.gff` and the other `droMel_EG2.gff` and TE_Bench will benchmark them and produce comparative visualizations. 
    > In this case, you would want to clean both files with the earlGrey-compatible R script [EG_gff_to_csv.R](https://github.com/hkania/TE_Bench/blob/main/scripts/EG_gff_to_csv.R). This can be ran as a standalone script outside of snakemake.
    > An example command for this case:
    > ```
    > Rscript ./scripts/EG_gff_to_csv.R input/annotationdata/SAMPLE_NAME_EG2.gff output/cleaned_csvs/SAMPLE_NAME/full/comprehensive/SAMPLE_NAME_EG2.csv SAMPLE_NAME
    > ```
    
## EDTA
### 1. Inputs

* EDTA expects a FASTA file as input. 
  * When using TE_Bench, you can use the .fasta file(s) found in `output/sim_fastas/SAMPLE_NAME/SAMPLE_NAME_split/` as reference FASTAs for benchmarking after you run Stage 1 of TE_Bench.
  * Doing so will allow you to compare the output annotation(s) from EDTA to the output annotation(s) from Stage 2 of TE_Bench: `output/cleaned_csvs/SAMPLE_NAME/full/comprehensive/SAMPLE_NAME*_Garlic.csv`

* Here is a sample EDTA command for discovering LTRs with 16 threads, and we recommend checking [EDTA's official documentation](https://github.com/oushujun/EDTA) for more information!
  * For the case studies in TE_Bench's manuscript, we ran a [Divided and Conquer approach](https://github.com/oushujun/EDTA#divide-and-conquer), starting with ltr, then line, then sine, then tir, and finally helitron.

> ```
> perl EDTA/bin/EDTA_raw.pl --genome FASTA_PATH --type ltr --threads 16 --overwrite 0
> ```

* Example final command to generate the annotation GFF file:

> ```
> perl EDTA/bin/EDTA_raw.pl --genome FASTA_PATH --overwrite 0 --anno 1
> ```

### 2. Relevant Outputs for TE_Bench
* Once EDTA has completed, it will have created a parent directory containing the relevant file `SAMPLE_FASTA.mod.EDTA.TEanno.gff3`. 

### 3. Preparing the Output for TE_Bench
* We recommend first renaming the output file to `SAMPLE_NAME_EDTA.gff`. This nomenclature matches the default file extension expected by TE_Bench.

* Then, move or copy the renamed GFF file to TE_Bench's `input/annotationdata` directory.

* Then, prior to running Benchmark_Snakefile, make sure you have the correct file extension specified within `config_benchmark.yaml` or overwrite with `--config EDTA_gff_ext={XXX}` if you chose not to rename the file.

* This will permit TE_Bench to clean the GFF file prior to performing benchmark calculations and visualization steps.

### 4. Other Considerations
* TE_Bench is configured to run on any number of test annotation files. If you want to run the EDTA annotation against another program's annotation, be sure the basenames (SAMPLE_NAME) match.
  * For example, `droMel_EDTA.gff` will be compared with `droMel_EG.gff` but not `droMel_2_EG.gff`.
  
  * As another example, if you want to trial different parameters of EDTA, you could name one gff `droMel_EDTA.gff` and the other `droMel_EDTA2.gff` and TE_Bench will benchmark them and produce comparative visualizations. 
    > In this case, you would want to clean both files with the EDTA-compatible R script [EDTA_gff_to_csv.R](https://github.com/hkania/TE_Bench/blob/main/scripts/EDTA_gff_to_csv.R). This can be ran as a standalone script outside of snakemake.
    > An example command for this case:
    > ```
    > Rscript ./scripts/EDTA_gff_to_csv.R input/annotationdata/SAMPLE_NAME_EDTA2.gff output/cleaned_csvs/SAMPLE_NAME/full/comprehensive/SAMPLE_NAME_EDTA2.csv SAMPLE_NAME`
    > ```

## RepeatModeler2
### 1. Inputs

* RepeatModeler2 expects a FASTA file as input.
  * When using TE_Bench, you can use the .fasta file(s) found in `output/sim_fastas/SAMPLE_NAME/SAMPLE_NAME_split/` as reference FASTAs for benchmarking after you run Stage 1 of TE_Bench.
  * Doing so will allow you to compare the output annotation files from RepeatModeler to the output annotation(s) from Stage 2 of TE_Bench: `output/cleaned_csvs/SAMPLE_NAME/full/comprehensive/SAMPLE_NAME*_Garlic.csv`

* Here are a sample RepeatModeler2 commands run with 16 threads, and we recommend checking [RepeatModeler2's official documentation](https://github.com/Dfam-consortium/RepeatModeler) for more information!

> ```
> RepeatModeler/BuildDatabase -name SAMPLE_NAME FASTA_PATH
> ```

> ```
> RepeatModeler/RepeatModeler -database SAMPLE_NAME -threads 16 -engine ncbi -LTRStruct
> ```

### 2. Relevant Outputs for TE_Bench
* Once RepeatModeler2 has completed, it will have the relevant file within the directory it ran in: `SAMPLE-families.fa`. 

### 3. Preparing the Output for TE_Bench (_and RepeatMasker!_)
* We recommend first renaming the output FASTA file to `SAMPLE_NAME_RM2.fa`. This nomenclature matches the default file extension expected by TE_Bench.

* Then, move or copy the renamed FASTA file to TE_Bench's `input/annotationdata` directory.

* Then, prior to running Benchmark_Snakefile, make sure you have the correct file extension specified within `config_benchmark.yaml` or overwrite with `--config RM2_fasta_ext={XXX}` if you chose not to rename the file.

## RepeatMasker Post-RepeatModeler2
### 1. Inputs
* RepeatMasker then expects the FASTA used for RepeatModeler2 **AND** the output TE library consensi file from RepeatModeler2 to generate the final RM2 GFF file.
  * You will need `SAMPLE_NAME_RM2.fa` created above (does not matter if it is renamed or not).

* Here is a sample RepeatMasker command with 16 threads and rmblast engine, and we recommend checking [RepeatMasker's official documentation](https://repeatmasker.org/RepeatMasker/) for more information!

> ```
> RepeatMasker/RepeatMasker -pa 16 -gff -a -e rmblast \
>	-lib SAMPLE_RM2.fa \
>	FASTA_PATH
> ```

### 2. Relevant Outputs for TE_Bench
* Once RepeatMasker has completed, it will have created a parent directory containing the relevant file `SAMPLE_FASTA.out.gff`. 

### 3. Preparing the Output for TE_Bench
* We recommend first renaming the GFF output file to `SAMPLE_NAME_RM2.gff`. This nomenclature matches the default file extension expected by TE_Bench.

* Then, move or copy the renamed GFF file to TE_Bench's `input/annotationdata` directory.

* Then, prior to running Benchmark_Snakefile, make sure you have the correct file extension specified within `config_benchmark.yaml` or overwrite with `--config RM2_gff_ext={XXX}` if you chose not to rename the file.

* This will permit TE_Bench to clean the GFF file prior to performing benchmark calculations and visualization steps.

### 4. Other Considerations
* TE_Bench is configured to run on any number of test annotation files. If you want to run the RepeatModeler2 annotation against another program's annotation, be sure the basenames (SAMPLE_NAME) match.
  * For example, `droMel_RM2.gff` will be compared with `droMel_EDTA.gff` but not `droMel_2_EDTA.gff`.
  
  * As another example, if you want to trial different parameters of RepeatModeler2, you could name one gff `droMel_RM2.gff` and the other `droMel_RM2.2.gff` and TE_Bench will benchmark them and produce comparative visualizations. 
    > In this case, you would want to clean both files with the RM2-compatible R script [RM2_gff_to_csv.R](https://github.com/hkania/TE_Bench/blob/main/scripts/RM2_gff_to_csv.R). This can be ran as a standalone script outside of snakemake.
    > An example command for this case:
    > ```
    > Rscript ./scripts/RM2_gff_to_csv.R input/annotationdata/SAMPLE_NAME_RM2.2.gff input/annotationdata/SAMPLE_NAME_RM2.2.fa output/cleaned_csvs/SAMPLE_NAME/full/comprehensive/SAMPLE_NAME_RM2.2.csv SAMPLE_NAME
    > ```

# Computational References:
This workflow was built using the Snakemake resources provided by

[Mölder, F., Jablonski, K.P., Letcher, B., Hall, M.B., Tomkins-Tinch, C.H., Sochat, V., Forster, J., Lee, S., Twardziok, S.O., Kanitz, A., Wilm, A., Holtgrewe, M., Rahmann, S., Nahnsen, S., Köster, J., 2021. Sustainable data analysis with Snakemake. F1000Res 10, 33.](https://f1000research.com/articles/10-33/v2)

Data and scripts provided by

[Realistic artificial DNA sequences as negative controls for computational genomics. Caballero J, Smit AF, Hood L, Glusman G. Nucl. Acids Res. 2014 doi: 10.1093/nar/gku356 ](https://github.com/caballero/Garlic)

[Kania, H. P., Seifert, S. A., & Yoder, A. D. (2025). Data from: A foundational benchmarking workflow for transposable element discovery pipelines. Duke Research Data Repository. [https://doi.org/10.7924/r4r509](https://doi.org/10.7924/r4r509)

