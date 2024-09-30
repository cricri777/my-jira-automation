import logging
from urllib.parse import urlparse

import requests
from Tools.scripts.generate_opcode_h import header
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


def post_request(url: str, username: str, password: str, body: str):
    url_validate(url)
    logging.debug(f"POST request {url}")
    response = requests.post(url, auth=HTTPBasicAuth(username, password), data=body)
    if response.status_code == 200:
        return response.json()
    else:
        logging.warning(f"status code {response.status_code}, response={response.json()}")
        return response.json()


def post_request_bearer(url:str, bearer_token:str, prompt: str, data: dict):
    # TODO complete this
    url_validate(url)
    logging.debug(f"POST request bearer {url}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.debug("Response :", response.json())
        logging.debug(response.json()['choices'][0]['message']['content'])
    else:
        logging.warning("Error:", response.status_code, response.text)
    return response.json()


def url_validate(url_to_validate: str):
    result = urlparse(url_to_validate)
    is_url_valid = result.scheme and result.netloc
    if is_url_valid:
        logging.debug(f"valid URL={url_to_validate}")
    else:
        logging.warning(f"unvalid URL={url_to_validate}")

    return is_url_valid