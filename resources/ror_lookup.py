"""
Given a publication identifier, such as a DOI or PMID, retrieve all RORs associated with that publication from
author affiliations in OpenAlex
"""

import argparse
import requests


def work_to_affiliation_rors(ident: str) -> list:
    """
    Given a work identifier and the type of that identifier (one of 'doi' or 'pmid'),
    retrieves the ROR ids of the author affiliations for that work.
    :param ident: Identifier for a work
    :return: List of ROR ids corresponding to author affiliations of that work
    """
    resp = requests.get(f"https://api.openalex.org/works/{ident}")
    rors = []
    if resp.status_code == 200:
        result = resp.json()
        for author in result["authorships"]:
            for institution in author["institutions"]:
                ror = institution.get("ror")
                if ror:
                    rors.append(ror)
    return list(set(rors))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("external_id", help="DOI or PMID we want ROR affiliation ids from. "
                                            "DOIs must be full URLs, e.g. https://doi.org/10.7717/peerj.4375")
    args = parser.parse_args()

    rors = work_to_affiliation_rors(args.external_id)
    print(f"RORs found for {args.external_id}: {rors}")