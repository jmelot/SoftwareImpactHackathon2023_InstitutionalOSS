How we pulled relevant READMEs from The Stack:

1. Ingest [The Stack](https://huggingface.co/datasets/bigcode/the-stack) into BigQuery `thestack.files` <-- already done at CSET

2. Filter to READMEs

```sql
SELECT
  DISTINCT hexsha,
  size,
  ext,
  lang,
  max_stars_repo_path AS file_path,
  max_stars_repo_name AS repo_name,
  max_stars_count AS star_count,
  content,
  max_line_length,
  alphanum_fraction
FROM
  thestack.files
where regexp_contains(max_stars_repo_path, r"(?i)^read\.?me\b")
```

3. Filter to READMEs with relevant keywords (222,408 rows):

```sql
create or replace table czi_hackathon.contains_institution as 
select 
  repo_name, 
  file_path, 
  content 
from thestack.readmes 
where (lower(content) like "%institute%") or (lower(content) like "%university%") or (lower(content) like "%school%")
```

4. Export to Google Cloud Storage, take sample of 5K repos and READMEs, put output in `stack_institution_readmes/sample.jsonl` 