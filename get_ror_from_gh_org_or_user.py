import argparse
import json
from get_github_org_url import get_url
from get_urls_from_bulk_ror import clean_url


def check_for_ror_url(owner_name: str, ror_domain_json: str, ror_full_url_json: str):
    """
    Check whether a github org/user url appears in ROR, and return the ROR ids for that url if so
    :param owner_name:
    :param ror_domain_json:
    :param ror_full_url_json:
    :return:
    """
    gh_url = get_url(owner_name)
    if not gh_url:
        print(f"No url found for {owner_name} on github")
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
    print(f"No ROR id found for url {gh_url} from {owner_name} on github")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("owner_name")
    parser.add_argument("--ror_domain_json", default="ror_url_to_ids_domain.json")
    parser.add_argument("--ror_full_url_json", default="ror_url_to_ids_full.json")
    args = parser.parse_args()

    ror_ids = check_for_ror_url(args.owner_name, args.ror_domain_json, args.ror_full_url_json)
    if ror_ids:
        print(f"ROR ids found for {args.owner_name}: {ror_ids}")
