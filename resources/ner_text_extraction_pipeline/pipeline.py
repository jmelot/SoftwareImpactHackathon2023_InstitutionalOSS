import argparse
import csv
import json
import os
import re
import requests
import torch

from multiprocessing.pool import Pool
from transformers import BertTokenizerFast, BertForTokenClassification


MAX_NER_INPUT_LEN = 128
ROR_URL = "https://api.ror.org/organizations"


def load_model(model_path):
    """
    Load NER model.
    Copied from https://github.com/ror-community/affiliation-matching-experimental/tree/main/ner_tests/inference

    :param model_path: Path of the model directory
    :return: Model object
    """

    model = BertForTokenClassification.from_pretrained(model_path)
    model = model.cpu()
    return model


def preprocess_input(tokenizer, ner_input):
    """
    Preprocess input for NER model.
    Copied from https://github.com/ror-community/affiliation-matching-experimental/tree/main/ner_tests/inference

    :param tokenizer: NER tokenizer object
    :param ner_input: A list of input tokens
    :return: Preprocessed input object
    """

    return tokenizer(
        ner_input,
        is_split_into_words=True,
        return_offsets_mapping=True,
        padding="max_length",
        truncation=True,
        max_length=MAX_NER_INPUT_LEN,
        return_tensors="pt",
    )


def ner_inference(model, preprocessed_input):
    """
    Perform the NER inference.
    Copied from https://github.com/ror-community/affiliation-matching-experimental/tree/main/ner_tests/inference

    :param model: NER model object
    :param preprocessed_input: Preprocessed input object
    :return: NER token predictions
    """

    ids = preprocessed_input["input_ids"]
    mask = preprocessed_input["attention_mask"]
    outputs = model(ids, attention_mask=mask)
    logits = outputs[0]
    active_logits = logits.view(-1, model.num_labels)
    predictions = torch.argmax(active_logits, axis=1)
    return predictions


def postprocess_output(ner_input, token_predictions):
    """
    Postprocess NER inference output
    Adapted from https://github.com/ror-community/affiliation-matching-experimental/tree/main/ner_tests/inference

    :param ner_input: Preprocessed input object
    :param token_predictions: NER raw predictions
    :return: Token prediction labels or None if no organisation was detected
    """

    # NER model assigns a label to every token in the input sequence. Possible labels are:
    # B-ORG - the first token of an organisation name (B stands for begin)
    # I-ORG - the subsequent token of an organisation name (I stands for inner)
    # B-LOC - the first token of a location entity
    # I-LOC - the subsequent token of a location entity
    # O - other token (not part of any entity)
    #
    # An entity labelled correctly will start with one token labelled as B-*,
    # followed by zero or more tokens labelled as I-*. Examples:
    # O O O B-ORG O O
    # O B-ORG I-ORG I-ORG O O B-LOC O
    ids_to_labels = {0: "B-ORG", 1: "I-ORG", 2: "O", 3: "B-LOC", 4: "I-LOC"}
    token_labels = [ids_to_labels[i] for i in token_predictions.cpu().numpy()]
    predictions = []
    for token_label, mapping in zip(
        token_labels, ner_input["offset_mapping"].squeeze().tolist()
    ):
        if mapping[0] == 0 and mapping[1] != 0:
            predictions.append(token_label)

    # If there is no B-ORG label in the sequence, it means that no organisation
    # name was detected.
    if "B-ORG" not in predictions:
        return None
    return predictions


