# phylobook_pipeline
A program pipeline to run through multiple programs from sequence alignment fasta file to the resuts ready to publish on phylobook server

## Usage
In a working directory that contains sequence alignment fasta files, run
````
python3 WherePhylobookPipelineInstalled/script/phylobook.py -d WorkingDirectoryPath(default: .) -t SequenceType(nt or aa) -p NumberOfProcessors(default: 1) -l AverageSequenceLength
````
  - you have to provide the value of datatype (nt for nuclotide sequences, aa for amino acid sequences)
  - you have to provide the value of average sequence length
  - the default value of numberOfProcessors is 1. You can run multiprocessors by providing the value > 1 based on your computer settings
  - it will output enhanced ML tree and highlighter plot for each input sequence alignment file, ready for display and manipulate on phylobook server

## Installation and Configuration
The pipeline consists of three programming components ([run_phyml_batch](https://github.com/MullinsLab/run_phyml_batch), [figtree-enhanced-command-line](https://github.com/MullinsLab/figtree-enhanced-command-line) and [highlighter_bot](https://github.com/MullinsLab/highlighter_bot)). In order to process the pipeline successfully, you need to meet the requirements of the programming components

### 1. Clone this repository in your designated directory
```
git clone https://github.com/MullinsLab/phylobook_pipeline.git
```
  - it will create a directory called "phylobook_pipeline" in your designated directory (i.e. WherePhylobookPipelineInstalled)

### 2. Requirements for run_phyml_batch

#### a. Download [PhyML](https://github.com/stephaneguindon/phyml) in your designated directory
```
git clone -b v3.3.20220408 https://github.com/stephaneguindon/phyml.git phyml_v3.3.20220408
```
  - the current release is v3.3.20220408
  - it will create a directory called "phyml_3.3.20220408"

#### b. Update files in order to output pairwise distances after running phyml
```
cd phyml_v3.3.20220408/src
python WherePhylobookPipelineInstalled/script/updatefiles.py
cd ..
```

#### c. In the directory of phyml_v3.3.20220408/, install phyml following the instructions on PhyML [GitHub](https://github.com/stephaneguindon/phyml)

#### d. Modify path.py to set the correct path to run phyml in your computer
 - open WherePhylobookPipelineInstalled/script/path.py file in a text editor
 - replace "where_your_phyml_path/program_name" with the correct phyml path where you just installed, e.g "your_designated_directory/phyml_v3.3.20220408/src/phyml" (the path should include the program name), and save the file

### 3. Requirements for figtree-enhanced-command-line 
 - This source is an extension of Adam Rambaut's FigTree.  The original source can be found here:
https://github.com/rambaut/figtree/releases
 - Build Requirements (for further modifying the source code): java 8
 - Execution: A current version of figtree.jar can be found in WherePhylobookPipelineInstalled/figtree/figtree.jar

### 4. Requirements for highlighter_bot 
In a virtual Python 3 environment:
```
pip3 install robobrowser
pip3 install lxml
pip3 install wget
```

### 5. Install [ImageMagick](https://imagemagick.org/script/download.php) to trim highlighter image for Phylobook
