#!/usr/bin/python

######################################################################################
# This script parses the phyml output file and outputs pairwise distance file
# Author: Wenjie Deng
# Date: 2022-05-10
# Usage: python parse_dist.py inputPhymlFile outputDistFile
######################################################################################

import sys
import re
import argparse
from collections import defaultdict

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))


def main(infile, outfile):
    seqnnames, names, dists = [], [], []
    count, flag, pwcount = 0, 0, 0
    pwdist = nested_dict(2, str)

    with open(infile, "r") as fp:
        for line in fp:
            line = line.strip()
            if line:
                if re.match('- ML tree distance matrix \(after optimisation\)', line):
                    flag = 1
                    continue
                if (flag == 1 and re.match("\d+", line)):
                    count = int(re.match("(\d+)", line).group(1))
                    flag = 2
                    continue
                if re.search("^\.", line):
                    flag = 0
                if flag == 2:
                    linematch = re.search("^(\S+)\s+", line)
                    if linematch:
                        seqnnames.append(line)
                        names.append(linematch.group(1))

    if (len(names) != count and len(seqnnames) != count):
        sys.exit("names, sequnnames and count are not same: "+str(len(names))+", "+str(len(seqnnames))+" and "+str(count))

    for seqnname in seqnnames:
        seqnnamematch = re.search("^(\S+)\s+(.*?)$", seqnname)
        if seqnnamematch:
            name = seqnnamematch.group(1)
            diststr = seqnnamematch.group(2)
            dists = re.split("\s+", diststr)
            distcount = len(dists)
            if (distcount != count):
                sys.exit("distcount, count: "+str(distcount)+", "+str(count))
            for i in range(distcount):
                if name != names[i]:
                    pwdist[name][names[i]] = dists[i]

    with open(outfile, "w") as ofp:
        for i in range(count-1):
            for j in range(i+1, count):
                ofp.write(names[i]+"\t"+names[j]+"\t"+pwdist[names[i]][names[j]]+"\n")
                pwcount += 1

    log = "total " + str(count) + " sequences, "+str(pwcount)+" pairwise distances"

    return log

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input phyml output file")
    parser.add_argument("outfile", help="output pairwise distance file")
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    main(infile, outfile)
