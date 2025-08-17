#! /usr/bin/python3

import sys

text = sys.argv[1]
out = ''

for c in text:
    a = ord(c)
    out += '>'  # "allocate" memory cell
    out += '+' * a
    out += '.'

print(out)
