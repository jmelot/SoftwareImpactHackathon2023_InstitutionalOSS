#!/usr/bin/env python3

import argparse
import sys
import requests
from urllib.parse import urlencode
import csv
import os
import time
import re


def find_best_result(response):
    json_data = response.json()

    if json_data.get('number_of_results', 0) < 1:
        return {'proposed': '', 'ror_id': ''}

    rors = [item for item in json_data.get('items', [])]
    ror = next((i for i in rors if i.get('chosen') is True), None)

    # If no chosen item, use the first item
    ror = rors[0] if ror is None else ror

    return {'proposed': ror['organization']['name'], 'ror_id': ror['organization']['id']}


def best_ror(org_name):
    """Given an organization name, returns the best ROR ID for that organization"""
    query = urlencode({"affiliation": org_name})
    url = f"https://api.ror.org/organizations?{query}"

    # print(f"query {org_name}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.reason}")
        return None

    return find_best_result(response=response)


def empty_cell(cell_contents):
    return cell_contents == '#N/A' or not cell_contents


def github_slug(row):
    github_s = ''
    github_urls = ''
    resource_url = row.get('Resource_URL', '')
    alternate_urls = row.get('Alternate_URLs', '')

    if 'github.com' in resource_url:
        github_urls = resource_url

    if not github_urls and 'github.com' in alternate_urls:
        github_urls = alternate_urls

    github_url_list = [url.strip() for url in github_urls.split(',') if 'github.com' in url]
    github_url = github_url_list[0] if github_url_list else ''

    if github_url:
        m = re.match(r'^https://github.com/([^/]+/[^/]+)$', github_url)
        if m:
            github_s = m.group(1)

    return github_s


def proposed_ror_info(row, ror_cache):
    org_name = row['Parent Org Name']
    filled_ror = row['ROR and other mappings']
    org_info = {'proposed': '', 'ror_id': ''}

    if (not empty_cell(org_name)) and (not ('ror.org' in filled_ror)):
        if org_name in ror_cache:
            org_info = ror_cache[org_name]
        else:
            ror_info = best_ror(org_name)
            if ror_info:
                org_info = ror_info
            ror_cache[org_name] = org_info
            time.sleep(0.2) # limit hitting their API too fast and getting blocked or throttled

    return org_info


def full_enhance(args):
    ror_cache = {}
    out_file = os.path.join(os.path.dirname(args.input), 'scicrunch_working_file_enriched.csv')

    with (open(args.input, 'r') as csv_file):
        csv_reader = csv.DictReader(csv_file)
        headers = csv_reader.fieldnames

        last_column = 39
        fixed_headers = headers[:last_column + 1]
        new_headers = ['proposed_name', 'proposed_ror_id']
        all_headers = fixed_headers + new_headers
        processed_rows = 0

        with open(out_file, 'w', newline='') as csv_out:
            dict_writer = csv.DictWriter(csv_out, all_headers)
            dict_writer.writeheader()

            for row in csv_reader:
                processed_rows += 1
                if processed_rows % 100 == 0:
                    print(f"processed {processed_rows} rows")

                org_info = proposed_ror_info(row, ror_cache)
                new_row = {key: row[key] for key in fixed_headers} | \
                          {'proposed_name': org_info['proposed'], 'proposed_ror_id': org_info['ror_id']}
                dict_writer.writerow(new_row)


def minimal_info(args):
    ror_cache = {}

    with open(args.input, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        processed_rows = 0
        out_file = os.path.join(os.path.dirname(args.input), 'scicrunch_working_file_minimal.csv')
        with open(out_file, 'w', newline='') as csv_out:
            csv_writer = csv.writer(csv_out)
            csv_writer.writerow(['software_name', 'github_slug', 'ror_id', 'org_name', 'extraction_methods'])

            for row in csv_reader:
                processed_rows += 1
                if processed_rows % 100 == 0:
                    print(f"processed {processed_rows} rows")

                proposed_info = proposed_ror_info(row, ror_cache)
                if (not ('ror.org' in row['ROR and other mappings'])) and (not proposed_info['ror_id']):
                    continue

                ror_id = row['ROR and other mappings'] if ('ror.org' in row['ROR and other mappings']) else \
                    proposed_info['ror_id']
                org_name = row['Parent Org Name']
                sfw_name = row['Resource_Name']
                extraction_methods = 'human_curated' if ('ror.org' in row['ROR and other mappings']) else 'by_name'
                new_row = [sfw_name, github_slug(row), ror_id, org_name, extraction_methods]
                csv_writer.writerow(new_row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="The path to the input file")
    parser.add_argument("--format", help="one of 'full' or 'minimal'.  Full enriches the original CSV with RORs, "
                                         "minimal creates csv output for combining with other processors")
    args = parser.parse_args()

    if args.format == 'full':
        full_enhance(args)
    elif args.format == 'minimal':
        minimal_info(args)
    else:
        parser.print_help()
        sys.exit(1)
