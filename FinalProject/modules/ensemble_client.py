import http.client
import json
import termcolor

GEN_ID = "ENSP00000288602"  # FRAT
GEN_ID = "ENSG00000165879"
SERVER = "rest.ensembl.org"
ENDPOINT_PREFIX = "/sequence/id"
FULL_ENDPOINT = ENDPOINT_PREFIX + "/" + GEN_ID
PARAMS = "?content-type=application/json"
URL = SERVER + FULL_ENDPOINT + PARAMS

print()
print(f"Server: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", FULL_ENDPOINT + PARAMS)
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

print("Sequence:", response["seq"])
print("id:", response["id"])
print("desc:", response["desc"])
print("molecule:", response["molecule"])
print("version:", response["version"])
