import requests
import json
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin
import urllib

class EnsemblClient:
    """
    A Python client for the Ensembl REST API.
    """
    
    BASE_URL = "https://rest.ensembl.org/"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def trim_dict_length(self, data, max_length):
        """
        This function trims the dictionary data to ensure its total length does not exceed max_length.
        It tries to preserve key-value pairs, trimming the data accordingly.
        """
        # Convert the dictionary to a JSON string to check its length
        result_str = json.dumps(data)
        
        if len(result_str) > max_length:
            # If the result is too long, start trimming key-value pairs
            trimmed_data = {}
            current_length = 0
            
            for key, value in data.items():
                # Temporarily add the key-value pair to the result
                temp_data = {key: value}
                temp_str = json.dumps(temp_data)
                
                # If adding this key-value pair keeps us within the limit, add it to the trimmed dictionary
                if current_length + len(temp_str) <= max_length:
                    trimmed_data[key] = value
                    current_length += len(temp_str)
                else:
                    break  # Stop once the max length is reached
            
            return trimmed_data  # Return the trimmed dictionary
        else:
            return data  # No need to trim, return the original dictionary
        
    def limit_list_length(self, data, max_length):
        """
        Limit the length of the list by the total character length after converting elements to strings.
        """
        result = []
        total_length = 0
        
        for item in data:
            item_str = str(item)  # Convert the element to a string
            item_length = len(item_str)
            
            if total_length + item_length > max_length:
                break  # If adding the current element exceeds the max length, stop adding
            
            result.append(item)  # Otherwise, add the item to the result list
            total_length += item_length  # Update the total length with the current item's length
        
        return result
    
    def limit_json_length(self, data, max_length):
        """
        limit length
        """
        if isinstance(data, dict):
            
            return self.limit_dict_length(data, max_length)
        
        elif isinstance(data, list):
        
            return self.limit_list_length(data, max_length)
        
        return data


    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None, max_length: int = 8192) -> Dict:
        """Make a request to the Ensembl REST API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            max_length: Maximum length of the response (in approximate token count)
            
        Returns:
            Dictionary containing the response or error information
        """
        url = urljoin(self.BASE_URL, endpoint)
        try:
            response = self.session.request(method, url, params=params, 
                                         json=data if data else None)
            response.raise_for_status()
            result = response.json()
            
            # Limit response size based on approximate token count
            result = self.limit_json_length(result, max_length*4)            
            return result
        
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP Error: {str(e)}", "status_code": e.response.status_code}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection Error: Failed to connect to Ensembl API"}
        except requests.exceptions.Timeout:
            return {"error": "Timeout Error: Request to Ensembl API timed out"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request Error: {str(e)}"}
        except ValueError as e:
            return {"error": f"JSON Parsing Error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected Error: {str(e)}"}

    # Archive endpoints
    def get_archive_id(self, id: str) -> Dict:
        """Get latest version of an identifier."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"archive/id/{id}")

    def post_archive_id(self, ids: List[str]) -> Dict:
        """Get latest version for multiple identifiers."""
        return self._make_request("POST", "archive/id", data={"ids": ids})

    # Comparative Genomics endpoints
    def get_cafe_genetree_id(self, id: str) -> Dict:
        """Get cafe tree by gene tree stable identifier."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"cafe/genetree/id/{id}")

    def get_cafe_genetree_member_symbol(self, species: str, symbol: str) -> Dict:
        """Get cafe tree by gene symbol."""
        species = urllib.parse.quote(str(species))
        symbol = urllib.parse.quote(str(symbol))
        return self._make_request("GET", f"cafe/genetree/member/symbol/{species}/{symbol}")

    def get_cafe_genetree_member_id(self, species: str, id: str) -> Dict:
        """Get cafe tree by member ID."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"cafe/genetree/member/id/{species}/{id}")

    def get_genetree_id(self, id: str, max_length: int = 8192) -> Dict:
        """Get gene tree by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"genetree/id/{id}", max_length=max_length)

    def get_genetree_member_symbol(self, species: str, symbol: str) -> Dict:
        """Get gene tree by symbol."""
        species = urllib.parse.quote(str(species))
        symbol = urllib.parse.quote(str(symbol))
        return self._make_request("GET", f"genetree/member/symbol/{species}/{symbol}")

    def get_genetree_member_id(self, species: str, id: str) -> Dict:
        """Get gene tree by member ID."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"genetree/member/id/{species}/{id}")

    def get_alignment_region(self, species: str, region: str) -> Dict:
        """Get genomic alignments by region."""
        species = urllib.parse.quote(str(species))
        region = urllib.parse.quote(str(region))
        return self._make_request("GET", f"alignment/region/{species}/{region}")

    def get_homology_id(self, species: str, id: str) -> Dict:
        """Get homology information by ID."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"homology/id/{species}/{id}")

    def get_homology_symbol(self, species: str, symbol: str, max_length: int = 8192) -> Dict:
        """Get homology information by symbol."""
        species = urllib.parse.quote(str(species))
        symbol = urllib.parse.quote(str(symbol))
        return self._make_request("GET", f"homology/symbol/{species}/{symbol}", max_length=max_length)

    # Cross References endpoints
    def get_xrefs_symbol(self, species: str, symbol: str, max_length: int = 8192) -> Dict:
        """Get cross references by symbol."""
        species = urllib.parse.quote(str(species))
        symbol = urllib.parse.quote(str(symbol))
        return self._make_request("GET", f"xrefs/symbol/{species}/{symbol}", max_length=max_length)

    def get_xrefs_id(self, id: str) -> Dict:
        """Get cross references by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"xrefs/id/{id}")

    def get_xrefs_name(self, species: str, name: str) -> Dict:
        """Get cross references by name."""
        species = urllib.parse.quote(str(species))
        name = urllib.parse.quote(str(name))
        return self._make_request("GET", f"xrefs/name/{species}/{name}")

    # Information endpoints
    def get_info_analysis(self, species: str) -> Dict:
        """Get analysis information for a species."""
        species = urllib.parse.quote(str(species))
        return self._make_request("GET", f"info/analysis/{species}")

    def get_info_assembly(self, species: str, max_length: int = 8192) -> Dict:
        """Get assembly information for a species."""
        species = urllib.parse.quote(str(species))
        return self._make_request("GET", f"info/assembly/{species}", max_length=max_length)

    def get_assembly_info(self, species: str) -> Dict:
        """Get assembly information for a species. (Alias for get_info_assembly)"""
        return self.get_info_assembly(species)

    def get_assembly_region_info(self, species: str, region_name: str) -> Dict:
        """Get assembly information for a specific region."""
        species = urllib.parse.quote(str(species))
        region_name = urllib.parse.quote(str(region_name))
        return self._make_request("GET", f"info/assembly/{species}/{region_name}")

    def get_info_biotypes(self, species: str) -> Dict:
        """Get biotypes for a species."""
        species = urllib.parse.quote(str(species))
        return self._make_request("GET", f"info/biotypes/{species}")

    def get_biotypes(self, species: str) -> Dict:
        """Get biotypes for a species. (Alias for get_info_biotypes)"""
        return self.get_info_biotypes(species)

    def get_info_biotypes_groups(self, group: str, object_type: str) -> Dict:
        """Get biotype groups information."""
        group = urllib.parse.quote(str(group))
        object_type = urllib.parse.quote(str(object_type))
        return self._make_request("GET", f"info/biotypes/groups/{group}/{object_type}")

    def get_biotype_groups(self, group: str, object_type: str) -> Dict:
        """Get biotype groups information. (Alias for get_info_biotypes_groups)"""
        return self.get_info_biotypes_groups(group, object_type)

    def get_info_biotypes_name(self, name: str, object_type: str) -> Dict:
        """Get biotype information by name."""
        name = urllib.parse.quote(str(name))
        object_type = urllib.parse.quote(str(object_type))
        return self._make_request("GET", f"info/biotypes/name/{name}/{object_type}")

    def get_biotype_name(self, name: str, object_type: str) -> Dict:
        """Get biotype information by name. (Alias for get_info_biotypes_name)"""
        return self.get_info_biotypes_name(name, object_type)

    # Information endpoints (continued)
    def get_info_compara_methods(self) -> Dict:
        """Get comparative analysis methods."""
        return self._make_request("GET", "info/compara/methods")

    def get_compara_methods(self) -> Dict:
        """Get comparative analysis methods. (Alias for get_info_compara_methods)"""
        return self.get_info_compara_methods()

    def get_info_compara_species_sets(self, method: str) -> Dict:
        """Get species sets for a comparative analysis method."""
        method = urllib.parse.quote(str(method))
        return self._make_request("GET", f"info/compara/species_sets/{method}")

    def get_compara_species_sets(self, method: str) -> Dict:
        """Get species sets for a comparative analysis method. (Alias for get_info_compara_species_sets)"""
        return self.get_info_compara_species_sets(method)

    def get_info_comparas(self) -> Dict:
        """Get comparative genomics databases."""
        return self._make_request("GET", "info/comparas")

    def get_comparas(self) -> Dict:
        """Get comparative genomics databases. (Alias for get_info_comparas)"""
        return self.get_info_comparas()

    def get_info_data(self) -> Dict:
        """Get data release information."""
        return self._make_request("GET", "info/data")

    def get_data_info(self) -> Dict:
        """Get data release information. (Alias for get_info_data)"""
        return self.get_info_data()

    def get_info_eg_version(self) -> Dict:
        """Get Ensembl Genomes version."""
        return self._make_request("GET", "info/eg_version")

    def get_eg_version(self) -> Dict:
        """Get Ensembl Genomes version. (Alias for get_info_eg_version)"""
        return self.get_info_eg_version()

    def get_info_external_dbs(self, species: str) -> Dict:
        """Get external databases for a species."""
        species = urllib.parse.quote(str(species))
        return self._make_request("GET", f"info/external_dbs/{species}")

    def get_external_dbs(self, species: str) -> Dict:
        """Get external databases for a species. (Alias for get_info_external_dbs)"""
        return self.get_info_external_dbs(species)

    def get_info_divisions(self) -> Dict:
        """Get Ensembl divisions."""
        return self._make_request("GET", "info/divisions")

    def get_divisions(self) -> Dict:
        """Get Ensembl divisions. (Alias for get_info_divisions)"""
        return self.get_info_divisions()

    def get_info_genomes(self, genome_name: str) -> Dict:
        """Find information about a given genome."""
        genome_name = urllib.parse.quote(str(genome_name))
        return self._make_request("GET", f"info/genomes/{genome_name}")

    def get_info_genomes_accession(self, accession: str) -> Dict:
        """Find information about genomes containing a specified INSDC accession."""
        accession = urllib.parse.quote(str(accession))
        return self._make_request("GET", f"info/genomes/accession/{accession}")

    def get_info_genomes_assembly(self, assembly_id: str) -> Dict:
        """Find information about a genome with a specified assembly."""
        assembly_id = urllib.parse.quote(str(assembly_id))
        return self._make_request("GET", f"info/genomes/assembly/{assembly_id}")

    def get_info_genomes_division(self, division_name: str) -> Dict:
        """Find information about all genomes in a given division."""
        division_name = urllib.parse.quote(str(division_name))
        return self._make_request("GET", f"info/genomes/division/{division_name}")

    def get_info_genomes_taxonomy(self, taxon_name: str) -> Dict:
        """Find information about all genomes beneath a given node of the taxonomy."""
        taxon_name = urllib.parse.quote(str(taxon_name))
        return self._make_request("GET", f"info/genomes/taxonomy/{taxon_name}")

    def get_info_ping(self) -> Dict:
        """Checks if the service is alive."""
        return self._make_request("GET", "info/ping")

    def get_info_rest(self) -> Dict:
        """Shows the current version of the Ensembl REST API."""
        return self._make_request("GET", "info/rest")

    def get_info_software(self) -> Dict:
        """Shows the current version of the Ensembl API used by the REST server."""
        return self._make_request("GET", "info/software")

    def get_info_species(self) -> Dict:
        """Lists all available species, their aliases, available adaptor groups and data release."""
        return self._make_request("GET", "info/species")

    def get_info_variation(self, species: str) -> Dict:
        """List the variation sources used in Ensembl for a species."""
        species = urllib.parse.quote(str(species))
        return self._make_request("GET", f"info/variation/{species}")

    def get_info_variation_consequence_types(self) -> Dict:
        """Lists all variant consequence types."""
        return self._make_request("GET", "info/variation/consequence_types")

    def get_info_variation_populations(self, species: str, population_name: Optional[str] = None) -> Dict:
        """List all populations for a species or list all individuals for a population from a species."""
        species = urllib.parse.quote(str(species))
        if population_name:
            population_name = urllib.parse.quote(str(population_name))
            return self._make_request("GET", f"info/variation/populations/{species}/{population_name}")
        return self._make_request("GET", f"info/variation/populations/{species}")

    # Linkage Disequilibrium endpoints
    def get_ld(self, species: str, id: str, population_name: str) -> Dict:
        """Computes and returns LD values between the given variant and all other variants in a window."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        population_name = urllib.parse.quote(str(population_name))
        return self._make_request("GET", f"ld/{species}/{id}/{population_name}")

    def get_ld_pairwise(self, species: str, id1: str, id2: str) -> Dict:
        """Computes and returns LD values between the given variants."""
        species = urllib.parse.quote(str(species))
        id1 = urllib.parse.quote(str(id1))
        id2 = urllib.parse.quote(str(id2))
        return self._make_request("GET", f"ld/{species}/pairwise/{id1}/{id2}")

    def get_ld_region(self, species: str, region: str, population_name: str) -> Dict:
        """Computes and returns LD values between all pairs of variants in the defined region."""
        species = urllib.parse.quote(str(species))
        region = urllib.parse.quote(str(region))
        population_name = urllib.parse.quote(str(population_name))
        return self._make_request("GET", f"ld/{species}/region/{region}/{population_name}")

    # Lookup endpoints
    def get_lookup_id(self, id: str) -> Dict:
        """Look up an identifier."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"lookup/id/{id}")

    def post_lookup_id(self, ids: List[str]) -> Dict:
        """Look up multiple identifiers."""
        return self._make_request("POST", "lookup/id", data={"ids": ids})

    def get_lookup_symbol(self, species: str, symbol: str, max_length: int = 8192) -> Dict:
        """Look up a symbol."""
        species = urllib.parse.quote(str(species))
        symbol = urllib.parse.quote(str(symbol))
        return self._make_request("GET", f"lookup/symbol/{species}/{symbol}", max_length=max_length)

    def post_lookup_symbol(self, species: str, symbols: List[str]) -> Dict:
        """Look up multiple symbols."""
        species = urllib.parse.quote(str(species))
        return self._make_request("POST", f"lookup/symbol/{species}", data={"symbols": symbols})

    # Mapping endpoints
    def get_map_cdna(self, id: str, region: str) -> Dict:
        """Map cDNA coordinates to genomic coordinates."""
        id = urllib.parse.quote(str(id))
        region = urllib.parse.quote(str(region))
        return self._make_request("GET", f"map/cdna/{id}/{region}")

    def get_map_cds(self, id: str, region: str) -> Dict:
        """Map CDS coordinates to genomic coordinates."""
        id = urllib.parse.quote(str(id))
        region = urllib.parse.quote(str(region))
        return self._make_request("GET", f"map/cds/{id}/{region}")

    def get_map(self, species: str, asm_one: str, region: str, asm_two: str) -> Dict:
        """Map coordinates between assemblies."""
        species = urllib.parse.quote(str(species))
        asm_one = urllib.parse.quote(str(asm_one))
        region = urllib.parse.quote(str(region))
        asm_two = urllib.parse.quote(str(asm_two))
        return self._make_request("GET", f"map/{species}/{asm_one}/{region}/{asm_two}")

    def get_map_translation(self, id: str, region: str) -> Dict:
        """Map protein coordinates to genomic coordinates."""
        id = urllib.parse.quote(str(id))
        region = urllib.parse.quote(str(region))
        return self._make_request("GET", f"map/translation/{id}/{region}")

    # Ontologies and Taxonomy endpoints
    def get_ontology_ancestors(self, id: str) -> Dict:
        """Get ontology ancestors."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ontology/ancestors/{id}")

    def get_ontology_ancestors_chart(self, id: str) -> Dict:
        """Get ontology ancestors chart."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ontology/ancestors/chart/{id}")

    def get_ontology_descendants(self, id: str) -> Dict:
        """Get ontology descendants."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ontology/descendants/{id}")

    def get_ontology_id(self, id: str) -> Dict:
        """Get ontology by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ontology/id/{id}")

    def get_ontology_name(self, name: str) -> Dict:
        """Get ontology by name."""
        name = urllib.parse.quote(str(name))
        return self._make_request("GET", f"ontology/name/{name}")

    def get_taxonomy_classification(self, id: str) -> Dict:
        """Return the taxonomic classification of a taxon node."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"taxonomy/classification/{id}")

    def get_taxonomy_id(self, id: str) -> Dict:
        """Search for a taxonomic term by its identifier."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"taxonomy/id/{id}")

    def get_taxonomy_name(self, name: str) -> Dict:
        """Search for a taxonomic id by a non-scientific name."""
        name = urllib.parse.quote(str(name))
        return self._make_request("GET", f"taxonomy/name/{name}")

    # Overlap endpoints
    def get_overlap_id(self, id: str) -> Dict:
        """Get features overlapping a region defined by an identifier."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"overlap/id/{id}")

    def get_overlap_region(self, features: str, species: str, region: str) -> Dict:
        """Get features overlapping a genomic region."""
        features = urllib.parse.quote(str(features))
        species = urllib.parse.quote(str(species))
        region = urllib.parse.quote(str(region))
        return self._make_request("GET", f"overlap/region/{species}/{region}?{features}")

    def get_overlap_translation(self, id: str) -> Dict:
        """Get features overlapping a translation."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"overlap/translation/{id}")

    # Phenotype endpoints
    def get_phenotype_accession(self, species: str, accession: str, max_length: int = 8192) -> Dict:
        """Get phenotype annotations by accession."""
        species = urllib.parse.quote(str(species))
        accession = urllib.parse.quote(str(accession))
        return self._make_request("GET", f"phenotype/accession/{species}/{accession}", max_length=max_length)

    def get_phenotype_gene(self, species: str, gene: str, max_length: int = 8192) -> Dict:
        """Get phenotype annotations by gene."""
        params = {
            'include_associated': '1',
            'include_overlap': '1',
            'include_pubmed_id': '1'
        }
        return self._make_request("GET", f"phenotype/gene/{species}/{gene}", params=params, max_length=max_length)

    def get_phenotype_region(self, species: str, region: str, max_length: int = 8192) -> Dict:
        """Get phenotype annotations by region."""
        species = urllib.parse.quote(str(species))
        region = urllib.parse.quote(str(region))
        return self._make_request("GET", f"phenotype/region/{species}/{region}", max_length=max_length)

    def get_phenotype_term(self, species: str, term: str, max_length: int = 8192) -> Dict:
        """Get phenotype annotations by term."""
        species = urllib.parse.quote(str(species))
        term = urllib.parse.quote(str(term))
        return self._make_request("GET", f"phenotype/term/{species}/{term}", max_length=max_length)

    # Regulation endpoints 
    def get_species_binding_matrix(self, species: str, binding_matrix_stable_id: str) -> Dict:
        """Get binding matrix."""
        species = urllib.parse.quote(str(species))
        binding_matrix_stable_id = urllib.parse.quote(str(binding_matrix_stable_id))
        return self._make_request("GET", f"species/{species}/binding_matrix/{binding_matrix_stable_id}")

    # Sequence endpoints
    def get_sequence_id(self, id: str) -> Dict:
        """Get sequence by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"sequence/id/{id}")

    def post_sequence_id(self, ids: List[str]) -> Dict:
        """Get sequences by multiple IDs."""
        return self._make_request("POST", "sequence/id", data={"ids": ids})

    def get_sequence_region(self, species: str, region: str, max_length: int = 8192) -> Dict:
        """Get sequence by region."""
        species = urllib.parse.quote(str(species))
        region = urllib.parse.quote(str(region))
        return self._make_request("GET", f"sequence/region/{species}/{region}", max_length=max_length)

    def post_sequence_region(self, species: str, regions: List[Dict]) -> Dict:
        """Get sequences by multiple regions."""
        species = urllib.parse.quote(str(species))
        return self._make_request("POST", f"sequence/region/{species}", data={"regions": regions})

    # Transcript Haplotypes endpoints
    def get_transcript_haplotypes(self, species: str, id: str) -> Dict:
        """Computes observed transcript haplotype sequences based on phased genotype data."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"transcript_haplotypes/{species}/{id}")

    # VEP endpoints
    def get_vep_hgvs(self, species: str, hgvs_notation: str, max_length: int = 8192) -> Dict:
        """Get variant effect predictions by HGVS notation."""
        species = urllib.parse.quote(str(species))
        hgvs_notation = urllib.parse.quote(str(hgvs_notation))
        return self._make_request("GET", f"vep/{species}/hgvs/{hgvs_notation}", max_length=max_length)

    def post_vep_hgvs(self, species: str, hgvs_notations: List[str]) -> Dict:
        """Get variant effect predictions by multiple HGVS notations."""
        species = urllib.parse.quote(str(species))
        return self._make_request("POST", f"vep/{species}/hgvs", data={"hgvs_notations": hgvs_notations})

    def get_vep_id(self, species: str, id: str) -> Dict:
        """Get variant effect predictions by ID."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"vep/{species}/id/{id}")

    def post_vep_id(self, species: str, ids: List[str]) -> Dict:
        """Get variant effect predictions by multiple IDs."""
        species = urllib.parse.quote(str(species))
        return self._make_request("POST", f"vep/{species}/id", data={"ids": ids})

    def get_vep_region(self, species: str, region: str, allele: str) -> Dict:
        """Get variant effect predictions by region."""
        species = urllib.parse.quote(str(species))
        region = urllib.parse.quote(str(region))
        allele = urllib.parse.quote(str(allele))
        return self._make_request("GET", f"vep/{species}/region/{region}/{allele}")

    def post_vep_region(self, species: str, variants: List[Dict]) -> Dict:
        """Get variant effect predictions by multiple regions."""
        species = urllib.parse.quote(str(species))
        return self._make_request("POST", f"vep/{species}/region", data={"variants": variants})

    # Variation endpoints
    def get_variant_recoder(self, species: str, id: str) -> Dict:
        """Translate variant identifiers."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"variant_recoder/{species}/{id}")

    def post_variant_recoder(self, species: str, ids: List[str]) -> Dict:
        """Translate multiple variant identifiers."""
        species = urllib.parse.quote(str(species))
        return self._make_request("POST", f"variant_recoder/{species}", data={"ids": ids})

    def get_variation(self, species: str, id: str) -> Dict:
        """Get variation by ID."""
        species = urllib.parse.quote(str(species))
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"variation/{species}/{id}")

    def get_variation_pmcid(self, species: str, pmcid: str) -> Dict:
        """Get variations by PubMed Central ID."""
        species = urllib.parse.quote(str(species))
        pmcid = urllib.parse.quote(str(pmcid))
        return self._make_request("GET", f"variation/{species}/pmcid/{pmcid}")

    def get_variation_pmid(self, species: str, pmid: str) -> Dict:
        """Get variations by PubMed ID."""
        species = urllib.parse.quote(str(species))
        pmid = urllib.parse.quote(str(pmid))
        return self._make_request("GET", f"variation/{species}/pmid/{pmid}")

    def post_variation(self, species: str, ids: List[str]) -> Dict:
        """Get variations by multiple IDs."""
        species = urllib.parse.quote(str(species))
        return self._make_request("POST", f"variation/{species}", data={"ids": ids})

    # GA4GH endpoints
    def get_ga4gh_beacon(self) -> Dict:
        """Get Beacon information."""
        return self._make_request("GET", "ga4gh/beacon")

    def get_ga4gh_beacon_query(self, params: Dict) -> Dict:
        """Query Beacon."""
        return self._make_request("GET", "ga4gh/beacon/query", params=params)

    def post_ga4gh_beacon_query(self, data: Dict) -> Dict:
        """Query Beacon with POST."""
        return self._make_request("POST", "ga4gh/beacon/query", data=data)

    def get_ga4gh_features(self, id: str) -> Dict:
        """Get GA4GH features by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ga4gh/features/{id}")

    def post_ga4gh_features_search(self, data: Dict) -> Dict:
        """Search GA4GH features."""
        return self._make_request("POST", "ga4gh/features/search", data=data)

    def post_ga4gh_callsets_search(self, data: Dict) -> Dict:
        """Search GA4GH callsets."""
        return self._make_request("POST", "ga4gh/callsets/search", data=data)

    def get_ga4gh_callsets(self, id: str) -> Dict:
        """Get GA4GH callset by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ga4gh/callsets/{id}")

    def post_ga4gh_datasets_search(self, data: Dict) -> Dict:
        """Search GA4GH datasets."""
        return self._make_request("POST", "ga4gh/datasets/search", data=data)

    def get_ga4gh_datasets(self, id: str) -> Dict:
        """Get GA4GH dataset by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ga4gh/datasets/{id}")

    def post_ga4gh_featuresets_search(self, data: Dict) -> Dict:
        """Search GA4GH feature sets."""
        return self._make_request("POST", "ga4gh/featuresets/search", data=data)

    def get_ga4gh_featuresets(self, id: str) -> Dict:
        """Get GA4GH feature set by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ga4gh/featuresets/{id}")

    def get_ga4gh_variants(self, id: str) -> Dict:
        """Get GA4GH variant by ID."""
        id = urllib.parse.quote(str(id))
        return self._make_request("GET", f"ga4gh/variants/{id}")

    def post_ga4gh_variantannotations_search(self, data: Dict) -> Dict:
        """Search GA4GH variant annotations."""
        return self._make_request("POST", "ga4gh/variantannotations/search", data=data)

    def post_ga4gh_variants_search(self, data: Dict) -> Dict:
        """Search GA4GH variants."""
        return self._make_request("POST", "ga4gh/variants/search", data=data)

    def post_ga4gh_variantsets_search(self, data: Dict) -> Dict:
        """Search GA4GH variant sets."""
        return self._make_request("POST", "ga4gh/variantsets/search", data=data)

    def get_ga4gh_variantsets(self, id: str) -> Dict:
        """Get GA4GH variant set by ID."""
        return self._make_request("GET", f"ga4gh/variantsets/{id}")

    def post_ga4gh_references_search(self, data: Dict) -> Dict:
        """Search GA4GH references."""
        return self._make_request("POST", "ga4gh/references/search", data=data)

    def get_ga4gh_references(self, id: str) -> Dict:
        """Get GA4GH reference by ID."""
        return self._make_request("GET", f"ga4gh/references/{id}")

    def post_ga4gh_referencesets_search(self, data: Dict) -> Dict:
        """Search GA4GH reference sets."""
        return self._make_request("POST", "ga4gh/referencesets/search", data=data)

    def get_ga4gh_referencesets(self, id: str) -> Dict:
        """Get GA4GH reference set by ID."""
        return self._make_request("GET", f"ga4gh/referencesets/{id}")

    def post_ga4gh_variantannotationsets_search(self, data: Dict) -> Dict:
        """Search GA4GH variant annotation sets."""
        return self._make_request("POST", "ga4gh/variantannotationsets/search", data=data)

    def get_ga4gh_variantannotationsets(self, id: str) -> Dict:
        """Get GA4GH variant annotation set by ID."""
        return self._make_request("GET", f"ga4gh/variantannotationsets/{id}") 