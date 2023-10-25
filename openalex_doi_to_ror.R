# simple demo script for image J example 
library(openalexR)

doi_example <- "https://doi.org/10.1038/nmeth.2089"

# openalex connection
paper <-  oa_fetch(
  entity = "works",
  doi = doi_example,
  verbose = TRUE
)

# see ROR nested in author list
paper$author

