import argparse
import csv
import json
import os


def reformat_orca_url_matches(url_matches: str, full_data: str) -> list:
    """
    Reformat url matches over the ORCA data into the standard format
    :param url_matches: Name of file containing owner <-> ROR matches found from URL match over ORCA data
    :param full_data: Full ORCA data download
    :return: List of reformatted records
    """
    org_to_repos = {}
    reformatted = []
    with open(full_data) as f:
        for line in f:
            js = json.loads(line)
            owner = js["owner_name"]
            repo = js["current_name"]
            if owner not in org_to_repos:
                org_to_repos[owner] = []
            org_to_repos[owner].append(repo)
    with open(url_matches) as f:
        org_to_ror = json.loads(f.read())
    for owner in org_to_repos:
        unique_repos = set(org_to_repos[owner])
        for repo in unique_repos:
            name = f"{owner}/{repo}"
            for ror_id in org_to_ror.get(owner, []):
                reformatted.append({
                    "software_name": name,
                    "github_slug": name,
                    "ror_id": ror_id,
                    "extraction_method": "url_matches"
                })
    return reformatted


def reformat_stack_readme_matches(stack_matches: str) -> list:
    """
    Reformat url matches over the ORCA data into the standard format
    :param url_matches: Name of file containing owner <-> ROR matches found from URL match over ORCA data
    :param full_data: Full ORCA data download
    :return: List of reformatted records
    """
    reformatted = []
    with open(stack_matches) as f:
        reader = csv.DictReader(f)
        for line in reader:
            ror_id = line["ror_id"]
            if ror_id:
                reformatted.append({
                    "software_name": line["repo_name"],
                    "github_slug": line["repo_name"],
                    "ror_id": ror_id,
                    "extraction_method": "ner_text_extraction"
                })
    return reformatted


def reformat_working_curated(working_curated: str) -> list:
    """
    Reformat working curated data into the standard format
    :param working_curated: Name of file containing minimal working curated data
    :return: List of reformatted records
    """
    reformatted = []
    with open(working_curated) as f:
        reader = csv.DictReader(f)
        for row in reader:
            reformatted.append({
                "software_name": row["software_name"],
                "github_slug": row["github_slug"],
                "ror_id": row["ror_id"],
                "extraction_method": row["extraction_methods"]
            })
    return reformatted


def merge_rows(datasets: list) -> list:
    """
    Merge data across disparate sources, with one row per software-ROR pair
    :param datasets: List of lists of records in the format shown in `reformat_orca_url_matches`, one per data source
    :return: List of deduplicated records
    """
    id_to_record = {}
    # we are iterating through a list of records containing our output rows (see format in `reformat_orca_url_matches`).
    # We're creating an id for each row based on the name of the software and the ror id. If this id is present in
    # `id_to_record`, we will add the extraction method to the existing list. If not, we will add a new
    # record to `id_to_record`
    for dataset in datasets:
        for row in dataset:
            id = f"{row['software_name']}/{row['ror_id']}".lower()
            extraction_method = row["extraction_method"]
            if id in id_to_record:
                if extraction_method not in id_to_record[id]["extraction_methods"]:
                    id_to_record[id]["extraction_methods"].push(extraction_method)
            else:
                row["extraction_methods"] = [row.pop("extraction_method")]
                id_to_record[id] = row
    merged = [record for _, record in id_to_record.items()]
    merged.sort(key=lambda row: f"{row['software_name']}/{row['ror_id']}".lower())
    return merged


def write_reformatted(orca_url_matches: str, orca_data: str, stack_readme_matches: str, working_curated: str,
                      output_file: str):
    """
    Merge data from disparate sources and write out in a single CSV
    :param orca_url_matches: matches from repo owner urls to ROR urls
    :param orca_data: ORCA data download, containing additional metadata for each ORCA repo
    :param stack_readme_matches: Affiliations extracted from The Stack readmes using NER
    :param output_file: File where output csvs should be written
    :return: None
    """
    orca = reformat_orca_url_matches(orca_url_matches, orca_data)
    stack_readme = reformat_stack_readme_matches(stack_readme_matches)
    working = reformat_working_curated(working_curated)
    # TODO: write a reformat_<your data> function to put data in the format shown in `reformat_orca_url_matches`,
    # then put the output in the array below
    merged_rows = merge_rows([orca, stack_readme, working])

    rors = set()
    with open(output_file, mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=["software_name", "github_slug", "ror_id", "extraction_methods"])
        writer.writeheader()
        for row in merged_rows:
            rors.add(row["ror_id"])
            writer.writerow({
                "software_name": row["software_name"],
                "github_slug": row["github_slug"],
                "ror_id": row["ror_id"],
                "extraction_methods": ";".join(row["extraction_methods"])
            })
    print(f"Wrote {len(merged_rows)} software-ror links containing {len(rors)} distinct ROR ids")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--orca_url_matches", default="orca_org_rors.json")
    parser.add_argument("--orca_data", default="orca_download.jsonl")
    parser.add_argument("--stack_readme_affiliations",
                        default=os.path.join("stack_institution_readmes", "repo_institution_ids.csv"))
    parser.add_argument("--working_curated", default="working_file_minimal.csv")
    parser.add_argument("--output_file", default="software_to_ror.csv")
    # TODO: add more arguments to ingest more data sources
    args = parser.parse_args()

    write_reformatted(args.orca_url_matches, args.orca_data, args.stack_readme_affiliations, args.working_curated,
                      args.output_file)
