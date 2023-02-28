#!/usr/bin/python

######################################################################################
# This script calculates average sequence length in a fasta file
# Author: Wenjie Deng
# Date: 2023-02-28
# Usage: python average_length.py inputFastaFile
######################################################################################


def main(file):
    seqcount, seqlen, avglen = 0, 0, 0
    with open(file, "r") as fp:
        for line in fp:
            line = line.strip()
            if line:
                if line.startswith(">"):
                    seqcount += 1
                else:
                    line = line.replace("-", "")
                    seqlen += len(line)
        avglen = round(seqlen / seqcount)

        return avglen


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input sequence fasta file")
    args = parser.parse_args()
    infile = args.infile

    main(infile)
