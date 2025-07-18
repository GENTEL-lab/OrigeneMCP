import requests
import json

class UNIPROTAPI:
    BASE_URL = "https://rest.uniprot.org/"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
        "accept": "application/json"
        }
    def _get(self, endpoint, params=None):
        """Internal helper for GET requests."""
        url = self.BASE_URL + endpoint
        try:
            r = requests.get(url, params=params, headers=self.headers)
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            try:
                content_type = r.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    error_detail = r.json()
                    print("Error details (JSON):")
                    print(json.dumps(error_detail, indent=2))
                else:
                    print("Error details (text):")
                    print(r.text)
            except Exception as e:
                print(f"Failed to parse error response: {e}")
            return None
        except Exception as err:
            print(f"Other error occurred: {err}")
            return None

    def get_uniprotkb_entry_by_accession(self, accession):
        """Search UniProtKB by protein entry accession to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""

        params = {
        # "fields": [
        #     "accession",
        #     "protein_name",
        #     "cc_function",
        #     "ft_binding"
        # ]
        }
        endpoint = "uniprotkb/" + accession
        return self._get(endpoint, params=params)
    
    def stream_uniprotkb_entries(self, query):
        """The stream endpoint uses a request query to return all entries associated with the search term in a single download. 
        Specify fields to return only data for specific sections of that entry that are of interest to you """
        params = {
        "query": query,
        # "fields": [
        #     "accession",
        #     "protein_name",
        #     "cc_function",
        #     "ft_binding"
        # ],
        # "sort": "accession desc"
        }
        endpoint = "uniprotkb/search"
        return self._get(endpoint, params=params)
    
    def search_uniprotkb_entries(self, query):
        """The search endpoint uses a request query to return all entries associated with the search term in a paginated list of entries. 
        Use ‘size’ to specify the number of entries per page of results. Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "query": query,
        "fields": [
            "accession", "id", "gene_names", "gene_primary", "organism_name", "organism_id", "protein_name", "lineage", "lineage_ids",
            "length", "ft_variant", "ft_act_site", "cc_catalytic_activity", "cc_cofactor", "ft_dna_bind", "ec", "cc_function", "kinetics", "cc_pathway",
            "ph_dependence", "redox_potential", "rhea", "cc_developmental_stage", "cc_induction", "cc_tissue_specificity", "go", "go_p", "go_c", "go_f",
            "xref_ensembl",
            "cc_function",
            "ft_binding",
            "structure_3d"
        ],
        # "sort": "accession desc",
        "size": "50"
        }
        endpoint = "uniprotkb/search"
        return self._get(endpoint, params=params)

    def get_general_info_by_protein_or_gene_name(self,query: str, species: str = 'Homo sapiens'):
        """
        Get general information of a protein or gene by name from UniProt database.
        Args:
            name: Protein or gene name.
            sepcies: Species name.
        Returns:
            JSON string with general information of the protein or gene.
        """
        result = self.search_uniprotkb_entries(query=query)
        if isinstance(result, str):
            result = json.loads(result)
        result = result.get('results', [])
        target_data = None
        for item in result:
            if item.get('organism', {}).get('scientificName') == species:
                target_data = item
                break
        if not target_data:
            return f"No data found for the species: {species}"
        
        pdb_id = None
        for cross_ref in target_data['uniProtKBCrossReferences']:
            if cross_ref['database'] == 'PDB':
                pdb_id = cross_ref['id']
                break
        
        remain_keys = ['comments', 'genes']
        ret_data = {k: v for k, v in target_data.items() if k in remain_keys}
        ret_data['pdb_id'] = pdb_id
    
        return ret_data
    
    def get_uniref_cluster_by_id(self, uniref_id):
        """Search UniRef entry by id to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "id": uniref_id,
        # "fields": [
        #     "id",
        #     "name",
        #     "types",
        #     "organism",
        #     "identity"
        # ]
        }
        endpoint = "uniref/%7Bid%7D"
        return self._get(endpoint, params=params)
    
    def get_uniref_cluster_members_by_id(self, uniref_id):
        """Search UniRef entry by member id to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "id": uniref_id,
        "facetFilter": "member_id_type:uniprotkb_id",
        "size": "10"
        }
        endpoint = "uniref/%7Bid%7D/members"
        return self._get(endpoint, params=params)
    
    def get_uniref_light_cluster_by_id(self, uniref_id):
        """Search light UniRef entry by id to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        # "fields": [
        #     "id",
        #     "name",
        #     "types",
        #     "organism",
        #     "identity"
        # ]
        }
        endpoint = f"uniref/{uniref_id}/light"
        return self._get(endpoint, params=params)
    
    def stream_uniref_clusters(self, query):
        """The uniref stream endpoint uses a request query to return all entries associated with the search term in a single download. 
        Specify fields to return only data for specific sections of that entry that are of interest to you The stream endpoint has a maximum limit of 10 million entries"""
        params = {
        "query": query,
        # "fields": [
        #     "id",
        #     "name",
        #     "types",
        #     "organism",
        #     "identity"
        # ]
        }
        endpoint = "uniref/search"
        return self._get(endpoint, params=params)

    def search_uniref_clusters(self, query):
        """The uniref search endpoint uses a request query to return all entries associated with the search term in a paginated list of entries. 
        Use ‘size’ to specify the number of entries per page of results. Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "query": query,
        # "fields": [
        #     "id",
        #     "name",
        #     "types",
        #     "organism",
        #     "identity"
        # ],
        "size": "10"
        }
        endpoint = "uniref/search"
        return self._get(endpoint, params=params)
    
    def get_uniparc_entry_by_upi(self, uniparc_id):
        """Search UniParc entry by id(upi) to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        
        params = {
        "upi": uniparc_id,
        # "fields": [
        #     "upi",
        #     "organism",
        #     "length"
        # ],
        "dbTypes": "EnsemblBacteria,FlyBase",
        "taxonIds": "9606,10116,9913"
        }
        endpoint = "uniparc/%7Bupi%7D"
        return self._get(endpoint, params=params)
    
    def get_uniparc_light_entry_by_upi(self, uniparc_id):
        """Search UniParc entry by id(upi) to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        # "fields": [
        #     "upi",
        #     "organism",
        #     "length"
        # ],
        }
        endpoint = f"uniparc/{uniparc_id}/light"
        return self._get(endpoint, params=params)
    
    #to do: error handling
    def get_uniparc_cross_references_by_upi(self, uniparc_id):
        """Get a page of database cross-reference entries by a upi"""
        params = {
        # "fields": [
        #     "organism"
        # ],
        "id": "Q0GNZ6",
        "dbTypes": "EnsemblBacteria,FlyBase",
        "taxonIds": "9606,10116,9913",
        "size": "10"
        }

        endpoint = f"uniparc/{uniparc_id}/databases"
        return self._get(endpoint, params=params)
    
    #to do: error handling
    def stream_uniparc_cross_references_by_upi(self, uniparc_id):
        """Get a page of database cross-reference entries by a upi"""
        params = {
        # "fields": [
        #     "organism"
        # ],
        "id": "Q0GNZ6",
        "dbTypes": "EnsemblBacteria,FlyBase",
        "taxonIds": "9606,10116,9913"
        }
        endpoint = f"uniparc/{uniparc_id}/databases/search"
        return self._get(endpoint, params=params)

    def stream_uniparc_entries(self, uniparc_id):
        """The stream endpoint uses a request query to return all entries associated with the search term in a single download. 
        Specify fields to return only data for specific sections of that entry that are of interest to you The stream endpoint has a maximum limit of 10 million entries"""
        params = {
        "query": uniparc_id,
        # "sort": "upi asc",
        # "fields": [
        #     "upi",
        #     "organism",
        #     "length"
        # ]
        }
        endpoint = "uniparc/stream"
        return self._get(endpoint, params=params)
    
    def search_uniparc_entries(self, entry):
        """The search endpoint uses a request query to return all entries associated with the search term in a paginated list of entries. 
        Use ‘size’ to specify the number of entries per page of results. Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "query": entry,
        # "sort": "upi asc",
        # "fields": [
        #     "upi",
        #     "organism",
        #     "length"
        # ],
        
        "size": "10"
        }
        endpoint = "uniparc/search"
        return self._get(endpoint, params=params)
    
    # to do
    def get_gene_centric_by_accession(self, accession):
        """Retrieve a GeneCentric entry by UniProtKB accession.Search GeneCentric entry by protein accession to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        # "fields": [
        #     "accession",
        #     "gene_name",
        #     "proteome_id"
        # ]
        }
        endpoint = f"genecentric/{accession}"
        return self._get(endpoint, params=params)

    def get_gene_centric_by_proteome(self, upid):
        """Search GeneCentric entry by Proteome ID to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "upid": upid,
        # "fields": [
        #     "accession",
        #     "gene_name",
        #     "proteome_id"
        # ],
        "size": "10"
        }
        endpoint = "genecentric/upid/%7Bupid%7D"
        return self._get(endpoint, params=params)

    def stream_gene_centric(self, accession):
        """Stream GeneCentric entries matching a query (max 10M entries).The stream endpoint uses a request query to return all entries associated with the search term in a single download. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "query": accession
        }
        endpoint = "genecentric/stream"
        return self._get(endpoint, params=params)

    def search_gene_centric(self, accession):
        """Search GeneCentric entries with pagination.The search endpoint uses a request query to return all entries associated with the search term in a paginated list of entries. Use ‘size’ to specify the number of entries per page of results. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "query": accession,
        "size": "10"
        }
        endpoint = "genecentric/search"
        return self._get(endpoint, params=params)

    def get_proteome_by_id(self, upid):
        """Retrieve a proteome by UniProt Proteome ID.Search Proteome entry by Proteome ID(upid) to return all data associated with that entry. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        # "fields": [
        #     "upid",
        #     "organism",
        #     "organism_id"
        # ]
        }
        endpoint = f"proteomes/{upid}"
        return self._get(endpoint, params=params)

    def stream_proteomes(self, query):
        """Stream Proteome entries matching a query (max 10M entries).The stream endpoint uses a request query to return all entries associated with the search term in a single download. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        params = {
        "query": query,
        # "sort": "organism_name asc",
        # "fields": [
        #     "upid",
        #     "organism",
        #     "organism_id"
        # ],
        }
        endpoint = "proteomes/search"
        return self._get(endpoint, params=params)

    def search_proteomes(self, query):
        """Search Proteome entries with pagination. The search endpoint uses a request query to return all entries associated with the search term in a paginated list of entries. Use ‘size’ to specify the number of entries per page of results. 
        Specify fields to return only data for specific sections of that entry that are of interest to you"""
        
        params = {
        "query": query,
        # "sort": "organism_name asc",
        # "fields": [
        #     "upid",
        #     "organism",
        #     "organism_id"
        # ],
        "size": "10"
        }
        endpoint = "proteomes/search"
        return self._get(endpoint, params=params)



if __name__ == "__main__":

    # Initialize and run the server
    api = UNIPROTAPI()
    #result = api.get_uniprotkb_entry_by_accession(accession='P05067')
    #result = api.search_uniref_clusters(query='Transcription factors')
    #result = api.get_uniref_light_cluster_by_id(uniref_id='UniRef100_P05067')
    #result = api.get_uniparc_entry_by_upi(uniparc_id='UPI000002DB1C')
    #result = api.get_uniparc_light_entry_by_upi(uniparc_id='UPI000002DB1C')
    #result = api.get_uniparc_cross_references_by_upi(uniparc_id='UPI000002DB1C')
    #result = api.stream_uniparc_cross_references_by_upi(uniparc_id='UPI000002DB1C')
    #result = api.stream_uniparc_entries(uniparc_id='UPI000002DB1C')
    #result = api.search_uniparc_entries(entry='Homo Sapiens')
    result = api.get_gene_centric_by_proteome(accession='P05067')

    print(result)
