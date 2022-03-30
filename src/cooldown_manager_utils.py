import urllib
import validators


def get_permission_to_request_arxiv(cooldown_manager_uri:str):
    """Request permission to contact ArXiv.org API to the CooldownManager of the project

    Parameters:

    Returns:
    bool : True if the CooldownManager gave its permission, ConnectionRefusedError otherwise
    """

    if not validators.url(cooldown_manager_uri):
        raise ValueError(
                            "Wrong URI format for 'file_uri' argument.\
                            Expected an url-like string. Example 'http://172.17.0.2:5000/'"
                        )
    return urllib.request.urlopen(cooldown_manager_uri)