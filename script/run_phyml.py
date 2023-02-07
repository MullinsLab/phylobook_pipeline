#!/usr/bin/python

##########################################################################################
# Program: run_phyml.py
# Purpose: In the working directory with sequence alignment fasta files,
# run PhyML to produce estimated ML trees, pairwise distances
# Author: Wenjie Deng
# Date: 2023-02-03
##########################################################################################

import sys, re, os
import argparse
import glob
import fasta2phylip
import phyml
import parse_dist
from multiprocessing import Pool


def worker(file, logdir, dt):
    fields = file.split("/")
    filename = fields[-1]
    logfilename = filename.replace(".fasta", ".log")
    logfile = logdir + "/" + logfilename

    with open(logfile, "w") as lfp:
        # convert to phylip file
        phylipfile = file.replace(".fasta", ".phy")
        print("\n" + "=== Processing file " + file + " ===")
        covertlog = fasta2phylip.main(file, phylipfile)
        lfp.write("=== Processing file " + file + " ===" + "\n")
        lfp.write("** Convert " + file + " to " + phylipfile + "**\n")
        lfp.write("input: " + file + "\n")
        lfp.write("output: " + phylipfile + "\n")
        lfp.write(covertlog + "\n")

        # run phyml
        phymllog = phyml.main(phylipfile, dt)
        lfp.write("** Run PhyML on " + phylipfile + " **" + "\n")
        lfp.write("input: " + phylipfile + "\n")
        lfp.write("datatype: " + dt + "\n")
        lfp.write(phymllog + "\n")

        # output distance matrix file
        if re.search("PhyML succeed: ", phymllog):
            phymlout = phylipfile+"_phyml.txt"
            distfile = phylipfile+"_pwcoldist.txt"
            distlog = parse_dist.main(phymlout, distfile)
            lfp.write("** Parse pairwise distances in " + phymlout + " **" + "\n")
            lfp.write("input: " + phymlout + "\n")
            lfp.write("output: " + distfile + "\n")
            lfp.write(distlog + "\n")

            # output success info
            lfp.write("*** Succeed ***\n")

def main(wdir, dt, proc):
    logdir = wdir+"/run_phyml_logs"

    if os.path.isdir(logdir) is False:
        os.mkdir(logdir)

    files = []
    for file in glob.glob(os.path.join(wdir, '*.fasta')):
        files.append(file)

    pool = Pool(proc)
    pool.starmap(worker, [(file, logdir, dt) for file in files])

    pool.close()
    pool.join()

    alllogfile = logdir + "/run_phyml.log"
    with open(alllogfile, "w") as afp:
        for file in files:
            fields = file.split("/")
            filename = fields[-1]
            logfilename = filename.replace(".fasta", ".log")
            logfile = logdir + "/" + logfilename
            with open(logfile, "r") as lfp:
                for line in lfp:
                    afp.write(line)
                afp.write("\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--wdir", help="directory to hold input sequence fasta file", nargs="?", const=1, type=str, default=".")
    parser.add_argument("-t", "--datatype", help="sequence datatype, must be 'nt' for nucleotide or 'aa' for amino acid", nargs="?", const=1, type=str, required=True)
    parser.add_argument("-p", "--processes", help="number of processes for multiprocessing", nargs="?", const=1, type=int,
                        default="1")
    args = parser.parse_args()
    wdir = args.wdir
    dt = args.datatype
    proc = args.processes

    main(wdir, dt, proc)
    
    