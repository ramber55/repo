import GB_html_commons
import GB_rest_commons

WRONG_REST_ENDPOINT = "Wrong Rest Endpoint"
WRONG_HTML_SERVICE = "Wrong Service"

class GB_request_forwarder:

    def __init__(self):
        # nothing to do
        pass

    def build_error_response(self, rest_request, error_type, error_message, error_notes=None):
        if rest_request:
            return GB_rest_commons.build_json_error_msg(error_type, error_message, error_notes)
        else:
            return GB_html_commons.build_customized_error_page(error_type, error_message, error_notes)

    def build_species_list_response(self, rest_request, nb_of_species, limit, species_list):
        if rest_request:
            return GB_rest_commons.build_species_list_json_msg(nb_of_species, limit, species_list)
        else:
            return GB_html_commons.build_species_list_page(nb_of_species, limit, species_list)

    def build_karyotype_response(self, rest_request, species, karyotype):
        if rest_request:
            return GB_rest_commons.build_karyotype_json_msg(species, karyotype)
        else:
            return GB_html_commons.build_karyotype_page(species, karyotype)

    def build_chromo_length_response(self, rest_request, species, chromo, chromosome_length):
        if rest_request:
            return GB_rest_commons.build_chromo_length_json_msg(species, chromo, chromosome_length)
        else:
            return GB_html_commons.build_chromo_length_page(species, chromo, chromosome_length)

    def build_gene_seq_response(self, rest_request, gene_name, gene_seq):
        if rest_request:
            return GB_rest_commons.build_gene_seq_json_msg(gene_seq)
        else:
            return GB_html_commons.build_gene_seq_page(gene_name, gene_seq)

    def build_gene_info_response(self, rest_request, gene_name, stable_id, start, end, length, chromo):
        if rest_request:
            return GB_rest_commons.build_gene_info_json_msg(stable_id, start, end, length, chromo)
        else:
            return GB_html_commons.build_gene_info_page(gene_name, stable_id, start, end, length, chromo)

    def build_gene_calc_response(self, rest_request, gene_name, gene_len, gene_bases_percentage):
        if rest_request:
            return GB_rest_commons.build_gene_calc_json_msg(gene_len, gene_bases_percentage)
        else:
            return GB_html_commons.build_gene_calc_page(gene_name, gene_len, gene_bases_percentage)

    def build_gene_list_response(self, rest_request, chromo, start, end, gene_list):
        if rest_request:
            return GB_rest_commons.build_gene_list_json_msg(gene_list)
        else:
            return GB_html_commons.build_gene_list_page(chromo, start, end, gene_list)

