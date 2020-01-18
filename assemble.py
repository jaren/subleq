#!/usr/bin/python3
import argparse, re, sys

memsize = 10

parser = argparse.ArgumentParser(description='Assemble subleq code')
parser.add_argument("infile")
parser.add_argument("outfile")

args = parser.parse_args()

with open(args.infile) as f:
    parsetext = [x.strip() for x in f.readlines()]

label = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*:")
number = re.compile(r"-?[0-9]+")
instruction = re.compile(r"subleq\s+[a-zA-Z_][a-zA-Z_0-9]*\s+[a-zA-Z_][a-zA-Z_0-9]*(\s+[a-zA-Z_][a-zA-Z_0-9]*)?")

labels = {}
index = 0
# First pass, find labels
for realindex, line in enumerate(parsetext):
    if line == "" or line.startswith("//"):
        # Comment
        pass
    elif label.match(line):
        # Label
        labels[line[:-1]] = index
    elif number.match(line) or instruction.match(line):
        # Instruction or literal
        index += 1
    else:
        print(f"Invalid token on line {realindex + 1}")
        sys.exit(1)

# Split 32 bit number into array of 8 bit numbers
def split32(i):
   return [(i >> 24) & 0xff, (i >> 16) & 0xff, (i >> 8) & 0xff, (i & 0xff)]

memvals = []
index = 0
# Second pass, find memory values
for line in parsetext:
    # TODO: Should probably be some bounds check
    if number.match(line):
        i = int(line)
        # Split into bytes and append
        memvals.extend(split32(i))
        #print(line)
        #print(split32(i))
        index += 1
    if instruction.match(line):
        params = line.split()[1:]
        if len(params) == 2:
            params.append(str(index + 1))
        for i in range(3):
            if not number.match(params[i]):
                params[i] = labels[params[i]]
            params[i] = int(params[i])
            if params[i] < 0 or params[i] >= 2**memsize:
                print(f"Memory address out of range: {params[i]}")
                sys.exit(1)
        val = params[0] | (params[1] << 10) | (params[2] << 20)
        memvals.extend(split32(val))
        #print(line)
        #print(split32(val))
        index += 1

# Extend to proper size
if len(memvals) < 2**memsize:
    memvals.extend([0] * (2**memsize - len(memvals)))

with open(args.outfile, "wb") as f:
    f.write(bytearray(memvals))
