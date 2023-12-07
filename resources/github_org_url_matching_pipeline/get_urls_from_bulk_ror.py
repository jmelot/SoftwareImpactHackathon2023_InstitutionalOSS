import argparse
import json
import re


def clean_url(url: str) -> str:
    """
    Normalize format of url
    :param url: Raw url
    :return: Cleaned url
    """
    cleaned_url_match = re.search("(?i)https?:\/\/(www\.)?(.+)", url)
    if cleaned_url_match:
        return cleaned_url_match.group(2).strip("/")
    return url


def reformat_bulk_ror(bulk_ror_json: str, output_file_prefix: str):
    """
    Given bulk ROR JSON, create dicts mapping cleaned url (domain name or full url, minus https?://(www)?
    of each ror record to:
      - ROR ids with the cleaned url
      - full urls that share the cleaned url
    :param bulk_ror_json: Raw json from https://zenodo.org/records/8436953
    :param output_file_prefix: File prefix where json as described above should be written
    :return: None
    """
    with open(bulk_ror_json) as f:
        bulk_ror = json.loads(f.read())
    reformatted_full = {}
    reformatted_domain = {}
    for record in bulk_ror:
        for link in record["links"]:
            cleaned_url = clean_url(link)
            if cleaned_url:
                domain = cleaned_url.strip("/").split("/")[0]
                for obj, url in [[reformatted_full, cleaned_url], [reformatted_domain, domain]]:
                    if url not in obj:
                        obj[url] = {
                            "full_urls": [link],
                            "ror_ids": [record["id"]]
                        }
                    else:
                        obj[url]["full_urls"].append(link)
                        obj[url]["ror_ids"].append(record["id"])
    for obj in [reformatted_full, reformatted_domain]:
        for url in obj:
            obj[url]["full_urls"] = list(set(obj[url]["full_urls"]))
            obj[url]["ror_ids"] = list(set(obj[url]["ror_ids"]))
    with open(output_file_prefix+"_full.json", mode="w") as out:
        out.write(json.dumps(reformatted_full, indent=2))
    with open(output_file_prefix+"_domain.json", mode="w") as out:
        out.write(json.dumps(reformatted_domain, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bulk_ror_json")
    parser.add_argument("--output_file_prefix", default="ror_url_to_ids")
    args = parser.parse_args()

    reformat_bulk_ror(args.bulk_ror_json, args.output_file_prefix)
