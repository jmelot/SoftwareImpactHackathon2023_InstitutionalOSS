import argparse
import boto3
import csv
import re
import requests
import xml.etree.ElementTree as ET

from botocore import UNSIGNED
from botocore.config import Config
from collections import defaultdict
from multiprocessing.pool import Pool


s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

PMC_BUCKET = "pmc-oa-opendata"
OPENALEX_URL = "https://api.openalex.org"


def extract_citation_number(mention):
    """
    Extract the number of the formal citation from the mention, if the formal
    citation exists. For example, from the mention "We used Apache Spark [12]
    to process the logs.", the citation number "12" should be extracted.

    :param mention: Software mention object
    :return: Formal citation number or None
    """

    regex = re.escape(mention["software"]) + " *\[([1-9]\d*)"
    matched = re.search(regex, mention["text"])
    return matched.group(1) if matched else None


def generate_mentions(file_path):
    """
    Generator of software mention objects.

    :param file_path: File path of a TSV file from CZI dataset
    :return: Software mention objects
    """

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for mention in reader:
            if "software" == mention["curation_label"]:
                yield mention


def generate_mentions_with_citations(file_path):
    """
    Generator of software mentions with a formal citation.

    :param file_path: File path of a TSV file from CZI dataset
    :return: Tuples (software mention object, formal citation number)
    """

    for mention in generate_mentions(file_path):
        cit_num = extract_citation_number(mention)
        if cit_num is not None:
            yield mention, cit_num


def get_source_pmc_metadata(mention):
    """
    Get the metadata of the source paper of a mention from PMC.

    :param mention: Software mention object
    :return: Source metadata (XML JATS)
    """

    pmcid = mention["pmcid"]
    key = f"oa_comm/xml/all/PMC{pmcid}.xml"
    body = s3_client.get_object(Bucket=PMC_BUCKET, Key=key)["Body"].read()
    return ET.fromstring(body)


def extract_reference(citation_number, jats_metadata):
    """
    Extract a bibliographic reference from the PMC metadata based on the
    citation number.

    :param citation_number: Citation number
    :param jats_metadata: Metadata (XML JATS)
    :return: Bibliographic reference or None (XML JATS)
    """

    for ref_list in jats_metadata.findall(".//ref-list"):
        for reference in ref_list:
            if "ref" != reference.tag:
                continue
            # The references in JATS have "id" attributes which are typically
            # a number with a prefix, for example "CR12". To locate the right
            # reference, we ignore the prefix and compare the number with the
            # citation number from the software mention.
            reference_id = re.search("[1-9]\d*", reference.attrib["id"]).group()
            if citation_number == reference_id:
                return reference
    return None


def get_pub_id(reference, id_type):
    """
    Extract publication ID of a given type from a JATS reference.

    :param reference: Reference object (XML JATS)
    :param id_type: Type of identifier
    :return: Identifier
    """

    for field in reference:
        for subfield in field:
            if subfield.tag == "pub-id" and subfield.attrib["pub-id-type"] == id_type:
                return subfield.text
    return None


def get_reference_pub_ids(data):
    """
    Map a software mention with a formal citation to the DOI and/or PMID of the
    formally cited paper.

    :param data: A tuple containing sequence number (for displaying script's
        progress), software mention object, and formal citation number
    :return: Input mention and formal citation DOI and/or PMID
    """

    i, mention, citation_number = data
    print(f"Phase 1, mention {i}")

    metadata = get_source_pmc_metadata(mention)
    reference = extract_reference(citation_number, metadata)
    if reference is None:
        return mention, None, None
    return mention, get_pub_id(reference, "doi"), get_pub_id(reference, "pmid")


def record_ids(mention_ref_ids, mention, doi, pmid):
    """
    Record extracted IDs in the mention_ref_ids map.

    :param mention_ref_ids: The map to update
    :param mention: Software mention object
    :param doi: DOI of a paper formally cited with the mention
    :param PMID: PMID of a paper formally cited with the mention
    """

    mention_id = mention["ID"]
    software = mention["software"]
    if mention_id not in mention_ref_ids:
        mention_ref_ids[mention_id] = {
            "name": software,
            "dois": defaultdict(lambda: 0),
            "pmids": defaultdict(lambda: 0),
        }
    if doi is not None:
        mention_ref_ids[mention_id]["dois"][doi.lower()] += 1
    if pmid is not None:
        mention_ref_ids[mention_id]["pmids"][pmid] += 1


