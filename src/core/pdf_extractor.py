from src.core.pdf_extractor_utils import extract_pdf

from refextract.references.errors import FullTextNotAvailableError, UnknownDocumentTypeError
import toml
import traceback
from urllib.error import URLError
import validators


def lambda_handler(event, context):
    # 1 - parse query parameters
    try:
        if not validators.url(event['uri']):
            status = 400
            message = "Incorrect format for \'uri\' argument. Expected an url-like string"
            body = {}
        elif type(event['title'])!=str:
            status = 400
            message = "Incorrect format for \'title\' argument. Expected a string"
            body = {}
        elif type(event['authors'])!=list:
            status = 400
            message = "Incorrect format for \'authors\' argument. Expected a list of strings"
            body = {}
        else:  
            pdf_metadata = {
                        'uri':event['uri'],
                        'title':event['title'],
                        'authors':event['authors'],
                        'references':[]
                    }
            # 2 - construct the body of the response object
            try:
                pdf_dict = extract_pdf(pdf_metadata)
            except URLError as err: # Cooldown Manager not reachable
                status = 502
                message = str(err)
                body = {}
            except ConnectionRefusedError:
                status = 502
                message = 'Internal service CooldownManager did not allow to request ArXiv.org services'
                body = {}
            except FullTextNotAvailableError:
                status = 502
                message = 'Could not reach \''+pdf_metadata['uri']+'\' to fetch the PDF'
                body = {}
            except UnknownDocumentTypeError:
                status = 400
                message = 'Please provide an URI pointing to a PDF'
                body = {}
            except Exception as exc:
                status = 500
                message = 'An internal error occured: '+str(exc)+', traceback:\n{}'.format(traceback.format_exc())
                body = {}
            else:
                status = 200
                message = 'Success'
                body = pdf_dict
    except KeyError:
        status = 400
        message = "Please provide correct schema in POST body: \
        {\"uri\":<str>,\"title\":<str>,\"authors\":<list<str>>}"
        body = {}
    # 3 - construct the http response
    http_response = {
        'status':status,
        'headers':{
            'Content-Type':'application/json'
        },
        'message':message,
        'body': body

    }
    # 4 - return the http response
    return http_response

if __name__ == '__main__':
    event = {
        "uri": "http://arxiv.org/pdf/cs/9308102v1",
        "title": "Dynamic Backtracking",
        "authors": [
            "M. L. Ginsberg"
        ]
    }
    print(lambda_handler(event,''))