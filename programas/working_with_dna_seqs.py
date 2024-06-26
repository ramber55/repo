from pathlib import Path
from dna_seq_mgmt import *
from pprint import pprint


DNA_REPOSITORY = Path.cwd().parent / "resources"

ADA_filename = "Homo_sapiens_ADA_sequence.fa"
ADA_full_filename = DNA_REPOSITORY / ADA_filename

RNU6_269P_filename = "Homo_sapiens_RNU6_269P_sequence.fa"
RNU6_269P_full_filename = DNA_REPOSITORY / RNU6_269P_filename

ADA_sequence = DNA_SEQUENCE()
ADA_sequence.read_seq_from_file(ADA_full_filename)

RNU6_269P_sequence = DNA_SEQUENCE()
RNU6_269P_sequence.read_seq_from_file(RNU6_269P_full_filename)

print("DNA Header:", ADA_sequence.get_header())
print("---------------------------------------------------------------")
print("DNA Seq   :", ADA_sequence.get_body())

print("DNA file:", ADA_filename)
print("The first 20 bases are:")
print(ADA_sequence.get_body()[:20])

print("Gene ADA ->", len(ADA_sequence))

print(ADA_sequence)

print("DNA           Seq   :", ADA_sequence.get_body())
print("Complementary Seq   :", ADA_sequence.seq_complement())

print("ADA Bases report:")
pprint(ADA_sequence.seq_count())
print("Most Frequent base:", ADA_sequence.get_most_frequent_base())

print("RNU6_269P Bases report:")
pprint(RNU6_269P_sequence.seq_count())
print("Most Frequent base:", RNU6_269P_sequence.get_most_frequent_base())

print("\n\n======================\n\n")
seq_list1 = generate_seqs("ACXG", 4)
pprint(seq_list1)
print("\n\n======================\n\n")

seq1 = DNA_SEQUENCE("CORRECT SEQ HDR", "ACGTAAAAG")
seq2 = DNA_SEQUENCE(None, "BUAAAA")
seq3 = DNA_SEQUENCE(None, None)

list_of_sequences = [seq1, seq2, seq3]
print("Sequences:")
nb_of_sequence = 1
for dna_seq in list_of_sequences:
    print("------------")
    print("SEQUENCE", nb_of_sequence)
    print(dna_seq)
    print("Bases: ", str(dna_seq.seq_count()))
    print("Reverse:", dna_seq.seq_reverse())
    print("Complement:", dna_seq.seq_complement())
    nb_of_sequence += 1



