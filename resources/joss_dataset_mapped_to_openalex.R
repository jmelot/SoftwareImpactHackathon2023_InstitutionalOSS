# bring in joss titles / dois
joss <- jsonlite::fromJSON("joss_repo_to_doi_and_title.json")

joss_df <- as.data.frame(do.call(rbind, joss))
joss_df <- tibble::rownames_to_column(joss_df, "gh_repo")
joss_df <- as.data.frame(joss_df)
joss_df <- joss_df %>% mutate(doi = as.character(doi))

# Extract the DOIs
valid_dois <- unlist(joss_df$doi)

# Fetch papers using lapply
papers <- lapply(valid_dois, function(doi) {
  tryCatch({
    paper <- oa_fetch(entity = "works", identifier = doi)
    if (is.data.frame(paper)) return(paper)
  }, error = function(e) NULL)
})

# Bind the resulting data frames together
res_doi <- do.call(plyr::rbind.fill, papers)

res_doi_orgs <- res_doi %>%
  select(author, doi, ids, publication_year) %>%
  tidyr::unnest(author) %>%
  tidyr::unnest(ids) %>%
  mutate(pmid = ifelse(grepl("https://pubmed.ncbi.nlm.nih.gov/", ids), paste(ids), "")) %>%
  select(pmid, doi, publication_year, institution_ror, au_display_name, au_orcid, author_position, au_affiliation_raw) %>%
  unique()

res_doi_orgs <- res_doi_orgs %>% left_join(joss_df)
res_doi_orgs <- as.data.frame(res_doi_orgs) 
res_doi_orgs <- res_doi_orgs %>%
 mutate(software_name = stringr::str_extract(title, ".*\\:")) %>% #suggest name from title
  mutate(software_name = ifelse(is.na(software_name), sub(".*/", "", gh_repo), software_name)) %>% #if not clear, suggest name from repo
  mutate(software_name = gsub("\\:", "", software_name)) %>%
  mutate(pmid = gsub("https://pubmed.ncbi.nlm.nih.gov/", "", pmid)) %>%
  select(-title)
  

write.csv(res_doi_orgs, "joss_300_papers_openalex.csv", row.names = FALSE)


