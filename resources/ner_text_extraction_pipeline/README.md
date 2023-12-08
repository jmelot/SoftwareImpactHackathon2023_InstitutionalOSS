# Extracting the organisation information from READMEs

This pipeline takes the content of software READMEs on the input, runs Named Entity Recognition on them to extract the organisation names, and finally uses ROR's affiliation matching to map the organisation names to ROR IDs.

## Extracting READMEs

As input, we used READMEs extracted from The Stack:

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

A sample of 5K READMEs is available [here](stack_readmes/sample.jsonl).

## Extracting and mapping organization names

1. Download the NER model from [huggingface](https://huggingface.co/adambuttrick/ner-test-bert-base-uncased-finetuned-500K-AdamW-3-epoch-locations).

2. Run [pipeline.py](pipeline.py) script to extract organisation names and map them to ROR IDs:

```
python pipeline.py --input <stack READMEs dir> --model <NER model dir> --output <output file> [--threads <number of threads>] [--chunk <size of the imap chunk>]
```

The NER model is responsible for extracting organisation names from text. It was adapted from [this tool](https://github.com/ror-community/affiliation-matching-experimental/tree/main/ner_tests/inference).

The script uses ROR's affiliation matching service to map extracted organisation names to ROR IDs.

