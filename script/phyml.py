#!/usr/bin/python

######################################################################################
# This script takes sequence phylip file and run PhyML
# Author: Wenjie Deng
# Date: 2022-05-06
# Usage: python phyml.py inputPhylipFile datatype
######################################################################################

import sys
import re
import os
import argparse
from paths import phyml

def main(infile, dt):
    model = ""
    if dt == "nt":
        model = "GTR"
    elif dt == "aa":
        model = "HIVw"
    else:
        sys.exit("Wrong sequence datatype "+dt)

    phymlfile = infile + "_phyml.txt"
    logfile = infile + "_log.txt"
    command = phyml+" -i "+infile+" -d "+dt+" -q -b 0 -m "+model+" -v e -c 4 -o tlr -a e -f m --print_mat_and_exit --leave_duplicates >"+phymlfile
    log = ""
    rv = os.system(command)
    if rv == 0:
        log = command + "\nPhyML succeed: "+str(rv)
    else:
        log = command + "\nPhyML failed: "+str(rv)

    with open(logfile, "w") as lf:
        lf.write(log+"\n")

    return log

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input sequence fasta file")
    parser.add_argument("datatype", help="sequence datatype")
    args = parser.parse_args()
    infile = args.infile
    datatype = args.outfile

    main(infile, datatype)
