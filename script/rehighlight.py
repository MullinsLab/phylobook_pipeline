#!/usr/bin/python3

##########################################################################################
# Program: rehilight.py
# Purpose: Moves the naned sequence to the first line of the .fasta, making it the master
#   then runs highlighter_bot.py to build a new highligher plot
#   then trims the new highlighter plot
# Author: Peter Darley
# Date: 2023-04-24
##########################################################################################

import sys
import os
import argparse


def main(*, fasta_file: str=None, sequence_name: str=None, directory: str=None, amino_acid: bool=False):
    """ Do the main work of rehighlighting """

    outfile: str = ""
    base_file: str = fasta_file.replace(".fasta", "")

    png_file: str = f"{base_file}_highlighter.png"
    untrimmed_png_file = f"{base_file}_highlighter_untrimmed.png"
    highlighter_txt_file = f"{base_file}_highlighter.txt"
    highlighter_fasta_file = f"{base_file}_highlighter.fasta"

    pydir: str = os.path.dirname(os.path.realpath(__file__))
    
    print(f"\n**** Reordering {fasta_file} ****\n")

    # Step through the file to find the sequence that is the master
    found_line: bool = False

    with open(fasta_file, "r") as file_handle:
        for line in file_handle:
            line = line.strip()

            if found_line:
                if line.startswith(">"):
                    break
                outfile += f"{line}\n"

            if line == f">{sequence_name}":
                outfile += f"{line}\n"
                found_line = True
    
    if not found_line:
        sys.exit(f"Sequence name {sequence_name} not found in file {fasta_file}")
    
    # Step through again to find lines that aren't the master
    found_line = False

    with open(fasta_file, "r") as file_handle:
        for line in file_handle:
            line = line.strip()

            if found_line: 
                if line.startswith(">"):
                    found_line = False
                    outfile += f"{line}\n"
                continue

            if line == f">{sequence_name}":
                found_line = True
            else:
                outfile += f"{line}\n"

    # Write out the new file
    with open(f"{fasta_file}.temp", "wt+") as file_handle:
        file_handle.write(outfile)

    # Move the old file to .bak
    os.rename(fasta_file, f"{fasta_file}.bak")

    # Move the new file to the origional name
    os.rename(f"{fasta_file}.temp", fasta_file)

    # move the .png and delete the other _hilighter files
    if os.path.exists(png_file):
        os.rename(png_file, f"{png_file}.bak")

    if os.path.exists(untrimmed_png_file):
        os.remove(untrimmed_png_file)

    if os.path.exists(highlighter_txt_file):
        os.remove(highlighter_txt_file)

    if os.path.exists(highlighter_fasta_file):
        os.remove(highlighter_fasta_file)

    # Run the highlighter_bot
    print("\n**** Run highlight_bot ****\n")
    highlighter_script = os.path.join(pydir, "highlighter_bot.py")
    highlighter_command = f"python3 {highlighter_script} -d {directory} -f {fasta_file}"

    if amino_acid:
        highlighter_command += " -a"

    print(highlighter_command)
    os.system(highlighter_command)

    print("\n**** Crop highlighter image ****\n")
    # for file in glob.glob(os.path.join(wdir, '*_untrimmed.png')):
    #     pass

    cropcommand = f"convert -crop +0+150 -crop -0-50 {untrimmed_png_file} {png_file}"
    os.system(cropcommand)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fastafile", help="input sequence fasta file")
    parser.add_argument("sequencename", help="name of the sequence to make master")
    parser.add_argument("-d", "--dir", help="directory to hold input sequence fasta file", nargs="?", const=1, type=str, default=".")
    parser.add_argument("-a", "--aminoacid", help="flag for amino acid sequence")

    args = parser.parse_args()

    main(fasta_file=args.fastafile, sequence_name=args.sequencename, directory=args.dir, amino_acid=args.aminoacid)