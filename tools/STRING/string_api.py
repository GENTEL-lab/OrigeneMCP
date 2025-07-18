import requests

class StringAPI:
    BASE_URL = "https://version-12-0.string-db.org/api"
    
    def __init__(self):
        self.session = requests.Session()

    def mapping_identifiers(self,identifiers,species,limit=1,echo_query=1,output_format = "json",caller_identity="lglab"):
        """Get STRING identifiers for list of genes"""
        method = "get_string_ids"
        params = {
            "identifiers" : "\r".join(identifiers), # your protein list
            "species" : species, # NCBI/STRING taxon identifier 
            "limit" : limit, # only one (best) identifier per input protein
            "echo_query" : echo_query, # see your input identifiers in the output
            "caller_identity" : caller_identity # your app name
        }

        request_url = "/".join([self.BASE_URL, output_format, method])
        results = self.session.post(request_url, data=params)
        # for line in results.text.strip().split("\n"):
        #     l = line.split("\t")
        #     input_identifier, string_identifier = l[0], l[2]
        #     print("Input:", input_identifier, "STRING:", string_identifier, sep="\t")
        return results.text
    
    # def get_string_network_image(self, genes, species, output_format: str = "image", add_white_node=15,network_flavor="confidence",caller_identity="lglab"):
    #     """Get network for list of genes"""
    #     method = "network"
    #     request_url = "/".join([self.BASE_URL, output_format, method])
    #     results = []
    #     for gene in genes:
    #         params = {
    #         "identifiers" : gene, # your protein
    #         "species" : species, # NCBI/STRING taxon identifier 
    #         "add_white_nodes": add_white_node, # add 15 white nodes to my protein 
    #         "network_flavor": network_flavor, # show confidence links
    #         "caller_identity" : caller_identity # your app name
    #         }
    #         result = self.session.post(request_url, params=params)
    #         results.append(result.text)
    #     return results
    
    # def link_to_network_on_string_webpage(self):
    #     return None
    
    # def link_to_search_result_page(self):
    #     return None
    
    def get_string_network_interaction(self,identifiers,species,required_score,add_nodes,network_type='functional',show_query_node_labels=0,output_format = "json",caller_identity="lglab"):
        method = "network"
        params = {
            "identifiers" : "%0d".join(identifiers), # your protein list
            "species" : species, # NCBI/STRING taxon identifier
            "required_score": required_score,
            "add_nodes":add_nodes,
            "network_type":network_type,
            "show_query_node_labels":show_query_node_labels, 
            "caller_identity" : caller_identity # your app name
        }

        request_url = "/".join([self.BASE_URL, output_format, method])
        results = self.session.post(request_url, data=params)
        
        return results.text
    
    def get_all_interaction_partners_of_the_protein_set(self,identifiers,species,limit,required_score,network_type='functional',output_format = "json",caller_identity="lglab"):
        method = "interaction_partners"
        params = {
            "identifiers" : "%0d".join(identifiers), # your protein list
            "species" : species, # NCBI/STRING taxon identifier
            "required_score": required_score,
            "limit":limit,
            "network_type":network_type,
            "caller_identity" : caller_identity # your app name
        }

        request_url = "/".join([self.BASE_URL, output_format, method])
        results = self.session.post(request_url, data=params)
        return results.text
    
    def get_similarity_scores_of_the_protein_set(self,identifiers,species,output_format = "json",caller_identity="lglab"):
        method = "homology"
        params = {
            "identifiers" : "%0d".join(identifiers), # your protein list
            "species" : species, # NCBI/STRING taxon identifier
            "caller_identity" : caller_identity # your app name
        }
        request_url = "/".join([self.BASE_URL, output_format, method])
        results = self.session.post(request_url, data=params)
        return results.text
    
    def get_best_similarity_hits_between_species(self,identifiers,species,species_b,output_format = "json",caller_identity="lglab"):
        method = "homology_best"
        params = {
            "identifiers" : "%0d".join(identifiers), # your protein list
            "species" : species, # NCBI/STRING taxon identifier
            "species_b": species_b,
            "caller_identity" : caller_identity # your app name
        }
        request_url = "/".join([self.BASE_URL, output_format, method])
        results = self.session.post(request_url, data=params)
        return results.text
    
    def get_functional_enrichment(self,identifiers,background_string_identifiers,species,output_format = "json",caller_identity="lglab"):
        method = "enrichment"
        params = {
            "identifiers" : "%0d".join(identifiers), # your protein list
            "species" : species, # NCBI/STRING taxon identifier
            "background_string_identifiers": background_string_identifiers,
            "caller_identity" : caller_identity # your app name
        }
        request_url = "/".join([self.BASE_URL, output_format, method])
        results = self.session.post(request_url, data=params)
        return results.text
    
    def get_functional_annotation(self,identifiers,species,allow_pubmed=0,only_pubmed=0,output_format = "json",caller_identity="lglab"):
        method = "functional_annotation"
        params = {
            "identifiers" : "%0d".join(identifiers), # your protein list
            "species" : species, # NCBI/STRING taxon identifier
            "allow_pubmed": allow_pubmed,
            "only_pubmed": only_pubmed,
            "caller_identity" : caller_identity # your app name
        }
        request_url = "/".join([self.BASE_URL, output_format, method])
        results = self.session.post(request_url, data=params)
        return results.text
    
    # def get_enrichment_figure(self):
    #     return None
    
    def get_ppi_enrichment(self, identifiers, species, output_format: str = "json", caller_identity="lglab",**kwargs):
        """Get protein-protein interaction enrichment for list of genes by their STRING identifiers"""
        request_url = "/".join([self.BASE_URL, output_format, "ppi_enrichment"])
        params = {
            "identifiers" : "%0d".join(identifiers), # your proteins
            "species" : species, # NCBI/STRING taxon identifier 
            "caller_identity" : caller_identity # your app name
        }
        return self.session.post(request_url, params=params).text

    # def valuesranks_enrichment_submit(self, data: Dict, api_key: str, output_format: str = "json"):
    #     """Submit values/ranks enrichment analysis"""
    #     request_url = "/".join([self.BASE_URL, output_format, "valuesranks_enrichment_submit"])
    #     params = {"api_key": api_key}
    #     return self.session.post(request_url, params=params, json=data)
    
    # def valuesranks_enrichment_status(self, job_id: str, api_key: str, output_format: str = "json"):
    #     """Check status of enrichment analysis"""
    #     request_url = "/".join([self.BASE_URL, output_format, "valuesranks_enrichment_status"])
    #     params = {"api_key": api_key, "job_id": job_id}
    #     return self.session.get(request_url, params=params)

if __name__ == "__main__":
    # Initialize and run the server
    st = StringAPI()
    result = st.mapping_identifiers(genes=['DRD1','DRD2'],species=9606)
    print(result.text)

    result = st.get_ppi_enrichment(identifiers=['9606.ENSP00000377353','9606.ENSP00000354859'],species=9606)
    print(result.text)