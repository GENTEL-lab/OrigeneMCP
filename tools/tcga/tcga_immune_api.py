"""
TCGA Immune Correlation Analysis API
====================================
Analyze correlation between gene expression and immune cell infiltration in TCGA data.
Supports natural language input and recommends the most relevant immune cell type.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


# ==================== Configuration ====================

@dataclass
class ImmuneAPIConfig:
    """API configuration for immune correlation analysis"""
    # LLM config
    llm_api_key: str = ""
    llm_api_base: str = "https://api.openai-proxy.org/v1"
    llm_model: str = "gpt-4.1"
    llm_temperature: float = 0.1
    
    # Data directory
    data_dir: str = ""
    
    # Analysis config
    correlation_method: str = "spearman"
    fdr_threshold: float = 0.05


# ==================== Cancer Type Mapping ====================

CANCER_NAMES = {
    'LIHC': 'Liver Hepatocellular Carcinoma',
    'LUAD': 'Lung Adenocarcinoma',
    'LUSC': 'Lung Squamous Cell Carcinoma',
    'BRCA': 'Breast Invasive Carcinoma',
    'COAD': 'Colon Adenocarcinoma',
    'READ': 'Rectum Adenocarcinoma',
    'STAD': 'Stomach Adenocarcinoma',
    'ESCA': 'Esophageal Carcinoma',
    'PAAD': 'Pancreatic Adenocarcinoma',
    'PRAD': 'Prostate Adenocarcinoma',
    'BLCA': 'Bladder Urothelial Carcinoma',
    'KIRC': 'Kidney Renal Clear Cell Carcinoma',
    'KIRP': 'Kidney Renal Papillary Cell Carcinoma',
    'KICH': 'Kidney Chromophobe',
    'HNSC': 'Head and Neck Squamous Cell Carcinoma',
    'THCA': 'Thyroid Carcinoma',
    'OV': 'Ovarian Serous Cystadenocarcinoma',
    'UCEC': 'Uterine Corpus Endometrial Carcinoma',
    'CESC': 'Cervical Squamous Cell Carcinoma',
    'GBM': 'Glioblastoma Multiforme',
    'LGG': 'Brain Lower Grade Glioma',
    'SKCM': 'Skin Cutaneous Melanoma',
    'SARC': 'Sarcoma',
    'CHOL': 'Cholangiocarcinoma',
}

# Cancer name aliases for LLM parsing
CANCER_ALIASES = {
    'liver': 'LIHC', 'liver cancer': 'LIHC', 'hcc': 'LIHC', 'hepatocellular': 'LIHC',
    'lung adenocarcinoma': 'LUAD', 'lung adeno': 'LUAD',
    'lung squamous': 'LUSC', 'lung scc': 'LUSC',
    'breast': 'BRCA', 'breast cancer': 'BRCA',
    'colon': 'COAD', 'colon cancer': 'COAD', 'colorectal': 'COAD',
    'stomach': 'STAD', 'gastric': 'STAD', 'stomach cancer': 'STAD',
    'pancreatic': 'PAAD', 'pancreas': 'PAAD',
    'prostate': 'PRAD', 'prostate cancer': 'PRAD',
    'kidney': 'KIRC', 'renal': 'KIRC',
    'thyroid': 'THCA', 'thyroid cancer': 'THCA',
    'ovarian': 'OV', 'ovary': 'OV',
    'melanoma': 'SKCM', 'skin': 'SKCM',
    'glioblastoma': 'GBM', 'gbm': 'GBM',
}


# ==================== Core API Class ====================

class TCGA_Immune_API:
    """
    TCGA Immune Correlation Analysis API
    
    Workflow:
    1. LLM parses natural language query to extract gene and cancer type
    2. Fetch gene expression data from UCSC Xena
    3. Load immune infiltration data from local CIBERSORT file
    4. Perform Spearman correlation analysis
    5. Recommend the most relevant immune cell type
    6. Generate professional summary using LLM
    """
    
    def __init__(self, config: Optional[ImmuneAPIConfig] = None):
        """
        Initialize the API
        
        Args:
            config: API configuration, uses default if None
        """
        self.config = config or ImmuneAPIConfig()
        self.data_dir = Path(self.config.data_dir) if self.config.data_dir else Path(__file__).parent / "data"
        
        # Lazy load LLM
        self._llm = None
        
        # Cache for immune data
        self._immune_data_cache = {}
    
    @property
    def llm(self):
        """Lazy initialize LLM"""
        if self._llm is None:
            from langchain_openai import ChatOpenAI
            self._llm = ChatOpenAI(
                model=self.config.llm_model,
                api_key=self.config.llm_api_key,
                base_url=self.config.llm_api_base,
                temperature=self.config.llm_temperature
            )
        return self._llm
    
    # ==================== Main Entry ====================
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Execute complete analysis workflow
        
        Args:
            query: Natural language query, e.g.:
                - "Analyze GPR160 and immune cells in liver cancer"
                - "Analyze TP53 correlation with immune cells in lung adenocarcinoma"
        
        Returns:
            Complete analysis result dictionary
        """
        start_time = datetime.now()
        
        try:
            # Step 1: Parse query using LLM
            logger.info(f"Parsing query: {query}")
            params = self._parse_query(query)
            gene = params.get("gene")
            cancer = params.get("cancer")
            
            if not gene or not cancer:
                return {
                    "status": "error",
                    "error": "Failed to extract gene or cancer type from query",
                    "parsed_params": params
                }
            
            logger.info(f"Parsed params: gene={gene}, cancer={cancer}")
            
            # Step 2: Fetch expression data
            logger.info(f"Fetching expression data for {gene} in {cancer}")
            expr_data = self._fetch_expression_data(gene, cancer)
            if expr_data is None or len(expr_data) == 0:
                return {
                    "status": "error",
                    "error": f"Failed to fetch expression data for {gene} in TCGA-{cancer}",
                    "parsed_params": params
                }
            
            # Step 3: Fetch immune data
            logger.info(f"Loading immune infiltration data for {cancer}")
            immune_data = self._fetch_immune_data(cancer)
            if immune_data is None or len(immune_data) == 0:
                return {
                    "status": "error",
                    "error": f"Failed to load immune data for TCGA-{cancer}",
                    "parsed_params": params
                }
            
            # Step 4: Preprocess and merge data
            logger.info("Preprocessing and merging data")
            expr_data, immune_data = self._preprocess_and_merge(expr_data, immune_data, gene)
            
            if len(expr_data) == 0:
                return {
                    "status": "error",
                    "error": "No matching samples between expression and immune data",
                    "parsed_params": params
                }
            
            # Step 5: Add aggregated immune cell types
            immune_data = self._add_aggregated_cells(immune_data)
            
            # Step 6: Correlation analysis
            logger.info("Performing correlation analysis")
            correlation_results = self._correlation_analysis(expr_data, immune_data, gene)
            
            # Step 7: Prepare major immune cells results (needed for recommendation)
            major_immune_cells = self._get_major_immune_results(expr_data, immune_data, gene)
            
            # Step 8: Generate recommendation based on major immune cells
            recommendation = self._generate_recommendation(correlation_results, immune_data, major_immune_cells)
            
            # Step 9: Generate scatter plot for major immune cells
            logger.info("Generating scatter plot")
            self._generate_scatter_plot(expr_data, immune_data, gene, cancer, major_immune_cells)
            
            # Step 10: Generate summary using LLM
            logger.info("Generating analysis summary")
            summary = self._generate_summary(query, gene, cancer, correlation_results, 
                                            recommendation, major_immune_cells)
            
            # Build result
            duration = (datetime.now() - start_time).total_seconds()
            
            result = {
                "status": "success",
                "query": query,
                "parsed_params": {
                    "gene": gene,
                    "cancer": cancer,
                    "cancer_name": CANCER_NAMES.get(cancer, cancer)
                },
                "analysis_info": {
                    "n_samples": len(expr_data),
                    "n_cell_types": len([c for c in immune_data.columns if not c.endswith('_total')]),
                    "method": self.config.correlation_method
                },
                "recommendation": recommendation,
                "major_immune_cells": major_immune_cells,
                "top_correlations": self._get_top_correlations(correlation_results),
                "summary": summary,
                "duration_seconds": duration
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "query": query
            }
    
    # ==================== Query Parsing ====================
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """
        Use LLM to parse natural language query
        
        Args:
            query: Natural language query
            
        Returns:
            Dictionary with extracted gene and cancer type
        """
        system_prompt = """You are a bioinformatics assistant. Extract the gene symbol and cancer type from the user's query.

IMPORTANT:
1. gene: Extract the gene symbol (e.g., GPR160, TP53, EGFR, BRCA1)
2. cancer: Convert cancer type to TCGA project code:
   - Liver cancer / HCC / Hepatocellular → LIHC
   - Lung adenocarcinoma → LUAD
   - Lung squamous → LUSC
   - Breast cancer → BRCA
   - Colon cancer / Colorectal → COAD
   - Stomach / Gastric cancer → STAD
   - Pancreatic cancer → PAAD
   - Kidney / Renal cancer → KIRC
   - Prostate cancer → PRAD
   - Thyroid cancer → THCA
   - Ovarian cancer → OV
   - Melanoma → SKCM
   - Glioblastoma / GBM → GBM

Return ONLY a JSON object, no other text:
{"gene": "GENE_SYMBOL", "cancer": "TCGA_CODE"}

If you cannot determine the cancer type, use "LIHC" as default.
If you cannot determine the gene, set gene to null."""

        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ])
            
            content = response.content.strip()
            # Clean markdown code blocks
            content = content.replace("```json", "").replace("```", "").strip()
            
            params = json.loads(content)
            
            # Validate cancer code
            if params.get("cancer") and params["cancer"] not in CANCER_NAMES:
                # Try to find from aliases
                cancer_lower = params["cancer"].lower()
                if cancer_lower in CANCER_ALIASES:
                    params["cancer"] = CANCER_ALIASES[cancer_lower]
                else:
                    params["cancer"] = "LIHC"  # Default
            
            return params
            
        except Exception as e:
            logger.warning(f"LLM parsing failed: {e}")
            # Fallback: try simple regex extraction
            return self._fallback_parse(query)
    
    def _fallback_parse(self, query: str) -> Dict[str, Any]:
        """Fallback parsing without LLM"""
        import re
        
        # Try to find gene symbol (uppercase letters followed by optional numbers)
        gene_match = re.search(r'\b([A-Z][A-Z0-9]{1,10})\b', query)
        gene = gene_match.group(1) if gene_match else None
        
        # Try to find cancer type
        query_lower = query.lower()
        cancer = "LIHC"  # Default
        for alias, code in CANCER_ALIASES.items():
            if alias in query_lower:
                cancer = code
                break
        
        return {"gene": gene, "cancer": cancer}
    
    # ==================== Data Fetching ====================
    
    def _fetch_expression_data(self, gene: str, cancer: str) -> Optional[pd.DataFrame]:
        """
        Fetch gene expression data from UCSC Xena
        
        Args:
            gene: Gene symbol
            cancer: TCGA cancer code
            
        Returns:
            DataFrame with sample IDs and expression values
        """
        try:
            import xenaPython as xena
            
            hub = "https://tcga.xenahubs.net"
            dataset = f"TCGA.{cancer}.sampleMap/HiSeqV2"
            
            # Get samples
            samples = xena.dataset_samples(hub, dataset, None)
            if not samples:
                logger.warning(f"No samples found for {dataset}")
                return None
            
            # Get gene expression
            result = xena.dataset_gene_probe_avg(hub, dataset, samples, [gene])
            
            if result and len(result) > 0:
                gene_data = result[0]
                if 'scores' in gene_data and gene_data['scores']:
                    values = gene_data['scores'][0]
                    
                    # Filter valid values
                    valid_data = []
                    for s, v in zip(samples, values):
                        if v is not None and str(v) != 'NaN':
                            valid_data.append((s, float(v)))
                    
                    if valid_data:
                        samples_valid, values_valid = zip(*valid_data)
                        expr_df = pd.DataFrame({
                            'sample': samples_valid,
                            gene: values_valid
                        }).set_index('sample')
                        
                        logger.info(f"Fetched {len(expr_df)} samples for {gene}")
                        return expr_df
            
            return None
            
        except ImportError:
            logger.error("xenaPython not installed. Run: pip install xenaPython")
            return None
        except Exception as e:
            logger.error(f"Failed to fetch expression data: {e}")
            return None
    
    def _fetch_immune_data(self, cancer: str) -> Optional[pd.DataFrame]:
        """
        Load immune infiltration data from local CIBERSORT file
        
        Args:
            cancer: TCGA cancer code
            
        Returns:
            DataFrame with immune cell infiltration values
        """
        # Check cache
        if cancer in self._immune_data_cache:
            return self._immune_data_cache[cancer].copy()
        
        # Find data file
        data_file = self.data_dir / "TCGA_CIBERSORT.tsv"
        if not data_file.exists():
            logger.error(f"Data file not found: {data_file}")
            return None
        
        try:
            df = pd.read_csv(data_file, sep='\t', index_col=0)
            
            # Filter by cancer type
            if 'CancerType' in df.columns:
                cancer_df = df[df['CancerType'] == cancer].copy()
                cancer_df = cancer_df.drop(columns=['CancerType'], errors='ignore')
            else:
                # Filter by sample ID pattern
                cancer_df = df[df.index.str.contains(cancer)].copy()
            
            # Keep only numeric columns
            cancer_df = cancer_df.select_dtypes(include=[np.number])
            
            # Remove QC columns
            qc_cols = ['P.value', 'Correlation', 'RMSE', 'P-value', 'Absolute score']
            cancer_df = cancer_df.drop(columns=[c for c in qc_cols if c in cancer_df.columns], errors='ignore')
            
            logger.info(f"Loaded {len(cancer_df)} samples, {len(cancer_df.columns)} cell types for {cancer}")
            
            # Cache
            self._immune_data_cache[cancer] = cancer_df
            
            return cancer_df.copy()
            
        except Exception as e:
            logger.error(f"Failed to load immune data: {e}")
            return None
    
    # ==================== Data Preprocessing ====================
    
    def _preprocess_and_merge(self, expr_data: pd.DataFrame, immune_data: pd.DataFrame, 
                              gene: str) -> tuple:
        """
        Preprocess and merge expression and immune data
        
        Args:
            expr_data: Expression data DataFrame
            immune_data: Immune infiltration DataFrame
            gene: Gene symbol
            
        Returns:
            Tuple of (expression_df, immune_df) with matched samples
        """
        def normalize_id(s):
            """Normalize TCGA sample ID"""
            s = str(s).replace('.', '-')
            parts = s.split('-')
            if len(parts) >= 4:
                return '-'.join(parts[:4])[:15]
            return s
        
        def is_tumor_sample(sample_id):
            """Check if sample is tumor (01-09)"""
            s = str(sample_id).replace('.', '-')
            parts = s.split('-')
            if len(parts) >= 4:
                sample_type = parts[3][:2]
                try:
                    type_num = int(sample_type)
                    return 1 <= type_num <= 9
                except ValueError:
                    return False
            return False
        
        # Add normalized ID column
        expr_df = expr_data.reset_index()
        expr_df.columns = ['original_id'] + list(expr_df.columns[1:])
        expr_df['sample_short'] = [normalize_id(s) for s in expr_df['original_id']]
        
        immune_df = immune_data.reset_index()
        immune_df.columns = ['original_id'] + list(immune_df.columns[1:])
        immune_df['sample_short'] = [normalize_id(s) for s in immune_df['original_id']]
        
        # Filter tumor samples only
        expr_tumor_mask = [is_tumor_sample(s) for s in expr_df['original_id']]
        immune_tumor_mask = [is_tumor_sample(s) for s in immune_df['original_id']]
        
        expr_df = expr_df[expr_tumor_mask]
        immune_df = immune_df[immune_tumor_mask]
        
        # Merge on normalized ID
        merged = expr_df.merge(immune_df, on='sample_short', how='inner', suffixes=('_expr', '_immune'))
        
        logger.info(f"Merged {len(merged)} tumor samples")
        
        if len(merged) == 0:
            return pd.DataFrame(), pd.DataFrame()
        
        # Extract expression data
        expr_result = merged[['sample_short', gene]].copy()
        expr_result = expr_result.set_index('sample_short')
        
        # Extract immune data
        immune_cols = [c for c in merged.columns 
                      if c not in ['original_id_expr', 'original_id_immune', 'sample_short', gene]
                      and not c.endswith('_expr')]
        
        # Clean column names
        immune_cols_clean = []
        for c in immune_cols:
            if c.endswith('_immune'):
                immune_cols_clean.append(c[:-7])
            else:
                immune_cols_clean.append(c)
        
        immune_result = merged[['sample_short'] + immune_cols].copy()
        immune_result.columns = ['sample_short'] + immune_cols_clean
        immune_result = immune_result.set_index('sample_short')
        immune_result = immune_result.select_dtypes(include=[np.number])
        
        # Remove missing values
        valid_mask = ~(expr_result[gene].isna() | (immune_result.isna().any(axis=1)))
        expr_result = expr_result[valid_mask]
        immune_result = immune_result[valid_mask]
        
        return expr_result, immune_result
    
    def _add_aggregated_cells(self, immune_data: pd.DataFrame) -> pd.DataFrame:
        """
        Add aggregated immune cell types
        
        Args:
            immune_data: Immune infiltration DataFrame
            
        Returns:
            DataFrame with added aggregated columns
        """
        aggregation_rules = {
            'T_cells_total': ['T.cells', 'T cells', 'CD4', 'CD8', 'Treg', 'Th1', 'Th2', 'gamma.delta', 'follicular'],
            'Macrophage_total': ['Macrophage', 'M0', 'M1', 'M2'],
            'B_cells_total': ['B.cells', 'B cells', 'B-cells', 'Plasma'],
            'NK_cells_total': ['NK.cells', 'NK cells', 'NK-cells', 'NKT'],
            'DC_total': ['Dendritic', 'DC', 'pDC'],
            'Mast_cells_total': ['Mast'],
        }
        
        for agg_name, keywords in aggregation_rules.items():
            matching_cols = []
            for col in immune_data.columns:
                col_lower = col.lower()
                for kw in keywords:
                    kw_lower = kw.lower()
                    if kw_lower in col_lower:
                        # Avoid Mast cells matching T cells
                        if agg_name == 'T_cells_total' and 'mast' in col_lower:
                            continue
                        matching_cols.append(col)
                        break
            
            matching_cols = list(set(matching_cols))
            if matching_cols:
                immune_data[agg_name] = immune_data[matching_cols].sum(axis=1)
        
        return immune_data
    
    # ==================== Correlation Analysis ====================
    
    def _correlation_analysis(self, expr_data: pd.DataFrame, immune_data: pd.DataFrame,
                             gene: str) -> pd.DataFrame:
        """
        Perform Spearman correlation analysis
        
        Args:
            expr_data: Expression data
            immune_data: Immune infiltration data
            gene: Gene symbol
            
        Returns:
            DataFrame with correlation results
        """
        gene_values = expr_data[gene].values
        results = []
        
        # Only analyze original cell types (exclude _total columns)
        cell_columns = [c for c in immune_data.columns if not c.endswith('_total')]
        
        for cell_type in cell_columns:
            immune_values = immune_data[cell_type].values
            
            if self.config.correlation_method == 'spearman':
                corr, pvalue = stats.spearmanr(gene_values, immune_values)
            else:
                corr, pvalue = stats.pearsonr(gene_values, immune_values)
            
            results.append({
                'Cell_Type': cell_type,
                'Correlation': corr,
                'P_value': pvalue,
                'N_samples': len(gene_values)
            })
        
        results_df = pd.DataFrame(results)
        
        # FDR correction
        pvals = results_df['P_value'].values
        n = len(pvals)
        sorted_idx = np.argsort(pvals)
        sorted_pvals = pvals[sorted_idx]
        fdr = np.zeros(n)
        fdr[sorted_idx] = np.minimum.accumulate(
            (sorted_pvals * n / (np.arange(n) + 1))[::-1]
        )[::-1]
        results_df['FDR'] = np.clip(fdr, 0, 1)
        
        # Significance markers
        results_df['Significance'] = results_df['FDR'].apply(
            lambda x: '***' if x < 0.001 else ('**' if x < 0.01 else ('*' if x < 0.05 else 'ns'))
        )
        
        # Sort by absolute correlation
        results_df = results_df.sort_values('Correlation', key=abs, ascending=False)
        results_df = results_df.reset_index(drop=True)
        
        return results_df
    
    # ==================== Recommendation Generation ====================
    
    def _get_major_immune_results(self, expr_data: pd.DataFrame, immune_data: pd.DataFrame,
                                  gene: str) -> List[Dict]:
        """
        Get correlation results for major immune cell types
        
        Args:
            expr_data: Expression data
            immune_data: Immune infiltration data
            gene: Gene symbol
            
        Returns:
            List of results for T cells, Macrophage, DC, NK cells
        """
        major_cells = {
            'T cells': 'T_cells_total',
            'Macrophage': 'Macrophage_total',
            'DC': 'DC_total',
            'NK cells': 'NK_cells_total',
        }
        
        gene_values = expr_data[gene].values
        results = []
        
        for display_name, col_name in major_cells.items():
            if col_name not in immune_data.columns:
                continue
            
            immune_values = immune_data[col_name].values
            
            if self.config.correlation_method == 'spearman':
                corr, pval = stats.spearmanr(gene_values, immune_values)
            else:
                corr, pval = stats.pearsonr(gene_values, immune_values)
            
            results.append({
                'cell_type': display_name,
                'R': round(corr, 4),
                'P': pval,
                'significant': pval < self.config.fdr_threshold
            })
        
        # Sort by absolute R
        results.sort(key=lambda x: abs(x['R']), reverse=True)
        
        return results
    
    def _generate_recommendation(self, correlation_results: pd.DataFrame,
                                 immune_data: pd.DataFrame,
                                 major_immune_results: List[Dict] = None) -> Dict[str, Any]:
        """
        Generate recommendation for the most relevant immune cell type
        
        Args:
            correlation_results: Correlation analysis results
            immune_data: Immune infiltration data
            major_immune_results: Pre-calculated major immune cell results
            
        Returns:
            Recommendation dictionary
        """
        # Use pre-calculated major immune results if available
        if major_immune_results:
            # Find the best significant correlation
            best_cell = None
            best_r = 0
            best_p = 1
            
            for result in major_immune_results:
                r = result['R']
                p = result['P']
                if p < self.config.fdr_threshold and abs(r) > abs(best_r):
                    best_cell = result['cell_type']
                    best_r = r
                    best_p = p
            
            # If no significant, pick the strongest absolute correlation
            if best_cell is None and major_immune_results:
                best_result = max(major_immune_results, key=lambda x: abs(x['R']))
                best_cell = best_result['cell_type']
                best_r = best_result['R']
                best_p = best_result['P']
            
            if best_cell:
                direction = "positive" if best_r > 0 else "negative"
                significance = '***' if best_p < 0.001 else ('**' if best_p < 0.01 else ('*' if best_p < 0.05 else 'ns'))
                
                return {
                    "cell_type": best_cell,
                    "correlation": round(best_r, 4),
                    "p_value": best_p,
                    "direction": direction,
                    "significance": significance,
                    "reason": f"Strongest significant {direction} correlation among major immune cell types (T cells, Macrophage, DC, NK cells)"
                }
        
        return {
            "cell_type": "None",
            "correlation": 0,
            "p_value": 1,
            "direction": "none",
            "significance": "ns",
            "reason": "No significant correlation found among major immune cell types"
        }
    
    def _get_top_correlations(self, correlation_results: pd.DataFrame) -> Dict[str, List[Dict]]:
        """
        Get top positive and negative correlations
        
        Args:
            correlation_results: Correlation analysis results
            
        Returns:
            Dictionary with top positive and negative correlations
        """
        sig_results = correlation_results[correlation_results['FDR'] < self.config.fdr_threshold]
        
        positive = sig_results[sig_results['Correlation'] > 0].nlargest(5, 'Correlation')
        negative = sig_results[sig_results['Correlation'] < 0].nsmallest(5, 'Correlation')
        
        return {
            "positive": [
                {"cell_type": row['Cell_Type'], "R": round(row['Correlation'], 4), 
                 "P": row['P_value'], "FDR": round(row['FDR'], 6)}
                for _, row in positive.iterrows()
            ],
            "negative": [
                {"cell_type": row['Cell_Type'], "R": round(row['Correlation'], 4),
                 "P": row['P_value'], "FDR": round(row['FDR'], 6)}
                for _, row in negative.iterrows()
            ]
        }
    
    # ==================== Summary Generation ====================
    
    def _generate_summary(self, query: str, gene: str, cancer: str,
                         correlation_results: pd.DataFrame, recommendation: Dict,
                         major_immune_cells: List[Dict]) -> str:
        """
        Use LLM to generate professional analysis summary
        
        Args:
            query: Original query
            gene: Gene symbol
            cancer: Cancer type code
            correlation_results: Correlation results
            recommendation: Recommendation dictionary
            major_immune_cells: Major immune cell results
            
        Returns:
            Professional summary text
        """
        cancer_name = CANCER_NAMES.get(cancer, cancer)
        
        # Prepare data for LLM
        summary_data = {
            "gene": gene,
            "cancer": cancer,
            "cancer_name": cancer_name,
            "n_samples": correlation_results['N_samples'].iloc[0] if len(correlation_results) > 0 else 0,
            "recommendation": recommendation,
            "major_immune_cells": major_immune_cells,
            "top_positive": correlation_results[correlation_results['Correlation'] > 0].head(3).to_dict('records'),
            "top_negative": correlation_results[correlation_results['Correlation'] < 0].head(3).to_dict('records')
        }
        
        system_prompt = """You are a bioinformatics expert. Generate a professional summary for the immune correlation analysis results.

The summary should include:
1. Overview: Gene, cancer type, sample size
2. Main Finding: Recommended immune cell type and the correlation
3. Detailed Results: Correlations for T cells, Macrophage, DC, NK cells
4. Biological Implication: Brief interpretation of what this correlation may mean

Keep the summary concise (3-5 sentences). Use professional but accessible language."""

        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Query: {query}\n\nAnalysis Results:\n{json.dumps(summary_data, indent=2, default=str)}")
            ])
            
            return response.content.strip()
            
        except Exception as e:
            logger.warning(f"Failed to generate summary: {e}")
            # Fallback summary
            rec = recommendation
            return (f"{gene} expression was analyzed for correlation with immune cell infiltration in "
                   f"{cancer_name} (TCGA-{cancer}, n={summary_data['n_samples']}). "
                   f"The analysis recommends {rec['cell_type']} as the most relevant immune cell type "
                   f"(R={rec['correlation']}, P={rec['p_value']:.2e}, {rec['direction']} correlation). "
                   f"{rec['reason']}.")
    
    def _generate_scatter_plot(self, expr_data: pd.DataFrame, immune_data: pd.DataFrame,
                               gene: str, cancer: str, major_immune_cells: List[Dict]):
        """
        Generate scatter plot for 4 major immune cell types
        
        Args:
            expr_data: Expression data
            immune_data: Immune infiltration data
            gene: Gene symbol
            cancer: Cancer type code
            major_immune_cells: Pre-calculated correlation results
        """
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Output directory
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Major cell types mapping
            major_cells = {
                'T cells': 'T_cells_total',
                'Macrophage': 'Macrophage_total',
                'DC': 'DC_total',
                'NK cells': 'NK_cells_total',
            }
            
            # Filter available cells
            available_cells = {}
            for name, col in major_cells.items():
                if col in immune_data.columns:
                    available_cells[name] = col
            
            if len(available_cells) < 2:
                logger.warning("Not enough cell types for scatter plot")
                return
            
            n_plots = len(available_cells)
            fig, axes = plt.subplots(1, n_plots, figsize=(4*n_plots, 4))
            if n_plots == 1:
                axes = [axes]
            
            gene_values = expr_data[gene].values
            
            # Find correlation values from major_immune_cells
            corr_dict = {r['cell_type']: r for r in major_immune_cells}
            
            for i, (cell_name, col_name) in enumerate(available_cells.items()):
                ax = axes[i]
                immune_values = immune_data[col_name].values
                
                # Get correlation from pre-calculated results
                if cell_name in corr_dict:
                    corr = corr_dict[cell_name]['R']
                    pval = corr_dict[cell_name]['P']
                else:
                    corr, pval = stats.spearmanr(gene_values, immune_values)
                
                # Scatter plot with regression line
                sns.regplot(x=gene_values, y=immune_values, ax=ax,
                           scatter_kws={'alpha': 0.5, 's': 20, 'color': '#3498db'},
                           line_kws={'color': 'red', 'linewidth': 2},
                           ci=95)
                
                ax.set_xlabel(f'{gene} Expression', fontsize=10)
                ax.set_ylabel('Infiltration Score', fontsize=10)
                ax.set_title(f'{cell_name}\nR = {corr:.3f}, P = {pval:.2e}', fontsize=11, fontweight='bold')
            
            plt.tight_layout()
            
            # Save figure
            output_path = output_dir / f"scatter_{gene}_{cancer}.png"
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            logger.info(f"Scatter plot saved to {output_path}")
            
        except Exception as e:
            logger.warning(f"Failed to generate scatter plot: {e}")

    # ==================== Utility Methods ====================
    
    def get_supported_cancer_types(self) -> List[Dict[str, str]]:
        """Get list of supported cancer types"""
        return [{"id": k, "name": v} for k, v in CANCER_NAMES.items()]


# ==================== Convenience Functions ====================

_api_instance: Optional[TCGA_Immune_API] = None


def get_immune_api(config: Optional[ImmuneAPIConfig] = None) -> TCGA_Immune_API:
    """Get API singleton"""
    global _api_instance
    if _api_instance is None:
        _api_instance = TCGA_Immune_API(config)
    return _api_instance


def analyze_immune_correlation(query: str) -> Dict[str, Any]:
    """Quick analysis function"""
    return get_immune_api().run(query)
