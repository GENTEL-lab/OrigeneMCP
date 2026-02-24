#!/usr/bin/env python3
"""
TCGA Differential Gene Expression Analysis Module
=================================================
Core analysis module for TCGA differential expression analysis.

Features:
- Fetch real TCGA data from GDC API
- Perform Tumor vs Normal differential expression analysis (PyDESeq2)
- Generate publication-quality visualizations (mixed strategy: user-specified genes + top DEGs)
- Auto-save complete workflow logs to output directory

Visualization style: Blue (Normal) + Red (Tumor), publication-quality figure style

Dependencies:
pip install requests pandas numpy scipy matplotlib seaborn scikit-learn pydeseq2 mygene tqdm
"""

import os
import json
import gzip
import shutil
import tempfile
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

import requests
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# Constants
# ============================================================================

GDC_API_BASE = "https://api.gdc.cancer.gov"
GDC_FILES_ENDPOINT = f"{GDC_API_BASE}/files"
GDC_DATA_ENDPOINT = f"{GDC_API_BASE}/data"

# Cache directory
CACHE_DIR = Path(tempfile.gettempdir()) / "tcga_deg_cache"
CACHE_DIR.mkdir(exist_ok=True)

# Visualization config
FIGURE_DPI = 300

# ============================================================================
# Color Scheme - Blue + Red (Publication Style)
# ============================================================================

COLORS = {
    'normal': '#2166AC',      # Blue - Normal
    'tumor': '#B2182B',       # Red - Tumor
    'normal_light': '#67A9CF',
    'tumor_light': '#EF8A62',
    'ns': '#D3D3D3',          # Non-significant - Light gray
}

# Blue-White-Red gradient for DEG heatmap (upregulated red, downregulated blue)
DEG_HEATMAP_CMAP = LinearSegmentedColormap.from_list(
    'blue_white_red',
    ['#2166AC', '#67A9CF', '#FFFFFF', '#EF8A62', '#B2182B']
)


# ============================================================================
# Publication Style Settings
# ============================================================================

def setup_publication_style():
    """Set up publication-quality figure style"""
    sns.set_style("ticks", {
        'axes.linewidth': 1.2,
        'axes.edgecolor': '#333333',
    })
    
    plt.rcParams.update({
        # Font settings
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        
        # Lines and borders
        'axes.linewidth': 1.2,
        'axes.spines.top': False,
        'axes.spines.right': False,
        
        # Ticks
        'xtick.major.width': 1.0,
        'ytick.major.width': 1.0,
        'xtick.major.size': 4,
        'ytick.major.size': 4,
        
        # Figure background
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'savefig.edgecolor': 'none',
        
        # Legend
        'legend.frameon': False,
        'legend.loc': 'best',
    })


# ============================================================================
# Workflow Tracker
# ============================================================================

