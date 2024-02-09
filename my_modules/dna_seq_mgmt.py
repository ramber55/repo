from pathlib import Path
import termcolor

# DNA Sequence Management functions, classes, ...

DNA_Bases = ["A", "C", "G", "T"]
Complementary_Bases = {"A": "T", "T": "A", "C": "G", "G": "C"}


def seq_read_fasta(full_filename):
    try:

        with full_filename.open("r", encoding="latin-1") as f:
            header = next(f).replace("\n", "")
            seq = ""
            for line in f:
                seq += line.replace("\n", "")
            seq.replace("\n", "")

        f.close()

    except FileNotFoundError:
        print("ERROR: file", full_filename, "not found. Exiting.")
        exit()
    except PermissionError:
        print("ERROR: No permissions for file", full_filename, "Exiting.")
        exit()

    return header, seq


def seq_len(seq):
    return len(seq)


def is_dna_seq_ok(dna_seq):
    for base in dna_seq:
        if base not in DNA_Bases:
            return False
    return True


def generate_seqs(pattern, number):
    if is_dna_seq_ok(pattern) and number >= 1:
        seq_list = []
        aux_string = str(pattern)
        for i in range(number):
            seq_list.append(aux_string)
            aux_string += pattern
        return seq_list
    else:
        return ["ERROR"]


class DNA_SEQUENCE:

    def __init__(self, header=None, body=None):
        if header is None:
            self.header = "NO HEADER"
        else:
            self.header = header

        if body is None:
            self.body = "NULL"
        elif is_dna_seq_ok(body):
            self.body = body
        else:
            self.body = "ERROR"
            termcolor.cprint("DNA_SEQUENCE::constructor ERROR: Incorrect Sequence Detected!", "green")

    def read_seq_from_file(self, filename):
        self.header, self.body = seq_read_fasta(filename)
        if not is_dna_seq_ok(self.body):
            self.body = "ERROR"
            termcolor.cprint("DNA_SEQUENCE::read_seq_from_file ERROR: Incorrect Sequence Detected!", "green")

    def __len__(self):
        if self.body == "NULL" or self.body == "ERROR":
            return 0
        else:
            return len(self.body)

    def __str__(self):
        return f"DNA Sequence Header:{self.header}\nDNA #Bases:\t\t\t{len(self)}\nDNA Sequence Body:\t{self.body}"

    def __eq__(self, other):
        return self.body == other.get_body()

    def get_header(self):
        return self.header

    def get_body(self):
        return self.body

    def set_header(self, header):
        if header is None:
            self.header = "NO HEADER"
        else:
            self.header = header

    def set_body(self, body):
        if body is None:
            self.body = "NULL"
        elif is_dna_seq_ok(body):
            self.body = body
        else:
            self.body = "ERROR"
            termcolor.cprint("DNA_SEQUENCE::set_body ERROR: Incorrect Sequence Detected!", "yellow")

    def seq_count_base(self, base):
        return self.body.count(base)

    def seq_count(self):
        base_count = {}
        for base in DNA_Bases:
            nb_of_occurrences = self.seq_count_base(base)
            if nb_of_occurrences != 0:
                base_count[base] = nb_of_occurrences
        return base_count

    def get_most_frequent_base(self):
        base_count = self.seq_count()
        most_frequent_base = ""
        nb_of_most_frequent_base = 0
        for base, nb_of_occurrences in base_count.items():
            if nb_of_occurrences > nb_of_most_frequent_base:
                most_frequent_base = base
                nb_of_most_frequent_base = nb_of_occurrences
        return most_frequent_base

    def seq_reverse(self):
        return self.body[::-1]

    def seq_complement(self):
        complementary_chain = ""
        for base in self.body:
            complementary_chain += Complementary_Bases[base]
        return complementary_chain
