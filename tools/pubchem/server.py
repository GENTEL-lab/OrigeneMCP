from mcp.server.fastmcp import FastMCP

from tools.pubchem.pubchem_api import PubChemAPI


mcp = FastMCP(
    "pubchem_mcp",
    stateless_http=True,
)
pubchem_api = PubChemAPI()


@mcp.tool()
async def search_pubchem_by_name(name: str):
    """
    Search PubChem for compounds matching a chemical name.Be aware though that matching chemical names to structure is an inexact science at best, and a name may often refer to more than one record. 
    
    Args:
        name: Name (string)
        kwargs: kwargs (string)
    
    Query example: {"name": "aspirin", "kwargs": "{}"}
    
    Returns:
        sth
    """

    try:
        result = pubchem_api.search_pubchem_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while searching PubChem by name: {str(e)}"}
    return result

@mcp.tool()
async def search_pubchem_by_smiles(smiles: str):
    """
    Search PubChem for compounds matching a SMILES string.
    
    Args:
        smiles: The SMILES notation to search for
    
    Returns:
        Dictionary containing search results with compounds that match the SMILES
    
    Query example: {"smiles": "C[C@H](N)C(=O)O"}
    """


    try:
        result = pubchem_api.search_pubchem_by_smiles(smiles)
    except Exception as e:
        return {"error": f"An error occurred while searching PubChem by SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_pubchem_compound_by_cid(cid: str):
    """
    Get detailed compound information by PubChem CID.
    
    Args:
        cid: PubChem Compound ID (integer or string)
    
    Returns:
        Dictionary containing detailed information about the compound (Complete chemical properties, structural information, relevant biological activities,etc)
    
    Query example: {"cid": 2244}
    """


    try:
        result = pubchem_api.get_pubchem_compound_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting PubChem compound by CID: {str(e)}"}
    return result

@mcp.tool()
async def search_pubchem_advanced(query: str):
    """
    Perform an advanced search on PubChem using a complex query.
    
    Args:
        query: The advanced search query string following PubChem syntax
        **kwargs: Additional parameters for the API request
            
    Returns:
        Dictionary containing search results matching the advanced query
    """
    try:
        result = pubchem_api.search_pubchem_advanced(query)
    except Exception as e:
        return {"error": f"An error occurred during advanced PubChem search: {str(e)}"}
    return result

@mcp.tool()
async def get_substance_by_sid(sid: str):
    """
    Get substance information by PubChem SID.
    
    Args:
        sid: PubChem Substance ID
    
    Returns:
        Dictionary containing information about the substance.This example returns Substance(sid)
    
    Query example: {"sid": 347827035}
    """


    try:
        result = pubchem_api.get_substance_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance by SID: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_by_cid(cid: str):
    """
    Get compound information by PubChem CID.
    
    Args:
        cid: PubChem Compound ID

    Returns:
        Dictionary containing information about the compound
    """
    try:
        result = pubchem_api.get_compound_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting compound by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_by_name(name: str):
    """
    Get compound information by chemical name. Be aware though that matching chemical names to structure is an inexact science at best, and a name may often refer to more than one record.
    
    Args:
        name: Chemical name
    
    Returns:
        Dictionary containing information about the compound(CID, structure, properties, etc.)
    
    Query example: {"name": "aspirin"}
    """


    try:
        result = pubchem_api.get_compound_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting compound by name: {str(e)}"}
    return result

@mcp.tool()
async def get_substance_by_name(name: str):
    """
    Get substance information by name.
    
    Args:
        name: Substance name(string)
        
    Returns:
        Dictionary containing information about the substance
    
    Query example: {"name": "aspirin"}
    """


    try:
        result = pubchem_api.get_substance_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting substance by name: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_property_by_name(name: str, property_name: str):
    """
    Retrieve a specific chemical property for a compound by its name from PubChem.
    The response returns a table containing the requested property for the matching compound.
    
    Args:
        name: Chemical name of the compound (string)
        property_name: Name of the property to retrieve, e.g.,
            - MolecularWeight
            - MolecularFormula
            - XLogP
            - TPSA
            - etc.
    
    Returns:
        A dictionary containing:
        - PropertyTable:
            • Properties: List of property entries, each with:
                - CID:               PubChem Compound ID
                - <property_name>:   The requested property value for the compound
    
    Query example:
        {"name": "caffeine", "property_name": "MolecularFormula"}
    """


    try:
        result = pubchem_api.get_compound_property_by_name(name, property_name)
    except Exception as e:
        return {"error": f"An error occurred while getting compound property by name: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_synonyms_by_name(name: str):
    """
    Retrieve all known synonyms for a given compound by its chemical name from PubChem.
    The response returns a list of synonyms, including registry numbers, alternate names,
    trade names, database identifiers, and systematic names.
    
    Args:
        name: Chemical name of the compound (string)
    
    Returns:
        A dictionary containing:
        - InformationList:
            • Information: List of entries, each with:
                - CID:     PubChem Compound ID
                - Synonym: List of synonym strings for the compound
    
    Query example:
        {"name": "caffeine"}
    """


    try:
        result = pubchem_api.get_compound_synonyms_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting compound synonyms by name: {str(e)}"}
    return result

@mcp.tool()
async def get_description_by_sid(sid: str):
    """
    Get detailed description information for a PubChem substance given its SID.
    The response includes the full Record structure, containing sections such as
    2D Structure, Identity, Source, External ID, Synonyms, Deposit/Modify Dates,
    Status, and related compounds standardized from this substance.
    
    Args:
        sid: PubChem Substance ID (integer or string)
    
    Returns:
        A dictionary containing the full Record for the substance, with fields:
        - RecordType:      Type of record ("SID")
        - RecordNumber:    Numeric SID
        - RecordTitle:     Substance title/name
        - Section:         List of sections, each with:
            • TOCHeading:       Section heading (e.g., "2D Structure", "Identity")
            • Description:      Text describing the section
            • Information:      List of info entries (values, references, URLs)
        - Reference:       List of references, each with:
            • SourceName, SourceID, Description, URL
    
    Query example:
        {"sid": "12345"}
    """


    try:
        result = pubchem_api.get_description_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting description by SID: {str(e)}"}
    return result

@mcp.tool()
async def get_description_by_cid(cid: str):
    """
    Retrieve detailed description information for a PubChem compound given its CID.
    The response returns the full Record structure, including sections such as:
    • Structures (2D/3D depictions)
    • Identity (sources, external IDs, synonyms, versioning)
    • Deposit/Modify/Available dates
    • Status of the record
    • Related Records (related compounds, crystal data, articles, etc.)
    
    Args:
        cid: PubChem Compound ID (integer or string)
    
    Returns:
        A dictionary containing the full Record for the compound, with fields:
        - RecordType:      Type of record ("CID")
        - RecordNumber:    Numeric CID
        - RecordTitle:     Compound name/title
        - Section:         List of sections, each with:
            • TOCHeading:       Section heading (e.g., "Structures", "3D Conformer")
            • Description:      Text describing the section
            • Information:      List of detailed entries (values, references, URLs, tables)
        - Reference:       List of reference entries (source name, description, URL)
    
    Query example:
        {"cid": "2244"}
    """


    try:
        result = pubchem_api.get_description_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting description by CID: {str(e)}"}
    return result

@mcp.tool() 
async def get_general_info_by_compound_name(name: str):
    """
    Get detailed description of a compound by name, including overall information, drug and medication information, pharmacology and biochemistry information.
    
    Args:
        name: PubChem Compound Name

    Returns:
        Dictionary containing description of the compound
    """
    try:
        result = pubchem_api.get_description_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting description by name: {str(e)}"}
    return result

@mcp.tool()
async def get_description_by_aid(aid: str):
    """
    Retrieve detailed description information for a PubChem bioassay given its AID.
    The response returns the full Record structure, including sections such as:
    • Record Description (summary provided by depositor)
    • Description (bioassay overview and assay context)
    • Protocol (experimental protocol details)
    • Comment (depositor comments and references)
    • Result Definitions (data table column definitions)
    • Data Table (bioactivity results and flags)
    • Target (protein/gene targets)
    • Related Targets, Entrez Crosslinks
    • Identity (assay metadata: name, source, type, dates)
    • BioAssay Annotations (format, detection method, etc.)
    
    Args:
        aid: PubChem Assay ID (integer or string)
    
    Returns:
        A dictionary containing the full Record for the assay, with fields:
        - RecordType:      Type of record ("AID")
        - RecordNumber:    Numeric AID
        - RecordTitle:     Assay title/name
        - Section:         List of sections, each with:
            • TOCHeading:       Section heading (e.g., "Protocol", "Target")
            • Description:      Text describing the section
            • Information:      List of detailed entries (values, reference numbers, URLs)
        - Reference:       List of reference entries (source name, description, URL)
    
    Query example:
        {"aid": "450"}
    """


    try:
        result = pubchem_api.get_description_by_aid(aid)
    except Exception as e:
        return {"error": f"An error occurred while getting description by AID: {str(e)}"}
    return result

@mcp.tool()
async def get_assay_summary_by_cid(cid: str):
    """
    Retrieve a summary of bioassay activities for a given PubChem compound CID.
    The response includes a table of assays where the compound has been tested,
    with details on activity outcome, target information, assay metadata, and references.
    
    Args:
        cid: PubChem Compound ID (integer or string)
    
    Returns:
        A dictionary containing an assay summary table with fields:
        - Table:
            • Columns:
                - AID:             PubChem Assay ID
                - Panel Member ID: Identifier for assay panel (if applicable)
                - SID:             PubChem Substance ID
                - CID:             PubChem Compound ID
                - Activity Outcome: e.g., "Active", "Inactive"
                - Target GI:       GenInfo Identifier for the target
                - Target GeneID:   NCBI Gene ID of the target
                - Activity Value [uM]: Numeric activity measurement (µM)
                - Activity Name:   Name of the activity metric (e.g., "Kd")
                - Assay Name:      Description of the assay
                - Assay Type:      Category of assay (e.g., "Other", "Primary Screening")
                - PubMed ID:       PubMed literature reference
                - RNAi:            RNA interference annotation (if any)
            • Row: List of assay result entries
    
    Query example:
        {"cid": "2144"}
    """


    try:
        result = pubchem_api.get_assay_summary_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting assay summary by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_assay_summary_by_sid(sid: str):
    """
    Retrieve a summary of bioassay activities for a given PubChem substance SID.
    The response includes a table listing assays in which the substance was tested,
    with details on outcomes, target information, assay metadata, and references.
    
    Args:
        sid: PubChem Substance ID (integer or string)
    
    Returns:
        A dictionary containing an assay summary table with fields:
        - Table:
            • Columns:
                - AID:              PubChem Assay ID
                - Panel Member ID:  Identifier for assay panel (if applicable)
                - SID:              PubChem Substance ID
                - CID:              PubChem Compound ID
                - Activity Outcome: e.g., "Active", "Inconclusive", "Unspecified"
                - Target GI:        GenInfo Identifier for the target
                - Target GeneID:    NCBI Gene ID of the target
                - Activity Value [uM]: Numeric activity measurement (µM), if available
                - Activity Name:    Name of the activity metric (e.g., "Kd")
                - Assay Name:       Description/title of the assay
                - Assay Type:       Category of assay (e.g., "Other", "Primary Screening")
                - PubMed ID:        PubMed literature reference, if any
                - RNAi:             RNA interference annotation (if any)
            • Row: List of assay result entries, each as a dict with a "Cell" list
    
    Query example:
        {"sid": "8149208"}
    """


    try:
        result = pubchem_api.get_assay_summary_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting assay summary by SID: {str(e)}"}
    return result

@mcp.tool()
async def get_gene_summary_by_geneid(gene_id: str):
    """
    Get summary information for a gene by Gene ID.
    
    Args:
        gene_id: Gene ID

    Returns:
        Dictionary containing summary information for the gene
    """
    try:
        result = pubchem_api.get_gene_summary_by_geneid(gene_id)
    except Exception as e:
        return {"error": f"An error occurred while getting gene summary by Gene ID: {str(e)}"}
    return result

@mcp.tool()
async def get_protein_summary_by_accession(accession: str):
    """
    Retrieve summary information for a protein from PubChem by its UniProt or other accession number.
    The response includes basic annotations such as the protein’s name, taxonomy, and known synonyms.
    
    Args:
        accession: Protein accession number (string), e.g., UniProt ID or NCBI accession
    
    Returns:
        A dictionary containing:
        - ProteinSummaries:
            • ProteinSummary: List of summary entries, each with:
                - ProteinAccession: The queried accession number
                - Name: Official protein name
                - TaxonomyID: NCBI taxonomy identifier (e.g., 9606)
                - Taxonomy: Latin name and common name of the organism
                - Synonym: List of alternative names or enzyme classifications
    
    Query example:
        {"accession": "P00734"}
    """


    try:
        result = pubchem_api.get_protein_summary_by_accession(accession)
    except Exception as e:
        return {"error": f"An error occurred while getting protein summary by accession: {str(e)}"}
    return result

@mcp.tool()
async def get_taxonomy_summary_by_taxonomyid(taxonomy_id: str):
    """
    Retrieve summary information for a biological taxonomy entry given its NCBI Taxonomy ID.
    The response includes scientific and common names, rank, lineage, and synonyms.
    
    Args:
        taxonomy_id: NCBI Taxonomy ID (integer or string)
    
    Returns:
        A dictionary containing:
        - TaxonomySummaries:
            • TaxonomySummary: List of summary entries, each with:
                - TaxonomyID:      Numeric taxonomy identifier
                - ScientificName:  Latin scientific name (e.g., "Homo sapiens")
                - CommonName:      Common name (e.g., "human")
                - Rank:            Taxonomic rank (e.g., "species")
                - RankedLineage:   Hierarchical lineage with keys:
                    • Superkingdom, Kingdom, Phylum, Class, Order, Family, Genus, Species
                - Synonym:         List of alternative names or historic names
    
    Query example:
        {"taxonomy_id": "9606"}
    """


    try:
        result = pubchem_api.get_taxonomy_summary_by_taxonomyid(taxonomy_id)
    except Exception as e:
        return {"error": f"An error occurred while getting taxonomy summary by Taxonomy ID: {str(e)}"}
    return result

@mcp.tool()
async def get_conformers_by_cid(cid: str):
    """
    Retrieve available conformer identifiers for a given PubChem compound CID.
    Conformers represent different 3D geometries computed or provided for the compound.
    
    Args:
        cid: PubChem Compound ID (integer or string)
    
    Returns:
        A dictionary containing:
        - InformationList:
            • Information: List of entries, each with:
                - CID:          PubChem Compound ID
                - ConformerID:  List of conformer identifiers for the compound
    
    Query example:
        {"cid": "2244"}
    """


    try:
        result = pubchem_api.get_conformers_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting conformers by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_by_smiles(smiles: str):
    """
    Retrieve compound objects from PubChem based on a given SMILES string.
    Each returned object represents a matching compound entry.
    
    Args:
        smiles: SMILES string of the query structure (e.g., "CCO" for ethanol)
    
    Returns:
        A list of compound objects matching the SMILES query.
        For example, "Compound(702)" indicates the PubChem compound with CID 702.
    
    Query example:
        {"smiles": "CCO"}
    """


    try:
        result = pubchem_api.get_compounds_by_smiles(smiles)
    except Exception as e:
        return {"error": f"An error occurred while getting compounds by SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_by_formula(formula: str):
    """
    Retrieve compound objects from PubChem based on a molecular formula.
    The response returns a list of matching compound entries.
    
    Args:
        formula: Molecular formula string (e.g., "C2H6O")
    
    Returns:
        A list of compound objects matching the formula.
        Each entry is represented as "Compound(<CID>)", where <CID> is the PubChem Compound ID.
    
    Query example:
        {"formula": "C2H6O"}
    """


    try:
        result = pubchem_api.get_compounds_by_formula(formula)
    except Exception as e:
        return {"error": f"An error occurred while getting compounds by formula: {str(e)}"}
    return result

@mcp.tool()
async def get_molecular_formula(compound):
    """
    Get the molecular formula of a compound.
    
    Args:
        compound: A PubChemPy Compound object
            
    Returns:
        The molecular formula of the compound
    """
    try:
        result = pubchem_api.get_molecular_formula(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting molecular formula: {str(e)}"}
    return result

@mcp.tool()
async def get_molecular_weight(compound):
    """
    Get the molecular weight of a compound.
    
    Args:
        compound: A PubChemPy Compound object
            
    Returns:
        The molecular weight of the compound
    """
    try:
        result = pubchem_api.get_molecular_weight(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting molecular weight: {str(e)}"}
    return result

@mcp.tool()
async def get_isomeric_smiles(compound):
    """
    Get the isomeric SMILES of a compound.
    
    Args:
        compound: A PubChemPy Compound object
            
    Returns:
        The isomeric SMILES of the compound
    """
    try:
        result = pubchem_api.get_isomeric_smiles(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting isomeric SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_xlogp(compound):
    """
    Get the XLogP value of a compound.
    
    Args:
        compound: A PubChemPy Compound object
            
    Returns:
        The XLogP value of the compound
    """
    try:
        result = pubchem_api.get_xlogp(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting XLogP: {str(e)}"}
    return result

@mcp.tool()
async def get_iupac_name(compound):
    """
    Get the IUPAC name of a compound.
    
    Args:
        compound: A PubChemPy Compound object
            
    Returns:
        The IUPAC name of the compound
    """
    try:
        result = pubchem_api.get_iupac_name(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting IUPAC name: {str(e)}"}
    return result

@mcp.tool()
async def get_synonyms(compound):
    """
    Get the synonyms of a compound.
    
    Args:
        compound: A PubChemPy Compound object
            
    Returns:
        List of synonyms of the compound
    """
    try:
        result = pubchem_api.get_synonyms(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting synonyms: {str(e)}"}
    return result

@mcp.tool()
async def get_cids_by_smiles(smiles: str):
    """
    Obtain the CID corresponding to the drug smiles
    
    Args:
        smiles: SMILES notation
        
    Returns:
        List of CIDs
    
    Args:
        smiles: Smiles (string)
    
    Query example: {"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"}
    
    Returns:
        A list of cids
    """


    try:
        result = pubchem_api.get_cids_by_smiles(smiles)
    except Exception as e:
        return {"error": f"An error occurred while getting CIDs by SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_cids_by_formula(formula: str):
    """
    Get a list of CIDs by molecular formula.
    
    Args:
        formula: Formula of the drug(string)
    
    Query example: {"formula": "C9H8O4"}
    
    Returns:
        List of CIDs
    """


    try:
        result = pubchem_api.get_cids_by_formula(formula)
    except Exception as e:
        return {"error": f"An error occurred while getting CIDs by formula: {str(e)}"}
    return result

@mcp.tool()
async def get_sids_by_name(name: str):
    """
    Get a list of SIDs by name.
    
    Args:
        name: Name of the substance
    
    Query example: {"name": "aspirin"}
    
    Returns:
        A dict containing the following fields:
            CID: the cid of the drug
            SID: a list of SIDs
    """


    try:
        result = pubchem_api.get_sids_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting SIDs by name: {str(e)}"}
    return result

@mcp.tool()
async def get_substance_by_sid_pcp(sid: str):
    """
    Get a Substance object by SID using PubChemPy.
    
    Args:
        sid: PubChem Substance ID
        
    Returns:
        A PubChemPy Substance object (But this tool returns Substance(sid))
    
    Query example: {"sid": 4594}
    """


    try:
        result = pubchem_api.get_substance_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance by SID (PubChemPy): {str(e)}"}
    return result

@mcp.tool()
async def get_substances_by_name_pcp(name: str):
    """
    Get a list of Substance objects by name using PubChemPy.
    
    Args:
        name: Substance name
        
    Returns:
        List of PubChemPy Substance objects (A list whose elements are "Substance(sid)")
    
    Query example: {"name": "aspirin"}
    """


    try:
        result = pubchem_api.get_substances_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting substances by name (PubChemPy): {str(e)}"}
    return result

@mcp.tool()
async def get_substances_source_id(sid: str):
    """
    Get the source ID (Unique identifier assigned to the compound or substance by the original database (e.g. DrugBank, ChEMBL, etc.)) of a substance by SID.
    
    Args:
        sid: PubChem Substance ID
        
    Returns:
        The source ID of the substance
    
    Query example: {"sid": 123456}
    """


    try:
        result = pubchem_api.get_substances_source_id(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance source ID: {str(e)}"}
    return result

@mcp.tool()
async def get_substances_synonyms(sid: str):
    """
    Get the synonyms (Different names or identifiers for the same chemical substance) of a substance by SID.
    
    Args:
        sid: PubChem Substance ID
        
    Returns:
        List of synonyms of the substance
    
    Query example: {"sid": 123456}
    """


    try:
        result = pubchem_api.get_substances_synonyms(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance synonyms: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_dict(compound, properties):
    """
    Get a dictionary of a compound's properties.
    
    Args:
        compound: A PubChemPy Compound object
        properties: List of property names to include in the dictionary
            
    Returns:
        Dictionary containing the specified properties of the compound
    """
    try:
        result = pubchem_api.get_compound_dict(compound, properties)
    except Exception as e:
        return {"error": f"An error occurred while getting compound dictionary: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_3d(name: str):
    """
    Get a list of compound objects with 3D structures.
    
    Args:
        name: Chemical name
            
    Returns:
        List of PubChemPy Compound objects with 3D structures
    """
    try:
        result = pubchem_api.get_compounds_3d(name)
    except Exception as e:
        return {"error": f"An error occurred while getting 3D compounds: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_dict(compound_cid: str):
    """
    Get a dictionary representation of a compound by CID.
    
    Args:
        compound_cid: PubChem Compound ID
        
    Returns:
        Dictionary containing compound information
    
    Query example: {"compound_cid": 962}
    """


    try:
        result = pubchem_api.get_compounds_dict(compound_cid)
    except Exception as e:
        return {"error": f"An error occurred while getting compound dictionary by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_substructure_cas(smiles: str):
    """
    Get CAS Registry Numbers for compounds containing a specified substructure.
    
    Args:
        smiles: SMILES notation of the substructure (string)
    
    Query example: {"smiles": "CN"}
    
    Returns:
        List of CAS Registry Numbers
    """


    try:
        result = pubchem_api.get_substructure_cas(smiles)
    except Exception as e:
        return {"error": f"An error occurred while getting substructure CAS numbers: {str(e)}"}
    return result


@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    prompt = """You have access to tools for searching and retrieving chemical information from PubChem, which is a database of chemical molecules and their activities against biological assays. PubChem is maintained by the National Center for Biotechnology Information (NCBI), a component of the National Library of Medicine (NLM), which is part of the United States National Institutes of Health (NIH).

You can search for compounds by name, SMILES notation, molecular weight, or structural features. You can retrieve detailed information about compounds, including their properties, synonyms, and descriptions.

Use the API tools to extract relevant chemical information for the user's queries. When the user asks about a chemical or drug, try to provide comprehensive information including:
- Basic identifiers (CID, molecular formula)
- Physical properties (molecular weight, etc.)
- Common names and synonyms
- Chemical structure information when available
- Biological activities when relevant

Fill in missing arguments with sensible values if the user hasn't provided them."""
    return prompt
