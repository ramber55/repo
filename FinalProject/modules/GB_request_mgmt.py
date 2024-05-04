import sys
from pathlib import Path

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

    def getGeneCalc(self, rest_request, parsed_arguments):
        if "gene" not in parsed_arguments:
            error_message = "Gene name must be specified."
            contents = super().build_error_response(rest_request, PARAMETER_ERROR, error_message)
            return contents

        friendly_gene_name = parsed_arguments["gene"][0]

        try:
            ensembl_rest_error, gene_seq = self.ensembl_handler.get_gene_info_by_friendly_name(friendly_gene_name)
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
            contents = super().build_gene_calc_response(friendly_gene_name)
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