def extract_organisation_names(tokenizer, model, text):
    """
    Extract organisation names from text using a NER model.
    Adapted from https://github.com/ror-community/affiliation-matching-experimental/tree/main/ner_tests/inference

    :param tokenizer: NER tokenizer object
    :param model: NER model object
    :param text: Input text
    :return: List of extracted organisation names
    """

    tokens = text.lower().split()
    names = set()

    # The NER model used here was trained on affiliation strings rather than
    # arbitrary text, and as such has a fairly low upper limit of the number
    # of input tokens (128). At the same time, our input data (GitHub repo
    # READMEs) will typically be much longer. To overcome this limitation,
    # we move a sliding window over the input text to obtain multiple shorter
    # substrings, and each of them is passed to the NER model separately. The
    # detected organisation names are then concatenated and returned.
    offset = 0
    while offset < len(tokens):
        tokens_chunk = tokens[offset : offset + MAX_NER_INPUT_LEN]
        preprocessed_input = preprocess_input(tokenizer, tokens_chunk)
        token_predictions = ner_inference(model, preprocessed_input)
        predictions = postprocess_output(preprocessed_input, token_predictions)

        if predictions is not None:
            organization_name = " ".join(
                w for p, w in zip(predictions, tokens_chunk) if p in ["B-ORG", "I-ORG"]
            )
            names.add(organization_name)

        # We move the sliding window by slightly less than the maximum NER
        # input length, so that the substrings passed to the NER model are
        # slightly overlapping. If the substrings were not overlapping,
        # we might miss those organisation names that happen to span over
        # two consecutive substrings.
        #
        # Example:
        #
        # ... You are from University of Gallifrey, are you not? ...
        # ------ substring #1 ------| |------ non-overlapping substring #2
        #         |---------- overlapping substring #2 -------------------
        offset += MAX_NER_INPUT_LEN - 8

    return list(names)


def get_ror_id(org_name):
    """
    Using ROR's affiliation matching service, map organisation name to ROR ID.

    :param org_name: Organisation name
    :return: ROR ID or None
    """

    # the name has to contain at least one letter
    if org_name is None or not re.search("[a-zA-Z]", org_name):
        return None

    # remove characters that cause ROR API to return 500
    org_name = re.sub('[{."\\\\]', "", org_name)

    matched = requests.get(ROR_URL, {"affiliation": org_name})
    if matched.status_code != 200:
        print(
            f"ROR API request failed; input {org_name}, status code: "
            + f"{matched.status_code}, content: {matched.content}"
        )
        return None
    matched = matched.json()

    for matched_org in matched["items"]:
        if matched_org["chosen"]:
            return matched_org["organization"]["id"]
    return None


def generate_readmes(input_dir):
    """
    Generator of README objects.

    :param input_dir: Input directory
    :return: A sequence of README objects
    """

    for f_name in os.listdir(input_dir):
        f_path = os.path.join(input_dir, f_name)
        with open(f_path, "r") as f:
            for line in f:
                yield json.loads(line)


def extract_ror_ids_from_readme(data):
    """
    Extract ROR IDs from a given README object.

    :param data: A tuple containing sequence number, README object, NER
        tokenizer and model.
    :return: A tuple containing repository name and extracted organisation
        names and ROR IDs
    """

    i, readme, tokenizer, model = data
    print(f"Processing README #{i} {readme['repo_name']}")

    org_names = extract_organisation_names(tokenizer, model, readme["content"])
    ror_ids = [get_ror_id(org_name) for org_name in org_names]
    names_ids = [(n, r) for n, r in zip(org_names, ror_ids) if r is not None]
    return readme["repo_name"], names_ids


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input directory path", required=True)
    parser.add_argument("--model", help="NER model directory path", required=True)
    parser.add_argument("--threads", help="number of threads", type=int, default=4)
    parser.add_argument("--chunk", help="imap chunk size", type=int, default=16)
    parser.add_argument("--output", help="output CSV file", required=True)
    args = parser.parse_args()

    model = load_model(args.model)
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
    readme_generator = generate_readmes(args.input)

    with open(args.output, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["repo_name", "org_name", "ror_id"])
        with Pool(args.threads) as p:
            args_generator = map(
                lambda r: (r[0], r[1], tokenizer, model), enumerate(readme_generator)
            )
            for repo_name, names_ids in p.imap(
                extract_ror_ids_from_readme, args_generator, args.chunk
            ):
                for org_name, ror_id in names_ids:
                    writer.writerow([repo_name, org_name, ror_id])
