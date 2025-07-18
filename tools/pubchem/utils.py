import re
import ast
from typing import Optional, List

from langchain_openai import ChatOpenAI


def get_llm(base_url: str, api_key: str, model: str) -> ChatOpenAI:
    """
    Get GPT-4 1 mini model configuration.

    Returns:
        Configured ChatOpenAI instance for GPT-4 1 mini
    """
    if base_url and api_key and model:
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            openai_api_base=base_url,
            max_tokens=128000,
        )
    else:
        return None
    

def extract_and_convert_list(text: str) -> Optional[List]:
    """
    Extract and convert a list from text using regex and ast.literal_eval.

    Args:
        text: Text containing a Python list representation

    Returns:
        Parsed list or None if extraction/conversion fails
    """
    if not text:
        return None

    # Regex pattern to match list structures, including nested ones
    pattern = r"\[(?:[^\[\]]*|\[(?:[^\[\]]*|\[[^\[\]]*\])*\])*\]"
    match = re.search(pattern, text)

    if match:
        list_str = match.group()
        try:
            python_list = ast.literal_eval(list_str)
            return python_list if isinstance(python_list, list) else None
        except (SyntaxError, ValueError):
            return None
    return None
    

def extract_description(response):
    # Only keep data related to specific properties
    related_sections = [
        "Names and Identifiers",
        "Drug and Medication Information", 
        "Pharmacology and Biochemistry",
    ]

    def get_summary(input_data):
        try:
            summary_info = {"Others": []}
            data = input_data["Section"][0]["Information"]
        except:
            return summary_info
        
        for each in data:
            try:
                value = each["Value"]["StringWithMarkup"][0]["String"]
            except:
                continue

            if "Description" not in each:
                desc = "Others"
                summary_info[desc].append(value)
            else:
                desc = each["Description"]
                summary_info[desc] = value
        return summary_info

    extracted_result = {}
    for data in response["Record"]["Section"]:
        if data["TOCHeading"] in related_sections:
            extracted_result[data["TOCHeading"]] = get_summary(data)
    return extracted_result