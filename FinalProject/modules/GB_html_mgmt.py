import sys
from pathlib import Path

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
            error_message = f"'limit' must be a positive integer number."
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