class WorkflowTracker:
    """Track agent workflow progress"""
    
    def __init__(self):
        self.question: str = ""
        self.tool_called: str = ""
        self.tool_input: Dict = {}
        self.steps: List[Dict[str, Any]] = []
        self.result: Dict[str, Any] = {}
        self.start_time: datetime = None
        self.end_time: datetime = None
    
    def set_question(self, question: str):
        self.question = question
        self.start_time = datetime.now()
    
    def add_step(self, step_name: str, description: str, details: Any = None):
        step = {
            "step_number": len(self.steps) + 1,
            "name": step_name,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.steps.append(step)
        logger.info(f"[Step {step['step_number']}] {step_name}: {description}")
    
    def set_tool_call(self, tool_name: str, tool_input: Dict):
        self.tool_called = tool_name
        self.tool_input = tool_input
    
    def set_result(self, result: Dict):
        self.result = result
        self.end_time = datetime.now()
    
    def get_summary(self) -> Dict:
        """Get complete workflow summary"""
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        
        return {
            "question": self.question,
            "tool_called": self.tool_called,
            "tool_input": self.tool_input,
            "workflow_steps": [
                f"Step {s['step_number']}: {s['name']} -> {s['description']}"
                for s in self.steps
            ],
            "result": self.result,
            "duration_seconds": round(duration, 2)
        }


# Global tracker instance
workflow_tracker = WorkflowTracker()


# ============================================================================
# Data Classes and Config
# ============================================================================

@dataclass
class AnalysisConfig:
    """Analysis configuration"""
    cancer_type: str
    genes: Optional[List[str]] = None
    min_samples: int = 3
    max_samples_per_group: int = 20
    min_count_threshold: int = 10
    min_sample_with_counts: int = 2
    fdr_threshold: float = 0.05
    log2fc_threshold: float = 1.0
    output_dir: str = "./output"
    use_cache: bool = True
    max_workers: int = 4


# ============================================================================
# GDC API Data Fetcher Module (Real Data)
# ============================================================================

class GDCDataFetcher:
    """GDC data fetcher"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def get_file_uuids(self) -> Tuple[List[Dict], List[Dict]]:
        """Get HTSeq-Counts file UUIDs for specified cancer type"""
        workflow_tracker.add_step(
            "Query GDC API",
            f"Querying expression data files for {self.config.cancer_type}",
            {"api_endpoint": GDC_FILES_ENDPOINT}
        )
        
        filters = {
            "op": "and",
            "content": [
                {"op": "in", "content": {"field": "cases.project.project_id", "value": [self.config.cancer_type]}},
                {"op": "in", "content": {"field": "files.data_category", "value": ["Transcriptome Profiling"]}},
                {"op": "in", "content": {"field": "files.data_type", "value": ["Gene Expression Quantification"]}},
                {"op": "in", "content": {"field": "files.analysis.workflow_type", "value": ["STAR - Counts"]}}
            ]
        }
        
        fields = ["file_id", "file_name", "cases.case_id", "cases.submitter_id", 
                  "cases.samples.sample_type", "cases.samples.sample_id"]
        
        params = {
            "filters": json.dumps(filters),
            "fields": ",".join(fields),
            "format": "JSON",
            "size": "10000"
        }
        
        try:
            response = self.session.get(GDC_FILES_ENDPOINT, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.error(f"Failed to query file list: {e}")
            raise
        
        hits = data.get("data", {}).get("hits", [])
        logger.info(f"Found {len(hits)} files")
        
        tumor_files, normal_files = [], []
        
        for hit in hits:
            file_info = {
                "file_id": hit["file_id"],
                "file_name": hit["file_name"],
                "case_id": None,
                "sample_type": None
            }
            
            cases = hit.get("cases", [])
            if cases:
                case = cases[0]
                file_info["case_id"] = case.get("submitter_id", case.get("case_id"))
                samples = case.get("samples", [])
                if samples:
                    sample_type = samples[0].get("sample_type", "")
                    file_info["sample_type"] = sample_type
                    
                    if "Normal" in sample_type:
                        normal_files.append(file_info)
                    elif "Tumor" in sample_type or "Primary" in sample_type:
                        tumor_files.append(file_info)
        
        # Random sampling
        import random
        random.seed(42)
        
        max_n = self.config.max_samples_per_group
        if len(tumor_files) > max_n:
            tumor_files = random.sample(tumor_files, max_n)
        
        if len(normal_files) > max_n:
            normal_files = random.sample(normal_files, max_n)
        
        workflow_tracker.add_step(
            "Sample selection complete",
            f"Tumor samples: {len(tumor_files)}, Normal samples: {len(normal_files)}",
            {"tumor_count": len(tumor_files), "normal_count": len(normal_files)}
        )
        
        return tumor_files, normal_files
    
    def download_file(self, file_info: Dict, output_dir: Path, max_retries: int = 3) -> Optional[Path]:
        """Download a single file"""
        file_id = file_info["file_id"]
        file_name = file_info["file_name"]
        
        cache_path = CACHE_DIR / f"{file_id}.tsv"
        if self.config.use_cache and cache_path.exists():
            return cache_path
        
        url = f"{GDC_DATA_ENDPOINT}/{file_id}"
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, stream=True, timeout=(15, 120), verify=False)
                response.raise_for_status()
                
                temp_path = output_dir / file_name
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                
                if file_name.endswith('.gz'):
                    decompressed_path = output_dir / file_name.replace('.gz', '')
                    with gzip.open(temp_path, 'rb') as f_in:
                        with open(decompressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    temp_path.unlink()
                    temp_path = decompressed_path
                
                if self.config.use_cache:
                    shutil.copy(temp_path, cache_path)
                
                return temp_path
                
            except Exception as e:
                logger.warning(f"Download attempt {attempt+1}/{max_retries} failed ({file_name}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return None
    
    def download_files_parallel(self, file_list: List[Dict], output_dir: Path, sample_type: str) -> Dict[str, Path]:
        """Download files in parallel"""
        workflow_tracker.add_step(
            f"Download {sample_type} sample data",
            f"Downloading expression data for {len(file_list)} {sample_type} samples in parallel",
            {"sample_count": len(file_list), "max_workers": self.config.max_workers}
        )
        
        results = {}
        total = len(file_list)
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            future_to_file = {executor.submit(self.download_file, f, output_dir): f for f in file_list}
            
            for future in as_completed(future_to_file):
                file_info = future_to_file[future]
                completed += 1
                try:
                    path = future.result()
                    if path:
                        sample_id = f"{file_info['case_id']}_{file_info['sample_type']}"
                        results[sample_id] = path
                    print(f"\r  Download progress: {completed}/{total} ({100*completed/total:.0f}%)", end="", flush=True)
                except Exception as e:
                    logger.error(f"Failed to process file: {e}")
        
        print()
        return results


# ============================================================================
# Data Parsing and Processing Module
# ============================================================================

class DataProcessor:
    """Data processor"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def parse_counts_file(self, file_path: Path) -> pd.Series:
        """Parse a single counts file"""
        try:
            df = pd.read_csv(file_path, sep='\t', comment='#', header=0)
            
            if 'gene_id' in df.columns and 'unstranded' in df.columns:
                df = df[['gene_id', 'unstranded']]
                df.columns = ['gene_id', 'count']
            elif df.shape[1] >= 2:
                df = df.iloc[:, :2]
                df.columns = ['gene_id', 'count']
            
            df = df[~df['gene_id'].str.startswith('__')]
            df = df[~df['gene_id'].str.startswith('N_')]
            
            df['gene_id'] = df['gene_id'].str.split('.').str[0]
            df = df.set_index('gene_id')
            return df['count']
            
        except Exception as e:
            logger.error(f"Failed to parse file {file_path}: {e}")
            return pd.Series()
    
    def build_count_matrix(self, file_paths: Dict[str, Path]) -> pd.DataFrame:
        """Build gene expression matrix"""
        workflow_tracker.add_step(
            "Build expression matrix",
            f"Building gene expression matrix from {len(file_paths)} sample files"
        )
        
        count_dict = {}
        for sample_id, path in file_paths.items():
            counts = self.parse_counts_file(path)
            if not counts.empty:
                count_dict[sample_id] = counts
        
        if not count_dict:
            raise ValueError("No files were successfully parsed")
        
        count_matrix = pd.DataFrame(count_dict)
        count_matrix = count_matrix.fillna(0).astype(int)
        
        workflow_tracker.add_step(
            "Expression matrix built",
            f"Matrix size: {count_matrix.shape[0]} genes x {count_matrix.shape[1]} samples",
            {"n_genes": count_matrix.shape[0], "n_samples": count_matrix.shape[1]}
        )
        
        return count_matrix
    
    def build_metadata(self, tumor_files: List[Dict], normal_files: List[Dict]) -> pd.DataFrame:
        """Build sample metadata"""
        metadata_list = []
        
        for f in tumor_files:
            sample_id = f"{f['case_id']}_{f['sample_type']}"
            metadata_list.append({
                'sample_id': sample_id,
                'case_id': f['case_id'],
                'condition': 'Tumor',
                'sample_type': f['sample_type']
            })
        
        for f in normal_files:
            sample_id = f"{f['case_id']}_{f['sample_type']}"
            metadata_list.append({
                'sample_id': sample_id,
                'case_id': f['case_id'],
                'condition': 'Normal',
                'sample_type': f['sample_type']
            })
        
        metadata = pd.DataFrame(metadata_list)
        metadata = metadata.set_index('sample_id')
        return metadata
    
    def filter_low_expression(self, count_matrix: pd.DataFrame) -> pd.DataFrame:
        """Filter low expression genes"""
        original_count = count_matrix.shape[0]
        mask = (count_matrix >= self.config.min_count_threshold).sum(axis=1) >= self.config.min_sample_with_counts
        filtered = count_matrix.loc[mask]
        
        workflow_tracker.add_step(
            "Filter low expression genes",
            f"Retained {filtered.shape[0]} genes (original {original_count})",
            {"before": original_count, "after": filtered.shape[0]}
        )
        
        return filtered
    
    def convert_gene_ids(self, gene_ids: List[str]) -> Dict[str, str]:
        """Convert ENSEMBL IDs to Gene Symbols"""
        workflow_tracker.add_step(
            "Gene ID conversion",
            f"Converting {len(gene_ids)} ENSEMBL IDs to Gene Symbols"
        )
        
        try:
            import mygene
            mg = mygene.MyGeneInfo()
            results = mg.querymany(gene_ids, scopes='ensembl.gene', fields='symbol', species='human')
            
            id_to_symbol = {}
            for r in results:
                query = r.get('query', '')
                symbol = r.get('symbol', query)
                id_to_symbol[query] = symbol if symbol else query
            
            return id_to_symbol
            
        except Exception as e:
            logger.warning(f"Gene ID conversion failed: {e}")
            return {g: g for g in gene_ids}


# ============================================================================
# Differential Expression Analysis Module
# ============================================================================

class DEGAnalyzer:
    """Differential expression analyzer"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def run_analysis(self, count_matrix: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
        """Run differential analysis, prefer PyDESeq2"""
        try:
            return self._run_pydeseq2(count_matrix, metadata)
        except ImportError:
            logger.warning("PyDESeq2 not installed, using simplified differential analysis")
            return self._run_simple_deg(count_matrix, metadata)
    
    def _run_pydeseq2(self, count_matrix: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
        """Run differential analysis using PyDESeq2"""
        workflow_tracker.add_step(
            "Run PyDESeq2 differential expression analysis",
            "Performing Tumor vs Normal differential expression analysis using PyDESeq2",
            {"method": "PyDESeq2", "contrast": ["Tumor", "Normal"]}
        )
        
        from pydeseq2.dds import DeseqDataSet
        from pydeseq2.ds import DeseqStats
        
        common_samples = count_matrix.columns.intersection(metadata.index)
        count_matrix = count_matrix[common_samples]
        metadata = metadata.loc[common_samples]
        
        counts_for_deseq = count_matrix.T
        
        dds = DeseqDataSet(
            counts=counts_for_deseq,
            metadata=metadata,
            design_factors="condition",
            refit_cooks=True,
            n_cpus=self.config.max_workers
        )
        
        dds.deseq2()
        
        stat_res = DeseqStats(dds, contrast=["condition", "Tumor", "Normal"], n_cpus=self.config.max_workers)
        stat_res.summary()
        
        results_df = stat_res.results_df.reset_index()
        results_df.columns = ['gene_id', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj']
        
        results_df['regulation'] = 'ns'
        up_mask = (results_df['padj'] < self.config.fdr_threshold) & (results_df['log2FoldChange'] > self.config.log2fc_threshold)
        down_mask = (results_df['padj'] < self.config.fdr_threshold) & (results_df['log2FoldChange'] < -self.config.log2fc_threshold)
        results_df.loc[up_mask, 'regulation'] = 'up'
        results_df.loc[down_mask, 'regulation'] = 'down'
        
        workflow_tracker.add_step(
            "Differential analysis complete",
            f"Upregulated genes: {up_mask.sum()}, Downregulated genes: {down_mask.sum()}",
            {"n_up": int(up_mask.sum()), "n_down": int(down_mask.sum()), "n_total": len(results_df)}
        )
        
        return results_df
    
    def _run_simple_deg(self, count_matrix: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
        """Simplified differential analysis (T-test)"""
        workflow_tracker.add_step(
            "Run simplified differential analysis",
            "Using t-test + Benjamini-Hochberg correction",
            {"method": "t-test", "correction": "BH"}
        )
        
        tumor_samples = [s for s in metadata[metadata['condition'] == 'Tumor'].index if s in count_matrix.columns]
        normal_samples = [s for s in metadata[metadata['condition'] == 'Normal'].index if s in count_matrix.columns]
        
        cpm = count_matrix * 1e6 / count_matrix.sum(axis=0)
        log_cpm = np.log2(cpm + 1)
        
        results = []
        for gene in log_cpm.index:
            tumor_expr = log_cpm.loc[gene, tumor_samples].values
            normal_expr = log_cpm.loc[gene, normal_samples].values
            
            log2fc = tumor_expr.mean() - normal_expr.mean()
            
            if len(tumor_expr) >= 2 and len(normal_expr) >= 2:
                _, pvalue = stats.ttest_ind(tumor_expr, normal_expr)
            else:
                pvalue = 1.0
            
            results.append({
                'gene_id': gene,
                'baseMean': cpm.loc[gene].mean(),
                'log2FoldChange': log2fc,
                'pvalue': pvalue if not np.isnan(pvalue) else 1.0
            })
        
        results_df = pd.DataFrame(results)
        
        pvals = results_df['pvalue'].values
        n = len(pvals)
        sorted_idx = np.argsort(pvals)
        adjusted = np.zeros(n)
        adjusted[sorted_idx[-1]] = pvals[sorted_idx[-1]]
        for i in range(n-2, -1, -1):
            adjusted[sorted_idx[i]] = min(adjusted[sorted_idx[i+1]], pvals[sorted_idx[i]] * n / (i + 1))
        results_df['padj'] = np.clip(adjusted, 0, 1)
        
        results_df['regulation'] = 'ns'
        up_mask = (results_df['padj'] < self.config.fdr_threshold) & (results_df['log2FoldChange'] > self.config.log2fc_threshold)
        down_mask = (results_df['padj'] < self.config.fdr_threshold) & (results_df['log2FoldChange'] < -self.config.log2fc_threshold)
        results_df.loc[up_mask, 'regulation'] = 'up'
        results_df.loc[down_mask, 'regulation'] = 'down'
        
        return results_df
    
    def get_normalized_counts(self, count_matrix: pd.DataFrame) -> pd.DataFrame:
        """Get normalized expression (log2 CPM)"""
        cpm = count_matrix * 1e6 / count_matrix.sum(axis=0)
        return np.log2(cpm + 1)


# ============================================================================
# Visualization Module - Publication Style (Blue + Red)
# ============================================================================

class Visualizer:
    """Visualization generator - Publication style"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Apply publication style
        setup_publication_style()
    
    def plot_combined_figure(self, normalized_counts: pd.DataFrame, metadata: pd.DataFrame,
                              deg_results: pd.DataFrame, gene_symbols: Dict[str, str],
                              boxplot_genes: List[str]) -> str:
        """
        Plot combined figure: A-Volcano, B-PCA, C-Heatmap, D-Boxplot
        """
        workflow_tracker.add_step(
            "Generate combined visualization",
            "Generating combined figure with volcano plot, PCA, heatmap, and boxplot (publication style)"
        )
        
        fig = plt.figure(figsize=(14, 12))
        
        gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30, 
                              left=0.08, right=0.95, top=0.95, bottom=0.08)
        
        # A: Volcano plot
        ax_a = fig.add_subplot(gs[0, 0])
        self._plot_volcano_subplot(ax_a, deg_results, gene_symbols)
        ax_a.text(-0.15, 1.08, 'A', transform=ax_a.transAxes, fontsize=18, 
                  fontweight='bold', va='top', ha='left')
        
        # B: PCA plot
        ax_b = fig.add_subplot(gs[0, 1])
        self._plot_pca_subplot(ax_b, normalized_counts, metadata)
        ax_b.text(-0.15, 1.08, 'B', transform=ax_b.transAxes, fontsize=18, 
                  fontweight='bold', va='top', ha='left')
        
        # C: Heatmap
        ax_c = fig.add_subplot(gs[1, 0])
        self._plot_heatmap_subplot(ax_c, normalized_counts, metadata, deg_results, gene_symbols)
        ax_c.text(-0.15, 1.08, 'C', transform=ax_c.transAxes, fontsize=18, 
                  fontweight='bold', va='top', ha='left')
        
        # D: Boxplot
        ax_d = fig.add_subplot(gs[1, 1])
        self._plot_boxplot_subplot(ax_d, normalized_counts, metadata, boxplot_genes, 
                                    deg_results, gene_symbols)
        ax_d.text(-0.15, 1.08, 'D', transform=ax_d.transAxes, fontsize=18, 
                  fontweight='bold', va='top', ha='left')
        
        output_path = self.output_dir / f"combined_figure_{self.config.cancer_type}.png"
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        plt.close()
        
        return str(output_path)
    
    def _plot_volcano_subplot(self, ax, deg_results: pd.DataFrame, gene_symbols: Dict[str, str]):
        """Volcano plot - Blue + Red style"""
        df = deg_results.copy()
        df['neg_log10_padj'] = -np.log10(df['padj'].clip(lower=1e-300))
        
        # Group by regulation
        ns_mask = df['regulation'] == 'ns'
        up_mask = df['regulation'] == 'up'
        down_mask = df['regulation'] == 'down'
        
        # Non-significant genes (light gray)
        ax.scatter(df.loc[ns_mask, 'log2FoldChange'], 
                   df.loc[ns_mask, 'neg_log10_padj'],
                   c=COLORS['ns'], alpha=0.5, s=20, edgecolors='none', label='NS')
        
        # Downregulated genes (blue)
        ax.scatter(df.loc[down_mask, 'log2FoldChange'], 
                   df.loc[down_mask, 'neg_log10_padj'],
                   c=COLORS['normal'], alpha=0.7, s=25, edgecolors='none', label='Down')
        
        # Upregulated genes (red)
        ax.scatter(df.loc[up_mask, 'log2FoldChange'], 
                   df.loc[up_mask, 'neg_log10_padj'],
                   c=COLORS['tumor'], alpha=0.7, s=25, edgecolors='none', label='Up')
        
        # Threshold lines (dashed)
        ax.axhline(-np.log10(self.config.fdr_threshold), color='#666666', 
                   linestyle='--', linewidth=0.8, alpha=0.6)
        ax.axvline(self.config.log2fc_threshold, color='#666666', 
                   linestyle='--', linewidth=0.8, alpha=0.6)
        ax.axvline(-self.config.log2fc_threshold, color='#666666', 
                   linestyle='--', linewidth=0.8, alpha=0.6)
        
        # Label top genes
        top_up = df[df['regulation'] == 'up'].nsmallest(5, 'padj')
        top_down = df[df['regulation'] == 'down'].nsmallest(5, 'padj')
        
        for _, row in pd.concat([top_up, top_down]).iterrows():
            gene_id = row['gene_id']
            symbol = gene_symbols.get(gene_id, gene_id)
            ax.annotate(symbol, (row['log2FoldChange'], row['neg_log10_padj']),
                        fontsize=8, fontstyle='italic', alpha=0.9,
                        xytext=(4, 4), textcoords='offset points')
        
        ax.set_xlabel('log₂(Fold Change)', fontweight='bold')
        ax.set_ylabel('-log₁₀(adjusted P-value)', fontweight='bold')
        ax.set_title('Volcano Plot', fontweight='bold', pad=10)
        
        # Statistics box
        n_up = up_mask.sum()
        n_down = down_mask.sum()
        stats_text = f'Up: {n_up}\nDown: {n_down}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='#CCCCCC', alpha=0.9))
        
        ax.legend(loc='upper right', frameon=False, fontsize=8)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    def _plot_pca_subplot(self, ax, normalized_counts: pd.DataFrame, metadata: pd.DataFrame):
        """PCA plot - Blue + Red style"""
        common_samples = [s for s in metadata.index if s in normalized_counts.columns]
        data = normalized_counts[common_samples].T
        
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled_data)
        
        # Plot scatter
        for condition, color in [('Normal', COLORS['normal']), ('Tumor', COLORS['tumor'])]:
            mask = metadata.loc[common_samples, 'condition'] == condition
            ax.scatter(pca_result[mask, 0], pca_result[mask, 1],
                       c=color, label=condition, alpha=0.8, s=60, 
                       edgecolors='white', linewidths=0.5)
        
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontweight='bold')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontweight='bold')
        ax.set_title('PCA Plot', fontweight='bold', pad=10)
        ax.legend(frameon=False, loc='best', fontsize=9)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    def _plot_heatmap_subplot(self, ax, normalized_counts: pd.DataFrame, metadata: pd.DataFrame,
                            deg_results: pd.DataFrame, gene_symbols: Dict[str, str], top_n: int = 25):
        """Heatmap - sorted by log2FC, upregulated and downregulated genes separated"""
        # Get upregulated and downregulated genes separately, sorted by padj
        up_genes = deg_results[deg_results['regulation'] == 'up'].nsmallest(top_n // 2, 'padj')
        down_genes = deg_results[deg_results['regulation'] == 'down'].nsmallest(top_n // 2, 'padj')
        
        # Sort by log2FC: downregulated (ascending) on top, upregulated (descending) on bottom
        down_genes = down_genes.sort_values('log2FoldChange', ascending=True)
        up_genes = up_genes.sort_values('log2FoldChange', ascending=False)
        
        # Merge gene list (downregulated on top, upregulated on bottom)
        sorted_genes = pd.concat([down_genes, up_genes])['gene_id'].tolist()
        
        if not sorted_genes:
            sorted_genes = deg_results.nsmallest(top_n, 'padj')['gene_id'].tolist()
        
        valid_genes = [g for g in sorted_genes if g in normalized_counts.index]
        if not valid_genes:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax.transAxes)
            return
        
        heatmap_data = normalized_counts.loc[valid_genes]
        
        # Sort samples (Normal first, Tumor second)
        common_samples = [s for s in metadata.index if s in heatmap_data.columns]
        sorted_samples = metadata.loc[common_samples].sort_values('condition').index.tolist()
        heatmap_data = heatmap_data[sorted_samples]
        
        # Z-score normalization
        heatmap_data = (heatmap_data.T - heatmap_data.mean(axis=1)) / heatmap_data.std(axis=1)
        heatmap_data = heatmap_data.T.clip(-2, 2)
        
        # Update gene names
        heatmap_data.index = [gene_symbols.get(g, g)[:12] for g in valid_genes]
        
        # Plot heatmap
        sns.heatmap(heatmap_data, ax=ax, cmap=DEG_HEATMAP_CMAP, center=0, 
                    vmin=-2, vmax=2,
                    xticklabels=False, yticklabels=True, 
                    cbar_kws={'shrink': 0.5, 'label': 'Z-score', 'aspect': 20})
        
        # Add separator line between upregulated and downregulated genes
        n_down = len([g for g in valid_genes if deg_results[deg_results['gene_id'] == g]['regulation'].values[0] == 'down'])
        if 0 < n_down < len(valid_genes):
            ax.axhline(y=n_down, color='black', linewidth=1.5, linestyle='-')
        
        # Add sample type color bar (top)
        sample_colors = [COLORS['normal'] if metadata.loc[s, 'condition'] == 'Normal' 
                        else COLORS['tumor'] for s in sorted_samples]
        
        for i, color in enumerate(sample_colors):
            ax.add_patch(plt.Rectangle((i, len(valid_genes)), 1, 0.8, 
                                        facecolor=color, edgecolor='none', 
                                        clip_on=False, transform=ax.transData))
        
        ax.set_ylabel('', fontsize=10)
        ax.set_xlabel('Samples', fontweight='bold', labelpad=15)
        ax.set_title(f'Top DEGs Heatmap (n={len(valid_genes)})', fontweight='bold', pad=15)
        ax.tick_params(axis='y', labelsize=7)
        
        # Legend
        legend_elements = [Patch(facecolor=COLORS['normal'], label='Normal'),
                        Patch(facecolor=COLORS['tumor'], label='Tumor')]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=8, 
                bbox_to_anchor=(1.0, 1.0), frameon=False)

    def _plot_boxplot_subplot(self, ax, normalized_counts: pd.DataFrame, metadata: pd.DataFrame,
                            genes: List[str], deg_results: pd.DataFrame, gene_symbols: Dict[str, str]):
        """Boxplot with scatter overlay - Blue + Red style"""
        valid_genes = [g for g in genes if g in normalized_counts.index][:8]
        
        if not valid_genes:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax.transAxes)
            return
        
        # Prepare data
        plot_data = []
        for gene in valid_genes:
            for sample_id in normalized_counts.columns:
                if sample_id in metadata.index:
                    condition = metadata.loc[sample_id, 'condition']
                    expr = normalized_counts.loc[gene, sample_id]
                    symbol = gene_symbols.get(gene, gene)
                    plot_data.append({
                        'Gene': symbol[:10],
                        'Expression': expr,
                        'Condition': condition,
                        'gene_id': gene
                    })
        
        plot_df = pd.DataFrame(plot_data)
        
        # Calculate significance
        significance = {}
        for gene in valid_genes:
            gene_data = plot_df[plot_df['gene_id'] == gene]
            tumor_expr = gene_data[gene_data['Condition'] == 'Tumor']['Expression']
            normal_expr = gene_data[gene_data['Condition'] == 'Normal']['Expression']
            
            if len(tumor_expr) >= 2 and len(normal_expr) >= 2:
                _, pval = stats.ttest_ind(tumor_expr, normal_expr)
                if pval < 0.001: significance[gene] = '***'
                elif pval < 0.01: significance[gene] = '**'
                elif pval < 0.05: significance[gene] = '*'
                else: significance[gene] = 'ns'
            else:
                significance[gene] = 'ns'
        
        gene_order = [gene_symbols.get(g, g)[:10] for g in valid_genes]
        palette = {'Normal': COLORS['normal'], 'Tumor': COLORS['tumor']}
        
        # Plot boxplot
        sns.boxplot(
            data=plot_df, x='Gene', y='Expression', hue='Condition',
            order=gene_order, hue_order=['Normal', 'Tumor'],
            palette=palette, ax=ax, width=0.6, linewidth=1.2,
            fliersize=0  # Hide outliers
        )
        
        # Overlay scatter points
        sns.stripplot(
            data=plot_df, x='Gene', y='Expression', hue='Condition',
            order=gene_order, hue_order=['Normal', 'Tumor'],
            palette=palette, ax=ax, size=4, alpha=0.6,
            dodge=True, jitter=0.15, legend=False
        )
        
        # Annotate significance
        for i, gene in enumerate(valid_genes):
            sig = significance[gene]
            gene_name = gene_symbols.get(gene, gene)[:10]
            gene_expr = plot_df[plot_df['Gene'] == gene_name]['Expression']
            y_max = gene_expr.max()
            y_range = gene_expr.max() - gene_expr.min()
            
            if sig != 'ns':
                ax.text(i, y_max + y_range * 0.1, sig, ha='center', va='bottom', 
                        fontsize=10, fontweight='bold')
        
        ax.set_xlabel('')
        ax.set_ylabel('Expression (log₂ CPM)', fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=9,
                        fontstyle='italic')
        ax.set_title('Gene Expression', fontweight='bold', pad=10)
        
        # Legend
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[:2], labels[:2], title='', loc='upper right', 
                frameon=False, fontsize=9)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


