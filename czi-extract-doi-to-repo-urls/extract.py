import pandas as pd

def get_doi_to_software():

    csv_file = "/Users/serafeim/Downloads/doi_10.5061_dryad.6wwpzgn2c__v8/raw/comm_raw.tsv"  # Replace with the actual file name and path if it's not in your working directory

    df = pd.read_csv(csv_file, sep="\t")

    selected_data = df[['doi', 'ID']]

    return selected_data

def get_software_to_repo():

    csv_file = "/Users/serafeim/Downloads/doi_10.5061_dryad.6wwpzgn2c__v8/linked/normalized/github_df.csv"

    df = pd.read_csv(csv_file)

    selected_data = df[['ID', 'github_repo']]

    return selected_data


doi_to_software = get_doi_to_software() 
software_to_repo = get_software_to_repo()

print(doi_to_software)
print(software_to_repo)

result_df = pd.merge(doi_to_software, software_to_repo, on='ID')
print(result_df)

output_csv_file = 'output-data/out.csv'
result_df.to_csv(output_csv_file, index=False, sep='\t', header=True)
