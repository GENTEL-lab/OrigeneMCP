import os
import requests


def convert_openalex_abstract(abstract_inverted_index: dict) -> str:
    """
    Convert an OpenAlex 'abstract_inverted_index' object into a readable text abstract.

    Args:
        abstract_inverted_index (dict): The 'abstract_inverted_index' field from OpenAlex API response.

    Returns:
        str: The reconstructed abstract text.
    """
    if not abstract_inverted_index:
        return ""
    
    try:
        # Reverse mapping: index -> word
        position_map = {}
        for word, positions in abstract_inverted_index.items():
            for pos in positions:
                position_map[pos] = word
        
        # Sort by position and concatenate
        abstract_words = [position_map[i] for i in sorted(position_map.keys())]
        abstract_text = " ".join(abstract_words)
    except Exception as e:
        print(f"Error converting abstract: {e}")
        return abstract_inverted_index
    
    return abstract_text


def has_all_concepts(work, concept_ids):
    work_concepts = {c["id"].split('/')[-1] for c in work["concepts"]}
    return all(cid in work_concepts for cid in concept_ids)


def openalex_search(
    query=None,
    concepts=None,
    authors=None,
    publication_year=None,
    cited_by_count=None,
    is_open_access=None,
    has_doi=None,
    has_pdf=None,
    publication_type=None,
    n_results=30,
    sort_by='relevance_score:desc'
):
    """
    OpenAlex advanced filter search - fully based on filters
    
    Args:
        query: Optional search keywords
        concepts: List of concept IDs or names, e.g. ['machine_learning', 'deep_learning'] or ['C119857082']
        journals: List of journal IDs or names, e.g. ['nature', 'science']
        institutions: List of institution IDs or names, e.g. ['stanford', 'mit']
        authors: List of author OpenAlex IDs, e.g. ['A2208157607']
        publication_year: Publication year, supports range like '2020-2024' or single year '2023'
        cited_by_count: Citation count range, e.g. '>100' or '50-200'
        is_open_access: True/False, whether open access
        has_doi: True/False, whether has DOI
        has_pdf: True/False, whether has PDF
        publication_type: Article type, e.g. 'journal-article', 'preprint'
        n_results: Number of results per page (1-200)
        sort_by: Sort method, options:
            - 'cited_by_count:desc' (citation count descending, default)
            - 'publication_date:desc' (publication date descending)
            - 'relevance_score:desc' (relevance score descending, requires query)
    
    Returns:
        List containing article information
    """
    base_url = "https://api.openalex.org/works"
    
    params = {
        'per_page': min(n_results * 3, 200),
        'sort': sort_by,
        'mailto': 'your-email@example.com'
    }
    
    # Add search keywords (optional)
    if query:
        params['search'] = query
    
    # Build filter conditions
    filters = []
    
    # Year filter
    if publication_year:
        if '-' in str(publication_year):  # Range
            start, end = publication_year.split('-')
            filters.append(f"publication_year:{start}-{end}")
        else:  # Single year
            filters.append(f"publication_year:{publication_year}")
    
    # Citation count filter
    if cited_by_count:
        filters.append(f"cited_by_count:{cited_by_count}")
    
    # Boolean filters
    if is_open_access is not None:
        filters.append(f"is_oa:{str(is_open_access).lower()}")
    
    if has_doi is not None:
        filters.append(f"has_doi:{str(has_doi).lower()}")
    
    if has_pdf is not None:
        filters.append(f"has_pdf:{str(has_pdf).lower()}")
    
    # Publication type filter
    if publication_type:
        filters.append(f"type:{publication_type}")
    
    # Combine all filter conditions
    if filters:
        params['filter'] = ','.join(filters)
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    works = data.get('results', [])
    meta = data.get('meta', {})
    total_count = meta.get('count', 0)
    
    print(f"Found {total_count} articles in total, currently displaying {len(works)}\n")
    
    results = []
    for idx, work in enumerate(works, 1):
        
        if not isinstance(work, dict):
            continue
        
        try:
            title = work.get('title', 'No title')
            authors = [a.get('author', {}).get('display_name', '') 
                        for a in work.get('authorships', [])]
            
            primary_loc = work.get('primary_location', {})
            venue = primary_loc.get('source', {}).get('display_name', 'Unknown')
            
            year = work.get('publication_date', 'N/A')
            doi = work.get('doi', '')
            
            abstract = convert_openalex_abstract(work.get('abstract_inverted_index'))
            
            if not abstract:
                continue
            
            result = {
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'venue': venue,
                'year': year,
                'doi': doi
            }
            results.append(result)
        
        except Exception as e:
            print(f"API request error: {e}")
            
    print(f"Finally get {len(results)} papers, and return the first {min(len(results), n_results)} papers")

    return results[:n_results]

 