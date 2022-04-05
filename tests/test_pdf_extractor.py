from src.core.pdf_extractor import lambda_handler
from tests.conftest import WRONG_PDF_URI

import pytest
from refextract.references.errors import UnknownDocumentTypeError

def test_lambda_handler(mocker, extract_pdf_result_reference, correct_event):
    # Correct event
    mocker.patch('src.core.pdf_extractor.extract_pdf', return_value = extract_pdf_result_reference)
    response = lambda_handler(correct_event,'')
    expected_response = {
        'status':200,
        'headers':{
            'Content-Type':'application/json'
        },
        'message':'Success',
        'body': extract_pdf_result_reference
    }
    assert response == expected_response
    # Wrong 'uri', 'title' and 'authors' arguments
    incorrect_events={
        'event_w_incorrect_uri':correct_event,
        'event_w_incorrect_title':correct_event,
        'event_w_incorrect_authors':correct_event
    }
    incorrect_events['event_w_incorrect_uri']['uri']=WRONG_PDF_URI
    incorrect_events['event_w_incorrect_uri']['title']=[]
    incorrect_events['event_w_incorrect_uri']['authors']=''

    for key, _ in incorrect_events.items():
        response = lambda_handler(incorrect_events[key],'')
        assert response['status'] == 400
        assert len(response['message']) != 0
        assert response['body'] == {}
    # Facing UnknownDocumentTypeError
    mocker.patch(
        'src.core.pdf_extractor.extract_pdf',
        side_effects = UnknownDocumentTypeError
    )
    response = lambda_handler(correct_event,'')
    expected_response = {
        'status':400,
        'headers':{
            'Content-Type':'application/json'
        },
        'message':'Please provide an URI pointing to a PDF',
        'body': {}
    }