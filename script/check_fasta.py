#!/usr/bin/python3

##########################################################################################
# Program: rehilight.py
# Purpose: Checks the .fasta file for incorrectly formatted names and if it finds any, 
# it will back up the file and fix the names
# Author: Peter Darley
# Date: 2023-04-24
##########################################################################################

import sys
import os
import argparse


def main(target: str):
    """ Check all the names in the fasta file and fix them if needed """

    files: list = []

    if os.path.isfile(target):
        files.append(target)

    elif os.path.isdir(target):
        for file in os.listdir(target):
            if file.endswith(".fasta"):
                files.append(f"{target}/{file}")
        
    else:
        sys.exit("Either fasta_file or directory must be specified")

    for file in files:
        if fix_names_in_file(fasta_file=file):
            print(f"Fixed file:\n\t {file} \nand saved the original as: \n\t{file}.bak")
            

def fix_names_in_file(*, fasta_file: str=None) -> bool:
    """ Fix the fasta file """

    is_bad: bool = False
    new_file: str = ""

    with open(fasta_file, "r") as file_handle:
        for line in file_handle:
            line = line.strip()

            if line.startswith(">"):
                if name := fix_name(name=line):
                    is_bad = True

                    new_file += f"{name}\n"
                else:
                    new_file += f"{line}\n"
            else:
                new_file += f"{line}\n"

    if is_bad:
        backup_file: str = f"{fasta_file}.bak"
        os.rename(fasta_file, backup_file)

        with open(fasta_file, "w") as file_handle:
            file_handle.write(new_file)

    return is_bad   


def fix_name(*, name: str) -> str:
    """ Returns true if the name has disallowed characters """

    # Strip the first character (>)
    if name.startswith(">"):
        name = name[1:]

    good_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    bad_chars: set = set()

    for char in name:
        if char not in good_chars and char not in bad_chars:
            bad_chars.add(char)
    
    for char in bad_chars:
        name = name.replace(char, "_")

    if bad_chars:
        return f">{name}"
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="input sequence fasta file or directory", nargs="+", type=str)
    # parser.add_argument("-d", "--dir", help="directory to hold input sequence fasta file", nargs="?", const=1, type=str, default=".")

    targets = parser.parse_args().target

    if type(targets) != list:
        targets = [targets]
    
    for target in targets:
        main(target=target)