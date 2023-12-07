# Scicrunch data

## Data processing script

This directory contains human-curated data relating software to organizations from SciCrunch, plus a script to populate 
its most likely organizations and RORs. To run the script:

```bash
$ python3 enrich_sci_crunch_csv.py --input=scicrunch_working_file_software.csv --format=minimal
# This will output a file called "scicrunch_working_file_minimal.csv" that can be fed into the consolidate_links.py
# script.  To produce an enriched version of the original csv, use --format=full and it outputs "scicrunch_working_file_enriched.csv"
```

## Ground truth

### RRID to ROR Software Mapping Data, Please cite as Bandrowski 2023 Zenodo DOI:10.5281/zenodo.10048228

`scicrunch_working_file_software.csv` is a file that has been extracted from the SciCrunch Registry, accessible on the web: [https://scicrunch.org/resources](https://scicrunch.org/resources/data/source/nlx_144509-1/search)

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