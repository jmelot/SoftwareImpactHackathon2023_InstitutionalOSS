import argparse
import json
import os
import sys

sys.path.append("..")

from bs4 import BeautifulSoup
from utils import ror_lookup


def get_repo_metadata(joss_entry: str) -> list:
    """
    Given a file from JOSS, retrieve RORs for affiliations of authors of described software
    :param joss_entry: path to JOSS file
    :return: list of dicts of ROR ids and software metadata
    """
    with open(joss_entry) as f:
        html_content = f.read()
        html_content = html_content.replace("body = <<-EOF\n", "").replace("EOF\n", "")
        soup = BeautifulSoup(html_content, "html.parser")
        paper_data = soup.find("div", class_="accepted-paper")
        header = paper_data.find("h1")
        if not header:
            return []
        title = header.text
        metadata = paper_data.find_all("span", class_="repo")
        doi, repo = None, None
        for meta in metadata:
            if "DOI:" in meta.text:
                doi = meta.find("a").text
            elif "Repository:" in meta.text:
                repo = meta.find("a")["href"]
        if repo and doi:
            rors = ror_lookup.work_to_affiliation_rors(doi)
            if rors:
                return [{
                    "software_name": title,
                    "github_slug": repo,
                    "ror_id": ror,
                } for ror in rors]
    return []


def get_joss_repo_paper_mappings(joss_directory: str, output_file: str):
    """
    Given a directory of JOSS papers, extract github repos, paper titles, and dois
    :param joss_directory: Directory containing JOSS data, from https://github.com/openjournals/joss-papers
    :param output_file: File where a mapping from github repo to paper title and doi should be written
    :return: None
    """
    output_data = {}
    with open(output_file, mode="w") as out:
        for paper_dir in os.listdir(joss_directory):
            if not os.path.isdir(os.path.join(joss_directory, paper_dir)):
                continue
            for fi in os.listdir(os.path.join(joss_directory, paper_dir)):
                if not fi.endswith(".html"):
                    continue
                repo_meta = get_repo_metadata(os.path.join(joss_directory, paper_dir, fi))
                for row in repo_meta:
                    out.write(json.dumps(row)+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--joss_directory", default="joss-papers")
    parser.add_argument("--output_file", default="joss_rors.jsonl")
    args = parser.parse_args()

    get_joss_repo_paper_mappings(args.joss_directory, args.output_file)
