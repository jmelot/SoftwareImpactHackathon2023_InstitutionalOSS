import pandas as pd

def load_software_to_repo():

    csv_file = "/Users/serafeim/Downloads/doi_10.5061_dryad.6wwpzgn2c__v8/linked/normalized/github_df.csv"

    df = pd.read_csv(csv_file)

    df = df[['ID', 'github_repo']]
    df.rename(columns={'ID': 'mention_id'}, inplace=True)

    return df



def load_formal_citation_data():

    csv_file = "data_from_formal_citations_cleaned.csv"  # Replace with the actual file name and path if it's not in your working directory

    df = pd.read_csv(csv_file, sep=",")

    return df

citation_data = load_formal_citation_data()
software_to_repo_data = load_software_to_repo()

print(citation_data)
print(software_to_repo_data)

result_df = pd.merge(citation_data, software_to_repo_data, on='mention_id', how='left')

print(result_df)

output_csv_file = 'data_from_formal_citations_cleaned_joined.csv'
result_df.to_csv(output_csv_file, index=False, sep=',', header=True)


