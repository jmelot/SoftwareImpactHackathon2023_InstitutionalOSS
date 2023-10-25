# Linking Research Software to Research Organizations

Goal of our efforts during this hackathon: surface a list of _possible links_ from software repositories to ROR IDs (the idea being that this would be followed by manual curations).

[Project planning document](https://docs.google.com/document/d/1dxEUORt-m0I9tDicAQU77__gDR4TvVnUGXOatI1CS_A/edit).

## Resources

* Regex for grabbing GitHub repos from freetext: `(?i)github.com/([A-Za-z0-9-_.]+/[A-Za-z0-9-_.]*[A-Za-z0-9-_])`
* Script for extracting urls of Github orgs/users: `get_github_org_url.py` - part of ROR url to GitHub org/user url linking
* Script for mapping urls to ROR ids: `get_urls_from_bulk_ror.py`
    * Resulting data in `ror_url_to_ids_domain.json` (domain names to ror ids) and `ror_url_to_ids_full.json` (cleaned full urls to ror ids)
* Script for extracting github urls from the Journal of Open-Source software and mapping them to DOIs and paper titles: `get_dois_and_repos_from_joss.py`
    * Resulting data in `repo_to_doi_and_title.json`

## (partial) Solutions

Script for retrieving ROR IDs from github users or org names, if available: `get_ror_from_gh_org.py`. Sample usage:

```bash
$ python3 get_ror_from_gh_org_or_user.py MITHaystack
ROR ids found for MITHaystack: ['https://ror.org/03db3by08']
$ python3 get_ror_from_gh_org_or_user.py foo
No ROR id found for url https://maciej.pacut.pl from foo on github
$ python3 get_ror_from_gh_org_or_user.py jmelot
No url found for jmelot on github
```

## RRID to ROR Software Mapping Data File Readme Section

This is a file that has been extracted from the SciCrunch Registry, accessible on the web: [https://scicrunch.org/resources](https://scicrunch.org/resources/data/source/nlx_144509-1/search)

The data is human curated and filtered by "Software" additional resource type. 
These data are openly available and any resource can be freely accessed by using the scicrunch or another resolving service without an API key (be kind with the number of times you access this or be banned). Example: 
https://scicrunch.org/resolver/[RRID] for bots add .json at the end

The data contains the columns described below:

| Field name |	description	| field type |
|--- |---|---|
|	scr_id	|	scicrunch registry identifier can be used to pull metadata via n2t.net/RRID:SCR_$###	|	text	|
|	original_id	|	original identifier	|	text	|
|	type	|	organization or resource	|	text	|
|	parent_organization_id	|	typically only parents come from ROR entities (e.g., University not a program)	|	text	|
|	Resource_Name	|	unique across the registry for all curated items; resource names that are the same follow rules specifying how to augment the name, usually the university name or vendor name goes first (e.g., Graphpad Prism)	|	longtext	|
|	Defining_Citation	|	a manuscript written about the resource	|	longtext	|
|	Supercategory	|	Resource for all of these data	|	longtext	|
|	Species	|	not usually used for software, but the main species that is covered by the resource	|	longtext	|
|	Related_Disease	|	not usually used for software, but the main disease that is covered by the resource	|	longtext	|
|	Additional_Resource_Types	|	type hirearchy: https://bioportal.bioontology.org/ontologies/NIFSTD?p=classes&conceptid=http%3A%2F%2Furi.neuinfo.org%2Fnif%2Fnifstd%2Fnlx_res_20090101	|	longtext	|
|	Synonyms	|	comma delimited list	|	longtext	|
|	Abbreviation	|	comma delimited list	|	longtext	|
|	Keywords	|	comma delimited list	|	longtext	|
|	Resource_URL	|	current URL	|	longtext	|
|	Availability	|	license information if explicit license not available, also may not be in service	|	longtext	|
|	Related_Application	|	typically for biological applications	|	longtext	|
|	Funding_Information	|	ignore, there probably are not enough of these in software to worry about	|	longtext	|
|	Publication_Link	|	link to defining citation field	|	longtext	|
|	Twitter_Handle	|	twitter handle without the at sign	|	longtext	|
|	Alternate_URLs	|	other URLs that may be documentation, or other instances of the tool	|	longtext	|
|	Terms_Of_Use_URLs	|	URL to the terms of use	|	longtext	|
|	Old_URLs	|	URLs that are no longer used	|	longtext	|
|	Alternate_IDs	|	Any Identifiers that are not RRIDs, can be resolved by RRID resolver, comma delimeted	|	longtext	|
|	Comment	|	curation comment	|	longtext	|
|	Social_URLs	|	social media URLs	|	longtext	|
|	Supporting_Agency	|	the funding agency that supports the resource	|	longtext	|
|	Editorial_Note	|	ignore	|	longtext	|
|	Canonical_ID	|	the RRID in curie syntax	|	longtext	|
|	License	|	Explicit license	|	longtext	|
|	relationship_strings	|	bar delimited list of relationship labels with resources_scr_ids	|	mediumtext	|
|	resources_scr_ids	|	bar delimited list of other resources that are related to this RRID via the relationship listed in the relationship_strings field	|	text	|

***

## About this project

This repository was developed as part of the [Mapping the Impact of Research Software in Science](https://github.com/chanzuckerberg/software-impact-hackathon-2023) hackathon hosted by the Chan Zuckerberg Initiative (CZI). By participating in this hackathon, owners of this repository acknowledge the following:
1. The code for this project is hosted by the project contributors in a repository created from a template generated by CZI. The purpose of this template is to help ensure that repositories adhere to the hackathon’s project naming conventions and licensing recommendations.  CZI does not claim any ownership or intellectual property on the outputs of the hackathon. This repository allows the contributing teams to maintain ownership of code after the project, and indicates that the code produced is not a CZI product, and CZI does not assume responsibility for assuring the legality, usability, safety, or security of the code produced.
2. This project is published under a MIT license.

## Code of Conduct

Contributions to this project are subject to CZI’s Contributor Covenant [code of conduct](https://github.com/chanzuckerberg/.github/blob/master/CODE_OF_CONDUCT.md). By participating, contributors are expected to uphold this code of conduct. 

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting the repository owner via the ‘security’ tab above.
