import http.client
import json
import termcolor

ENSEMBL_SERVER = "rest.ensembl.org"
PARAMS = "?content-type=application/json"

ENDPOINT_INFO_SPECIES = "/info/species"
GEN_ID = "ENSG00000165879"
ENDPOINT_GET_GEN = "/sequence/id/" + GEN_ID

class GB_ensembl_handler:
    def __init__(self):
        print("GB_ensemble_client initialized. Server:", ENSEMBL_SERVER)

    def send_request(self, service_endpoint):
        full_endpoint = service_endpoint + PARAMS
        conn = http.client.HTTPConnection(ENSEMBL_SERVER)

        # exceptions arisen from request are catched at the calling function:
        print("Endpoint:", full_endpoint)
        conn.request("GET", full_endpoint)

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Print the status line
        print(f"Response received!: {r1.status} {r1.reason}\n")

        # -- Read the response's body
        response = json.loads(r1.read().decode("utf-8"))

        termcolor.cprint("Received INFO", 'yellow', end="", force_color=True)
        print()
        return response

    def get_list_of_species(self, limit):
        ensembl_species = self.send_request(ENDPOINT_INFO_SPECIES)

        ensembl_list_of_species = ensembl_species["species"]

        limit_to_apply = False
        if limit != 0:
            limit_to_apply = True

        list_of_species = []
        nb_of_species = 0
        copied_species = 0
        for specie_item in ensembl_list_of_species:
            if specie_item["division"] == "EnsemblVertebrates":
                nb_of_species += 1
                if not limit_to_apply or copied_species < limit:
                    list_of_species.append(specie_item["display_name"])
                    copied_species += 1
            else:
                print("descartado")

        return nb_of_species, list_of_species
