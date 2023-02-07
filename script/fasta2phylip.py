#!/usr/bin/python

######################################################################################
# This script takes alignment sequence fasta file and converts it to phylip file
# Author: Wenjie Deng
# Date: 2022-05-05
# Usage: python fasta2Pphylip.py inputFastaFile outputPhilipFile
######################################################################################

import sys
import re
import argparse

def main(infile, outfile):
    names = []
    seqname = ""
    count, alignlen, seqlen, convertcount = 0, 0, 0, 0
    nameseq = {}

    with open(infile, "r") as fp:
        for line in fp:
            line = line.strip()
            if line:
                linematch = re.match(r'^>(\S+)', line)
                if linematch:
                    if count >= 1:
                        if seqlen != alignlen:
                            sys.exit("Sequences were not aligned: "+str(seqlen)+" vs "+str(alignlen))
                    count += 1
                    seqname = linematch.group(1)
                    names.append(seqname)
                    nameseq[seqname] = ""
                    seqlen = 0
                else:
                    nameseq[seqname] += line.upper()
                    seqlen += len(line)
                    if count == 1:
                        alignlen = seqlen
        if seqlen != alignlen:
            sys.exit("Sequences were not aligned")

    with open(outfile, "w") as of:
        of.write(str(count) + " " + str(alignlen) + "\n")
        for name in names:
            convertcount += 1
            seq = nameseq[name].replace("*", "-")
            of.write(name + "\t" + seq + "\n")

    log = "processed " + str(count) + " sequences, " + str(convertcount) + " converted"
    print(log)
    return log

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input sequence fasta file")
    parser.add_argument("outfile", help="output sequence phylip file")
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    main(infile, outfile)
