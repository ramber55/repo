from dna_seq_mgmt import *

DNA_REPOSITORY = "../recursos/"
filename = "Homo_sapiens_ADA_sequence.fa"
dna_header, dna_chain = seq_read_fasta(DNA_REPOSITORY + filename)

print("DNA Header:", dna_header)
print("---------------------------------------------------------------")
print("DNA Seq   :", dna_chain)

print("DNA file:", filename)
print("The first 20 bases are:")
print(dna_chain[:20])

print("Gene ADA ->", seq_len(dna_chain))