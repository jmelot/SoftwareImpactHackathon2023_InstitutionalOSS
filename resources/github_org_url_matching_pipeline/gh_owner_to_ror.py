import argparse
import json
from get_github_org_url import get_url
from get_urls_from_bulk_ror import clean_url


def get_ror_from_url(owner_name: str, ror_domain_json: str = "ror_domain_to_ids.json",
                      ror_full_url_json: str = "ror_url_to_ids.json") -> list:
    """
    Check whether a github org/user url appears in ROR, and return the ROR ids for that url if so
    :param owner_name: Name of github repo owner, such as `apache` for `apache/airflow`
    :param ror_domain_json: Path to local JSON mapping domain names to ROR ids
    :param ror_full_url_json: Path to local JSON mapping full urls to ROR ids
    :return: ROR ids associated with the `owner_name`, based on URL matches
    """
    gh_url = get_url(owner_name)
    if not gh_url:
        print(f"No url found for {owner_name} on github")
        return
    if "linkedin.com" in gh_url or "sites.google.com" in gh_url:
        print(f"Skipping {gh_url} for {owner_name}")
        return
    cleaned_gh_url = clean_url(gh_url)

    with open(ror_full_url_json) as f:
        full_ror_json = json.loads(f.read())
    if cleaned_gh_url in full_ror_json:
        return full_ror_json[cleaned_gh_url]["ror_ids"]
    with open(ror_domain_json) as f:
        domain_json = json.loads(f.read())
    gh_url_domain = cleaned_gh_url.split("/")[0]
    if gh_url_domain in domain_json:
        return domain_json[gh_url_domain]["ror_ids"]
    # handle cases like nlp.standford.edu
    stripped_domain = ".".join(gh_url_domain.split(".")[-2:])
    if stripped_domain in domain_json:
        return domain_json[stripped_domain]["ror_ids"]
    print(f"No ROR id found for url {gh_url} from {owner_name} on github")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("owner_name")
    parser.add_argument("--ror_domain_json", default="ror_domain_to_ids.json")
    parser.add_argument("--ror_full_url_json", default="ror_url_to_ids.json")
    args = parser.parse_args()

    ror_ids = get_ror_from_url(args.owner_name, args.ror_domain_json, args.ror_full_url_json)
    if ror_ids:
        print(f"ROR ids found for {args.owner_name}: {ror_ids}")
