"""
Test DepMap API functions
"""

import sys
import json
from pathlib import Path

# add path to import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.depmap.depmap_api import DepMapAPI
from tools.depmap.server import load_config


def test_depmap():
    print("=" * 60)
    print("Test DepMap API functions")
    print("=" * 60)
    data_dir = load_config()["depmap_data_dir"]
    print(f"\ninitialize DepMap API, data directory: {data_dir}")
    api = DepMapAPI(data_dir=data_dir)

    if not api.initialized:
        print("❌ API initialization failed\n")
        return

    print("✅ API initialization successful\n")

    # test 1: dependency analysis
    print("-" * 60)
    print("test 1: dependency analysis (ERBB2 @ Breast)")
    print("-" * 60)
    result = api.get_dependency("ERBB2", "Breast")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # test 2: expression analysis
    print("\n" + "-" * 60)
    print("test 2: expression analysis (ERBB2 @ Breast)")
    print("-" * 60)
    result = api.get_expression("ERBB2", "Breast")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # test 3: mutation analysis
    print("\n" + "-" * 60)
    print("test 3: mutation analysis (KRAS @ Pancreas)")
    print("-" * 60)
    result = api.get_mutation("KRAS", "Pancreas")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # test 4: comprehensive analysis
    print("\n" + "-" * 60)
    print("test 4: comprehensive analysis (ERBB2 @ Breast)")
    print("-" * 60)
    result = api.get_comprehensive_analysis("ERBB2", "Breast")
    print(
        {
            "gene": result.get("gene"),
            "cancer_type": result.get("cancer_type"),
            "dependency_success": result.get("dependency", {}).get("success"),
            "expression_success": result.get("expression", {}).get("success"),
            "mutation_success": result.get("mutation", {}).get("success"),
        }
    )

    print("\n" + "=" * 60)
    print("✅ All tests completed")
    print("=" * 60)


if __name__ == "__main__":
    test_depmap()
