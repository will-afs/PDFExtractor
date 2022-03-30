from tests.conftest import (
                        DATA_FILE_PATH,
                        PDF_URI,
                        NOT_FOUND_PDF_URI,
                        NOT_PDF_URI,
                        PDF_DATA_REFERENCE_FILE_NAME,
                        PDF_CONTENT_REFERENCE_FILE_NAME,
                        PDF_METADATA_REFERENCE_FILE_NAME,
                        WRONG_PDF_URI,
                        COOLDOWN_MANAGER_URI,
                        APA_RAW_REF_VALUE,
                        UNKNOWN_RAW_REF_VALUE
)
from src.core.pdf_extractor_utils import (
    extract_pdf,
    extract_authors_from_apa_ref,
    extract_references_from_pdf_uri,
    predict_ref_style,
    extract_authors_from_ref,
    RefStyle                                         
)

import pytest
from unittest.mock import Mock

def test_extract_references_from_pdf_uri(mocker):
    # Check raises ValueError when uncorrect pdf_uri format
    with pytest.raises(ValueError):
        extract_references_from_pdf_uri(WRONG_PDF_URI, COOLDOWN_MANAGER_URI)
    # Check raise ConnectionRefusedError when no permission from CooldownManager
    mocker.patch('src.core.pdf_extractor_utils.get_permission_to_request_arxiv', return_value = False)
    with pytest.raises(ConnectionRefusedError):
        extract_references_from_pdf_uri(PDF_URI, COOLDOWN_MANAGER_URI)
    # Check success
    mocker.patch('src.core.pdf_extractor_utils.get_permission_to_request_arxiv', return_value = True)
    dummy_references_list = [{'authors':['Cheeseman, P.', 'Kanefsky, B.']}]
    mock = mocker.patch('src.core.pdf_extractor_utils.extract_references_from_url', return_value = dummy_references_list)
    assert extract_references_from_pdf_uri(PDF_URI, COOLDOWN_MANAGER_URI) == dummy_references_list
    # Check return empty list when error raised by extract_references_from_url
    mock = mocker.patch('src.core.pdf_extractor_utils.extract_references_from_url', return_value = '')
    mock.side_effect=Exception('foo')
    assert extract_references_from_pdf_uri(PDF_URI, COOLDOWN_MANAGER_URI) == []

def test_predict_ref_style():
    # Style APA
    raw_ref = APA_RAW_REF_VALUE
    assert predict_ref_style(raw_ref) == RefStyle.APA
    # Unknown style
    raw_ref = UNKNOWN_RAW_REF_VALUE
    assert predict_ref_style(raw_ref) == RefStyle.Unknown

def test_extract_pdf(pdf_metadatas_reference, clean_references_reference, refextract_references_reference, mocker):
    # Check when success
    pdf_metadata_id = 11
    mocker.patch('src.core.pdf_extractor_utils.extract_references_from_pdf_uri', return_value = refextract_references_reference)
    pdf_metadata = extract_pdf(pdf_metadatas_reference[pdf_metadata_id], COOLDOWN_MANAGER_URI)
    assert list(pdf_metadata.keys()) == ['uri', 'authors', 'title', 'references']
    assert pdf_metadata['uri'] == pdf_metadatas_reference[pdf_metadata_id]['uri']
    assert pdf_metadata['authors'] == pdf_metadatas_reference[pdf_metadata_id]['authors']
    assert pdf_metadata['title'] == pdf_metadatas_reference[pdf_metadata_id]['title']
    assert pdf_metadata['references'][pdf_metadata_id]['authors'] == [
        'Mitchell, D.',
        'Selman, B.',
        'Levesque, H.'
    ]
    # Check when no reference found
    mocker.patch('src.core.pdf_extractor_utils.extract_references_from_pdf_uri', return_value = [])
    pdf_metadata_id = 0
    pdf_metadata = extract_pdf(pdf_metadatas_reference[pdf_metadata_id], COOLDOWN_MANAGER_URI)
    assert pdf_metadata['uri'] == pdf_metadatas_reference[pdf_metadata_id]['uri']
    assert pdf_metadata['authors'] == pdf_metadatas_reference[pdf_metadata_id]['authors']
    assert pdf_metadata['title'] == pdf_metadatas_reference[pdf_metadata_id]['title']
    assert pdf_metadata['references'] == []
    # Check when unkown reference style
    mocker.patch('src.core.pdf_extractor_utils.predict_ref_style', RefStyle.Unknown)
    assert pdf_metadata['uri'] == pdf_metadatas_reference[pdf_metadata_id]['uri']
    assert pdf_metadata['authors'] == pdf_metadatas_reference[pdf_metadata_id]['authors']
    assert pdf_metadata['title'] == pdf_metadatas_reference[pdf_metadata_id]['title']
    assert pdf_metadata['references'] == []

def test_extract_authors_from_ref(mocker):
    # Checking with RefStyle.Unknown
    authors_list = extract_authors_from_ref(APA_RAW_REF_VALUE, RefStyle.Unknown)
    assert authors_list == []
    # Checking with RefStyle.APA
    dummy_authors = Mock()
    extract_authors_from_apa_ref_mock = mocker.patch('src.core.pdf_extractor_utils.extract_authors_from_apa_ref', return_value = dummy_authors)
    authors_list = extract_authors_from_ref(APA_RAW_REF_VALUE, RefStyle.APA)
    assert authors_list == dummy_authors
    # Checking Exception
    extract_authors_from_apa_ref_mock.side_effect=Exception('foo')
    authors_list = extract_authors_from_ref(APA_RAW_REF_VALUE, RefStyle.APA)
    assert authors_list == []

def test_extract_authors_from_apa_ref(refextract_references_reference):
    # Pattern to match : ' P. (1990)'
    raw_string = refextract_references_reference[23]['raw_ref'][0]
    assert extract_authors_from_apa_ref(raw_string) == [
        'Minton, S.', 
        'Johnston, M. D.',
        'Philips, A. B.',
        'Laird, P.'
        ]
    # Pattern to match : ' H. (1995b)'
    raw_string = refextract_references_reference[29]['raw_ref'][0]
    assert extract_authors_from_apa_ref(raw_string) == [
        'Selman, B.',
        'Kautz, H.'
    ]