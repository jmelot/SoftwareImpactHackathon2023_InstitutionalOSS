import argparse
import csv
import os


def add_github_slugs(links_file: str, output_file: str, czi_mapping: str) -> None:
    """
    Adds github slugs to links.csv produced by pipeline.py
    :param links_file: Output of pipeline.py
    :param output_file: Location where output should be written
    :param czi_mapping: Linkage metadata provided by CZI, including software id to github mappings
    :return: None
    """
    software_id_to_github = {}
    with open(czi_mapping) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for line in reader:
            github = line["github_repo"]
            if github == "[None]":
                github = None
            if github:
                github = github.replace("['", "").replace("']", "").split(",")[0]
                software_id_to_github[line["ID"]] = github.replace("https://github.com/", "")
    with open(output_file, mode="w") as out:
        writer = csv.DictWriter(out, fieldnames=["mention_id", "mention", "DOI", "PMID", "ROR_ID", "github_slug"])
        writer.writeheader()
        with open(links_file) as f:
            for line in csv.DictReader(f):
                line["github_slug"] = software_id_to_github.get(line["mention_id"])
                writer.writerow(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_to_czi_linked_metadata",
                        default=os.path.join("doi_10_5061_dryad_6wwpzgn2c__v20220919", "linked", "metadata.tsv"))
    args = parser.parse_args()

    add_github_slugs("links.csv", "links_with_slugs.csv", args.path_to_czi_linked_metadata)
