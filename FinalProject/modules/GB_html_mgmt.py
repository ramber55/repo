import sys
from pathlib import Path
from pprint import pprint

import GB_html_commons
import GB_ensembl_client


GBSERVER_DIR = Path.cwd()
HTML_FOLDER = GBSERVER_DIR / "HTML"

gb_ensembl_handler = GB_ensembl_client.GB_ensembl_handler()

class GB_html_handler:
    def __init(self):
        print("GB_html_handler initialized")

    def getSpeciesList(self, parsed_arguments):
        received_limit = parsed_arguments.get("limit", ["0"])
        try:
            limit = int(received_limit[0])
        except ValueError:
            error_message = f"limit = {received_limit} is not valid. It must be a positive integer number."
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.INPUT_DATA_ERROR, error_message)
            return contents

        if limit < 0:
            error_message = "'limit' must be a positive integer number."
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.INPUT_DATA_ERROR, error_message)
            return contents

        try:
            species_list = gb_ensembl_handler.get_list_of_species(limit)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        try:
            contents = GB_html_commons.build_species_list_page(species_list[0], limit, species_list[1])
        except FileNotFoundError:
            error_message = "SpeciesList.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        return contents

    def getGeneSeq(self, parsed_arguments):
        if "gene" not in parsed_arguments:
            error_message = "Gene name must be specified."
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.INPUT_DATA_ERROR, error_message)
            return contents

        friendly_gene_name = parsed_arguments["gene"][0]

        try:
            ensembl_rest_error, gene_seq = gb_ensembl_handler.get_gene_seq_by_friendly_name(friendly_gene_name)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{friendly_gene_name} has not been found in Ensembl database"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.INPUT_DATA_ERROR, error_message)
            return contents

        try:
            contents = GB_html_commons.build_gene_seq_page(friendly_gene_name, gene_seq)
        except FileNotFoundError:
            error_message = "GeneSeq.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        return contents

    def getChromosomeLenght(self, parsed_arguments):

        species = parsed_arguments["species"][0]
        chromo = parsed_arguments["chromo"][0]

        try:
            ensembl_rest_error, chromosome_length = gb_ensembl_handler.get_chromosome_length(species, chromo)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        try:
            contents = GB_html_commons.build_chromo_length_page(species, chromo, chromosome_length)
        except FileNotFoundError:
            error_message = "ChromosomeLength.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.PAGEFILE_NOTFOUND_ERROR, error_message)
            return contents

        return contents
    def getKaryotype(self, parsed_arguments):

        species = parsed_arguments["species"][0]

        try:
            ensembl_rest_error, karyotype = gb_ensembl_handler.get_karyotype(species)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        try:
            contents = GB_html_commons.build_karyotype_page(species, karyotype)
        except FileNotFoundError:
            error_message = "Karyotype.html is not present"
            error_notes = "Genome Browser installation may be corrupted"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.PAGEFILE_NOTFOUND_ERROR, error_message, error_notes)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_html_commons.build_customized_error_page(GB_html_commons.PAGEFILE_NOTFOUND_ERROR, error_message)
            return contents

        return contents
