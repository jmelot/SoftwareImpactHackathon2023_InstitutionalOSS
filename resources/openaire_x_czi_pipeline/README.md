# Affiliations joining OpenAIRE data (DOI to RORid) and CZI mentions data (DOI to repositories)

1. Download [CZI mentions dataset](https://datadryad.org/stash/dataset/doi:10.5061/dryad.6wwpzgn2c)

2. Unzip it into the `input/` folder

3. Rename the unzipped folder into `czi_mentions_data` or edit the value of variable `CZI_DATA_DIR` in `config.properties` file.

4. Untar `raw.tar.gz` and `linked.tar.gz` files in `input/czi_mentions_data/` folder

```
tar -xvf input/czi_mentions_data/raw.tar.gz -C input/czi_mentions_data/
tar -xvf input/czi_mentions_data/linked.tar.gz -C input/czi_mentions_data/
```

5. Ensure that your machine has connection to the internet; OpenAIRE data are downloaded from the `pipeline.py` script

6. Parameter values are set in the `config.properties` file
Note that the code is set up to produce a sample output. 
If you want to produce the full output, you have to change the value of the variable `OPENAIRE_DOI_TO_RORID_INPUT_FILE` in `config.properties`, i.e., comment line 2 and uncomment line 5
For that you will need a machine with large memory (the full output was produced with a machine with 256GB of RAM)

5. Execute pipeline with:

```
python3 pipeline.py
```

6. The output file is produced under the `output/` folder

