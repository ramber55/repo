import json


BAD_PARAMETER = "Bad Parameter Error"
DATA_NOT_FOUND = "Not found in Ensembl database"
ENSEMBL_COM_ERROR = "Communication problems with Ensembl server"
WRONG_REST_ENDPOINT = "Wrong Endpoint"


def build_json_error_msg(error_type, error_message, error_notes=None):
    error_dict = {"error_type": error_type, "error_message": error_message}
    if error_notes is not None:
        error_dict["error_notes"] = error_notes

    return json.dumps(error_dict)


def build_species_list_json_msg(nb_of_species, limit, species_list):
    response_dict = {"nb_of_species": nb_of_species, "limit": limit, "species": species_list}

    return json.dumps(response_dict)


def build_gene_seq_json_msg(gene_seq):
    response_dict = {"seq": gene_seq}

    return json.dumps(response_dict)


def build_chromo_length_json_msg(species, chromo, chromosome_length):
    response_dict = {"species": species, "chromo": chromo, "chromosome_length": chromosome_length}

    return json.dumps(response_dict)

