import argparse
import json
from get_ror_from_gh_org_or_user import check_for_ror_url


def get_orca_org_rors(orca_data: str, output_file: str) -> None:
    """
    Get ROR ids from ORCA repo owners, when available, and write out as JSON
    :param orca_data: Path to ORCA download
    :param output_file: Path where data should be written
    :return: None
    """
    owner_to_ror = {}
    # use this set to avoid re-checking owners, since owners are not unique within ORCA
    checked = set()
    with open(orca_data) as f:
        for line in f:
            js = json.loads(line)
            owner = js["owner_name"]
            if owner in checked:
                continue
            checked.add(owner)
            ror = check_for_ror_url(owner)
            if ror:
                owner_to_ror[owner] = ror
    with open(output_file, mode="w") as f:
        f.write(json.dumps(owner_to_ror, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--orca_data", default="orca_download.jsonl")
    parser.add_argument("--output_file", default="orca_org_rors.json")
    args = parser.parse_args()

    get_orca_org_rors(args.orca_data, args.output_file)