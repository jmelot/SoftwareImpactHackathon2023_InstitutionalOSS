import pandas as pd

def get_doi_to_repo_urls():

    csv_file = "/home/serafeim/oss_to_orgs/czi-extract-doi-to-repo-urls/output-data/doi_to_github_repo_urls.csv"  # Replace with the actual file name and path if it's not in your working directory

    df = pd.read_csv(csv_file, sep="\t")

    selected_data = df[['doi', 'github_repo']]

    return selected_data

def get_doi_to_ror():

    csv_file = "/data/out/doi_ror_relations.csv"

    df = pd.read_csv(csv_file, sep="\t")
    df = df.rename(columns={'DOI': 'doi'})

    return df


doi_to_repos = get_doi_to_repo_urls() 
print(doi_to_repos)

doi_to_ror = get_doi_to_ror()
print(doi_to_ror)

result_df = pd.merge(doi_to_repos, doi_to_ror, on='doi')
print(result_df)

output_csv_file = '/data/out/doi_to_rorid.csv'
result_df.to_csv(output_csv_file, index=False, sep='\t', header=True)
