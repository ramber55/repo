from pathlib import Path

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


class DNA_SEQUENCE:

    def __init__(self):
        self.header = ""
        self.body = ""

    def read_seq_from_file(self, filename):
        self.header, self.body = seq_read_fasta(filename)

    def __len__(self):
        return len(self.body)

    def __str__(self):
        return f"DNA Sequence Header:{self.header}\nDNA #Bases:\t\t\t{len(self.body)}\nDNA Sequence Body:\t{self.body}"

    def __eq__(self, other):
        return self.body == other.get_body()

    def get_header(self):
        return self.header

    def get_body(self):
        return self.body

    def set_header(self, header):
        self.header = header

    def set_body(self, body):
        self.body = body

    def seq_count_base(self, base):
        return self.body.count(base)

    def seq_count(self):
        base_count = {}
        for base in DNA_Bases:
            nb_of_occurrences = self.seq_count_base(base)
            if nb_of_occurrences != 0:
                base_count[base] = nb_of_occurrences
        return base_count

    def seq_reverse(self):
        return self.body[::-1]

    def seq_complement(self):
        complementary_chain = ""
        for base in self.body:
            complementary_chain += Complementary_Bases[base]
        return complementary_chain
