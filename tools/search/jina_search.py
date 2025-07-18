import requests
import json
import time
from typing import Dict, List, Any


class JinaSearchEngine:    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def run(self, query: str) -> List[Dict[str, Any]]:
        """
        Run the search engine with a given query, retrieving and filtering results.
        This implements a two-phase retrieval approach: 
        1. Get preview information for many results
        2. Filter the previews for relevance
        3. Get full content for only the relevant results
        
        Args:
            query: The search query
            
        Returns:
            List of search results with full content (if available)
        """
        
        chance = 3
        current_try = 0
        while current_try < chance:
            try:
                url = 'https://deepsearch.jina.ai/v1/chat/completions'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key}'
                }

                data = {
                    "model": "jina-deepsearch-v1",
                    "messages": [
                        {
                            "role": "user",
                            "content": "Hi!"
                        },
                        {
                            "role": "assistant",
                            "content": "Hi, how can I help you?"
                        },
                        {
                            "role": "user",
                            "content": query
                        }
                    ],
                    "stream": False,
                    "reasoning_effort": "low",
                    "max_attempts": 1,
                    "no_direct_answer": False
                }
                start_time = time.time()
                response = requests.post(url, headers=headers, json=data, timeout=(30, 300))

                if response.status_code == 200:
                    result_json = response.json()
                else:
                    raise ValueError(f"API response error: {response.status_code}")

                end_time = time.time()
                print(f"Jina search takes {end_time - start_time} seconds")
                
                if result_json is None:
                    raise ValueError("failed to get deep search results")
                else:
                    delta_content = result_json["choices"][0].get("delta")
                    if not delta_content:
                        delta_content = result_json["choices"][0].get('message', {})
                    search_result = delta_content.get("content")
                    annotations = delta_content.get("annotations", [])
                    
                    search_citations = []
                    try:
                        for i, item in enumerate(annotations):
                            search_citations.append({
                                "index": i+1,
                                "link": item["url_citation"]["url"],
                                "title": item["url_citation"]["title"],
                                "snippet": item["url_citation"]["exactQuote"],
                                "content": item["url_citation"]["exactQuote"],
                                "full_content": item["url_citation"]["exactQuote"]
                            })
                    except Exception as e:
                        print(f"Error: {e}")
                        pass
                    search_citations.append(search_result)
                    break
                    
            except Exception as e:
                print('Error: ', e)
                print("reach RPM, sleep for 60 seconds")
                time.sleep(60)
                print("finish sleeping, retrying")
                current_try += 1
                
        return search_citations