def most_popular_id(dictionary, min_count=5):
    """
    Get most popular ID from a counter dictionary.

    :param dictionary: A counter dictionary (ID->count)
    :param min_count: Minimum count
    :return: The most popular ID or None
    """

    sorted_values = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    if sorted_values and sorted_values[0][1] >= min_count:
        return sorted_values[0][0]
    return None


def get_openalex_metadata(pub_id_type, pub_id):
    """
    Get metadata from OpenAlex.

    :param pub_id_type: Identifier type, either doi or pmid
    :param pub_id: Identifier
    :return: OpenAlex metadata record
    """

    data = requests.get(f"{OPENALEX_URL}/works/{pub_id_type}:{pub_id}")
    return data.json() if data.status_code == 200 else None


def extract_openalex_ror_ids(pub_id_type, pub_id):
    """
    Extract ROR IDs from OpenAlex metadata.

    :param pub_id_type: Identifier type, either doi or pmid
    :param pub_id: Identifier
    :return: A set of ROR IDs
    """

    ids = set()
    if pub_id is None:
        return ids
    metadata = get_openalex_metadata(pub_id_type, pub_id)
    if metadata is None:
        return ids
    for author in metadata["authorships"]:
        for institution in author["institutions"]:
            ids.add(institution["ror"])
    return ids


def extract_ror_ids(data):
    """
    Extract ROR IDs from OpenAlex metadata.

    :param data: A tuple containing sequence number (for displaying script's
        progress), and a dictionary with DOI and/or PMID extracted from the
        formally cited paper.
    :return: A tuple (mention object, ROR IDs extracted based on DOI,
        ROR IDs extracted based on PMID)
    """

    i, mention_data = data
    print(f"Phase 2, mention {i}")

    doi = mention_data["doi"]
    ror_ids_from_doi = extract_openalex_ror_ids("doi", doi)

    pmid = mention_data["pmid"]
    ror_ids_from_pmid = extract_openalex_ror_ids("pmid", pmid)

    return mention_data, ror_ids_from_doi, ror_ids_from_pmid


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", help="path of a TSV file from CZI dataset)", required=True
    )
    parser.add_argument(
        "--min-count", help="minimum DOI/PMID count", type=int, default=5
    )
    parser.add_argument("--output", help="output CSV file", required=True)
    parser.add_argument("--threads", help="number of threads", type=int, default=4)
    parser.add_argument("--chunk", help="imap chunk size", type=int, default=16)
    args = parser.parse_args()

    # First, we extract DOIs and PMIDs from the formal citations associated with
    # the software mentions. As we process the data, the resulting DOIs and PMIDs
    # are gathered in mention_ref_ids map.
    mention_ref_ids = {}
    mentions_generator = generate_mentions_with_citations(args.input)
    with Pool(args.threads) as p:
        args_generator = map(
            lambda r: (r[0], r[1][0], r[1][1]), enumerate(mentions_generator)
        )
        results = p.imap(get_reference_pub_ids, args_generator, args.chunk)
        for mention, doi, pmid in results:
            record_ids(mention_ref_ids, mention, doi, pmid)

    # For every mention ID, we leave only the top DOI and the top PMID, if the
    # number of occurrences is at least args.min_count. Everything else is
    # discarded.
    for mention_id, mention_data in mention_ref_ids.items():
        mention_data["ID"] = mention_id
        mention_data["doi"] = most_popular_id(
            mention_data["dois"], min_count=args.min_count
        )
        mention_data["pmid"] = most_popular_id(
            mention_data["pmids"], min_count=args.min_count
        )
        del mention_data["dois"]
        del mention_data["pmids"]

    # For every chosen DOI and PMID, we extract its metadata record from
    # OpenAlex, and extract all ROR IDs from it.
    with open(args.output, "w") as f, Pool(args.threads) as p:
        writer = csv.writer(f)
        arguments = enumerate(mention_ref_ids.values())
        results = p.imap(extract_ror_ids, arguments, args.chunk)
        for mention_data, ror_ids_from_doi, ror_ids_from_pmid in results:
            for ror_id in ror_ids_from_doi.union(ror_ids_from_pmid):
                source_doi = mention_data["doi"] if ror_id in ror_ids_from_doi else ""
                source_pmid = (
                    mention_data["pmid"] if ror_id in ror_ids_from_pmid else ""
                )
                writer.writerow(
                    [
                        mention_data["ID"],
                        mention_data["name"],
                        source_doi,
                        source_pmid,
                        ror_id,
                    ]
                )
