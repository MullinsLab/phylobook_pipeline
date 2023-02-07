# phylobook_pipeline
A program pipeline to run through multiple programs from sequence alignment fasta file to the resuts ready to publish on phylobook server

## Usage
In a working directory that contains sequence alignment fasta files, run
````
python3 wherePipelineIntalled/script/phylobook.py -d workingDirectoryPath(default: .) -t sequenceType(nt or aa) -p multiprocessing(default: 1) -l averageSequenceLength
````

## Installation and Configuration
The pipeline consists of three programming components. In order to process the pipeline successfully, you need to meet the requirements of following programming components:
  - run_phyml_batch (https://github.com/MullinsLab/run_phyml_batch)
  - figtree-enhanced-command-line (https://github.com/MullinsLab/figtree-enhanced-command-line)
  - highlighter_bot (https://github.com/MullinsLab/highlighter_bot)

Finally, you need to modify path.py in script/ to set the correct paths of phyml and figtree excutables you have installed in your computer
