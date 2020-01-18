#!/usr/bin/python3
import argparse, re, sys

memsize = 10

parser = argparse.ArgumentParser(description='Assemble subleq code')
parser.add_argument("infile")
parser.add_argument("outfile")

args = parser.parse_args()

with open(args.infile) as f:
    parsetext = f.readlines()

labels = {}
index = 0
for realindex, line in enumerate(parsetext):
    parsed = line.strip()
    if parsed == "" or parsed.startswith("//"):
        # Comment
        pass
    elif re.match(r"[a-zA-Z_][a-zA-Z_0-9]*:", parsed):
        # Label
        labels[parsed[:-1]] = index
    elif re.match(r"subleq\s+[a-zA-Z_][a-zA-Z_0-9]*\s+[a-zA-Z_][a-zA-Z_0-9]*\s+[a-zA-Z_][a-zA-Z_0-9]*"):
        index += 1
    else:
        print(f"Invalid token on line {realindex}")
        sys.exit(1)
instructions = []

