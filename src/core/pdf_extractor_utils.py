from src.cooldown_manager_utils import get_permission_to_request_arxiv

from enum import Enum
import re
from refextract import extract_references_from_url
import validators

def extract_references_from_pdf_uri(pdf_uri:str, cooldown_manager_uri:str)->list:
    """Return the references of a PDF in a list. If none are found, return an empty list

    Parameters:
    pdf_uri (str) : the PDF URI. If not in a correct format, raise a ValueError
    cooldown_manager_uri (str) : the CooldownManager URI to ask permission before
    requesting arXiv.org services. If it refuses, raise a ConnectionRefusedError

    Returns:
    list: A list of the references found in the PDF
    """
    if not validators.url(pdf_uri):
        raise ValueError(
                            "Wrong URI format for 'pdf_uri' argument.\
                            Expected an url-like string. Example 'http://arxiv.org/pdf/cs/9308101v1'"
                        )
    elif get_permission_to_request_arxiv(cooldown_manager_uri):
        try:
            return extract_references_from_url(pdf_uri)
        except:
            return []
    else:
        raise ConnectionRefusedError('CooldownManager refused permission to connect to ArXiv.org')

def extract_pdf(pdf_metadata:dict, cooldown_manager_uri:str) -> dict:
    """Extract the references of a PDF and aggregates them to the PDF metadata

    Parameters:
    pdf_metadata (dict) : the PDF metadata (as: {
        'uri':str,
        'authors':list<str>,
        'title':str,
        'references': list<dict>,
    } with references: list<{'authors:list<str>}>)
    cooldown_manager_uri (str) : the URI through which ask permission to CooldownManager\
        to request ArXiv.org services

    Returns:
    dict: Text PDF metadata and references as a dictionnary
    """
    # 1 - Initialize the PDF dictionnary to return
    pdf_dict = {
        'uri':pdf_metadata['uri'],
        'authors':pdf_metadata['authors'],
        'title':pdf_metadata['title'],
        'references': [],

    }

    # 2 - Extract references
    extracted_references = extract_references_from_pdf_uri(pdf_metadata['uri'], cooldown_manager_uri)
    if len(extracted_references) == 0:
        return pdf_dict

    # 3 - Predict PDF References style
    ref_style = predict_ref_style(extracted_references[0]['raw_ref'][0])
    if ref_style == RefStyle.Unknown:
        print('Unkown reference style for article with URN:\'{}\''.format(pdf_metadata['uri']))
        return pdf_dict
    # 4 - Extract named entities from references
    for reference_dict in extracted_references:
        reference = {
            'authors':None
        }
        try:
            # Check whether refextract found any author in ref, but don't use it
            # Sometimes, refextract finds wrong authors in ref
            reference_dict['author'] 
        except: # no author found
            pass
        else:
            # Extract authors from raw_ref
            reference['authors'] = extract_authors_from_ref(reference_dict['raw_ref'][0], ref_style)
            if reference['authors']:
                pdf_dict['references'].append(reference)
            else:
                print('Could not extract author for ref:\'{}\''.format(reference_dict['raw_ref'][0]))
    return pdf_dict

class RefStyle(Enum):
    Unknown = 0
    APA = 1

def predict_ref_style(raw_ref)->RefStyle:
    """Predict the style of a reference (e.g. \'APA\', \'IEEE\', etc.)

    Parameters:
    raw_ref (str) : the string from which predict the style

    Returns:
    RefStyle: the style of reference
    """
    # Check APA
    pattern_author = re.compile(r"([a-z]|[A-Z])+\, [A-Z]\.")
    pattern_date = re.compile(r"\.\ \([1-2][0-9][0-9][0-9][a-z]*\)\.")
    if re.search(pattern_author, raw_ref, flags=0) \
        and re.search(pattern_date, raw_ref, flags=0):
        return RefStyle.APA
    # Unknown reference style
    return RefStyle.Unknown

def extract_authors_from_ref(raw_ref, ref_style)->list:
    """Extract the authors from a raw reference

    Parameters:
    raw_ref (str) : the string which might contain authors
    ref_style (RefStyle) : the style of the reference

    Returns:
    list: the list of authors as string elements
    """
    try:
        if ref_style == RefStyle.Unknown:
            return []
        elif ref_style == RefStyle.APA:
            return extract_authors_from_apa_ref(raw_ref)
    except:
        return []
    
def extract_authors_from_apa_ref(apa_ref:str)->list:
    """Extract the authors from an APA reference

    Parameters:
    authors_string (str) : the string which might contain authors
    
    Returns:
    list: the list of authors as string elements
    """
    authors = []
    # Searching pattern '. (1995)' or '. (1995b)' like
    pattern = re.compile(r"\.\ \([1-2][0-9][0-9][0-9][a-z]*\)") #  [A-Z]
    # 1 = len('.'), which should be included in authors_string
    end_authors_section_idx = re.search(pattern, apa_ref, flags=0).start() + 1
    authors_string = apa_ref[0:end_authors_section_idx]
    authors_string = authors_string.replace('& ', '')
    authors_string = authors_string.replace('.,', '..,')
    authors = authors_string.split('., ')
    return authors

if __name__ == '__main__':
    pdf_metadata = {
        "uri": "http://arxiv.org/pdf/cs/9308102v1",
        "title": "A Market-Oriented Programming Environment and its Application to\n  Distributed Multicommodity Flow Problems",
        "authors": ["M. P. Wellman"]
        }
    coooldown_manager_uri = "http://172.17.0.2:5000/"
    pdf_dict = extract_pdf(pdf_metadata, coooldown_manager_uri)
    
