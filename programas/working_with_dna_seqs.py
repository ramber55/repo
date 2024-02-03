from pathlib import Path
from dna_seq_mgmt import *
from pprint import pprint


DNA_REPOSITORY = Path.cwd().parent / "recursos"
filename = "Homo_sapiens_ADA_sequence.fa"
ADA_full_filename = DNA_REPOSITORY / filename

ADA_sequence = DNA_SEQUENCE()
ADA_sequence.read_seq_from_file(ADA_full_filename)

print("DNA Header:", ADA_sequence.get_header())
print("---------------------------------------------------------------")
print("DNA Seq   :", ADA_sequence.get_body())

print("DNA file:", filename)
print("The first 20 bases are:")
print(ADA_sequence.get_body()[:20])

print("Gene ADA ->", len(ADA_sequence))

print(ADA_sequence)

print("DNA           Seq   :", ADA_sequence.get_body())
print("Complementary Seq   :", ADA_sequence.seq_complement())

print("ADA Bases report:")
pprint(ADA_sequence.seq_count())
print("Most Frequent base:", ADA_sequence.get_most_frequent_base())
