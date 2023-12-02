# Affiliations joining OpenAIRE data (DOI to RORid) and CZI mentions data (DOI to repositories)

1. Download [CZI mentions dataset](https://datadryad.org/stash/dataset/doi:10.5061/dryad.6wwpzgn2c)

2. Prepare input data using:
```
python3 prepare <czi mentions data zip file downloaded in step.1>
```

3. Ensure that your machine has connection to the internet; OpenAIRE data are downloaded from the `pipeline.py` script

4. Note that the code is configured to produce a sample output. 
If you want to produce the full output, you have to change the value of the variable `OPENAIRE_DOI_TO_RORID_INPUT_FILE` in `config.properties`, i.e., comment line 2 and uncomment line 5
For that you will need a machine with large memory (the full output was produced with a machine with 256GB of RAM)

5. Execute pipeline with:

```
python3 pipeline.py
```

6. The output file is produced under the `output/` folder

