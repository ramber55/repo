from pathlib import Path

import jinja2 as j

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
        limit = int(received_limit[0])
        species_list = gb_ensembl_handler.get_list_of_species(limit)
        contents = GB_html_commons.build_species_list_page(species_list[0], limit, species_list[1])

        return contents
