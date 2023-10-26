library(dplyr)
library(openalexR)

# Loading in CZI  dataset and formatting ------
czi_data <- read.csv("data_from_formal_citations_cleaned.csv")
czi_data[is.na(czi_data)] <- "BLANK"
czi_data_links <- read.csv("data_from_formal_citations.csv") %>% select(mention_id, ext.link)
czi_data <- czi_data %>% left_join(czi_data_links)

czi_df_with_doi <- czi_data %>%
  select(mention, most_popular_doi, ext.link) %>%
  filter(!most_popular_doi =="BLANK") %>%
  filter(!most_popular_doi =="") %>%
  mutate(most_popular_doi = paste0("https://doi.org/", most_popular_doi))

czi_df_with_pmid <- czi_data %>%
  select(mention, most_popular_pmid, ext.link) %>%
  filter(!most_popular_pmid =="BLANK") %>%
  filter(!most_popular_pmid =="") %>%
  mutate(most_popular_pmid = paste0("pmid:", most_popular_pmid))


# Use PMIDs to query openalex ------

# Extract the valid PMIDs
valid_pmids <- czi_df_with_pmid$most_popular_pmid

# Fetch papers using lapply
papers <- lapply(valid_pmids, function(pmid) {
  tryCatch({
    paper <- oa_fetch(entity = "works", identifier = pmid)
    if (is.data.frame(paper)) return(paper)
  }, error = function(e) NULL)
})

# Bind the resulting data frames together
res_pmid <- do.call(plyr::rbind.fill, papers)
save(res_pmid, file="res_pmid_czi.Rdata")

# Use DOIs to query openalex ------

# Extract the valid DOIs
czi_df_with_doi_now <- czi_df_with_doi %>%
  filter(!most_popular_doi %in% res_pmid$doi)
valid_dois <- czi_df_with_doi_now$most_popular_doi

# Fetch papers using lapply
papers <- lapply(valid_dois, function(doi) {
  tryCatch({
    paper <- oa_fetch(entity = "works", identifier = doi)
    if (is.data.frame(paper)) return(paper)
  }, error = function(e) NULL)
})


# Bind the resulting data frames together
res_doi <- do.call(plyr::rbind.fill, papers)
save(res_doi, file="res_doi_czi.Rdata")

# saving and reloading to avoid R crashes
# save(res_doi, file="res_doi.Rdata")
# save(res_doi, file="res_pmid.Rdata")
load("res_doi_czi.Rdata")
load("res_pmid_czi.Rdata")

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
czi_combined_formatted <- plyr::rbind.fill(czi_df_with_doi, czi_df_with_pmid) %>%
  unique() 

czi_combined_formatted1 <- inner_join(czi_combined_formatted, combined_software_orgs, by=c("most_popular_doi"="doi")) 
czi_combined_formatted2 <- inner_join(czi_combined_formatted, combined_software_orgs, by=c("most_popular_pmid"="pmid")) 
czi_combined_formatted <- full_join(czi_combined_formatted1, czi_combined_formatted2)
czi_combined_formatted <- czi_combined_formatted %>% filter(!is.na(institution_ror)) # removing rows with no ror mapping via openalex

# Compare ROR info to RRID dataset ----
czi_software_ror_mapped <- czi_combined_formatted %>%
  select(mention, pmid, ext.link, most_popular_doi, institution_ror, au_display_name, au_orcid, author_position, au_affiliation_raw) %>%
  unique() %>%
  rename(doi = most_popular_doi) %>%
  rename(software_name = mention) %>%
  mutate(gh_repo = ifelse(grepl("github",ext.link), paste(ext.link), "")) %>%
  mutate(other_repo = ifelse(grepl("github",ext.link), "", paste(ext.link))) %>%
  select(-ext.link) %>%
  unique()
  

write.csv(czi_software_ror_mapped, "czi_software_ror_mapped.csv", row.names = FALSE)



