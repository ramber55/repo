from pathlib import Path

import jinja2 as j

GBSERVER_DIR = Path.cwd()
HTML_FOLDER = GBSERVER_DIR / "HTML"

INPUT_DATA_ERROR = "Input Data Error"


def read_html_file(filename):
    contents = Path(HTML_FOLDER / filename).read_text()
    contents = j.Template(contents)
    return contents


def list_to_html_list(python_list):
    html_list = "<ul>\n"
    for item in python_list:
        html_list += f"<li>{item}</li>\n"
    html_list += "</ul>\n"
    return html_list


def build_customized_error_page(error_type, error_message, error_notes=None):
    if error_notes is None:
        error_notes = ""
    contents = read_html_file("customized_error.html").render(context={"error_type": error_type, "error_message": error_message, "error_notes": error_notes})
    return contents


def build_species_list_page(nb_of_species, limit, species_list):
    limit_str = str(limit)
    if limit == 0:
        limit_str = "None"
    html_list = list_to_html_list(species_list)
    contents = read_html_file("SpeciesList.html").render(context={"nb_of_species": nb_of_species, "limit": limit_str, "species_list": html_list})
    return contents


