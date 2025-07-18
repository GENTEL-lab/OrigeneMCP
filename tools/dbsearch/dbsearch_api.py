from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO, Entrez
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from typing import List, Optional, Union, Dict
import time
import os
import requests
import re
import pandas as pd
from io import StringIO


NOW_DIR = os.path.dirname(os.path.abspath(__file__))
CYTO_FILE = os.path.join(NOW_DIR, 'cytoBand.txt')
CACHE_FILE = os.path.join(NOW_DIR, 'refseq_cache.fa')


class DBSearch:
    """Unified class combining all database search APIs from db_search directory"""
    
    def __init__(self, cyto_file=CYTO_FILE, email="liyu0377@lglab.ac.cn"):
        """
        Initialize DBSEARCH with common configurations.
        
        Args:
            cyto_file (str): Path to UCSC-style cytoBand.txt file (for Ensembl queries)
            email (str): Email for NCBI/Entrez queries
        """
        # Common configurations
        self.email = email
        self.CACHE_FILE = CACHE_FILE
        self.cyto_file = cyto_file
        self.promoter_dir = "./genes_promoter[-1000,+100]"
        
        # API endpoints
        self.entrez_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
        self.gsea_base_url = "https://www.gsea-msigdb.org/gsea/msigdb/human/download_geneset.jsp"
        self.phipster_base_url = "http://ec2-18-215-31-69.compute-1.amazonaws.com:8000/home/"
        self.uniprot_api_url = "https://rest.uniprot.org/uniprotkb/search"
        
        # Initialize session objects
        self.session = requests.Session()
        self.headers = {"accept": "application/json"}

    # --------------------------
    # CLINVAR API Methods
    # --------------------------
    def load_cache(self) -> dict:
        """Load cached RefSeq sequences from FASTA file into memory."""
        if not os.path.exists(self.CACHE_FILE):
            return {}
        cache = {}
        for record in SeqIO.parse(self.CACHE_FILE, "fasta"):
            cache[str(record.seq)] = record.id
        return cache

    def append_to_cache(self, refseq_id: str, sequence: str) -> None:
        """Append a new RefSeq ID and sequence to the cache file."""
        record = SeqRecord(Seq(sequence), id=refseq_id, description="")
        with open(self.CACHE_FILE, "a", newline='\n') as f:
            SeqIO.write(record, f, "fasta")

    def clinvar_get_best_refseqid_by_sequence(self, seq: str, retries: int = 3, wait: int = 5) -> Optional[str]:
        """Find best matching RefSeq ID for a protein sequence using BLASTP."""
        cache = self.load_cache()
        if seq in cache:
            return cache[seq]

        for i in range(retries):
            try:
                result_handle = NCBIWWW.qblast(
                    program="blastp",
                    database="nr",
                    sequence=seq,
                    hitlist_size=10,
                    expect=1e-5,
                    format_type="XML",
                    service="plain"
                )
                break
            except Exception as e:
                time.sleep(wait)
        
        blast_record = NCBIXML.read(result_handle)
        for alignment in blast_record.alignments:
            if alignment.accession.startswith('NP'):
                for hsp in alignment.hsps:
                    if hsp.identities == hsp.align_length:
                        best_refseqid = alignment.accession
                        self.append_to_cache(best_refseqid, seq)
                        return best_refseqid
        return None

    def clinvar_query_variant_significance(self, refseqid: Optional[str] = None, 
                                         variant: Optional[str] = None,
                                         hgvs: Optional[str] = None) -> Union[dict, str]:
        """Query ClinVar for variant classification/significance."""
        Entrez.email = self.email
        if hgvs is None:
            if not (refseqid and variant):
                return "Error: Either hgvs or (refseqid and variant) must be provided"
            hgvs = f"{refseqid}:p.{variant}"
        if "=" in hgvs:
            return {'description': 'Likely benign'}
        
        try:
            handle = Entrez.esearch(db="clinvar", term=hgvs)
            record = Entrez.read(handle)
            handle.close()

            if not record["IdList"]:
                return {'description': 'Not found'}

            clinvar_id = record["IdList"][0]
            params = {'db': 'clinvar', 'id': clinvar_id, 'retmode': 'json'}
            res = requests.get(self.entrez_url, params=params)
            return res.json()['result'][clinvar_id]['germline_classification']
        except Exception as e:
            return f"Error: {str(e)}"

    # --------------------------
    # ENSEMBL API Methods
    # --------------------------
    def get_genes_in_region(self, chrom: str, start: int, end: int) -> List[str]:
        """Query Ensembl REST API to get genes within a genomic region."""
        region = f"{chrom}:{start}-{end}"
        url = f"https://rest.ensembl.org/overlap/region/human/{region}?feature=gene"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return [gene["external_name"] for gene in data if "external_name" in gene]

    def ensembl_get_genes_by_band(self, query_band: str) -> List[str]:
        """Extract genes in a cytogenetic band region (e.g., 'chr10q21')."""
        match = re.match(r'chr(\d+|X|Y)([pq])(\d+)', query_band)
        if not match:
            raise ValueError("Invalid input format, expected like 'chr10q21'")

        chrom = f'chr{match.group(1)}'
        arm = match.group(2)
        band_prefix = match.group(3)
        target_prefix = f"{arm}{band_prefix}"

        regions = []
        with open(self.cyto_file) as f:
            for line in f:
                fields = line.strip().split('\t')
                chr_name, start, end, band_name, stain = fields
                if chr_name != chrom:
                    continue
                if band_name.startswith(target_prefix):
                    regions.append((int(start), int(end)))

        if not regions:
            raise ValueError(f"No bands found for {query_band} in {self.cyto_file}.")

        MAX_SPAN = 4000000
        genes = []
        for start, end in regions:
            start, end = min(start, end), max(start, end)
            if end - start < MAX_SPAN:
                genes += self.get_genes_in_region(chrom, start, end)
            else:
                for chunk_start in range(start, end, MAX_SPAN):
                    chunk_end = min(chunk_start + MAX_SPAN, end)
                    genes += self.get_genes_in_region(chrom, chunk_start, chunk_end)
        return genes

    # --------------------------
    # GSEA API Methods
    # --------------------------
    def gsea_get_genelist_from_genesetname(self, genesetname: str) -> List[str]:
        """Retrieve gene list from a GSEA gene set."""
        params = {"geneSetName": genesetname, "fileType": "json"}
        d = self._get_gsea(params=params)
        return d[genesetname]['geneSymbols'] if d else []

    def _get_gsea(self, params=None):
        """Internal helper for GSEA GET requests."""
        try:
            r = requests.get(self.gsea_base_url, params=params, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except Exception as err:
            print(f"GSEA API error: {err}")
            return None

    # --------------------------
    # GTRD API Methods
    # --------------------------
    def gtrd_gene_to_entry(self, gene_name: str, organism: str = "9606") -> str:
        """Convert gene symbol to UniProt protein entry ID."""
        params = {
            "query": f"gene:{gene_name} AND organism_id:{organism} AND reviewed:true",
            "fields": "accession",
            "format": "json",
            "size": 10
        }

        try:
            response = requests.get(self.uniprot_api_url, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])
            if not results:
                raise ValueError(f"No UniProt entry found for gene: {gene_name}")
            return results[0]["primaryAccession"]
        except Exception as e:
            raise Exception(f"Failed to query UniProt: {str(e)}")

    def gtrd_entry_to_target_genes(self, entry: str) -> List[str]:
        """Query promoter files for target genes of a UniProt entry."""
        file_path = os.path.join(self.promoter_dir, f"{entry}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Promoter file not found: {file_path}")

        target_genes = []
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    target_genes.append(parts[1])
        return target_genes

    # --------------------------
    # MIRDB API Methods
    # --------------------------
    def mirdb_get_geneset_by_mirname(self, mirname: str, candidates: List[str]) -> dict:
        """Get predicted target genes for a miRNA."""
        url = "https://mirdb.org/cgi-bin/search.cgi"
        data = {
            "species": "Human",
            "searchBox": mirname,
            "submitButton": "Go",
            "searchType": "miRNA"
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://mirdb.org",
            "Referer": "https://mirdb.org/mirdb/index.html",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = requests.post(url, data=data, headers=headers, timeout=10)
            response.raise_for_status()
            tables = pd.read_html(StringIO(response.text))
            if not tables:
                return {"error": "EmptyResult", "message": f"No result for miRNA '{mirname}'", "fallback": True}

            df = tables[0]
            header = df.iloc[0].tolist()
            df.columns = header
            df = df[1:]
            gene_list = df["Gene Symbol"].dropna().tolist()
            gene_set = set(gene_list)
            matched = [g for g in candidates if g in gene_set]
            unmatched = [g for g in candidates if g not in gene_set]
            return {"predicted_targets": matched, "not_predicted_targets": unmatched}
        except Exception as e:
            return {"error": "ToolExecutionError", "message": str(e), "fallback": True}

    # --------------------------
    # MOUSEMINE API Methods
    # --------------------------
    def mousemine_get_geneset_from_mpid(self, mpid: str) -> List[str]:
        """Get mouse gene symbols associated with a MGI phenotype ID."""
        url = f"https://www.mousemine.org/mousemine/keywordSearchResults.do?searchTerm={mpid}&searchSubmit=search"
        tables = pd.read_html(url)
        df = tables[0]
        gene_names = []
        for i, row in df.iterrows():
            if row['Type'] == 'Protein Coding Gene':
                parts = row['Details'].split('|')
                if len(parts) >= 2:
                    gene = parts[1].strip().split()[0]
                    gene_names.append(gene)
        return gene_names

    # --------------------------
    # PHIPSTER API Methods
    # --------------------------
    def phipster_vpname2vpid(self, vpname: str) -> Optional[str]:
        """Convert viral protein name to VPID."""
        params = {"format": "json"}
        d = self._get_phipster("vpid2name", params=params)
        if d:
            for k, v in d.items():
                if vpname in v:
                    return k
        return None

    def phipster_get_hpid_list_by_vpid(self, vpid: str) -> List[str]:
        """Get human protein IDs interacting with a viral protein."""
        params = {"format": "json"}
        endpoint = f"ppi/vp-lrfilter/{vpid}/100"
        vpid_hpid_ppi = self._get_phipster(endpoint, params=params)
        return [entry["humanprotein_id"] for entry in vpid_hpid_ppi] if vpid_hpid_ppi else []

    def phipster_hpid_list_to_hpname_list(self, hpid_list: List[str]) -> List[str]:
        """Convert human protein IDs to names."""
        params = {"format": "json"}
        d_hpid2name = self._get_phipster("hpid2name", params=params)
        return [d_hpid2name.get(str(hpid), f"Unknown_{hpid}") for hpid in hpid_list] if d_hpid2name else []

    def _get_phipster(self, endpoint: str, params=None):
        """Internal helper for PHIPSTER GET requests."""
        url = self.phipster_base_url + endpoint
        try:
            r = requests.get(url, params=params, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except Exception as err:
            print(f"PHIPSTER API error: {err}")
            return None

