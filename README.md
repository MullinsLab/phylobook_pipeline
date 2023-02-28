# phylobook_pipeline
A program pipeline to run through multiple programs from sequence alignment fasta file to the resuts ready to publish on phylobook server

## Usage
In a working directory that contains sequence alignment fasta files, run
````
python3 WherePhylobookPipelineInstalled/script/phylobook.py -d WorkingDirectoryPath(default: .) -t SequenceType(nt or aa) -p NumberOfProcessors(default: 1) -l AverageSequenceLength
````
  - you have to provide the value of SequencType (nt for nuclotide sequences, aa for amino acid sequences)
  - you have to provide the value of AverageSequenceLength
  - the default value of numberOfProcessors is 1. You can run multiprocessors by providing the value > 1 based on your computer settings
  - it will output enhanced ML tree and highlighter plot for each input sequence alignment file, ready for display and manipulate on phylobook server

## Installation and Configuration
The pipeline consists of three programming components ([run_phyml_batch](https://github.com/MullinsLab/run_phyml_batch), [figtree-enhanced-command-line](https://github.com/MullinsLab/figtree-enhanced-command-line) and [highlighter_bot](https://github.com/MullinsLab/highlighter_bot)). In order to process the pipeline successfully, you need to meet the requirements of the programming components

If you are wanting to run the pipeline in a Docker contianer, see the [Docker](#docker) section of this document.

### 1. Clone this repository in your designated directory
```
git clone https://github.com/MullinsLab/phylobook_pipeline.git
```
  - it will create a directory called "phylobook_pipeline" in your designated directory (i.e. WherePhylobookPipelineInstalled)

### 2. Requirements for run_phyml_batch

#### a. Download [PhyML](https://github.com/stephaneguindon/phyml) in the directory "phylobook_pipeline"
```
cd phylobook_pipeline
git clone https://github.com/stephaneguindon/phyml.git
```
  - the current release is v3.3.20220408
  - it will create a subdirectory called "phyml"

#### b. Update files in order to output pairwise distances after running phyml
```
cd phyml/src
python WherePhylobookPipelineInstalled/script/updatefiles.py
cd ..
```

#### c. In the directory of phyml/, install phyml following the instructions on PhyML [GitHub](https://github.com/stephaneguindon/phyml)

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

&nbsp;
## Docker

phylobook_pipeline includes a Dockerfile and a docker-compose.yml file to allow it to run in a Docker container. Please follow these installation steps  

### 1. Ensure you have Docker installed on your system
See https://www.docker.com/

### 2. Clone this repository in your designated directory
```
git clone https://github.com/MullinsLab/phylobook_pipeline.git
```
it will create a directory called "phylobook_pipeline" in your designated directory (i.e. WherePhylobookPipelineInstalled)

### 3. If you are running the container on a Linux computer
If you are running phylobook_pipeline on a Linux computer the files created by the pipeline will not have the correct user ownership.  In order to get around this, edit the docker-compose.yml file to have your userid and groupid.

You can find these using the id command on the command line.

Edit line 12 in docker-compose.yml, deleting the # sign, and replacing the userid:groupid parts of the line. 
```
    # user: userid:groupid
```
will be changed to look similar to:
```
    user: 1001:1001
```

### 4. Build and run the container
```
cd phylobook_pipeline
docker compose up -d --build
```
This will likely take more than a full minute, depending on the speed of your computer.

### 5. Start a command line inside the docker container
```
docker exec -it phylobook_pipeline bash
```
This will put you into a Linux command line where you can operate the pipeline.

You can exit using ^d (control key + d).

### 6. Getting data "into" the Docker container.
Under the default setup, the only portion of the host computer's file system that is visible within the Docker container is the phylobook_pipeline directory (and subfolders therein). Anything that gets created inside the docker's phylobook_pipeline directory will show up in the host machine.  Thus the easiest way to make data available to the Phylobook Pipeline in the Docker container is to create a subdirectory under the phylobook_pipeline and move data there on the host machine.
