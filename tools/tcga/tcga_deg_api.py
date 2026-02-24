"""
TCGA Differential Expression Analysis API
==========================================
Complete API wrapper for Agent analysis workflow: Query -> LLM parsing -> Analysis -> Visualization -> Summary
"""

import base64
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


# ==================== Configuration ====================

@dataclass
class APIConfig:
    """API configuration"""
    # LLM config
    llm_api_key: str = ""
    llm_api_base: str = "https://api.openai-proxy.org/v1"
    llm_model: str = "gpt-4.1"
    llm_temperature: float = 0.1
    
    # Data fetching config
    cache_enabled: bool = True
    
    # Analysis default parameters
    default_max_samples: int = 15
    default_fdr_threshold: float = 0.05
    default_log2fc_threshold: float = 1.0
    
    # Output config
    output_dir: str = "./output"


# ==================== Result Data Classes ====================

@dataclass
class AnalysisStepLog:
    """Analysis step log"""
    step_number: int
    name: str
    description: str
    timestamp: str
    details: Any = None


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    # Basic info
    status: str  # "success" / "error"
    query: str   # Original query
    
    # LLM parsed parameters
    parsed_params: Dict[str, Any] = field(default_factory=dict)
    
    # Analysis statistics
    cancer_type: str = ""
    n_tumor_samples: int = 0
    n_normal_samples: int = 0
    n_genes_analyzed: int = 0
    n_upregulated: int = 0
    n_downregulated: int = 0
    
    # Gene results
    target_gene_results: List[Dict] = field(default_factory=list)
    top_upregulated: List[Dict] = field(default_factory=list)
    top_downregulated: List[Dict] = field(default_factory=list)
    
    # Figures (base64)
    figures: Dict[str, Dict] = field(default_factory=dict)
    
    # LLM generated summary
    summary: str = ""
    
    # Workflow log
    workflow_steps: List[Dict] = field(default_factory=list)
    
    # Meta info
    duration_seconds: float = 0.0
    timestamp: str = ""
    error_message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON serializable dictionary"""
        return {
            "status": self.status,
            "query": self.query,
            "parsed_params": self.parsed_params,
            "analysis_summary": {
                "cancer_type": self.cancer_type,
                "n_tumor_samples": self.n_tumor_samples,
                "n_normal_samples": self.n_normal_samples,
                "n_genes_analyzed": self.n_genes_analyzed,
                "n_upregulated": self.n_upregulated,
                "n_downregulated": self.n_downregulated,
            },
            "results": {
                "target_genes": self.target_gene_results,
                "top_upregulated": self.top_upregulated,
                "top_downregulated": self.top_downregulated,
            },
            "figures": self.figures,
            "llm_summary": self.summary,
            "workflow_steps": self.workflow_steps,
            "meta": {
                "duration_seconds": self.duration_seconds,
                "timestamp": self.timestamp,
            },
            "error": self.error_message if self.status == "error" else None
        }


# ==================== Core API Class ====================

class TCGA_DEG_API:
    """
    TCGA Differential Expression Analysis API
    
    Complete analysis workflow:
    1. LLM parses user query to extract cancer type and genes
    2. Download real data from GDC API
    3. PyDESeq2 differential analysis
    4. Generate publication-quality visualizations
    5. LLM generates result summary
    6. Return structured results (with base64 figures)
    """
    
    def __init__(self, config: Optional[APIConfig] = None):
        """
        Initialize API
        
        Args:
            config: API configuration, None uses default config
        """
        self.config = config or APIConfig()
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize LLM
        self._llm = None
        
        # Lazy load analysis module
        self._analyse_module = None
    
    @property
    def llm(self):
        """Lazy initialize LLM"""
        if self._llm is None:
            self._llm = ChatOpenAI(
                model=self.config.llm_model,
                api_key=self.config.llm_api_key,
                base_url=self.config.llm_api_base,
                temperature=self.config.llm_temperature
            )
        return self._llm
    
    def _get_analyse_module(self):
        """Lazy load analysis module"""
        if self._analyse_module is None:
            from tools.tcga import tcga_analyse
            self._analyse_module = tcga_analyse
        return self._analyse_module
    
    # ==================== Main Entry ====================
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Execute complete analysis workflow
        
        Args:
            query: Natural language query, e.g., "Analyze TP53 and EGFR expression in lung adenocarcinoma"
            
        Returns:
            Complete analysis result dictionary containing:
            - status: Status
            - parsed_params: LLM parsed parameters
            - analysis_summary: Analysis statistics
            - results: Gene results
            - figures: Base64 encoded figures
            - llm_summary: LLM generated summary
            - workflow_steps: Analysis step logs
        """
        start_time = datetime.now()
        workflow_steps = []
        
        result = AnalysisResult(
            status="running",
            query=query,
            timestamp=start_time.isoformat()
        )
        
        try:
            # Step 1: LLM parse user intent
            workflow_steps.append(self._log_step(1, "Parse user intent", "Using LLM to extract analysis parameters from query"))
            params = self._parse_query(query)
            result.parsed_params = params
            workflow_steps.append(self._log_step(2, "Parameter extraction complete", f"Cancer type: {params.get('cancer_type')}, Genes: {params.get('genes')}"))
            
            # Step 2: Execute analysis
            workflow_steps.append(self._log_step(3, "Start differential analysis", "Downloading data and executing PyDESeq2 analysis"))
            raw_result, analysis_steps = self._run_analysis(params)
            workflow_steps.extend(analysis_steps)
            
            # Step 3: Process results
            workflow_steps.append(self._log_step(len(workflow_steps) + 1, "Process analysis results", "Organizing statistics and gene results"))
            self._populate_result(result, raw_result)
            
            # Step 4: Convert figures to base64
            workflow_steps.append(self._log_step(len(workflow_steps) + 1, "Process visualization figures", "Converting figures to base64 format"))
            result.figures = self._convert_figures(raw_result.get('figures', {}))
            
            # Step 5: Generate summary
            workflow_steps.append(self._log_step(len(workflow_steps) + 1, "Generate analysis summary", "Using LLM to generate professional summary"))
            result.summary = self._generate_summary(query, raw_result)
            
            result.status = "success"
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            result.status = "error"
            result.error_message = str(e)
            workflow_steps.append(self._log_step(len(workflow_steps) + 1, "Error", str(e)))
        
        # Complete
        result.duration_seconds = (datetime.now() - start_time).total_seconds()
        result.workflow_steps = workflow_steps
        
        return result.to_dict()
    
    # ==================== Internal Methods ====================
    
    def _log_step(self, num: int, name: str, desc: str, details: Any = None) -> Dict:
        """Log step"""
        step = {
            "step": num,
            "name": name,
            "description": desc,
            "timestamp": datetime.now().isoformat(),
        }
        if details:
            step["details"] = details
        logger.info(f"[Step {num}] {name}: {desc}")
        return step
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """Use LLM to parse user query"""
        system_prompt = """You are a bioinformatics analysis assistant. Please extract the following parameters from the user's question:

1. cancer_type: TCGA project ID, format "TCGA-XXX", common types:
   - TCGA-LUAD: Lung Adenocarcinoma
   - TCGA-LUSC: Lung Squamous Cell Carcinoma
   - TCGA-BRCA: Breast Cancer
   - TCGA-COAD: Colon Cancer
   - TCGA-LIHC: Liver Cancer
   - TCGA-STAD: Stomach Cancer
   - TCGA-KIRC: Kidney Clear Cell Carcinoma
   - TCGA-PRAD: Prostate Cancer
   - TCGA-THCA: Thyroid Cancer
   
2. genes: List of gene symbols mentioned by user (e.g., TP53, EGFR, KRAS, BRCA1)

3. max_samples: Number of samples per group, default 15

Please return strictly in JSON format, no other content:
{"cancer_type": "TCGA-XXX", "genes": ["GENE1", "GENE2"], "max_samples": 15}

If the user hasn't specified a cancer type, infer the most likely type from context.
If the user hasn't specified genes, set genes to null."""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ])
            
            content = response.content.strip()
            # Clean markdown code blocks
            content = content.replace("```json", "").replace("```", "").strip()
            
            params = json.loads(content)
            
            # Validate and set defaults
            if not params.get("cancer_type"):
                params["cancer_type"] = "TCGA-LUAD"
            if not params.get("max_samples"):
                params["max_samples"] = self.config.default_max_samples
                
            return params
            
        except Exception as e:
            logger.warning(f"LLM parsing failed, using defaults: {e}")
            return {
                "cancer_type": "TCGA-LUAD",
                "genes": None,
                "max_samples": self.config.default_max_samples
            }
    
    def _run_analysis(self, params: Dict) -> tuple:
        """Execute actual analysis"""
        tcga_analyse = self._get_analyse_module()
        
        # Build config
        config = tcga_analyse.AnalysisConfig(
            cancer_type=params["cancer_type"],
            genes=params.get("genes"),
            output_dir=str(self.output_dir),
            fdr_threshold=self.config.default_fdr_threshold,
            log2fc_threshold=self.config.default_log2fc_threshold,
            max_samples_per_group=params.get("max_samples", self.config.default_max_samples),
            use_cache=self.config.cache_enabled
        )
        
        # Reset workflow_tracker
        tcga_analyse.workflow_tracker = tcga_analyse.WorkflowTracker()
        tcga_analyse.workflow_tracker.set_question(params.get("query", ""))
        
        # Execute analysis
        analyzer = tcga_analyse.TCGADEGAnalyzer(config)
        result = analyzer.run()
        
        # Get analysis steps
        analysis_steps = [
            {
                "step": s["step_number"] + 10,  # Offset to avoid conflicts
                "name": s["name"],
                "description": s["description"],
                "timestamp": s["timestamp"]
            }
            for s in tcga_analyse.workflow_tracker.steps
        ]
        
        return result, analysis_steps
    
    def _populate_result(self, result: AnalysisResult, raw_result: Dict):
        """Populate result object"""
        meta = raw_result.get('meta_info', {})
        
        result.cancer_type = meta.get('cancer_type', '')
        result.n_tumor_samples = meta.get('n_tumor_samples', 0)
        result.n_normal_samples = meta.get('n_normal_samples', 0)
        result.n_genes_analyzed = meta.get('n_genes_analyzed', 0)
        result.n_upregulated = meta.get('n_deg_up', 0)
        result.n_downregulated = meta.get('n_deg_down', 0)
        
        result.target_gene_results = raw_result.get('target_gene_results', [])
        result.top_upregulated = raw_result.get('top_upregulated', [])
        result.top_downregulated = raw_result.get('top_downregulated', [])
    
    def _convert_figures(self, figures: Dict[str, str]) -> Dict[str, Dict]:
        """Convert figures to base64"""
        result = {}
        
        for name, path in figures.items():
            if path and Path(path).exists():
                try:
                    with open(path, 'rb') as f:
                        image_data = f.read()
                    
                    suffix = Path(path).suffix.lower()
                    mime_type = {
                        '.png': 'image/png',
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.svg': 'image/svg+xml',
                        '.pdf': 'application/pdf'
                    }.get(suffix, 'image/png')
                    
                    result[name] = {
                        "filename": Path(path).name,
                        "mime_type": mime_type,
                        "base64": base64.b64encode(image_data).decode('utf-8'),
                        "size_bytes": len(image_data)
                    }
                except Exception as e:
                    logger.warning(f"Figure conversion failed {path}: {e}")
                    result[name] = {"error": str(e)}
            else:
                result[name] = {"error": "file_not_found", "path": str(path)}
        
        return result
    
    def _generate_summary(self, query: str, raw_result: Dict) -> str:
        """Use LLM to generate analysis summary"""
        summary_data = {
            "meta": raw_result.get('meta_info'),
            "target_genes": raw_result.get('target_gene_results'),
            "top_up": raw_result.get('top_upregulated', [])[:5],
            "top_down": raw_result.get('top_downregulated', [])[:5]
        }
        
        system_prompt = """You are a professional bioinformatics analyst. Please generate a professional summary report based on the TCGA differential expression analysis results.

The report should include:
1. **Analysis Overview**: Cancer type, sample size, analysis method
2. **Key Findings**: Number of DEGs, top upregulated/downregulated genes
3. **Target Gene Analysis**: If user specified genes, describe their expression changes in detail
4. **Biological Significance**: Brief explanation of potential biological implications

Please use professional but accessible language, suitable for researchers to read."""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"User query: {query}\n\nAnalysis data:\n{json.dumps(summary_data, ensure_ascii=False, indent=2)}")
            ])
            return response.content
        except Exception as e:
            logger.warning(f"Summary generation failed: {e}")
            return f"Summary generation failed: {e}"
    
    # ==================== Helper Methods ====================
    
    def get_supported_cancer_types(self) -> List[Dict[str, str]]:
        """Get supported cancer types"""
        return [
            {"id": "TCGA-LUAD", "name": "Lung Adenocarcinoma"},
            {"id": "TCGA-LUSC", "name": "Lung Squamous Cell Carcinoma"},
            {"id": "TCGA-BRCA", "name": "Breast Invasive Carcinoma"},
            {"id": "TCGA-COAD", "name": "Colon Adenocarcinoma"},
            {"id": "TCGA-READ", "name": "Rectum Adenocarcinoma"},
            {"id": "TCGA-LIHC", "name": "Liver Hepatocellular Carcinoma"},
            {"id": "TCGA-STAD", "name": "Stomach Adenocarcinoma"},
            {"id": "TCGA-KIRC", "name": "Kidney Renal Clear Cell Carcinoma"},
            {"id": "TCGA-PRAD", "name": "Prostate Adenocarcinoma"},
            {"id": "TCGA-THCA", "name": "Thyroid Carcinoma"},
        ]


# ==================== Convenience Functions ====================

_api_instance: Optional[TCGA_DEG_API] = None


def get_api(config: Optional[APIConfig] = None) -> TCGA_DEG_API:
    """Get API singleton"""
    global _api_instance
    if _api_instance is None:
        _api_instance = TCGA_DEG_API(config)
    return _api_instance


def analyze(query: str) -> Dict[str, Any]:
    """Quick analysis function"""
    return get_api().run(query)
