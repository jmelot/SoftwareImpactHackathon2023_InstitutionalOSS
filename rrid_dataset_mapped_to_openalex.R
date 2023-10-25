library(dplyr)
library(openalexR)

# Loading in RRID dataset and formatting ------
rrid <- read.csv("working file software.csv")
rrid[is.na(rrid)] <- "BLANK"

rrid_df_with_doi <- rrid %>%
  select(Resource_Name, Defining_Citation, Alternate_URLs, ROR.and.other.mappings) %>%
  tidyr::separate_rows(Defining_Citation, sep=", ") %>%
  mutate(doi_valid = ifelse(grepl("DOI:", Defining_Citation), paste(Defining_Citation), paste("BLANK"))) %>%
  mutate(doi_valid = gsub("DOI:", "", doi_valid)) %>%
  filter(!doi_valid =="BLANK") %>%
  mutate(doi_valid = paste0("https://doi.org/", doi_valid))

rrid_df_with_pmid <- rrid %>%
  select(Resource_Name, Defining_Citation, Alternate_URLs, ROR.and.other.mappings) %>%
  tidyr::separate_rows(Defining_Citation, sep=", ") %>%
  mutate(pmid_valid = ifelse(grepl("PMID:", Defining_Citation), paste(Defining_Citation), paste("BLANK"))) %>%
  filter(!pmid_valid =="BLANK") %>%
  mutate(pmid_valid = tolower(pmid_valid)) %>%
  mutate(pmid_valid = stringr::str_replace_all(string=pmid_valid, pattern=" ", repl=""))

# Use PMIDs to query openalex ------

# Extract the valid PMIDs
valid_pmids <- rrid_df_with_pmid$pmid_valid

# Fetch papers using lapply
papers <- lapply(valid_pmids, function(pmid) {
  tryCatch({
    paper <- oa_fetch(entity = "works", identifier = pmid)
    if (is.data.frame(paper)) return(paper)
  }, error = function(e) NULL)
})

# Bind the resulting data frames together
res_pmid <- do.call(plyr::rbind.fill, papers)

# Use DOIs to query openalex ------

# Extract the valid DOIs
valid_dois <- rrid_df_with_doi$doi_valid

# Fetch papers using lapply
papers <- lapply(valid_dois, function(doi) {
  tryCatch({
    paper <- oa_fetch(entity = "works", identifier = doi)
    if (is.data.frame(paper)) return(paper)
  }, error = function(e) NULL)
})

# Bind the resulting data frames together
res_doi <- do.call(plyr::rbind.fill, papers)

# saving and reloading to avoid R crashes
# save(res_doi, file="res_doi.Rdata")
# save(res_doi, file="res_pmid.Rdata")
load("res_doi.Rdata")
load("res_pmid.Rdata")

# Loading in RRID dataset and formatting ------
res_doi_orgs <- res_doi %>%
  select(author, doi, ids, publication_year) %>%
  tidyr::unnest(author) %>%
  tidyr::unnest(ids) %>%
  filter(grepl("pubmed", ids)) %>%
  mutate(pmid = gsub("https://pubmed.ncbi.nlm.nih.gov/", "", ids)) %>%
  select(pmid, doi, publication_year, institution_ror, au_display_name, au_orcid, author_position, au_affiliation_raw)

res_pmid_orgs <- res_pmid %>%
  select(author, doi, ids, publication_year) %>%
  tidyr::unnest(author) %>%
  tidyr::unnest(ids) %>%
  filter(grepl("pubmed", ids)) %>%
  mutate(pmid = gsub("https://pubmed.ncbi.nlm.nih.gov/", "", ids)) %>%
  select(pmid, doi, publication_year, institution_ror, au_display_name, au_orcid, author_position, au_affiliation_raw)

# combined dataset from open alex with identifiers, authors, and ror info for each study in RRID dataset
combined_software_orgs <- rbind(res_doi_orgs, res_pmid_orgs)
combined_software_orgs <- unique(combined_software_orgs)

# Compare ROR info to RRID dataset ----
# not detailed yet
rrid_combined_formatted <- plyr::rbind.fill(rrid_df_with_doi, rrid_df_with_pmid) %>% 
  select(Resource_Name, pmid_valid, doi_valid, ROR.and.other.mappings) %>% 
  unique() %>%
  mutate(pmid_valid = gsub("pmid:", "", pmid_valid)) #making pmid format the same for joining 

rrid_combined_formatted1 <- inner_join(rrid_combined_formatted, combined_software_orgs, by=c("doi_valid"="doi")) %>% select(-pmid_valid)
rrid_combined_formatted2 <- inner_join(rrid_combined_formatted, combined_software_orgs, by=c("pmid_valid"="pmid")) %>% select(-doi_valid)
rrid_combined_formatted <- full_join(rrid_combined_formatted1, rrid_combined_formatted2)
rrid_combined_formatted <- rrid_combined_formatted %>% filter(!is.na(institution_ror)) # removing rows with no ror mapping via openalex

# Compare ROR info to RRID dataset ----
RRID_software_ror_mapped <- rrid_combined_formatted %>%
  select(Resource_Name, pmid, doi_valid, institution_ror, au_display_name, au_orcid, author_position, au_affiliation_raw) %>%
  unique()

write.csv(RRID_software_ror_mapped, "RRID_software_ror_mapped.csv", row.names = FALSE)



