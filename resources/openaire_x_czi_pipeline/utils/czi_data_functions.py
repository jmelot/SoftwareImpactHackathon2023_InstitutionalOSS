import pandas as pd
from utils import extract_github_slug

def get_doi_to_software(input_file):
    """
    Parse CZI Raw mentions from a compressed CSV file

    Parameters:
    - input_file (str): Path to the input compressed CSV file.

    Returns:
    - pd.DataFrame: A DataFrame containing selected columns ('doi', 'software', 'ID').
    """

    df = pd.read_csv(input_file, sep="\t", dtype=str, compression='gzip')

    selected_data = df[['doi', 'software', 'ID']]

    return selected_data

def get_software_to_repo(input_file):
    """
    Parse CZI normalized github repos from a compressed CSV file
    Parameters:
    - input_file (str): Path to the input CSV file.

    Returns:
    - pd.DataFrame: A DataFrame containing selected columns ('ID', 'github_repo').
    """

    df = pd.read_csv(input_file, dtype=str)
    df['github_repo'] = df['github_repo'].apply(extract_github_slug)

    selected_data = df[['ID', 'github_repo']]

    return selected_data


def prepare_czi_data(czi_raw_mentions_file, czi_normalized_github_repos_file):
    """
    Prepare a combined DataFrame with relevant information from raw mentions and normalized GitHub repositories files.

    Parameters:
    - czi_raw_mentions_file (str): Path to the raw mentions CSV file.
    - czi_normalized_github_repos_file (str): Path to the normalized GitHub repositories CSV file.

    Returns:
    - pd.DataFrame: A combined DataFrame containing columns ('doi', 'github_repo', 'software').
    """ 
    
    doi_to_software = get_doi_to_software(czi_raw_mentions_file) 
    software_to_repo = get_software_to_repo(czi_normalized_github_repos_file)

    df = pd.merge(doi_to_software, software_to_repo, on='ID')
    print(f"CZI mentions data parsed and joined from '{czi_raw_mentions_file}' and '{czi_normalized_github_repos_file}'")

    return df[['doi', 'github_repo', 'software']]
