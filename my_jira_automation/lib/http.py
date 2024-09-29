import logging
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth


def get_request(url: str, username, password):
    url_validate(url)
    logging.debug(f"GET request {url}")
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        logging.warning(f"status code {response.status_code}, response={response.json()}")
        return response.json()

def url_validate(url_to_validate: str):
    result = urlparse(url_to_validate)
    is_url_valid = result.scheme and result.netloc
    if is_url_valid:
        logging.debug(f"valid URL={url_to_validate}")
    else:
        logging.warning(f"unvalid URL={url_to_validate}")

    return is_url_valid