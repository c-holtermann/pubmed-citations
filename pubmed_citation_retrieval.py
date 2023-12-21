"""
PubMed Citation Retrieval Script

This script retrieves citation information for a list of PubMed IDs and creates an XML file
containing the list of citing papers for each publication. It utilizes the PubMed E-Utilities API
to fetch citation data.

Author: Christoph Holtermann

Date: 2023-12-21

License: GNU GENERAL PUBLIC LICENSE Version 3
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re  # Import regular expression module

# Define output file name
OUTPUT_FILE = "pubmed_results.xml"
TEMPLATE_FILE = "zotero_export.txt"  # Add the template file name

def parse_templates(file_path):
    """
    Parse template information from a text file.

    Parameters:
    - file_path (str): Path to the text file containing templates.

    Returns:
    - dict: Dictionary mapping keys to template values.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # The regular expression pattern for the "PMID" key
    pmid_pattern = re.compile(r'\bPMID\s*=\s*(\d+)\b')

    # Find matches in the text
    matches = pmid_pattern.findall(content)

    # Extract the content between {{ and }}
    templates_content = re.findall(r'{{(.*?)}}', content, re.DOTALL)

    # Create a dictionary with the "PMID" key and its corresponding value
    result_dict = {str(matches[i]): "{{"+templates_content[i].strip()+"}}" for i in range(len(matches))}

    return result_dict

def get_citations(pubmed_id, template_results):
    """
    Retrieve the list of PubMed IDs citing a given publication.

    Parameters:
    - pubmed_id (str): PubMed ID of the target publication.
    - template_results (dict): Dictionary containing template results.

    Returns:
    - list: List of PubMed IDs citing the target publication.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    citedby_url = f"{base_url}elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_citedin&id={pubmed_id}"

    # Get the list of citation IDs
    response = requests.get(citedby_url)
    soup = BeautifulSoup(response.content, 'xml')

    link_set_db = soup.find("LinkSetDb")
    if link_set_db:
        citation_ids = [item.find("Id").get_text() for item in link_set_db.find_all("Link")]
        return citation_ids
    else:
        return []

def create_xml(pubmed_ids, citing_papers_all):
    """
    Create an XML file with information about PubMed publications and their citing papers.

    Parameters:
    - pubmed_ids (list): List of PubMed IDs.
    - citing_papers_all (dict): Dictionary mapping PubMed IDs to lists of citing papers.
    """
    root = ET.Element("PubMedResults")

    for pubmed_id in pubmed_ids:
        pub_elem = ET.SubElement(root, "Publication", PubMedID=pubmed_id)

        # Retrieve citing papers from the provided dictionary
        citing_papers = citing_papers_all.get(pubmed_id, [])

        for citing_paper in citing_papers:
            ET.SubElement(pub_elem, "CitingPaper", PubMedID=citing_paper)

    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)


def main():
    # Parse templates from the template file
    template_results = parse_templates(TEMPLATE_FILE)

    # Dictionary to store the citation counts for each PubMed ID
    citation_counts = {}
    citing_papers_all = {}

    print("fetch ", end="")
    first=True
    # Call get_citations for each PubMed ID and count citations
    for pubmed_id in template_results.keys():
        if not first:
            print(", ", end="")
        else:
            first=False
        print(f"{pubmed_id}", end="", flush=True)
        citing_papers = get_citations(pubmed_id, template_results)
        citing_papers_all[pubmed_id] = citing_papers
        citation_counts[pubmed_id] = len(citing_papers)
    print()

    # Sort PubMed IDs by the number of citations
    sorted_pubmed_ids = sorted(citation_counts, key=citation_counts.get, reverse=True)

    # Print statistics
    print("Statistics:")
    for pubmed_id in sorted_pubmed_ids:
        citation_count = citation_counts[pubmed_id]
        print(f"PubMed ID: {pubmed_id}; Number of Citations: {citation_count}")

    create_xml(sorted_pubmed_ids, citing_papers_all)

if __name__ == "__main__":
    main()

