# URL Matching Pipeline

In this method, we link GitHub repositories to ROR ids using the urls of the "owner" entity. For example, for the
[fastpli](https://github.com/3d-pli/fastpli) project, we retrieve the owner, [3d-pli](https://github.com/3d-pli),
and attempt to match the listed url (https://www.fz-juelich.de/de/inm/inm-1) to ROR. Its domain name matches 
[Forschungszentrum Jülich](https://ror.org/02nv7yv05) in ROR, so we link `3d-pli/fastpli` to Forschungszentrum Jülich.

## Preparing to run URL matching 

### Preparing environment 

Create a new virtual environment using your favorite tool, and install the project requirements, e.g.:

```
virtualenv venv
pip install -r ../requirements.txt
. venv/bin/activate
```

Create two environment variables, `GITHUB_ACCESS_TOKEN` (which should contain a GitHub personal access token with
`read:org` and `read:user` scopes), and `GITHUB_USER`.

```bash
export GITHUB_ACCESS_TOKEN=your access token
export GITHUB_USER=your github username
```

### Preparing ROR data

The commands in this section only need to be run when you want to update the ROR data used in later scripts.

* Download the [latest ROR data from Zenodo](https://zenodo.org/records/8436953).
* Run `python3 get_urls_from_bulk_ror.py`. This will generate two JSONs, `ror_domain_to_ids.json`, which maps
domain names of organizations in ROR to ROR ids, and `ror_url_to_ids.json`, which maps full urls of
organizations in ROR to ROR ids

## Retrieving affiliation for a single GitHub repository owner 

To retrieve the affiliation for a single GitHub repository owner, run `gh_owner_to_ror.py` with one argument,
the owner name. For example, 

```bash
python3 gh_owner_to_ror.py stanfordnlp
ROR ids found for stanfordnlp: ['https://ror.org/00f54p054']
```

## Retrieving bulk links from software to ROR ids 

We have previously run software-ROR linking on software from the ORCA dataset, and on software from The Stack. 
These scripts are available in `get_{orca,stack}_org_rors.py` and can be run without arguments to update the default 
bulk data files.

