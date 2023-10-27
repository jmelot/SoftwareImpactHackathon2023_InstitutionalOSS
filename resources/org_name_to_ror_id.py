import requests
import csv


def get_ror_id(matched):
    for matched_org in matched["items"]:
        if matched_org["chosen"]:
            return matched_org["organization"]["id"]
    return ""


with open(
    "stack_institution_readmes/ner_extracted_institution_names_full_1.csv", "r"
) as f_in, open("stack_institution_readmes/repo_institution_ids_full_1.csv", "w") as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    for i, row in enumerate(reader):
        print(i)
        repo_name, org_name = row
        ror_id = ""
        if org_name:
            try:
                matched = requests.get(
                    "https://api.ror.org/organizations", {"affiliation": org_name}
                ).json()
                ror_id = get_ror_id(matched)
            except:
                pass
        if ror_id:
            writer.writerow([repo_name, org_name, ror_id])
