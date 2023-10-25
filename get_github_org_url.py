import argparse
import requests
import time
import os

RATE_LIMIT_INTERVAL = 2


def mk_auth() -> tuple:
    """
    Checks the environment for GITHUB_ACCESS_TOKEN and GITHUB_USER env variables and returns these as a
    tuple if set, otherwise complains
    :return: Tuple of values of (GITHUB_ACCESS_TOKEN, GITHUB_USER)
    """
    gh_tok = os.environ.get("GITHUB_ACCESS_TOKEN")
    assert gh_tok, "Please set the GITHUB_ACCESS_TOKEN environment variable"
    username = os.environ.get("GITHUB_USER")
    assert username, "Please set the GITHUB_USER environment variable"
    return username, gh_tok


def get_owner(owner: str) -> dict:
    """
    Retrieves metadata for repo owner, who may be a user or an organization
    :param owner: Name of repo owner
    :return: dict of owner metadata
    """
    AUTH = mk_auth()
    org_resp = requests.get(
        f"https://api.github.com/orgs/{owner}",
        auth=AUTH,
    )
    if org_resp.status_code == 200:
        return org_resp.json()
    time.sleep(RATE_LIMIT_INTERVAL)
    user_resp = requests.get(
        f"https://api.github.com/users/{owner}",
        auth=AUTH,
    )
    if user_resp.status_code == 200:
        return user_resp.json()
    print(f"{owner} not found as org or user")
    print(org_resp)
    print(user_resp)
    return None


def get_url(owner: str) -> str:
    owner_meta = get_owner(owner)
    return owner_meta.get("blog")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("owner_name")
    args = parser.parse_args()

    url = get_url(args.owner_name)
    print(f"URL for {args.owner_name} is {url} !")
