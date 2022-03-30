from src.cooldown_manager_utils import get_permission_to_request_arxiv

from tests.conftest import COOLDOWN_MANAGER_URI

def test_get_permission_to_request_arxiv(mocker):
    # Success
    mocker.patch('src.cooldown_manager_utils.urllib.request.urlopen', return_value = True)
    assert get_permission_to_request_arxiv(COOLDOWN_MANAGER_URI)
    # Failure
    mocker.patch('src.cooldown_manager_utils.urllib.request.urlopen', return_value = False)
    assert not get_permission_to_request_arxiv(COOLDOWN_MANAGER_URI)