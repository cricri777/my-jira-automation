from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth

from lib import log

logger = log.get_logger(__name__)

def get_request(url: str, username, password) -> dict:
    """
    :param url: URL to which the GET request is sent.
    :param username: Username for HTTP Basic Authentication.
    :param password: Password for HTTP Basic Authentication.
    :return: Parsed JSON response from the GET request if the status code is 200,
             else logs the warning and returns the JSON response.
    :return: dict
    """
    url_validate(url)
    logger.debug(f"GET request {url}")
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        logger.warning(f"get request: status={response.status_code}, response={response.json()}")
        return response.json()


def post_request(url: str, username: str, password: str, body: dict) -> dict:
    """
    :param url: target URL for the POST request.
    :param username: username for basic HTTP authentication.
    :param password: password for basic HTTP authentication.
    :param body: JSON payload to include in the POST request body.
    :return: JSON response from the server as a dictionary.
    """
    url_validate(url)
    logger.debug(f"POST request {url}")
    response = requests.post(url, auth=HTTPBasicAuth(username, password), json=body)
    if 300 > response.status_code >= 200:
        return response.json()
    else:
        logger.warning(f"post request: status={response.status_code}, response={response.json()}")
        return response.json()


def post_request_bearer(url:str, bearer_token:str, data: dict) -> dict:
    """
    :param url: The URL to which the POST request is to be sent.
    :param bearer_token: The Bearer token used for authorization.
    :param data: The payload to be sent in the post request, in dictionary format.
    :return: A dictionary containing the JSON response from the server.
    """
    url_validate(url)
    logger.debug(f"POST request with bearer {url}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
    response = requests.post(url, headers=headers, json=data)
    if 300 > response.status_code >= 200:
        logger.debug(f"Response : {response.json()}")
    else:
        logger.warning(f"post request bearer: status={response.status_code}, response={response.json()}")
    return response.json()

def get_request_bearer(url:str, bearer_token:str, params:dict) -> dict:
    """
    :param url: The endpoint URL to which the GET request is sent.
    :param bearer_token: The Bearer token used for authorization.
    :param params: Dictionary of query parameters to append to the URL.
    :return: The JSON response from the GET request as a dictionary.
    """
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
    """
    :param url_to_validate: The URL string to be validated.
    :return: Boolean indicating whether the URL is valid or not.
    """
    result = urlparse(url_to_validate)
    is_url_valid = result.scheme and result.netloc
    if is_url_valid:
        logger.debug(f"valid URL={url_to_validate}")
    else:
        logger.warning(f"unvalid URL={url_to_validate}")

    return is_url_valid