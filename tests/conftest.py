""""This file contains setup functions called fixtures that each test will use"""
import configparser
import json
import pytest


config = configparser.ConfigParser()
TESTS_DIRECTORY = "./tests"
config.read(TESTS_DIRECTORY + "/setup.cfg")

# [PATHS]
DATA_FILE_PATH = config["PATHS"]["DATA_FILE_PATH"]

# [PDF URIs]
PDF_URI = config["PDF URIs"]["PDF_URI"]
NOT_FOUND_PDF_URI = config["PDF URIs"]["NOT_FOUND_PDF_URI"]
NOT_PDF_URI = config["PDF URIs"]["NOT_PDF_URI"]
WRONG_PDF_URI = config["PDF URIs"]["WRONG_PDF_URI"]

# [REFERENCES]
PDF_DATA_REFERENCE_FILE_NAME = config["REFERENCES"]["PDF_DATA_REFERENCE_FILE_NAME"]
PDF_CONTENT_REFERENCE_FILE_NAME = config["REFERENCES"]["PDF_CONTENT_REFERENCE_FILE_NAME"]
PDF_METADATA_REFERENCE_FILE_NAME = config["REFERENCES"]["PDF_METADATA_REFERENCE_FILE_NAME"]
FEED_DATA_REFERENCE_FILE_NAME = config["REFERENCES"]["FEED_DATA_REFERENCE_FILE_NAME"]
PDF_METADATAS_REFERENCE_FILE_NAME = config["REFERENCES"]["PDF_METADATAS_REFERENCE_FILE_NAME"]
CLEAN_REFERENCES_REFERENCE_FILE_NAME = config["REFERENCES"]["CLEAN_REFERENCES_REFERENCE_FILE_NAME"]
REFEXTRACT_REFERENCES_REFERENCE_FILE_NAME = config["REFERENCES"]["REFEXTRACT_REFERENCES_REFERENCE_FILE_NAME"]
APA_RAW_REF_VALUE = config["REFERENCES"]["APA_RAW_REF_VALUE"]
UNKNOWN_RAW_REF_VALUE = config["REFERENCES"]["UNKNOWN_RAW_REF_VALUE"]
EXTRACT_PDF_RESULT_REFERENCE = config["REFERENCES"]["EXTRACT_PDF_RESULT_REFERENCE"]


@pytest.fixture
def pdf_metadatas_reference():
    with open(DATA_FILE_PATH + PDF_METADATAS_REFERENCE_FILE_NAME, "r") as pdf_metadatas_reference_file:
        pdf_metadatas_reference = json.load(pdf_metadatas_reference_file)
    return pdf_metadatas_reference

@pytest.fixture
def clean_references_reference():
    with open(DATA_FILE_PATH + CLEAN_REFERENCES_REFERENCE_FILE_NAME, "r") as clean_references_reference_file:
        clean_references_reference = json.load(clean_references_reference_file)
    return clean_references_reference

@pytest.fixture
def refextract_references_reference():
    with open(DATA_FILE_PATH + REFEXTRACT_REFERENCES_REFERENCE_FILE_NAME, "r") as refextract_references_reference_file:
        refextract_references_reference = json.load(refextract_references_reference_file)
    return refextract_references_reference

@pytest.fixture
def extract_pdf_result_reference():
    with open(DATA_FILE_PATH + EXTRACT_PDF_RESULT_REFERENCE, "r") as extract_pdf_result_reference_file:
        extract_pdf_result_reference = json.load(extract_pdf_result_reference_file)
    return extract_pdf_result_reference

@pytest.fixture
def correct_event():
    return {
        "uri":"http://arxiv.org/pdf/cs/9308101v1",
        "title":"Dynamic Backtracking",
        "authors": [
            "Matthew L. Ginsberg",
        ]
    }
    
