import sys

import GB_ensembl_client
import GB_rest_commons

gb_ensembl_handler = GB_ensembl_client.GB_ensembl_handler()

class GB_rest_handler:
    def __init(self):
        print("GB_rest_handler initialized")

    def getWrongRestEndpoint(self, path):
        error_message = f"Requested endpoint {path} does not exist."
        contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.WRONG_REST_ENDPOINT, error_message)
        return contents

    def getSpeciesList(self, parsed_arguments):
        received_limit = parsed_arguments.get("limit", ["0"])
        try:
            limit = int(received_limit[0])
        except ValueError:
            error_message = f"'limit' must be a positive integer number."
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.BAD_PARAMETER, error_message)
            return contents

        if limit < 0:
            error_message = f"'limit' must be a positive integer number."
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.BAD_PARAMETER, error_message)
            return contents

        try:
            species_list = gb_ensembl_handler.get_list_of_species(limit)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        contents = GB_rest_commons.build_species_list_json_msg(species_list[0], limit, species_list[1])

        return contents

    def getGeneSeq(self, parsed_arguments):
        if "gene" not in parsed_arguments:
            error_message = "'gene' must be specified."
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.BAD_PARAMETER, error_message)
            return contents

        friendly_gene_name = parsed_arguments["gene"][0]

        try:
            ensembl_rest_error, gene_seq = gb_ensembl_handler.get_gene_seq_by_friendly_name(friendly_gene_name)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        if ensembl_rest_error:
            error_message = f"{friendly_gene_name} has not be found in Ensembl database"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.DATA_NOT_FOUND, error_message)
            return contents

        contents = GB_rest_commons.build_gene_seq_json_msg(gene_seq)

        return contents
    def getChromosomeLenght(self, parsed_arguments):
        if "species" not in parsed_arguments:
            error_message = "Species name must be specified."
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.BAD_PARAMETER, error_message)
            return contents

        if "chromo" not in parsed_arguments:
            error_message = "Chromosome name must be specified."
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.BAD_PARAMETER, error_message)
            return contents

        species = parsed_arguments["species"][0]
        chromo = parsed_arguments["chromo"][0]

        try:
            ensembl_rest_error, chromosome_length = gb_ensembl_handler.get_chromosome_length(species, chromo)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        contents = GB_rest_commons.build_chromo_length_json_msg(species, chromo, chromosome_length)

        return contents
    def getKaryotype(self, parsed_arguments):
        if "species" not in parsed_arguments:
            error_message = "The species must be specified."
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.BAD_PARAMETER, error_message)
            return contents
        species = parsed_arguments["species"][0]

        try:
            ensembl_rest_error, karyotype = gb_ensembl_handler.get_karyotype(species)
        except ConnectionRefusedError:
            error_message = "Cannot connect to the Server"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents
        except Exception as ex:
            error_message = f"{type(ex)} {sys.exc_info()[0]}"
            contents = GB_rest_commons.build_json_error_msg(GB_rest_commons.ENSEMBL_COM_ERROR, error_message)
            return contents

        contents = GB_rest_commons.build_karyotype_json_msg(species, karyotype)

        return contents

