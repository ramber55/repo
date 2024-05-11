from pathlib import Path

import jinja2 as j

GBSERVER_DIR = Path.cwd()
HTML_FOLDER = GBSERVER_DIR / "HTML"

INPUT_DATA_ERROR = "Input Data Error"
ENSEMBL_COM_ERROR = "Communication problems with Ensembl"
PAGEFILE_NOTFOUND_ERROR = "A required html file is not found"


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

def simple_list(python_list):
    html_list = ""
    for item in python_list:
        html_list += f"{item}<br>"
    return html_list

def string_from_bases_percentage_dict(percentage_of_each_base):
    html_list = "<ul>\n"
    html_list += f"<li>A : {percentage_of_each_base['A']}%</li>\n"
    html_list += f"<li>C : {percentage_of_each_base['C']}%</li>\n"
    html_list += f"<li>G : {percentage_of_each_base['G']}%</li>\n"
    html_list += f"<li>T : {percentage_of_each_base['T']}%</li>\n"
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


def build_gene_seq_page(gene_name, gene_seq):
    contents = read_html_file("GeneSeq.html").render(context={"gene_name": gene_name, "gene_seq": gene_seq})
    return contents


def build_chromo_length_page(species, chromo, chromosome_length):
    contents = read_html_file("ChromosomeLength.html").render(context={"species": species, "chromo": chromo, "chromosome_length": chromosome_length})
    return contents


def build_karyotype_page(species, karyotype):
    karyotype_list = simple_list(karyotype)
    contents = read_html_file("Karyotype.html").render(context={"species": species, "karyotype": karyotype_list})
    return contents


def build_gene_info_page(gene_name, stable_id, start, end, length, chromo):
    contents = read_html_file("GeneInfo.html").render(context={"gene_name": gene_name, "id": stable_id, "start": start, "end": end, "length": length, "chromo": chromo})
    return contents


def build_gene_calc_page(gene_name, gene_len, gene_bases_percentage):
    html_list = string_from_bases_percentage_dict(gene_bases_percentage)
    contents = read_html_file("GeneCalc.html").render(context={"gene_name": gene_name, "gene_len": gene_len, "gene_bases_percentage": html_list})
    return contents


def build_gene_list_page(start, end, chromo, gene_list):
    html_list = list_to_html_list(gene_list)
    contents = read_html_file("GeneList.html").render(context={"chromo": chromo, "start": start, "end": end, "gene_list": html_list})
    return contents