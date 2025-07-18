#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PubChem API Client

This module provides a comprehensive interface to the PubChem REST API,
allowing users to search and retrieve information about chemical compounds,
substances, assays, and more from the PubChem database.

For more details on the PubChem API, visit:
https://pubchemdocs.ncbi.nlm.nih.gov/programmatic-access
"""
import os
import json
import re
import time
import urllib.parse
from typing import Dict, Optional, Union
import requests

import pubchempy as pcp

from tools.pubchem.utils import extract_description


class PubChemAPI:
    """PubChem API client for accessing chemical data from PubChem database."""

    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    VIEW_BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view"

    def __init__(self, delay: float = 0.2):
        """
        Initialize the PubChem API client.

        Args:
            delay: Time delay between API requests in seconds to avoid rate limiting
        """
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "PubChemPythonClient/1.0 (Python client for PubChem API)"}
        )
        self.delay = delay

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """
        Make an HTTP request to the PubChem API with rate limiting.

        Args:
            url: The API endpoint URL
            params: Query parameters

        Returns:
            The JSON response from the API

        Raises:
            requests.exceptions.RequestException: If the request fails
            ValueError: If the response is not JSON
        """
        time.sleep(self.delay)  # Rate limiting

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            if response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            else:
                # Some PubChem responses are not JSON
                return {"data": response.text}

        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "text"):
                error_info = f": {e.response.text}"
            else:
                error_info = ""
            raise requests.exceptions.RequestException(
                f"API request failed: {str(e)}{error_info}"
            )
        except ValueError as e:
            raise ValueError(f"Failed to parse API response as JSON: {str(e)}")

    def poll_pubchem_request(
        self, list_key: str, max_wait_time: int = 60, poll_interval: int = 2
    ) -> Dict:
        """
        Poll PubChem API for the status of an asynchronous request and retrieve results.

        Args:
            list_key: The ListKey returned by an asynchronous PubChem request
            max_wait_time: Maximum time to wait for the request to complete (seconds)
            poll_interval: Time between status checks (seconds)

        Returns:
            Dictionary containing the results of the completed request

        Raises:
            TimeoutError: If the request does not complete within max_wait_time
            Exception: If the API request fails
        """
        status_url = f"{self.BASE_URL}/compound/listkey/{list_key}/JSON"
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                response = requests.get(status_url, timeout=30)
                response.raise_for_status()
                status_response = response.json()

                if "Waiting" not in status_response:
                    # Request is complete, fetch the results
                    results_url = (
                        f"{self.BASE_URL}/compound/listkey/{list_key}/cids/JSON"
                    )
                    result_response = requests.get(results_url, timeout=30)
                    result_response.raise_for_status()
                    return result_response.json()

                print(f"Still waiting... {status_response['Waiting']['Message']}")
                time.sleep(poll_interval)
            except requests.exceptions.RequestException as e:
                raise Exception(f"API request failed: {e}")

        raise TimeoutError("Request did not complete within the maximum wait time")

    def search_pubchem_by_name(self, name: str, **kwargs) -> Dict:
        """
        Search PubChem for compounds matching a chemical name.

        Args:
            name: The chemical name to search for
            **kwargs: Additional parameters for the API request
                      (e.g., max_records: int)

        Returns:
            Dictionary containing search results with compounds that match the name
        """
        url = f"{self.BASE_URL}/compound/name/{urllib.parse.quote(name)}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def search_pubchem_by_smiles(self, smiles: str, **kwargs) -> Dict:
        """
        Search PubChem for compounds matching a SMILES string.

        Args:
            smiles: The SMILES notation to search for
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing search results with compounds that match the SMILES
        """
        url = f"{self.BASE_URL}/compound/smiles/{urllib.parse.quote(smiles)}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_pubchem_compound_by_cid(self, cid: Union[int, str], **kwargs) -> Dict:
        """
        Get detailed compound information by PubChem CID.

        Args:
            cid: PubChem Compound ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing detailed information about the compound
        """
        url = f"{self.BASE_URL}/compound/cid/{cid}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def search_pubchem_advanced(self, query: str, **kwargs) -> Dict:
        """
        Perform an advanced search on PubChem using a complex query.

        Args:
            query: The advanced search query string following PubChem syntax
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing search results matching the advanced query
        """
        # Encode the query for URL
        encoded_query = urllib.parse.quote(query)
        url = f"{self.BASE_URL}/compound/fastformula/{encoded_query}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_substance_by_sid(self, sid: Union[int, str], **kwargs) -> Dict:
        """
        Get substance information by PubChem SID.

        Args:
            sid: PubChem Substance ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing information about the substance
        """
        url = f"{self.BASE_URL}/substance/sid/{sid}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_compound_by_cid(self, cid: Union[int, str], **kwargs) -> Dict:
        """
        Get compound information by PubChem CID.

        Args:
            cid: PubChem Compound ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing information about the compound
        """
        # This is essentially the same as get_pubchem_compound_by_cid,
        # included for API completeness and consistency with todo list
        return self.get_pubchem_compound_by_cid(cid, **kwargs)

    def get_compound_by_name(self, name: str, **kwargs) -> Dict:
        """
        Get compound information by chemical name.

        Args:
            name: Chemical name
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing information about the compound
        """
        # First search for the compound by name to get the CID
        search_results = self.search_pubchem_by_name(name, **kwargs)

        if "PC_Compounds" in search_results and search_results["PC_Compounds"]:
            # Extract the CID from the search results
            cid = search_results["PC_Compounds"][0]["id"]["id"]["cid"]
            # Get the compound information by CID
            return self.get_compound_by_cid(cid, **kwargs)
        else:
            return {"error": f"No compound found with name: {name}"}

    def get_substance_by_name(self, name: str, **kwargs) -> Dict:
        """
        Get substance information by name.

        Args:
            name: Substance name
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing information about the substance
        """
        url = f"{self.BASE_URL}/substance/name/{urllib.parse.quote(name)}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def search_compound_by_substructure(self, smiles: str, **kwargs) -> Dict:
        """
        Search compounds containing a specified substructure.

        Args:
            smiles: SMILES notation of the substructure
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing compounds that contain the specified substructure
        """
        url = f"{self.BASE_URL}/compound/substructure/smiles/{urllib.parse.quote(smiles)}/JSON"
        params = kwargs
        response = self._make_request(url, params)
        if "Waiting" in response and "ListKey" in response["Waiting"]:
            list_key = response["Waiting"]["ListKey"]
            print(f"Request is processing with ListKey: {list_key}")
            return self.poll_pubchem_request(list_key)

        return response

    def search_compound_by_similarity(
        self, smiles: str, similarity: float = 95, **kwargs
    ) -> Dict:
        """
        Search compounds similar to a specified structure.

        Args:
            smiles: SMILES notation of the reference structure
            similarity: Minimum similarity threshold (0-100)
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing compounds similar to the specified structure
        """
        url = f"{self.BASE_URL}/compound/similarity/smiles/{urllib.parse.quote(smiles)}/JSON"
        params = {"Threshold": similarity, **kwargs}
        response = self._make_request(url, params)
        if "Waiting" in response and "ListKey" in response["Waiting"]:
            list_key = response["Waiting"]["ListKey"]
            print(f"Request is processing with ListKey: {list_key}")
            return self.poll_pubchem_request(list_key)
        return response

    def search_compound_by_identity(self, smiles: str, **kwargs) -> Dict:
        """
        Search compounds identical to a specified structure.

        Args:
            smiles: SMILES notation of the structure
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing compounds identical to the specified structure
        """
        url = f"{self.BASE_URL}/compound/identity/smiles/{urllib.parse.quote(smiles)}/JSON"
        params = kwargs
        response = self._make_request(url, params)
        if "Waiting" in response and "ListKey" in response["Waiting"]:
            list_key = response["Waiting"]["ListKey"]
            print(f"Request is processing with ListKey: {list_key}")
            return self.poll_pubchem_request(list_key)
        return response

    def search_compound_by_superstructure(self, smiles: str, **kwargs) -> Dict:
        """
        Search compounds that are superstructures of a specified structure.

        Args:
            smiles: SMILES notation of the structure
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing compounds that are superstructures of the specified structure
        """
        url = f"{self.BASE_URL}/compound/superstructure/smiles/{urllib.parse.quote(smiles)}/JSON"
        params = kwargs
        response = self._make_request(url, params)
        if "Waiting" in response and "ListKey" in response["Waiting"]:
            list_key = response["Waiting"]["ListKey"]
            print(f"Request is processing with ListKey: {list_key}")
            return self.poll_pubchem_request(list_key)
        return response

    def get_compound_property_by_name(
        self, name: str, property_name: str, **kwargs
    ) -> Dict:
        """
        Get a specific property of a compound by chemical name.

        Args:
            name: Chemical name
            property_name: Name of the property to retrieve (e.g., 'MolecularWeight', 'XLogP', 'TPSA')
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing the specified property of the compound
        """
        url = f"{self.BASE_URL}/compound/name/{urllib.parse.quote(name)}/property/{property_name}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_compound_synonyms_by_name(self, name: str, **kwargs) -> Dict:
        """
        Get synonyms of a compound by chemical name.

        Args:
            name: Chemical name
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing synonyms of the compound
        """
        url = f"{self.BASE_URL}/compound/name/{urllib.parse.quote(name)}/synonyms/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_description_by_sid(self, sid: Union[int, str], **kwargs) -> Dict:
        """
        Get description of a substance by SID.

        Args:
            sid: PubChem Substance ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing description of the substance
        """
        url = f"{self.VIEW_BASE_URL}/data/substance/{sid}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_description_by_cid(self, cid: Union[int, str], **kwargs) -> Dict:
        """
        Get description of a compound by CID.

        Args:
            cid: PubChem Compound ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing description of the compound
        """
        url = f"{self.VIEW_BASE_URL}/data/compound/{cid}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_description_by_name(self, name: str, **kwargs) -> Dict:
        """
        Get description of a compound by name.

        Args:
            name: PubChem Compound Name
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing description of the compound
        """
        result = self.search_pubchem_by_name(name, **kwargs)
        # try:
        cid = result["PC_Compounds"][0]["id"]["id"]["cid"]
        
        smiles = None
        for prop in result["PC_Compounds"][0]["props"]:
            if prop["urn"]["label"] == "SMILES":
                smiles = prop["value"]["sval"]
                break

        all_desc_info = self.get_description_by_cid(cid, **kwargs)

        try:
            desc_info = extract_description(all_desc_info)
        except Exception as e:
            print(f"Error: {e}")
            desc_info = "No description found for the compound"
        desc_info["SMILES"] = smiles
        return desc_info

    def get_description_by_aid(self, aid: Union[int, str], **kwargs) -> Dict:
        """
        Get description of an assay by AID.

        Args:
            aid: PubChem Assay ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing description of the assay
        """
        url = f"{self.VIEW_BASE_URL}/data/assay/{aid}/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_assay_summary_by_cid(self, cid: Union[int, str], **kwargs) -> Dict:
        """
        Get assay summary for a compound by CID.

        Args:
            cid: PubChem Compound ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing assay summary for the compound
        """
        url = f"{self.BASE_URL}/compound/cid/{cid}/assaysummary/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_assay_summary_by_sid(self, sid: Union[int, str], **kwargs) -> Dict:
        """
        Get assay summary for a substance by SID.

        Args:
            sid: PubChem Substance ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing assay summary for the substance
        """
        url = f"{self.BASE_URL}/substance/sid/{sid}/assaysummary/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_gene_summary_by_geneid(self, gene_id: Union[int, str], **kwargs) -> Dict:
        """
        Get summary information for a gene by Gene ID.

        Args:
            gene_id: Gene ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing summary information for the gene
        """
        url = f"{self.BASE_URL}/gene/geneid/{gene_id}/summary/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_protein_summary_by_accession(self, accession: str, **kwargs) -> Dict:
        """
        Get summary information for a protein by accession number.

        Args:
            accession: Protein accession number
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing summary information for the protein
        """
        url = f"{self.BASE_URL}/protein/accession/{accession}/summary/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_taxonomy_summary_by_taxonomyid(
        self, taxonomy_id: Union[int, str], **kwargs
    ) -> Dict:
        """
        Get summary information for a taxonomy by Taxonomy ID.

        Args:
            taxonomy_id: Taxonomy ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing summary information for the taxonomy
        """
        url = f"{self.BASE_URL}/taxonomy/taxid/{taxonomy_id}/summary/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_conformers_by_cid(self, cid: Union[int, str], **kwargs) -> Dict:
        """
        Get conformer information for a compound by CID.

        Args:
            cid: PubChem Compound ID
            **kwargs: Additional parameters for the API request

        Returns:
            Dictionary containing conformer information for the compound
        """
        url = f"{self.BASE_URL}/compound/cid/{cid}/conformers/JSON"
        params = kwargs
        return self._make_request(url, params)

    def get_compounds_by_smiles(self, smiles):
        """Get list of compound objects by SMILES"""
        return pcp.get_compounds(smiles, "smiles")

    def get_compounds_by_formula(self, formula):
        """Get list of compound objects by molecular formula"""
        return pcp.get_compounds(formula, "formula")

    def get_molecular_formula(self, compound):
        """Get molecular formula of compound"""
        return compound.molecular_formula

    def get_molecular_weight(self, compound):
        """Get molecular weight of compound"""
        return compound.molecular_weight

    def get_isomeric_smiles(self, compound):
        """Get isomeric SMILES of compound"""
        return compound.isomeric_smiles

    def get_xlogp(self, compound):
        """Get XLogP value of compound"""
        return compound.xlogp

    def get_iupac_name(self, compound):
        """Get IUPAC name of compound"""
        return compound.iupac_name

    def get_synonyms(self, compound):
        """Get list of synonyms for compound"""
        return compound.synonyms

    def get_cids_by_smiles(self, smiles):
        """Get list of CIDs by SMILES"""
        return pcp.get_cids(smiles, "smiles")

    def get_cids_by_formula(self, formula):
        """Get list of CIDs by molecular formula"""
        return pcp.get_cids(formula, "formula")

    def get_sids_by_name(self, name):
        """Get list of SIDs by name"""
        return pcp.get_sids(name, "name")

    def get_substance_by_sid(self, sid):
        """Get Substance object by SID"""
        substance = pcp.Substance.from_sid(sid)
        return substance.from_sid(sid)

    def get_substances_by_name(self, name):
        """Get list of Substance objects by name"""
        return pcp.get_substances(name, "name")

    def get_substances_source_id(self, sid):
        """Get source ID of Substance"""
        substance = pcp.Substance.from_sid(sid)
        return substance.source_id

    def get_substances_synonyms(self, sid):
        """Get list of synonyms for Substance"""
        substance = pcp.Substance.from_sid(sid)
        return substance.synonyms

    def download_structure_image_png(self, filename, query, query_type="name"):
        """Download structure image as PNG"""
        pcp.download("PNG", filename, query, query_type, overwrite=True)

    def download_properties_csv(self, filename, ids, properties):
        """Download properties as CSV"""
        pcp.download(
            "CSV",
            filename,
            ids,
            operation=f"property/{','.join(properties)}",
            overwrite=True,
        )

    def get_compound_dict(self, compound, properties):
        """Get dictionary of compound properties"""
        return compound.to_dict(properties=properties)

    def get_compounds_3d(self, name):
        """Get 3D structure compounds"""
        return pcp.get_compounds(name, "name", record_type="3d")

    def get_compounds_dict(self, compound):
        """Get compound dictionary"""
        c = pcp.Compound.from_cid(compound)
        return c.to_dict

    def get_substructure_cas(self, smiles):
        cas_rns = []
        results = pcp.get_synonyms(smiles, "smiles", searchtype="substructure")
        for result in results:
            for syn in result.get("Synonym", []):
                match = re.match(r"(\d{2,7}-\d\d-\d)", syn)
                if match:
                    cas_rns.append(match.group(1))
        return cas_rns

