import pandas as pd
import numpy as np
import json
import os
from pathlib import Path


class DepMapAPI:
    """
    DepMap Cancer Cell Line Analysis API

    Provides comprehensive analysis of:
    - Gene dependency (CRISPR knockout effects)
    - Gene expression (RNA-seq)
    - Gene mutations
    across different cancer types
    """

    def __init__(self, data_dir=None):
        """
        Initialize DepMap API with data files.

        Args:
            data_dir: Directory containing DepMap data files. If None, uses default location.
        """
        if data_dir is None:
            # Try to find data directory
            data_dir = Path(__file__).parent / "data"
            if not data_dir.exists():
                data_dir = Path.cwd()

        self.data_dir = Path(data_dir)
        print(f"Initializing DepMap API from: {self.data_dir}")

        try:
            # 1. load metadata (Model.csv)
            model_path = self.data_dir / "Model.csv"
            df_model = pd.read_csv(model_path)
            self.meta_map = df_model.set_index("ModelID")["OncotreeLineage"].to_dict()
            self.name_map = (
                df_model.set_index("ModelID")["StrippedCellLineName"]
                .fillna(df_model["ModelID"])
                .to_dict()
            )

            # 2. load summary statistics
            stats_path = self.data_dir / "analysis_results" / "full_stats.json"
            with open(stats_path, "r") as f:
                self.stats = json.load(f)

            # 3. load detailed matrix
            print("  -> Loading Effect Matrix...")
            self.df_effect = pd.read_csv(
                self.data_dir / "clean_crispr_effect.csv", index_col=0
            )
            self.df_effect["CancerType"] = self.df_effect.index.map(self.meta_map)

            print("  -> Loading Expression Matrix...")
            self.df_expr = pd.read_csv(
                self.data_dir / "clean_expression.csv", index_col=0
            )
            self.df_expr["CancerType"] = self.df_expr.index.map(self.meta_map)

            print("  -> Loading Mutation Table...")
            self.df_mut = pd.read_csv(
                self.data_dir / "clean_mutation.csv", low_memory=False
            )
            self.df_mut["CancerType"] = self.df_mut["ModelID"].map(self.meta_map)

            print("DepMap API Ready.")
            self.initialized = True

        except Exception as e:
            print(f"Error initializing DepMap API: {e}")
            self.initialized = False
            raise

    def _get_cell_name(self, model_id):
        """helper function: convert ACH-xxx to cell line name"""
        return self.name_map.get(model_id, model_id)

    def _get_stats(self, gene, cancer_type, category):
        try:
            return self.stats[gene][cancer_type].get(category, {})
        except KeyError:
            return {}

    def get_dependency(self, gene: str, cancer_type: str) -> dict:
        """
        Analyze gene dependency in specific cancer type.

        Args:
            gene: Gene symbol (e.g., "ERBB2", "KRAS")
            cancer_type: Cancer type (e.g., "Breast", "Pancreas")

        Returns:
            Dictionary containing:
            - success: bool
            - gene: str
            - cancer_type: str
            - dependency_analysis: dict with scores, stats, top sensitive lines, conclusion
        """
        try:
            s = self._get_stats(gene, cancer_type, "effect")
            s_prob = self._get_stats(gene, cancer_type, "prob")

            if not s:
                return {
                    "success": False,
                    "error": f"No dependency data for {gene} in {cancer_type}",
                }

            score = s.get("score", 0)
            prob = s_prob if isinstance(s_prob, (int, float)) else 0
            kill_ratio = s.get("kill_ratio", 0)

            result = {
                "success": True,
                "gene": gene,
                "cancer_type": cancer_type,
                "dependency_analysis": {
                    "chronos_score_mean": float(score),
                    "probability_mean": float(prob),
                    "lethal_ratio": float(kill_ratio),
                    "top_5_sensitive_lines": [],
                    "conclusion": "",
                },
            }

            subset = self.df_effect[self.df_effect["CancerType"] == cancer_type]
            if gene in subset.columns:
                top = subset[gene].sort_values(ascending=True).head(5)
                result["dependency_analysis"]["top_5_sensitive_lines"] = [
                    {
                        "cell_line": self._get_cell_name(cell_id),
                        "model_id": cell_id,
                        "chronos_score": float(val),
                    }
                    for cell_id, val in top.items()
                ]

                # Generate conclusion
                conclusion = self._generate_dep_conclusion(
                    gene, cancer_type, score, prob, subset
                )

                # Add driver analysis
                driver_conclusion = self._analyze_driver_potential(
                    gene, cancer_type, subset
                )
                if driver_conclusion:
                    conclusion += " " + driver_conclusion

                result["dependency_analysis"]["conclusion"] = conclusion

            return result

        except Exception as e:
            return {"success": False, "error": f"Error analyzing dependency: {str(e)}"}

    def _generate_dep_conclusion(self, gene, cancer_type, score, prob, subset_effect):
        """generate dependency analysis conclusion"""
        sentence_parts = []

        # intensity judgment
        intensity = ""
        if score < -0.7:
            intensity = "a strong, core essential"
        elif score < -0.5:
            intensity = "a significant"
        elif score < -0.3:
            intensity = "a moderate"
        else:
            intensity = "a weak or non-essential"

        sentence_parts.append(
            f"{gene} is identified as {intensity} dependency gene in {cancer_type} cancer cell lines"
        )

        # add detailed statistical information
        if gene in subset_effect.columns:
            effect_values = subset_effect[gene].dropna()
            std_val = effect_values.std()
            min_val = effect_values.min()
            # calculate the proportion of highly sensitive cell lines (Chronos score < -0.5)
            sensitive_ratio = (effect_values < -0.5).sum() / len(effect_values) * 100

            sentence_parts.append(
                f" (Mean: {score:.2f}, Std: {std_val:.2f}). "
                f"Dependency effect ranges from {min_val:.2f} to {effect_values.max():.2f}, "
                f"with {sensitive_ratio:.1f}% of cell lines showing strong sensitivity (score < -0.5)"
            )

        # confidence supplement
        if prob > 0.7:
            sentence_parts.append(", supported by high confidence probability data")
        elif prob < 0.3 and score > -0.3:
            sentence_parts.append(", consistent with low dependency probability")

        return "".join(sentence_parts) + "."

    def _analyze_driver_potential(self, gene, cancer_type, subset_effect):
        """compare the difference in dependency between mutant and wild-type"""
        try:
            mut_subset = self.df_mut[
                (self.df_mut["HugoSymbol"] == gene)
                & (self.df_mut["CancerType"] == cancer_type)
            ]
            mutated_cell_ids = set(mut_subset["ModelID"].unique())

            all_cells = subset_effect.index
            mut_group = [c for c in all_cells if c in mutated_cell_ids]
            wt_group = [c for c in all_cells if c not in mutated_cell_ids]

            if len(mut_group) < 2 or len(wt_group) < 2:
                return ""

            mut_mean = subset_effect.loc[mut_group, gene].mean()
            wt_mean = subset_effect.loc[wt_group, gene].mean()
            diff = mut_mean - wt_mean

            if diff < -0.3:
                return (
                    f"Moreover, {gene}-mutant cell lines show significantly higher dependency compared to wild-type "
                    f"(Diff: {diff:.2f}), suggesting that {gene} is a driver dependency (Oncogene Addiction) in {cancer_type}."
                )
            elif diff > 0.3:
                return f"However, mutant cells appear less dependent than wild-type cells (Diff: +{diff:.2f})."
            else:
                return f"Dependency levels do not show a significant difference between {gene}-mutant and wild-type cells."
        except:
            return ""

    def get_expression(self, gene: str, cancer_type: str) -> dict:
        """
        Analyze gene expression in specific cancer type.

        Args:
            gene: Gene symbol
            cancer_type: Cancer type

        Returns:
            Dictionary with expression statistics, top expressing lines, conclusion
        """
        try:
            s = self._get_stats(gene, cancer_type, "expr")
            if not s:
                return {
                    "success": False,
                    "error": f"No expression data for {gene} in {cancer_type}",
                }

            mean_val = s.get("mean", 0)
            median_val = s.get("median", 0)

            result = {
                "success": True,
                "gene": gene,
                "cancer_type": cancer_type,
                "expression_analysis": {
                    "mean": float(mean_val),
                    "median": float(median_val),
                    "expression_level": "",
                    "top_5_high_expression": [],
                    "conclusion": "",
                },
            }

            # judge the expression level
            level = ""
            if mean_val > 6:
                level = "high"
            elif mean_val < 1:
                level = "low"
            else:
                level = "moderate"

            result["expression_analysis"]["expression_level"] = level

            subset = self.df_expr[self.df_expr["CancerType"] == cancer_type]
            if gene in subset.columns:
                top = subset[gene].sort_values(ascending=False).head(5)
                result["expression_analysis"]["top_5_high_expression"] = [
                    {
                        "cell_line": self._get_cell_name(cell_id),
                        "model_id": cell_id,
                        "expression": float(val),
                    }
                    for cell_id, val in top.items()
                ]

                # Generate detailed conclusion
                expr_values = subset[gene].dropna()
                std_val = expr_values.std()
                max_val = expr_values.max()
                detection_rate = (expr_values > 0).sum() / len(expr_values) * 100

                conclusion = (
                    f"{gene} is ubiquitously expressed (detectable in {detection_rate:.1f}% of lines) "
                    f"at a **{level} level** (Mean: {mean_val:.2f}). "
                    f"Expression varies with a Std of {std_val:.2f}, peaking at {max_val:.2f} logTPM."
                )

                result["expression_analysis"]["conclusion"] = conclusion

            return result

        except Exception as e:
            return {"success": False, "error": f"Error analyzing expression: {str(e)}"}

    def get_mutation(self, gene: str, cancer_type: str) -> dict:
        """
        Analyze gene mutations in specific cancer type.

        Args:
            gene: Gene symbol
            cancer_type: Cancer type

        Returns:
            Dictionary with mutation frequency, types, hotspots, conclusion
        """
        try:
            s = self._get_stats(gene, cancer_type, "mut")
            count = s.get("count", 0)

            # dynamically calculate the denominator
            subset_cancer = self.df_effect[self.df_effect["CancerType"] == cancer_type]
            total = len(subset_cancer)
            if total == 0:
                total = 1
            freq = count / total

            result = {
                "success": True,
                "gene": gene,
                "cancer_type": cancer_type,
                "mutation_analysis": {
                    "frequency": float(freq),
                    "mutated_count": int(count),
                    "total_cell_lines": int(total),
                    "frequency_category": "",
                    "variant_types": [],
                    "hotspots": [],
                    "conclusion": "",
                },
            }

            # frequency classification
            freq_desc = ""
            if freq > 0.3:
                freq_desc = "frequently mutated driver gene"
            elif freq > 0.05:
                freq_desc = "recurrently mutated gene"
            elif freq > 0:
                freq_desc = "rarely mutated gene"
            else:
                freq_desc = "gene with no detected mutations"

            result["mutation_analysis"]["frequency_category"] = freq_desc

            if count > 0:
                subset = self.df_mut[
                    (self.df_mut["HugoSymbol"] == gene)
                    & (self.df_mut["CancerType"] == cancer_type)
                ]

                col_type = (
                    "VariantInfo"
                    if "VariantInfo" in subset.columns
                    else "Variant_Classification"
                )
                col_prot = (
                    "ProteinChange"
                    if "ProteinChange" in subset.columns
                    else "Protein_Change"
                )

                # mutation type statistics
                if col_type in subset.columns:
                    types = subset[col_type].value_counts().head(3)
                    result["mutation_analysis"]["variant_types"] = [
                        {"type": str(idx), "count": int(val)}
                        for idx, val in types.items()
                    ]

                # Hotspot statistics
                if col_prot in subset.columns:
                    changes = subset[col_prot].dropna().value_counts().head(5)
                    result["mutation_analysis"]["hotspots"] = [
                        {"protein_change": str(idx), "count": int(val)}
                        for idx, val in changes.items()
                    ]

                # generate detailed conclusion
                conclusion = f"{gene} is a **{freq_desc}** in {cancer_type} (Frequency: {freq:.2%}, {count}/{total})"

                # add the main mutation type information
                if col_type in subset.columns:
                    types = subset[col_type].value_counts()
                    if len(types) > 0:
                        top_type = types.index[0]
                        top_type_ratio = types.iloc[0] / len(subset) * 100
                        conclusion += f", dominated by {top_type} ({top_type_ratio:.0f}% of mutations)"

                # add the most common hotspot
                if col_prot in subset.columns:
                    changes = subset[col_prot].dropna().value_counts()
                    if len(changes) > 0:
                        top_hotspot = changes.index[0]
                        top_hotspot_count = changes.iloc[0]
                        conclusion += f". The most common hotspot is **{top_hotspot}** ({top_hotspot_count} lines)"

                result["mutation_analysis"]["conclusion"] = conclusion + "."
            else:
                result["mutation_analysis"]["conclusion"] = (
                    f"{gene} has no detected mutations in {cancer_type} cancer cell lines."
                )

            return result

        except Exception as e:
            return {"success": False, "error": f"Error analyzing mutations: {str(e)}"}

    def get_comprehensive_analysis(self, gene: str, cancer_type: str) -> dict:
        """
        Perform comprehensive analysis including dependency, expression, and mutation.

        Args:
            gene: Gene symbol
            cancer_type: Cancer type

        Returns:
            Dictionary with all three analyses combined
        """
        return {
            "gene": gene,
            "cancer_type": cancer_type,
            "dependency": self.get_dependency(gene, cancer_type),
            "expression": self.get_expression(gene, cancer_type),
            "mutation": self.get_mutation(gene, cancer_type),
        }


if __name__ == "__main__":
    # Test code
    api = DepMapAPI(data_dir="/path/to/depmap/data")
    result = api.get_expression("ERBB2", "Breast")
    print(json.dumps(result, indent=2))
