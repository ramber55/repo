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


