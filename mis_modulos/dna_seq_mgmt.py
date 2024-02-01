# DNA Sequence Management functions, classes, ...
def seq_read_fasta(filename):
    try:

        with open(filename, "r", encoding="latin-1") as f:
            header = next(f).replace("\n", "")
            seq = ""
            for line in f:
                seq += line.replace("\n", "")
            seq.replace("\n", "")

        f.close()

    except FileNotFoundError:
        print("ERROR: file", filename, "not found. Exiting.")
        exit()
    except PermissionError:
        print("ERROR: No permissions for file", filename, "Exiting.")
        exit()

    return header, seq


def seq_len(seq):
    return len(seq)


class DNA_SEQUENCE:

    def __init__(self):
        self.header = ""
        self.body = ""

    def read_seq_from_file (self, filename):
        self.header, self.body = seq_read_fasta(filename)

    def __len__(self):
        return len(self.body)

    def __str__(self):
        return f"DNA Sequence Header: {self.header}\nDNA #Bases:  {len(self.body)}\nDNA Sequence Body:   {self.body}"

    def get_header(self):
        return self.header

    def get_body(self):
        return self.body

    def set_header(self, header):
        self.header = header

    def set_body(self, body):
        self.body = body
