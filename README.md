# phylobook_pipeline
A program pipeline to run through multiple programs from sequence alignment fasta file to the resuts ready to publish on phylobook server

## Usage
In a working directory that contains sequence alignment fasta files, run
````
python3 wherePipelineIntalled/script/phylobook.py -d WorkingDirectoryPath(default: .) -t SequenceType(nt or aa) -p NumberOfProcessors(default: 1) -l AverageSequenceLength
````
  - you have to provide the value of datatype (nt for nuclotide sequences, aa for amino acid sequences)
  - you have to provide the value of average sequence length
  - the default value of numberOfProcessors is 1. You can run multiprocessors by providing the value > 1 based on your computer settings
  - it will output enhanced ML tree and highlighter plot for each input sequence alignment file, ready for display and manipulate on phylobook server

## Installation and Configuration
The pipeline consists of three programming components (run_phyml_batch, figtree-enhanced-command-line and highlighter_bot). In order to process the pipeline successfully, you need to meet the requirements of following programming components:
  - run_phyml_batch (https://github.com/MullinsLab/run_phyml_batch)
  - figtree-enhanced-command-line (https://github.com/MullinsLab/figtree-enhanced-command-line)
  - highlighter_bot (https://github.com/MullinsLab/highlighter_bot)

Finally, you need to modify path.py in script/ to set the correct paths of phyml and figtree excutables you have installed in your computer
