import http.client
import json
import termcolor

ENSEMBL_SERVER = "rest.ensembl.org"
PARAMS = "?content-type=application/json"

ENDPOINT_INFO_SPECIES = "/info/species"

class GB_ensemble_client:
    def __init__(self):
        print("GB_ensemble_client initialized. Server:", ENSEMBL_SERVER)

    def send_request(self, service_endpoint):
        full_endpoint = service_endpoint + PARAMS
        conn = http.client.HTTPConnection(ENSEMBL_SERVER)

        try:
            conn.request("GET", full_endpoint + PARAMS)
        except ConnectionRefusedError:
            print("ERROR! Cannot connect to the Server")
            exit()

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Print the status line
        print(f"Response received!: {r1.status} {r1.reason}\n")

        # -- Read the response's body
        response = json.loads(r1.read().decode("utf-8"))

        termcolor.cprint("Received INFO", 'yellow', end="", force_color=True)
        print()
        return response

