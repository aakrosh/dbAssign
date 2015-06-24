#!/usr/bin/env python

"""
Read and write fasta files
"""

__author__ = "Aakrosh Ratan"
__email__  = "ratan@bx.psu.edu"

from sys import argv
import string

class fastasequence:
    def __init__(self, name, seq):
        self.name = name
        self.seq  = seq

    @staticmethod
    def prettyprint_dna(seq, size):
        str = ""
        for i in range(0, len(seq), size):
            str += seq[i:i+size]
            str += "\n"
        return str[:-1]

    @staticmethod
    def reverse_complement(seq):
        complement = string.maketrans('atcgnATCGN', 'tagcnTAGCN')
        return seq.translate(complement)[::-1]
      
    def __str__(self):
        str =  ">%s\n" % self.name
        str += self.prettyprint_dna(self.seq, 60)
        return str

    def __len__(self):
        return len(self.seq)

class fasta:
    def __init__(self, filename):
        self.file = open(filename, "rU")
        self.fastasequence = None
        self.cache = None

    def __iter__(self):
        return self

    def __del__(self):
        self.file.close()

    def close(self):
        self.file.close()

    def next(self):
        if self.cache != None:
            line = self.cache
        else:
            line = self.file.readline()
            
        if len(line) == 0:
            self.file.close()
            raise StopIteration
        assert line[0] == ">", "header should start with a > in a fasta file"
        assert line[-1] == "\n"
        name = line[1:-1]
        
        sequence = ""
        line = self.file.readline()

        while line[0] !=  ">" :
            sequence += line.strip()
            # if there is a gap in the sequence (which would be the case 
            # if the fasta sequence was of quality values)
            if(line.find(" ")) != -1:
                sequence += " "

            line = self.file.readline()
            if len(line) == 0:
                break

        self.cache = line
        self.fastasequence = fastasequence(name, sequence)
        return self
