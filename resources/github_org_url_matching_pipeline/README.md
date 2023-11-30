# URL Matching Pipeline

In this method, we link GitHub repositories to ROR ids using the urls of the "owner" entity. For example, for the
[fastpli](https://github.com/3d-pli/fastpli) project, we retrieve the owner, [3d-pli](https://github.com/3d-pli),
and attempt to match the listed url (https://www.fz-juelich.de/de/inm/inm-1) to ROR. Its domain name matches 
[Forschungszentrum Jülich](https://ror.org/02nv7yv05) in ROR, so we link `3d-pli/fastpli` to Forschungszentrum Jülich.

## Preparing to use this code

Create a new virtual environment using your favorite tool, and install the project requirements, e.g.:

```
virtualenv venv
pip install -r ../requirements.txt
. venv/bin/activate
```

## Preparing ROR data

The commands in this section only need to be done when you want to update the ROR data used in later scripts.

* Download the [latest ROR data from Zenodo](https://zenodo.org/records/8436953).
* Run `python3 get_stack_org_rors.py`. This will generate two JSONs, `ror_domain_to_ids.json`, which maps
domain names of organizations in ROR to ROR ids, and `ror_url_to_ids.json`, which maps full urls of
organizations in ROR to ROR ids

## Retrieving ROR-Software links

First, you need to select a corpus to run over. We have previously run ROR-software linking on software from the ORCA
dataset, and on software from The Stack. These scripts are available in `get_{orca,stack}_org_rors.py`. 

