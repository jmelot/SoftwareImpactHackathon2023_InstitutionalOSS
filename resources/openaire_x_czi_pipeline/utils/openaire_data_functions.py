import pandas as pd
import json
import gzip 

def prepare_openaire_data(input_file, output_file):
    """
    Prepare OpenAIRE data from a JSON file by flattening and selecting specific columns.

    Parameters:
    - input_file (str): Path to the input GZIP-compressed JSON file.
    - output_file (str): Path to the output CSV file.

    Returns:
    - pd.DataFrame: A DataFrame containing selected columns ('doi', 'RORid').
    """

    # Read the JSON file into a list of dictionaries
    data = []
    with gzip.open(input_file, 'rt', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)

    # Flatten the "Matchings" array into separate rows
    df = df.explode('Matchings').reset_index(drop=True)

    # Expand the "Matchings" dictionary into separate columns
    df = pd.concat([df.drop(['Matchings'], axis=1), df['Matchings'].apply(pd.Series)], axis=1)

    # Select and rename columns for the CSV export
    df = df[['DOI', 'RORid']]

    # remove any duplicates
    df = df.drop_duplicates()

    df = df.rename(columns={'DOI': 'doi'})

    # Export to a CSV file
    # df.to_csv(output_file, index=False, sep='\t', header=True)

    print(f"OpenAIRE data from '{input_file}' were parsed successfully into '{output_file}'")

    return df