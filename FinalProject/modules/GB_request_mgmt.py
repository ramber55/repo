import sys
from pathlib import Path

from seq1 import Seq

import GB_ensembl_client
import GB_req_forwarder


GBSERVER_DIR = Path.cwd()
HTML_FOLDER = GBSERVER_DIR / "HTML"

PARAMETER_ERROR = "Bad Parameter Error"
ENSEMBL_COMM_ERROR = "Communication problems with Ensembl"
# just for html requests:
PAGEFILE_NOTFOUND_ERROR = "A required html file is not found"
UNKNOWN_ERROR = "Unknown Error"
WRONG_REST_ENDPOINT = "Wrong Rest Endpoint"
HUMAN_KARYOTYPE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "X", "Y", "MT"]

def get_gene_calculations(gene_seq):
    seq = Seq(gene_seq)
    gene_len = seq.seq_len()
    dict_of_bases, percentage_of_each_base = seq.percentage_of_bases()
    return gene_len, percentage_of_each_base

class GB_request_handler (GB_req_forwarder.GB_request_forwarder):

    def __init__(self):
        super().__init__()
        self.ensembl_handler = GB_ensembl_client.GB_ensembl_handler()

    def getSpeciesList(self, rest_request, parsed_arguments):
        received_limit = parsed_arguments.get("limit", ["0"])
        try:
            limit = int(received_limit[0])
        except ValueError:
            error_message = f"limit = {received_limit} is not valid. It must be a positive integer number."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        if limit < 0:
            error_message = "'limit' must be a positive integer number."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        try:
            nb_of_species, list_of_species = self.ensembl_handler.get_list_of_species(limit)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents

        try:
            # this request in the case of a html request may arise an FileNotFoundError exception
            # for the SpeciesList.html
            contents = super().build_species_list_response(rest_request, nb_of_species, limit, list_of_species)
        except FileNotFoundError:
            error_message = "SpeciesList.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = super().build_error_response(rest_request, PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, UNKNOWN_ERROR, error_message)
            return contents

        return contents

    def getKaryotype(self, rest_request, parsed_arguments):
        if "species" not in parsed_arguments:
            error_message = "The species must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        species = parsed_arguments["species"][0]

        try:
            ensembl_rest_error, karyotype = self.ensembl_handler.get_karyotype(species)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{species} has not been found in Ensembl database"
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        try:
            contents = super().build_karyotype_response(rest_request, species, karyotype)
        except FileNotFoundError:
            error_message = "Karyotype.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = super().build_error_response(rest_request, PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, UNKNOWN_ERROR, error_message)
            return contents

        return contents

    def getChromosomeLenght(self, rest_request, parsed_arguments):
        if "species" not in parsed_arguments:
            error_message = "Species name must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        if "chromo" not in parsed_arguments:
            error_message = "Chromosome name must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        species = parsed_arguments["species"][0]
        chromo = parsed_arguments["chromo"][0]

        try:
            ensembl_rest_error, chromosome_length = self.ensembl_handler.get_chromosome_length(species, chromo)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = super().build_error_response(rest_request,ENSEMBL_COMM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{species} or its Chromosome {chromo} has not been found in Ensembl database"
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        try:
            contents = super().build_chromo_length_response(rest_request, species, chromo, chromosome_length)
        except FileNotFoundError:
            error_message = "ChromosomeLength.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = super().build_error_response(rest_request, PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, UNKNOWN_ERROR, error_message)
            return contents

        return contents

    def getGeneSeq(self, rest_request, parsed_arguments):
        if "gene" not in parsed_arguments:
            error_message = "Gene name must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        friendly_gene_name = parsed_arguments["gene"][0]

        try:
            ensembl_rest_error, gene_seq = self.ensembl_handler.get_gene_seq_by_friendly_name(friendly_gene_name)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{friendly_gene_name} has not been found in Ensembl database"
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        try:
            # this request in the case of a html request may arise an FileNotFoundError exception
            # for the SpeciesList.html
            contents = super().build_gene_seq_response(rest_request, friendly_gene_name, gene_seq)
        except FileNotFoundError:
            error_message = "GeneSeq.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = super().build_error_response(rest_request, PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, UNKNOWN_ERROR, error_message)
            return contents

        return contents

    def getGeneInfo(self, rest_request, parsed_arguments):
        if "gene" not in parsed_arguments:
            error_message = "Gene name must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        friendly_gene_name = parsed_arguments["gene"][0]

        try:
            ensembl_rest_error, stable_id, start, end, length, chromo = self.ensembl_handler.get_gene_info(friendly_gene_name)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{friendly_gene_name} has not been found in Ensembl database"
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        try:
            contents = super().build_gene_info_response(rest_request, friendly_gene_name, stable_id, start, end, length, chromo)
        except FileNotFoundError:
            error_message = "GeneInfo.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = super().build_error_response(rest_request, PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, UNKNOWN_ERROR, error_message)
            return contents

        return contents

    def getGeneCalc(self, rest_request, parsed_arguments):
        if "gene" not in parsed_arguments:
            error_message = "Gene name must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        friendly_gene_name = parsed_arguments["gene"][0]

        try:
            ensembl_rest_error, gene_seq = self.ensembl_handler.get_gene_seq_by_friendly_name(friendly_gene_name)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{friendly_gene_name} has not been found in Ensembl database"
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        gene_len, gene_bases_percentage = get_gene_calculations(gene_seq)

        try:
            contents = super().build_gene_calc_response(rest_request, friendly_gene_name, gene_len, gene_bases_percentage)
        except FileNotFoundError:
            error_message = "GeneCalc.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = super().build_error_response(rest_request, PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, UNKNOWN_ERROR, error_message)
            return contents

        return contents

    def getGeneList(self, rest_request, parsed_arguments):
        if "chromo" not in parsed_arguments:
            error_message = "Chromosomes name must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents
        if "start" not in parsed_arguments:
            error_message = "Start must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents
        if "end" not in parsed_arguments:
            error_message = "End must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        chromo = parsed_arguments["chromo"][0]

        if chromo not in HUMAN_KARYOTYPE:
            error_message = f"The chromosome ({chromo}) you entered is not part of the human karyotype, try from 1 to 22, X or Y."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        start_int = 0
        end_int = 0
        try:
            start_int = int(parsed_arguments["start"][0])
            end_int = int(parsed_arguments["end"][0])
        except ValueError:
            error_message = f"Start ({start_int}) and End ({end_int}) must be integers."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        if start_int < 0 or end_int < 0:
            error_message = f"Start ({start_int}) and End ({end_int}) must be positive."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        if (end_int - start_int) > 5000000:
            error_message = f"The maximum number of bases range allowed is 5000000."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        try:
            ensembl_rest_error, gene_list = self.ensembl_handler.get_gene_list(chromo, start_int, end_int)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, ENSEMBL_COMM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{chromo} has not been found in Ensembl database"
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents


        try:
            contents = super().build_gene_list_response(rest_request, chromo, start_int, end_int, gene_list)
        except FileNotFoundError:
            error_message = "GeneList.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = super().build_error_response(rest_request, PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = super().build_error_response(rest_request, UNKNOWN_ERROR, error_message)
            return contents

        return contents

    def build_WrongRestEndpoint_rest_msg(self, path):
        rest_request = True
        error_message = f"Requested endpoint {path} does not exist."
        contents = super().build_error_response(rest_request, WRONG_REST_ENDPOINT, error_message)
        return contents
        # error.html must be served

    def build_WrongResource_html_page(self, path):
        file_to_serve = HTML_FOLDER / "error.html"
        contents = file_to_serve.read_text("utf-8")
        return contents
