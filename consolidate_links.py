import argparse
import csv
import json


def reformat_orca(url_matches: str, full_data: str) -> list:
    """

    :param url_matches:
    :param full_data:
    :return:
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
    for org in org_to_repos:
        unique_repos = set(org_to_repos[org])
        for repo in unique_repos:
            name = f"{owner}/{repo}"
            for ror_id in org_to_ror.get(org, []):
                reformatted.append({
                    "software_name": name,
                    "github_slug": name,
                    "ror_id": ror_id,
                    "extraction_method": "url_matches"
                })
    return reformatted


def merge_rows(orca: list) -> list:
    id_to_record = {}
    # we are iterating through a list of records containing our output rows (see format in `reformat_orca`).
    # We're creating an id for each row based on the name of the software and the ror id. If this id is present in
    # `id_to_record`, we will add the extraction method to the existing list. If not, we will add a new
    # record to `id_to_record`
    for row in orca:
        id = f"{row['software_name']}/{row['ror_id']}".lower()
        extraction_method = row["extraction_method"]
        if id in id_to_record:
            if extraction_method not in id_to_record[id]["extraction_methods"]:
                id_to_record[id]["extraction_methods"].push(extraction_method)
        else:
            row["extraction_methods"] = [row.pop("extraction_method")]
            id_to_record[id] = row
    # todo: add more elements to id_to_record here
    return [record for _, record in id_to_record.items()]


def write_reformatted(orca_url_matches, orca_data, output_file):
    orca = reformat_orca(orca_url_matches, orca_data)
    merged_rows = merge_rows(orca)
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
    parser.add_argument("--output_file", default="software_to_ror.csv")
    args = parser.parse_args()

    write_reformatted(args.orca_url_matches, args.orca_data, args.output_file)
