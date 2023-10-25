# Linking Research Software to Research Organizations

Goal of our efforts during this hackathon: surface a list of _possible links_ from software repositories to ROR IDs (the idea being that this would be followed by manual curations).

## Resources

Regex for grabbing GitHub repos from freetext: `(?i)github.com/([A-Za-z0-9-_.]+/[A-Za-z0-9-_.]*[A-Za-z0-9-_])`

This is a template repo for external hackathon projects. Please build your project off of this template:
1. Click the ‘use this template’ button above to create a new repository, and choose an appropriate name for your project. The suggested naming scheme is: `SoftwareImpactHackathon2023_PROJECT`.
2. Turn on basic [security features](https://docs.github.com/en/code-security/getting-started/github-security-features) for your repository under Settings -> Security and Analysis. We strongly recommend you enable at least [Private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository), [Dependabot security updates](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates) and [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/configuring-secret-scanning-for-your-repositories).
4. Add your project link and description to the list of hackathon projects we’re curating at https://github.com/chanzuckerberg/software-impact-hackathon-2023 , by making a pull request to that repo.
5. Add your name or an appropriate copyright owner to the LICENSE file. CZI will not own the code in your repository.
6. [Grant privileges](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository)  to other collaborators, if desired.
7. Replace this section of the readme and the above "Hackathon-Template" heading with an appropriate readme and title for your project.

*Please do not modify or delete any other part of the readme below this line.*

***

## About this project

This repository was developed as part of the [Mapping the Impact of Research Software in Science](https://github.com/chanzuckerberg/software-impact-hackathon-2023) hackathon hosted by the Chan Zuckerberg Initiative (CZI). By participating in this hackathon, owners of this repository acknowledge the following:
1. The code for this project is hosted by the project contributors in a repository created from a template generated by CZI. The purpose of this template is to help ensure that repositories adhere to the hackathon’s project naming conventions and licensing recommendations.  CZI does not claim any ownership or intellectual property on the outputs of the hackathon. This repository allows the contributing teams to maintain ownership of code after the project, and indicates that the code produced is not a CZI product, and CZI does not assume responsibility for assuring the legality, usability, safety, or security of the code produced.
2. This project is published under a MIT license.

## Code of Conduct

Contributions to this project are subject to CZI’s Contributor Covenant [code of conduct](https://github.com/chanzuckerberg/.github/blob/master/CODE_OF_CONDUCT.md). By participating, contributors are expected to uphold this code of conduct. 

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting the repository owner via the ‘security’ tab above.


## RRID to ROR Software Mapping Data File Readme Section

This is a file that has been extracted from the SciCrunch Registry, accessible on the web: [https://scicrunch.org/resources](https://scicrunch.org/resources/data/source/nlx_144509-1/search)

The data is human curated and filtered by "Software" additional resource type. 
These data are openly available and any resource can be freely accessed by using the scicrunch or another resolving service without an API key (be kind with the number of times you access this or be banned). Example: 
https://scicrunch.org/resolver/[RRID] for bots add .json at the end




The data contains the columns described below:

Field name |	description	| field type
scr_id	|	scicrunch registry identifier can be used to pull metadata via n2t.net/RRID:SCR_$###	|	text
original_id	|	original identifier	|	text
type	|	organization or resource	|	text
parent_organization_id	|	typically only parents come from ROR entities (e.g., University not a program)	|	text
Resource_Name	|	unique across the registry for all curated items; resource names that are the same follow rules specifying how to augment the name, usually the university name or vendor name goes first (e.g., Graphpad Prism)	|	longtext
Defining_Citation	|	a manuscript written about the resource	|	longtext
Supercategory	|	Resource for all of these data	|	longtext
Species	|	not usually used for software, but the main species that is covered by the resource	|	longtext
Related_Disease	|	not usually used for software, but the main disease that is covered by the resource	|	longtext
Additional_Resource_Types	|	type hirearchy: https://bioportal.bioontology.org/ontologies/NIFSTD?p=classes&conceptid=http%3A%2F%2Furi.neuinfo.org%2Fnif%2Fnifstd%2Fnlx_res_20090101	|	longtext
Synonyms	|	comma delimited list	|	longtext
Abbreviation	|	comma delimited list	|	longtext
Keywords	|	comma delimited list	|	longtext
Resource_URL	|	current URL	|	longtext
Availability	|	license information if explicit license not available, also may not be in service	|	longtext
Related_Application	|	typically for biological applications	|	longtext
Funding_Information	|	ignore, there probably are not enough of these in software to worry about	|	longtext
Publication_Link	|	link to defining citation field	|	longtext
Twitter_Handle	|	twitter handle without the at sign	|	longtext
Alternate_URLs	|	other URLs that may be documentation, or other instances of the tool	|	longtext
Terms_Of_Use_URLs	|	URL to the terms of use	|	longtext
Old_URLs	|	URLs that are no longer used	|	longtext
Alternate_IDs	|	Any Identifiers that are not RRIDs, can be resolved by RRID resolver, comma delimeted	|	longtext
Comment	|	curation comment	|	longtext
Social_URLs	|	social media URLs	|	longtext
Supporting_Agency	|	the funding agency that supports the resource	|	longtext
Editorial_Note	|	ignore	|	longtext
Canonical_ID	|	the RRID in curie syntax	|	longtext
License	|	Explicit license	|	longtext
relationship_strings	|	bar delimited list of relationship labels with resources_scr_ids	|	mediumtext
resources_scr_ids	|	bar delimited list of other resources that are related to this RRID via the relationship listed in the relationship_strings field	|	text
