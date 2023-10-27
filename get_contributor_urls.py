import argparse
import re
import requests
import time

from get_github_org_url import RATE_LIMIT_INTERVAL, mk_auth, get_url


def get_contributors(repo: str) -> dict:
    """
    Retrieves metadata for repo owner, who may be a user or an organization
    :param owner: Name of repo owner
    :return: dict of owner metadata
    """
    time.sleep(RATE_LIMIT_INTERVAL)
    AUTH = mk_auth()
    contrib_resp = requests.get(
        f"https://api.github.com/repos/{repo}/contributors",
        auth=AUTH,
    )
    if contrib_resp.status_code == 200:
        return contrib_resp.json()
    print(f"Contributors for {repo} not found")


def get_bio_org_urls(user_obj: dict) -> list:
    bio = user_obj.get("bio")
    if not bio:
        return []
    org_urls = set()
    orgs = re.findall(r"@\s*(\S+)", bio)
    for org in orgs:
        org_link = get_url(org)
        if org_link:
            print(f"Found an org in a bio! {org_link} from {user_obj['login']}")
            org_urls.add(org_link)
    return list(org_urls)


def get_contributor_urls(owner: str) -> list:
    contributors = get_contributors(owner)
    urls = []
    for contributor in contributors:
        username = contributor["login"]
        url = get_url(username)
        bio_urls = get_bio_org_urls(contributor)
        if url:
            print(f"Found url {url} for contributor {username}")
            urls.append(url)
        for url in bio_urls:
            urls.append(url)
    return list(set(urls))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_name")
    args = parser.parse_args()

    urls = get_contributor_urls(args.repo_name)
    print(f"Contributor URLs for {args.repo_name} are {urls} !")
