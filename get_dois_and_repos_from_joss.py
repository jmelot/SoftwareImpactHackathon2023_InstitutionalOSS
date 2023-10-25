import argparse
import json
import os

from bs4 import BeautifulSoup


def get_joss_repo_paper_mappings(joss_directory: str, output_file: str):
    """
    Given a directory of JOSS papers, extract github repos, paper titles, and dois
    :param joss_directory: Directory containing JOSS data, from https://github.com/openjournals/joss-papers
    :param output_file: File where a mapping from github repo to paper title and doi should be written
    :return: None
    """
    output_data = {}
    for paper_dir in os.listdir(joss_directory):
        if not os.path.isdir(os.path.join(joss_directory, paper_dir)):
            continue
        for fi in os.listdir(os.path.join(joss_directory, paper_dir)):
            if not fi.endswith(".html"):
                continue
            with open(os.path.join(joss_directory, paper_dir, fi)) as f:
                html_content = f.read()
                html_content = html_content.replace("body = <<-EOF\n", "").replace("EOF\n", "")
                soup = BeautifulSoup(html_content, "html.parser")
                paper_data = soup.find("div", class_="accepted-paper")
                header = paper_data.find("h1")
                if not header:
                    continue
                title = header.text
                metadata = paper_data.find_all("span", class_="repo")
                doi, repo = None, None
                for meta in metadata:
                    if "DOI:" in meta.text:
                        doi = meta.find("a").text.replace("https://doi.org/", "")
                    elif "Repository:" in meta.text:
                        repo = meta.find("a")["href"]
                if repo:
                    output_data[repo] = {
                        "doi": doi,
                        "title": title
                    }
    with open(output_file, mode="w") as f:
        f.write(json.dumps(output_data, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--joss_directory", default="joss-papers")
    parser.add_argument("--output_file", default="joss_repo_to_doi_and_title.json")
    args = parser.parse_args()

    get_joss_repo_paper_mappings(args.joss_directory, args.output_file)
