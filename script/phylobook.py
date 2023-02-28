#!/usr/bin/python

##########################################################################################
# Program: phylobook.py
# Purpose: In user's working directory with sequence alignment fasta files,
# performs run_phyml.py to estimate ML phylogenetic trees,
# performs figtree-enhanced-conmandline to modify the ML trees,
# performs highlighter_bot to produce highlighter plots of the sequence alignments
# Author: Wenjie Deng
# Date: 2023-02-03
##########################################################################################


import sys, re, os
import argparse
import glob
import run_phyml
import average_length


def main(wdir, dt, proc):
	print("**** Run PhyML ***")
	run_phyml.main(wdir, dt, proc)
	
	pydir = os.path.dirname(os.path.realpath(__file__))
	
	print("\n**** Run figtree-enhanced-command-line ****\n")
	pdir = os.path.dirname(pydir)
	figtree = os.path.join(pdir, "figtree", "figtree.jar")
	for file in glob.glob(os.path.join(wdir, '*phyml_tree.txt')):
		print("=== Processing file "+file+" ===")
		fastafile = file.replace(".phy_phyml_tree.txt", ".fasta")
		alen = average_length.main(fastafile)
		print(f"Average sequence length: {alen}")
		command = "java -jar "+figtree+" -avg_seq_length "+str(alen)+" -colors extract -newickexport -nexusexport -graphic SVG -height 768 -width 783 "+file
		print(command)
		rv = os.system(command)
		if rv == 0:
			print("figtree succeed: "+str(rv))
		else:
			print("figtree failed: "+str(rv))
			
	print("\n**** Run highlight_bot ****\n")
	pydir = os.path.dirname(os.path.realpath(__file__))
	highlighter_bot = os.path.join(pydir, "highlighter_bot.py")
	hlcommand = "python3 "+highlighter_bot+" -d "+wdir
	if dt == 'aa':
		hlcommand += " -a"
	print(hlcommand)
	os.system(hlcommand)
	
	print("\n**** Crop highlighter images ****\n")
	for file in glob.glob(os.path.join(wdir, '*_untrimmed.png')):
		cropfile = file.replace("_untrimmed.png", ".png")
		cropcommand = "convert -crop +0+150 -crop -0-50 "+file+" "+cropfile
		os.system(cropcommand)
	

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="directory to hold input sequence fasta file", nargs="?", const=1, type=str, default=".")
    parser.add_argument("-t", "--datatype", help="sequence datatype, must be 'nt' for nucleotide or 'aa' for amino acid", nargs="?", const=1, type=str, required=True)
    parser.add_argument("-p", "--processes", help="number of processes for multiprocessing", nargs="?", const=1, type=int,
                        default="1")
    args = parser.parse_args()
    wdir = args.dir
    dt = args.datatype
    proc = args.processes

    main(wdir, dt, proc)
