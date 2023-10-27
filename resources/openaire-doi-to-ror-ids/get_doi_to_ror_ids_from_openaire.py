import pandas as pd
import json

# Read the JSON file into a list of dictionaries
data = []
with open('/home/serafeim/doi_to_rorids_crossref_Aug_2023.jsonl', 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Flatten the "Matchings" array into separate rows
df = df.explode('Matchings').reset_index(drop=True)

# Expand the "Matchings" dictionary into separate columns
df = pd.concat([df.drop(['Matchings'], axis=1), df['Matchings'].apply(pd.Series)], axis=1)

# Select and rename columns for the CSV export
df = df[['DOI', 'RORid', 'Confidence']]
df = df.rename(columns={'DOI': 'DOI', 'RORid': 'ROR_ID', 'Confidence': 'Confidence'})

# Export to a CSV file
df.to_csv('/data/out/doi_ror_relations.csv', index=False, sep='\t', header=True)

# Print the DataFrame for reference
# print(df)