import pandas as pd
from utils import extract_github_slug

def get_doi_to_software(input_file):

    df = pd.read_csv(input_file, sep="\t", dtype=str)

    selected_data = df[['doi', 'software', 'ID']]

    return selected_data

def get_software_to_repo(input_file):

    df = pd.read_csv(input_file, dtype=str)
    df['github_repo'] = df['github_repo'].apply(extract_github_slug)

    selected_data = df[['ID', 'github_repo']]

    return selected_data


def prepare_czi_data(czi_raw_mentions_file, czi_normalized_github_repos_file):

    doi_to_software = get_doi_to_software(czi_raw_mentions_file) 
    software_to_repo = get_software_to_repo(czi_normalized_github_repos_file)

    df = pd.merge(doi_to_software, software_to_repo, on='ID')

    return df[['doi', 'github_repo', 'software']]
