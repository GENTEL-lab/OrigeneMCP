import requests
import json

class PDBAPI:
    BASE_URL = "https://data.rcsb.org/rest/v1/"
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"accept": "application/json"}
    
    def _get(self, endpoint, params=None):
        """Internal helper for GET requests."""
        url = self.BASE_URL + endpoint
        try:
            r = requests.get(url, params=params, headers=self.headers)
            r.raise_for_status()
            return r.json()
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

    # Entry-related methods
    def get_structure(self, entry_id: str) -> dict:
        """
        Retrieve detailed structure information for a given PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            
        Returns:
            dict: A dictionary containing structure information with keys:
                - 'rcsb_id': PDB ID
                - 'rcsb_accession_info': accession details
                - 'struct': structure metadata
                - 'exptl': experimental details
                - 'citation': publication info
                - 'cell': unit cell parameters
                - 'symmetry': symmetry info
                - 'pdbx_database_status': entry status
                
            Returns None if entry not found or error occurs.
            
        Example:
            >>> api.get_structure("1CRN")
            {
                'rcsb_id': '1CRN',
                'struct': {'title': 'CRAMBIN'},
                ...
            }
        """
        endpoint = f"core/entry/{entry_id}"
        return self._get(endpoint)

    def get_pubmed_annotations(self, entry_id: str) -> dict:
        """
        Retrieve PubMed literature annotations for a given PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            
        Returns:
            dict: A dictionary containing PubMed annotations with keys:
                - 'rcsb_id': PDB ID
                - 'pubmed': list of PubMed articles with:
                    - 'id': PubMed ID
                    - 'title': article title
                    - 'journal': journal info
                    - 'authors': author list
                    - 'year': publication year
                    
            Returns None if no annotations found or error occurs.
            
        Example:
            >>> api.get_pubmed_annotations("1CRN")
            {
                'rcsb_id': '1CRN',
                'pubmed': [{
                    'id': '123456',
                    'title': 'Structure of crambin...',
                    ...
                }]
            }
        """
        endpoint = f"core/pubmed/{entry_id}"
        return self._get(endpoint)

    # Entity-related methods
    def get_polymer_entity(self, entry_id: str, entity_id: str) -> dict:
        """
        Retrieve detailed information about a polymer entity in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            entity_id (str): The polymer entity identifier (usually "1", "2", etc.)
            
        Returns:
            dict: A dictionary containing polymer entity info with keys:
                - 'entity': 
                    - 'id': entity ID
                    - 'type': entity type (e.g. "polymer")
                    - 'src_method': source method
                    - 'pdbx_description': description
                    - 'pdbx_number_of_molecules': molecule count
                    - 'pdbx_ec': EC numbers
                    - 'pdbx_mutation': mutation info
                    - 'pdbx_fragment': fragment info
                - 'rcsb_polymer_entity': 
                    - 'container_identifiers': container info
                    - 'entity_poly': polymer details
                    
            Returns None if entity not found or error occurs.
            
        Example:
            >>> api.get_polymer_entity("1CRN", "1")
            {
                'entity': {
                    'id': '1',
                    'type': 'polymer',
                    'pdbx_description': 'CRAMBIN',
                    ...
                },
                'rcsb_polymer_entity': {
                    'entity_poly': {
                        'type': 'polypeptide(L)',
                        ...
                    }
                }
            }
        """
        endpoint = f"core/polymer_entity/{entry_id}/{entity_id}"
        return self._get(endpoint)

    def get_branched_entity(self, entry_id: str, entity_id: str) -> dict:
        """
        Retrieve detailed information about a branched entity in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "4CYG")
            entity_id (str): The branched entity identifier (usually "2", etc.)
            
        Returns:
            dict: A dictionary containing branched entity info with keys:
                - 'entity':
                    - 'id': entity ID
                    - 'type': entity type (e.g. "branched")
                    - 'pdbx_description': description
                    - 'pdbx_number_of_molecules': molecule count
                - 'rcsb_branched_entity':
                    - 'container_identifiers': container info
                    - 'branched_entity': branched details
                    - 'branched_entity_instance_count': instance count
                    
            Returns None if entity not found or error occurs.
            
        Example:
            >>> api.get_branched_entity("1XYZ", "1")
            {
                'entity': {
                    'id': '1',
                    'type': 'branched',
                    'pdbx_description': 'BRANCHED SUGAR',
                    ...
                },
                'rcsb_branched_entity': {
                    'branched_entity': {
                        'type': 'oligosaccharide',
                        ...
                    }
                }
            }
        """
        endpoint = f"core/branched_entity/{entry_id}/{entity_id}"
        return self._get(endpoint)

    def get_nonpolymer_entity(self, entry_id: str, entity_id: str) -> dict:
        """
        Retrieve detailed information about a non-polymer entity in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            entity_id (str): The non-polymer entity identifier (usually "1", "2", etc.)
            
        Returns:
            dict: A dictionary containing non-polymer entity info with keys:
                - 'entity':
                    - 'id': entity ID
                    - 'type': entity type (e.g. "non-polymer")
                    - 'pdbx_description': description
                    - 'pdbx_number_of_molecules': molecule count
                - 'rcsb_non_polymer_entity':
                    - 'container_identifiers': container info
                    - 'non_polymer_comp': chemical component details
                    - 'non_polymer_entity_instance_count': instance count
                    
            Returns None if entity not found or error occurs.
            
        Example:
            >>> api.get_non_polymer_entity("1XYZ", "1")
            {
                'entity': {
                    'id': '1',
                    'type': 'non-polymer',
                    'pdbx_description': 'HEME GROUP',
                    ...
                },
                'rcsb_non_polymer_entity': {
                    'non_polymer_comp': {
                        'chem_comp_id': 'HEM',
                        ...
                    }
                }
            }
        """
        endpoint = f"core/nonpolymer_entity/{entry_id}/{entity_id}"
        return self._get(endpoint)

    # Entity instance methods
    def get_polymer_entity_instance(self, entry_id: str, instance_id: str) -> dict:
        """
        Retrieve detailed information about a polymer entity instance in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            instance_id (str): ID of the instance (chain) that needs to be fetched. (usually "A", "B", etc.)
            
        Returns:
            dict: A dictionary containing polymer entity instance info with keys:
                - 'rcsb_polymer_entity_instance':
                    - 'id': instance ID
                    - 'asym_id': asymmetric unit ID
                    - 'auth_asym_id': author asymmetric unit ID
                    - 'entity_id': parent entity ID
                    - 'transformation': transformation matrix
                    - 'struct_asym': structure asymmetric unit info
                    - 'rcsb_polymer_entity_instance_container_identifiers': container info
                    
            Returns None if instance not found or error occurs.
            
        Example:
            >>> api.get_polymer_entity_instance("1CRN", "1")
            {
                'rcsb_polymer_entity_instance': {
                    'id': '1',
                    'asym_id': 'A',
                    'entity_id': '1',
                    'transformation': [[1,0,0],[0,1,0],[0,0,1]],
                    ...
                }
            }
        """
        endpoint = f"core/polymer_entity_instance/{entry_id}/{instance_id}"
        return self._get(endpoint)

    def get_branched_entity_instance(self, entry_id: str, instance_id: str) -> dict:
        """
        Retrieve detailed information about a branched entity instance in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            instance_id (str): ID of the instance (chain) that needs to be fetched. (usually "A", "B", etc.)
            
        Returns:
            dict: A dictionary containing branched entity instance info with keys:
                - 'rcsb_branched_entity_instance':
                    - 'id': instance ID
                    - 'asym_id': asymmetric unit ID
                    - 'auth_asym_id': author asymmetric unit ID
                    - 'entity_id': parent entity ID
                    - 'transformation': transformation matrix
                    - 'struct_asym': structure asymmetric unit info
                    - 'rcsb_branched_entity_instance_container_identifiers': container info
                    
            Returns None if instance not found or error occurs.
            
        Example:
            >>> api.get_branched_entity_instance("1XYZ", "1")
            {
                'rcsb_branched_entity_instance': {
                    'id': '1',
                    'asym_id': 'B',
                    'entity_id': '1',
                    'transformation': [[1,0,0],[0,1,0],[0,0,1]],
                    ...
                }
            }
        """
        endpoint = f"core/branched_entity_instance/{entry_id}/{instance_id}"
        return self._get(endpoint)

    def get_nonpolymer_entity_instance(self, entry_id: str, instance_id: str) -> dict:
        """
        Retrieve detailed information about a non-polymer entity instance in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            instance_id (str): ID of the instance (chain) that needs to be fetched. (usually "A", "B", etc.)
            
        Returns:
            dict: A dictionary containing non-polymer entity instance info with keys:
                - 'rcsb_non_polymer_entity_instance':
                    - 'id': instance ID
                    - 'asym_id': asymmetric unit ID
                    - 'auth_asym_id': author asymmetric unit ID
                    - 'entity_id': parent entity ID
                    - 'transformation': transformation matrix
                    - 'struct_asym': structure asymmetric unit info
                    - 'rcsb_non_polymer_entity_instance_container_identifiers': container info
                    
            Returns None if instance not found or error occurs.
            
        Example:
            >>> api.get_non_polymer_entity_instance("1XYZ", "1")
            {
                'rcsb_non_polymer_entity_instance': {
                    'id': '1',
                    'asym_id': 'C',
                    'entity_id': '1',
                    'transformation': [[1,0,0],[0,1,0],[0,0,1]],
                    ...
                }
            }
        """
        endpoint = f"core/nonpolymer_entity_instance/{entry_id}/{instance_id}"
        return self._get(endpoint)

    # Annotation methods
    def get_uniprot_annotations(self, entry_id: str, entity_id: str) -> dict:
        """
        Retrieve UniProt annotations for a polymer entity in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            entity_id (str): The polymer entity identifier (usually "1", "2", etc.)
            
        Returns:
            dict: A dictionary containing UniProt annotations with keys:
                - 'rcsb_id': PDB ID
                - 'entity_id': entity ID
                - 'uniprot_accession': UniProt accession number
                - 'uniprot_id': UniProt ID
                - 'uniprot_name': protein name
                - 'uniprot_description': protein description
                - 'uniprot_sequence': protein sequence
                - 'uniprot_organism': source organism
                - 'uniprot_gene': gene name
                - 'uniprot_domain': domain annotations
                
            Returns None if no annotations found or error occurs.
            
        Example:
            >>> api.get_uniprot_annotations("1CRN", "1")
            {
                'rcsb_id': '1CRN',
                'entity_id': '1',
                'uniprot_accession': 'P01542',
                'uniprot_id': 'CRAM_HORVU',
                'uniprot_name': 'Crambin',
                ...
            }
        """
        endpoint = f"core/uniprot/{entry_id}/{entity_id}"
        return self._get(endpoint)

    def get_drugbank_annotations(self, component_id: str) -> dict:
        """
        Retrieve DrugBank annotations for a chemical component in PDB.
        
        Args:
            component_id (str): The 3-letter chemical component ID (e.g. "ATP", "HEM")
            
        Returns:
            dict: A dictionary containing DrugBank annotations with keys:
                - 'drugbank_id': DrugBank ID
                - 'name': drug name
                - 'description': drug description
                - 'groups': drug groups (e.g. approved, experimental)
                - 'indication': therapeutic indications
                - 'pharmacology': pharmacological action
                - 'mechanism_of_action': mechanism description
                - 'toxicity': toxicity information
                - 'metabolism': metabolic pathway
                - 'targets': list of drug targets with:
                    - 'uniprot_id': UniProt ID
                    - 'gene_name': gene name
                    - 'action': drug action on target
                    
            Returns None if no annotations found or error occurs.
            
        Example:
            >>> api.get_drugbank_annotations("ATP")
            {
                'drugbank_id': 'DB00171',
                'name': 'Adenosine triphosphate',
                'groups': ['approved'],
                'targets': [{
                    'uniprot_id': 'P0A7E2',
                    'gene_name': 'ATP1A1',
                    'action': 'binder'
                }],
                ...
            }
        """
        endpoint = f"core/drugbank/{component_id}"
        return self._get(endpoint)

    # Assembly methods
    def get_structural_assembly(self, entry_id: str, assembly_id: str = "1") -> dict:
        """
        Retrieve structural assembly information for a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            assembly_id (str): The assembly identifier (default: "1")
            
        Returns:
            dict: A dictionary containing assembly information with keys:
                - 'rcsb_struct_assembly':
                    - 'id': assembly ID
                    - 'details': assembly description
                    - 'method': assembly method
                    - 'oligomeric_details': oligomeric state
                    - 'polymer_entity_instance_count': instance count
                    - 'rcsb_struct_assembly_provenance': provenance info
                    - 'rcsb_struct_assembly_container_identifiers': container info
                - 'assemblies': list of assembly components with:
                    - 'assembly_id': component ID
                    - 'asym_id_list': list of asymmetric unit IDs
                    - 'transformation': transformation matrix
                    
            Returns None if assembly not found or error occurs.
            
        Example:
            >>> api.get_structural_assembly("1CRN")
            {
                'rcsb_struct_assembly': {
                    'id': '1',
                    'details': 'author_defined_assembly',
                    'method': 'PISA',
                    ...
                },
                'assemblies': [{
                    'assembly_id': '1',
                    'asym_id_list': ['A'],
                    'transformation': [[1,0,0],[0,1,0],[0,0,1]],
                    ...
                }]
            }
        """
        endpoint = f"core/assembly/{entry_id}/{assembly_id}"
        return self._get(endpoint)

    # Interface methods
    def get_polymer_interface(self, entry_id: str, assembly_id: str, interface_id: str) -> dict:
        """
        Retrieve detailed information about a polymer interface in a PDB entry.
        
        Args:
            entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
            assembly_id(str): ASSEMBLY ID of the biological assembly.(usually "1", "2", etc.)
            interface_id (str): The interface identifier (usually "1", "2", etc.)
            
        Returns:
            dict: A dictionary containing interface information with keys:
                - 'rcsb_interface_info':
                    - 'id': interface ID
                    - 'interface_area': interface area in Å²
                    - 'solvent_content': solvent content percentage
                    - 'interface_type': interface classification
                    - 'interface_chemistry': chemical composition
                - 'interface_partner':
                    - 'asym_id': list of asymmetric unit IDs
                    - 'entity_id': list of entity IDs
                    - 'interface_residues': list of interface residues
                - 'interface_features':
                    - 'hydrogen_bonds': count and details
                    - 'salt_bridges': count and details
                    - 'disulfide_bonds': count and details
                    
            Returns None if interface not found or error occurs.
            
        Example:
            >>> api.get_polymer_interface("1XYZ", "1")
            {
                'rcsb_interface_info': {
                    'id': '1',
                    'interface_area': 1200.5,
                    'interface_type': 'protein-protein',
                    ...
                },
                'interface_partner': {
                    'asym_id': ['A', 'B'],
                    'entity_id': ['1', '2'],
                    ...
                }
            }
        """
        endpoint = f"core/interface/{entry_id}/{assembly_id}/{interface_id}"
        return self._get(endpoint)

    # Chemical component methods
    def get_chemical_component(self, component_id: str) -> dict:
        """
        Retrieve detailed information about a chemical component in PDB.
        
        Args:
            component_id (str): The 3-letter chemical component ID (e.g. "ATP", "HEM")
            
        Returns:
            dict: A dictionary containing chemical component info with keys:
                - 'chem_comp': 
                    - 'id': component ID
                    - 'name': chemical name
                    - 'formula': molecular formula
                    - 'type': component type
                    - 'pdbx_type': PDB classification
                    - 'formula_weight': molecular weight
                    - 'pdbx_formal_charge': formal charge
                    - 'pdbx_modified_date': last modified date
                    - 'pdbx_release_status': release status
                    
            Returns None if component not found or error occurs.
            
        Example:
            >>> api.get_chemical_component("ATP")
            {
                'chem_comp': {
                    'id': 'ATP',
                    'name': 'ADENOSINE-5\'-TRIPHOSPHATE',
                    'formula': 'C10 H16 N5 O13 P3',
                    ...
                }
            }
        """
        endpoint = f"core/chemcomp/{component_id}"
        return self._get(endpoint)


    # Group methods
    def get_entry_groups(self, group_id: str) -> dict:
        """
        Retrieve detailed group information from RCSB PDB for a specified Group Deposition ID.

        This function sends a GET request to the RCSB PDB Core API endpoint `/core/entry_groups/{group_id}`,
        which returns metadata and group composition information for a specified group of PDB entries 
        deposited together.

        Parameters:
            group_id (str): The PDB Group Deposition ID (e.g., "G_1002011").

        Returns:
            dict: A JSON response containing the following fields (if found):
                - rcsb_id: Group-level RCSB identifier
                - rcsb_group_container_identifiers: Group and member ID relationships
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info: Name, description, granularity, and member count
                - rcsb_group_statistics: Similarity score cutoff and score range
                - rcsb_group_accession_info: Version information
                - rcsb_group_related: Related group structures (if any)

        Raises:
            requests.HTTPError: If the request fails with a 4xx or 5xx error.
            ValueError: If an invalid group_id is provided.

        Example:
            >>> get_pdb_group_by_id("G_1002011")
        """
        endpoint = f"core/entry_groups/{group_id}"
        return self._get(endpoint)

    def get_polymer_entity_groups(self, group_id: str) -> dict:
        """
        Retrieve a polymer entity group from RCSB PDB by UniProt ID or sequence cluster ID.

        This function returns structural and metadata information for a group of polymer entities (e.g., proteins, nucleic acids)
        that are associated with the same UniProt accession or belong to the same sequence cluster.

        Parameters:
            group_id (str): A UniProt ID (e.g., "Q3Y9I6") or RCSB sequence cluster ID representing the polymer entity group.

        Returns:
            dict: A JSON-formatted dictionary containing group-level metadata and composition details, including:
                - rcsb_id: Identifier for the entity group
                - rcsb_group_container_identifiers:
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info:
                    - group_name
                    - group_description
                    - group_members_granularity (e.g., assembly, chain)
                    - group_members_count
                - rcsb_group_statistics:
                    - similarity_cutoff
                    - similarity_score_min / max
                - rcsb_group_accession_info:
                    - version
                - rcsb_group_related: Related group entries
                - rcsb_polymer_entity_group_members_rankings: Ranking info for group members
                - rcsb_polymer_entity_group_sequence_alignment:
                    - abstract_reference: Reference sequence info
                    - group_members_alignment: Aligned member sequences

        Raises:
            requests.HTTPError: If the request fails with a client or server error.
            ValueError: If the group ID is improperly formatted or missing.

        Example:
            >>> get_polymer_entity_group("Q3Y9I6")
        """
        endpoint = f"core/polymer_entity_groups/{group_id}"
        return self._get(endpoint)

    def get_nonpolymer_entity_groups(self, group_id: str) -> dict:
        """
        Retrieve a non-polymer entity group object from RCSB PDB by Chemical Component ID.
        Obtain detailed information about a group of non-polymer entities (e.g., ligands, cofactors, ions) that share a common chemical component ID.

        Parameters:
            group_id (str): The Chemical Component ID of interest (e.g., "HEM" for heme group).

        Returns:
            dict: A dictionary containing the group metadata and structure, which may include:
                - rcsb_id: Group-level identifier
                - rcsb_group_container_identifiers:
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info:
                    - group_name
                    - group_description
                    - group_members_granularity
                    - group_members_count
                - rcsb_group_statistics:
                    - similarity_cutoff
                    - similarity_score_min / max
                - rcsb_group_accession_info:
                    - version
                - rcsb_group_related: Related groups (if any)
                - rcsb_polymer_entity_group_members_rankings: Ranking information for group members
                - rcsb_polymer_entity_group_sequence_alignment:
                    - abstract_reference
                    - group_members_alignment

        Raises:
            requests.HTTPError: If the request returns a 4xx or 5xx error.
            ValueError: If the provided group_id is invalid.

        Example:
            >>> get_nonpolymer_entity_group("HEM")
        """
        endpoint = f"core/nonpolymer_entity_groups/{group_id}"
        return self._get(endpoint)


