import argparse
import json
import os
from get_ror_from_gh_org_or_user import check_for_ror_url


def get_stack_org_rors(stack_path: str, output_file: str) -> None:
    """
    Get ROR ids from repo owners in The Stack, when available, and write out as JSON
    :param stack_path: Path to The Stack download, a directory containing multiple JSONL files
    :param output_file: Path where data should be written
    :return: None
    """
    owner_to_ror = {}
    # use this set to avoid re-checking owners, since owners are not unique
    checked = set()
    with open(output_file, mode="w") as out:
        for fi in os.listdir(stack_path):
            with open(os.path.join(stack_path, fi)) as f:
                for line in f:
                    js = json.loads(line)
                    repo = js["repo_name"]
                    owner = repo.split("/")[0]
                    if owner in checked:
                        if owner in owner_to_ror:
                            out.write(json.dumps({
                                "owner": owner,
                                "software": repo,
                                "ror_id": owner_to_ror[owner]
                            }))
                        continue
                    checked.add(owner)
                    ror = check_for_ror_url(owner)
                    if ror:
                        out.write(json.dumps({
                            "owner": owner,
                            "software": repo,
                            "ror_id": ror
                        }))
                        owner_to_ror[owner] = ror


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stack_data", default=os.path.join("stack_institution_readmes", "full_data"))
    parser.add_argument("--output_file", default="stack_org_rors.json")
    args = parser.parse_args()

    get_stack_org_rors(args.stack_data, args.output_file)