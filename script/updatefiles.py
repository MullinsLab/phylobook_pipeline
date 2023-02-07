#!/usr/bin/python

######################################################################################
# This script updates main.c to include distance matrix output
# Author: Wenjie Deng
# Date: 2022-05-09
# Usage: python updatemain.py inputMainFile outputFile
######################################################################################

import os
import re
import argparse

def updatemain(infile, outfile):
    with open (outfile, 'w') as ofp:
        with open(infile, "r") as fp:
            for line in fp:
                if re.search("exit\(-1\)", line):
                    line = "//" + line;
                elif re.search("\/\* Start from BioNJ tree \*\/", line):
                    insertion1 = line.replace("/* Start from BioNJ tree */", "printf(\"\\n\\n- ML tree distance matrix (after optimisation)\\n\\n\");")
                    insertion2 = line.replace("/* Start from BioNJ tree */",
                                              "Print_Mat(ML_Dist(cdata,mod));")
                    ofp.write(insertion1 + insertion2 + "\n")
                ofp.write(line)

def updateio(infile, outfile):
    flag = 0
    with open (outfile, 'w') as ofp:
        with open(infile, "r") as fp:
            for line in fp:
                if re.search(r'void Print_Mat\(matrix \*mat\)', line):
                    flag = 1
                if flag and re.search(r'for\(j=0;j<\d+;j\+\+\)', line):
                    line = re.sub(r'j<\d+', "j<50", line)
                    flag = 0
                ofp.write(line)


if __name__ == '__main__':
    updatemain("main.c", "main_updated.c")
    os.rename("main_updated.c", "main.c")

    updateio("io.c", "io_updated.c")
    os.rename("io_updated.c", "io.c")