if __name__ == "__main__":
    api = PDBAPI()
    
    # Test all functionality
    tests = [
        ("get_structure", ["4CYG"]),
        ("get_pubmed_annotations", ["4CYG"]),
        ("get_chemical_component", ["CEF"]),
        ("get_polymer_entity", ["4G22", "1"]),
        ("get_branched_entity", ["4CYG", "2"]),
        ("get_nonpolymer_entity", ["4G22", "2"]),
        ("get_polymer_entity_instance", ["2FBW", "E"]),
        ("get_branched_entity_instance", ["1US2", "C"]),
        ("get_nonpolymer_entity_instance", ["2FBW", "J"]),
        ("get_uniprot_annotations", ["4G22", "1"]),
        ("get_drugbank_annotations", ["ATP"]),
        ("get_structural_assembly", ["1RH7", "1"]),
        ("get_polymer_interface", ["1RH7", "1", "1"]),
        ("get_entry_groups", ["G_1002011"]),
        ("get_polymer_entity_groups", ["Q3Y9I6"]),
        ("get_nonpolymer_entity_groups", ["Q3Y9I6"]),
    ]
    
    
    for method, args in tests:
        print(f"\nTesting {method}() with args {args}:")

        result = getattr(api, method)(*args)
        if isinstance(result, dict):
            print(f"Result keys: {list(result.keys()) if result else 'None'}")
        elif isinstance(result, list):
            print(f"Result List Preview: {result[:2] if result else 'None'}")
        else:
            print(f"Result: {result}")
    

