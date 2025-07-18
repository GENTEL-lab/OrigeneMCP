import requests
import pandas as pd
from io import StringIO  # 修正点在这里

class TCGA_API:
    BASE_URL = "http://firebrowse.org/api/v1/Samples/mRNASeq"
    
    def __init__(self):
        self.session = requests.Session()

    def get_gene_specific_expression_in_cancer_type(self, gene: str):

        params = {
            "format": "tsv",
            "gene": gene,
            "sample_type": "TM,TP,TR",  # 原发肿瘤样本
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

            # 第一页提取列名
            if params["page"] == 1:
                df = pd.read_csv(StringIO(content), sep="\t")
                columns = df.columns
            else:
                df = pd.read_csv(StringIO(content), sep="\t", header=None)
                df.columns = columns  # 手动补上列名

            all_data.append(df)
            params["page"] += 1

        # 合并并保存
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)

        df_grouped = final_df.groupby("cohort")["expression_log2"].agg(["mean", "std", "count"]).sort_values("mean", ascending=False)
        df_grouped["zscore"] = (df_grouped["mean"] - df_grouped["mean"].mean()) / df_grouped["mean"].std()

        # 定义高低表达（zscore > 1 为高表达，< -1 为低表达）
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