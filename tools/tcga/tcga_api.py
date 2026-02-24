import requests
import pandas as pd
from io import StringIO  # Fix point here

class TCGA_API:
    BASE_URL = "http://firebrowse.org/api/v1/Samples/mRNASeq"
    
    def __init__(self):
        self.session = requests.Session()

    def get_gene_specific_expression_in_cancer_type(self, gene: str):

        params = {
            "format": "tsv",
            "gene": gene,
            "sample_type": "TM,TP,TR",  # Primary tumor samples
            "protocol": "RSEM",
            "page_size": 2000,
            "page": 1,
            "sort_by": "cohort"
        }

        all_data = []

        while True:
            print(f"Fetching page {params['page']}...")
            resp = self.session.get(self.BASE_URL, params=params)
            if resp.status_code != 200:
                print(f"Failed to fetch page {params['page']}: {resp.status_code}")
                break

            content = resp.text.strip()
            if not content or content.startswith("No records"):
                break

            # Extract column names from the first page
            if params["page"] == 1:
                df = pd.read_csv(StringIO(content), sep="\t")
                columns = df.columns
            else:
                df = pd.read_csv(StringIO(content), sep="\t", header=None)
                df.columns = columns  # Manually add column names

            all_data.append(df)
            params["page"] += 1

        # Merge and save
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)

        df_grouped = final_df.groupby("cohort")["expression_log2"].agg(["mean", "std", "count"]).sort_values("mean", ascending=False)
        df_grouped["zscore"] = (df_grouped["mean"] - df_grouped["mean"].mean()) / df_grouped["mean"].std()

        # Define high/low expression (zscore > 1 for high expression, < -1 for low expression)
        high_expr = df_grouped[df_grouped["zscore"] > 1].sort_values("mean", ascending=False)
        low_expr = df_grouped[df_grouped["zscore"] < -1].sort_values("mean")

        return {
            "high_expression_cancers": [
                {
                    "cancer_type": idx,
                    "mean_expression": float(round(row["mean"], 3)),
                    "sample_count": int(row["count"])
                }
                for idx, row in high_expr.iterrows()
            ],
            "low_expression_cancers": [
                {
                    "cancer_type": idx,
                    "mean_expression": float(round(row["mean"], 3)),
                    "sample_count": int(row["count"])
                }
                for idx, row in low_expr.iterrows()
            ]
        }
if __name__ == "__main__":
    # Initialize and run the server
    tcga = TCGA_API()
    result = tcga.get_gene_specific_expression_in_cancer_type(gene='TP53')
    print(result)