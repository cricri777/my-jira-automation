from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth

from lib import log

logger = log.get_logger(__name__)

def get_request(url: str, username, password) -> dict:
    url_validate(url)
    logger.debug(f"GET request {url}")
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        logger.warning(f"get request: status={response.status_code}, response={response.json()}")
        return response.json()


def post_request(url: str, username: str, password: str, body: dict) -> dict:
    url_validate(url)
    logger.debug(f"POST request {url}")
    response = requests.post(url, auth=HTTPBasicAuth(username, password), json=body)
    if 300 < response.status_code >= 200:
        return response.json()
    else:
        logger.warning(f"post request: status={response.status_code}, response={response.json()}")
        return response.json()


def post_request_bearer(url:str, bearer_token:str, data: dict) -> dict:
    url_validate(url)
    logger.debug(f"POST request with bearer {url}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logger.debug(f"Response : {response.json()}")
    else:
        logger.warning(f"post request bearer: status={response.status_code}, response={response.json()}")
    return response.json()

def get_request_bearer(url:str, bearer_token:str, params:dict) -> dict:
    url_validate(url)
    logger.debug(f"GET request with bearer {url}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
    response = requests.get(url, headers=headers, params=params)
    if 300 > response.status_code >= 200:
        logger.debug(f"Response : {response.json()}")
    else:
        logger.warning(f"get request with bearer: status={response.status_code}, response={response.json()}")
    return response.json()


def url_validate(url_to_validate: str):
    result = urlparse(url_to_validate)
    is_url_valid = result.scheme and result.netloc
    if is_url_valid:
        logger.debug(f"valid URL={url_to_validate}")
    else:
        logger.warning(f"unvalid URL={url_to_validate}")

    return is_url_valid