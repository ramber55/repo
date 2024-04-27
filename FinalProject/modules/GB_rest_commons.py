import json


BAD_PARAMETER = "Bad Parameter Error"


def build_json_error_msg(error_type, error_message, error_notes=None):
    error_dict = {"error_type": error_type, "error_message": error_message}
    if error_notes is not None:
        error_dict["error_notes"] = error_notes

    return json.dumps(error_dict)


def build_species_list_json_msg(nb_of_species, limit, species_list):
    response_dict = {"nb_of_species": nb_of_species, "limit": limit, "species": species_list}

    return json.dumps(response_dict)