# ============================================================================
# TCGA DEG Analysis Core Logic
# ============================================================================

class TCGADEGAnalyzer:
    """TCGA differential expression analyzer"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.fetcher = GDCDataFetcher(config)
        self.processor = DataProcessor(config)
        self.analyzer = DEGAnalyzer(config)
        self.visualizer = Visualizer(config)
    
    def run(self) -> Dict[str, Any]:
        """Execute complete differential expression analysis workflow (real data mode)"""
        start_time = datetime.now()
        
        # 1. Get file list
        tumor_files, normal_files = self.fetcher.get_file_uuids()
        
        if len(tumor_files) < self.config.min_samples:
            raise ValueError(f"Insufficient Tumor samples ({len(tumor_files)} < {self.config.min_samples})")
        if len(normal_files) < self.config.min_samples:
            raise ValueError(f"Insufficient Normal samples ({len(normal_files)} < {self.config.min_samples})")
        
        # 2. Download data
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            tumor_paths = self.fetcher.download_files_parallel(tumor_files, tmpdir, "Tumor")
            normal_paths = self.fetcher.download_files_parallel(normal_files, tmpdir, "Normal")
            
            all_paths = {**tumor_paths, **normal_paths}
            
            if not all_paths:
                raise ValueError("No files were successfully downloaded")
            
            # 3. Build data matrix
            count_matrix = self.processor.build_count_matrix(all_paths)
            metadata = self.processor.build_metadata(tumor_files, normal_files)
            
            common_samples = list(set(count_matrix.columns) & set(metadata.index))
            count_matrix = count_matrix[common_samples]
            metadata = metadata.loc[common_samples]
            
            # 4. Filter low expression genes
            count_matrix = self.processor.filter_low_expression(count_matrix)
            
            # 5. Run differential analysis
            deg_results = self.analyzer.run_analysis(count_matrix, metadata)
            
            # 6. Gene ID conversion
            gene_ids = deg_results['gene_id'].tolist()
            gene_symbols = self.processor.convert_gene_ids(gene_ids)
            deg_results['gene_symbol'] = deg_results['gene_id'].map(gene_symbols)
            
            # 7. Get normalized expression
            normalized_counts = self.analyzer.get_normalized_counts(count_matrix)
            
            workflow_tracker.add_step(
                "Generate visualization",
                "Generating combined figure (volcano plot, heatmap, PCA, boxplot) - publication style"
            )
            
            # 8. Generate visualization           
            figures = {}
            
            # Get top significant DEGs
            top_deg_genes = deg_results.nsmallest(12, 'padj')['gene_id'].tolist()
            
            # Get user-specified genes
            target_genes = []
            if self.config.genes:
                symbol_to_id = {v: k for k, v in gene_symbols.items()}
                for g in self.config.genes:
                    if g in symbol_to_id:
                        target_genes.append(symbol_to_id[g])
                    elif g in gene_symbols:
                        target_genes.append(g)
            
            # Combined list
            combined_genes = list(dict.fromkeys(target_genes + top_deg_genes))
            boxplot_genes = combined_genes[:20]
            
            # Generate combined figure
            combined_path = self.visualizer.plot_combined_figure(
                normalized_counts, metadata, deg_results, gene_symbols, boxplot_genes
            )
            if combined_path:
                figures['combined'] = combined_path
            
        # 9. Prepare output
        end_time = datetime.now()
        
        target_gene_results = []
        if self.config.genes:
            for gene in self.config.genes:
                gene_row = deg_results[deg_results['gene_symbol'] == gene]
                if not gene_row.empty:
                    row = gene_row.iloc[0]
                    target_gene_results.append({
                        "gene_symbol": gene,
                        "log2FoldChange": round(row['log2FoldChange'], 3),
                        "padj": f"{row['padj']:.2e}",
                        "regulation": row['regulation']
                    })
        
        top_up_genes = deg_results[deg_results['regulation'] == 'up'].nsmallest(10, 'padj')
        top_down_genes = deg_results[deg_results['regulation'] == 'down'].nsmallest(10, 'padj')
        
        meta_info = {
            'cancer_type': self.config.cancer_type,
            'analysis_date': start_time.isoformat(),
            'duration_seconds': (end_time - start_time).total_seconds(),
            'n_tumor_samples': len(tumor_files),
            'n_normal_samples': len(normal_files),
            'n_genes_analyzed': len(deg_results),
            'n_deg_up': int((deg_results['regulation'] == 'up').sum()),
            'n_deg_down': int((deg_results['regulation'] == 'down').sum()),
            'fdr_threshold': self.config.fdr_threshold,
            'log2fc_threshold': self.config.log2fc_threshold,
            'visualization_style': 'publication (blue + red)'
        }
        
        # Save CSV results
        output_dir = Path(self.config.output_dir)
        deg_output = deg_results[['gene_id', 'gene_symbol', 'baseMean', 'log2FoldChange', 'pvalue', 'padj', 'regulation']]
        deg_output.to_csv(output_dir / f"deg_results_{self.config.cancer_type}.csv", index=False)
        
        with open(output_dir / f"meta_info_{self.config.cancer_type}.json", 'w') as f:
            json.dump(meta_info, f, indent=2)
        
        return {
            'meta_info': meta_info,
            'figures': figures,
            'target_gene_results': target_gene_results,
            'top_upregulated': [
                {"gene": row['gene_symbol'], "log2FC": round(row['log2FoldChange'], 2), "padj": f"{row['padj']:.2e}"}
                for _, row in top_up_genes.iterrows()
            ],
            'top_downregulated': [
                {"gene": row['gene_symbol'], "log2FC": round(row['log2FoldChange'], 2), "padj": f"{row['padj']:.2e}"}
                for _, row in top_down_genes.iterrows()
            ],
            'status': 'success'
        }
