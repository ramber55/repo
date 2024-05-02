from pathlib import Path

DNA_BASES = ["A", "T", "C", "G"]
COMPLEMENTARY_BASES = {"A": "T", "C": "G", "G": "C", "T": "A"}

class Seq:
    def __init__(self, strbases=None):
        if strbases is None:
            print("NULL sequence created")
            self.strbases = "NULL"
        else:
            count = 0
            for base in DNA_BASES:
                count += strbases.count(base)

            if count == len(strbases):
                self.strbases = strbases
                print("New sequence created!")
            else:
                print("INVALID sequence created")
                self.strbases = "ERROR"



    def generate_seqs(pattern, number):
        seq_list = []
        seq = ""
        for i in range(number):
            seq += pattern
            seq_list.append(Seq(seq))
        return seq_list


    def __len__(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        else:
            return len(self.strbases)


    def __str__(self):
        return self.strbases

    def count_base(self, base):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        else:
            number = 0
            for each_base in self.strbases:
                if each_base == base:
                    number += 1
            return number

    def seq_len(self):
        return len(self)

    def seq_count(self):
        bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return bases_dict
        else:
            length = self.seq_len()
            if length != 0:
                for base in self.strbases:
                    bases_dict[base] += 1
            return bases_dict

    def seq_reverse(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        else:
            return self.strbases[::-1]

    def seq_complement(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        else:
            complementary_seq = ""
            for base in self.strbases:
                complementary_seq += COMPLEMENTARY_BASES[base]
            return complementary_seq

    def read_fasta(self, filename):
        with open(filename, "r") as f:
            file_contents = Path(filename).read_text()
            list_contents = file_contents.split("\n")
            complete_seq = ""
            for i in range(1, len(list_contents)):
                complete_seq += (list_contents[i])
            f.close()
            self.strbases = complete_seq


    def percentage_of_bases(self):
        seq_length = self.seq_len()
        dict_of_bases = {"A": 0, "T": 0, "C": 0, "G": 0}
        percentage_of_each_base = {"A": 0, "T": 0, "C": 0, "G": 0}
        if seq_length != 0:
            for e in self.strbases:
                dict_of_bases[e] += 1
            for e in dict_of_bases:
                percentage_of_each_base[e] = str(round((dict_of_bases[e] / seq_length * 100), 1))

        return dict_of_bases, percentage_of_each_base


    def most_frequent_base(self):
        bases_count_dict = self.seq_count()
        most_frequent_base = ""
        max_nb_occurrences = 0
        for base in bases_count_dict:
            if bases_count_dict[base] > max_nb_occurrences:
                max_nb_occurrences = bases_count_dict[base]
                most_frequent_base = base
        return most_frequent_base