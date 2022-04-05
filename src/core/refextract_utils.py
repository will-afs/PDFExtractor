import os
import requests
from refextract import extract_references_from_file
from refextract.references.api import (
    get_plaintext_document_body,
    extract_references_from_fulltext,
    parse_references,
    extract_texkeys_and_urls_from_pdf,
    update_reference_with_urls
    )
import magic
from refextract.references.errors import FullTextNotAvailableError
from tempfile import mkstemp


def extract_references_from_url(url, headers=None, chunk_size=1024, **kwargs):
    """Extract references from the pdf specified in the url.

    The first parameter is the URL of the file.
    It returns a list of parsed references.

    It raises FullTextNotAvailableError if the URL gives a 404,
    UnknownDocumentTypeError if it is not a PDF or plain text.

    The standard reference format is: {title} {volume} ({year}) {page}.

    E.g. you can change that by passing the reference_format:

    >>> extract_references_from_url(path, reference_format="{title},{volume},{page}")

    If you want to also link each reference to some other resource (like a record),
    you can provide a linker_callback function to be executed for every reference
    element found.

    To override KBs for journal names etc., use ``override_kbs_files``:

    >>> extract_references_from_url(path, override_kbs_files={'journals': 'my/path/to.kb'})

    """
    # Get temporary filepath to download to
    filename, filepath = mkstemp(
        suffix=u"_{0}".format(os.path.basename(url)),
    )
    os.close(filename)
    
    try:
        req = requests.get(
            url=url,
            headers=headers,
            stream=True,
            timeout=10
        )
        req.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        raise FullTextNotAvailableError(f"URL not found: '{url}'") from exc
    else:
        with open(filepath, 'wb') as f:
            for chunk in req.iter_content(chunk_size):
                f.write(chunk)
        # try:
        #     with open(filepath, "rb") as f:
        #         bytes = []
        #         byte = f.read(1)
        #         while byte:
        #             # Do stuff with byte.
        #             bytes.append(byte)
        #             byte = f.read(1)
        # except IOError:
        #     print('Error While Opening the file!')  
        references = extract_references_from_file(filepath, **kwargs)
        # raise Exception("References: {}".format(references))
    finally:
        os.remove(filepath)
    return references

def extract_references_from_file(path,
                                 recid=None,
                                 reference_format=u"{title} {volume} ({year}) {page}",
                                 linker_callback=None,
                                 override_kbs_files=None):
    """Extract references from a local pdf file.

    The first parameter is the path to the file.
    It returns a list of parsed references.
    It raises FullTextNotAvailableError if the file does not exist,
    UnknownDocumentTypeError if it is not a PDF or plain text.

    The standard reference format is: {title} {volume} ({year}) {page}.

    E.g. you can change that by passing the reference_format:

    >>> extract_references_from_file(path, reference_format=u"{title},{volume},{page}")

    If you want to also link each reference to some other resource (like a record),
    you can provide a linker_callback function to be executed for every reference
    element found.

    To override KBs for journal names etc., use ``override_kbs_files``:

    >>> extract_references_from_file(path, override_kbs_files={'journals': 'my/path/to.kb'})

    """
    if not os.path.isfile(path):
        raise FullTextNotAvailableError(u"File not found: '{0}'".format(path))

    docbody = get_plaintext_document_body(path)
    reflines, dummy, dummy = extract_references_from_fulltext(docbody)
    if not reflines:
        docbody = get_plaintext_document_body(path, keep_layout=True)
        reflines, dummy, dummy = extract_references_from_fulltext(docbody)

    parsed_refs, stats = parse_references(
        reflines,
        recid=recid,
        reference_format=reference_format,
        linker_callback=linker_callback,
        override_kbs_files=override_kbs_files,
    )

    if magic.from_file(path, mime=True) == "application/pdf":
        extracted_texkeys_urls = extract_texkeys_and_urls_from_pdf(path)
        if len(extracted_texkeys_urls) == len(parsed_refs):
            parsed_refs_updated = []
            for ref, ref_texkey_urls in zip(parsed_refs, extracted_texkeys_urls):
                update_reference_with_urls(ref, ref_texkey_urls.get('urls', []))
                parsed_refs_updated.append(dict(ref, texkey=[ref_texkey_urls['texkey']]))

            return parsed_refs_updated
    return parsed_refs