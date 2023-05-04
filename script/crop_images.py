#!/usr/bin/python

##########################################################################################
# Program: crop_images.py
# Purpose: In user's working directory with highlighter image files (*_untrimmed.png),
# crops images to the right size
# Author: Wenjie Deng
# Date: 2023-05-04
##########################################################################################


import sys, os
import argparse
import glob


def main(wdir):
	print("\n**** Crop highlighter images ****\n")
	for file in glob.glob(os.path.join(wdir, '*_untrimmed.png')):
		cropfile = file.replace("_untrimmed.png", ".png")
		cropcommand = f"convert -crop +0+150 -crop -0-50 {file} {cropfile}"
		print(cropcommand)
		os.system(cropcommand)
	

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="directory to hold input sequence fasta file", nargs="?", const=1, type=str, default=".")
    args = parser.parse_args()
    wdir = args.dir

    main(wdir)
