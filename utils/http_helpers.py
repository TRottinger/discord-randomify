import requests

import logging

log = logging.getLogger(__name__)


def handle_status_code(response):
    if response.status_code == 400:
        val = 'Bad Request'
    elif response.status_code == 401:
        val = 'Unauthorized'
    elif response.status_code == 403:
        val = 'Forbidden'
    elif response.status_code == 404:
        val = 'Not Found'
    elif response.status_code == 200:
        val = 'OK'
    elif response.status_code == 500:
        val = 'Server Error'
    elif response.status_code == 503:
        val = 'Service Unavailable'
    else:
        val = 'Unknown'
    return val


# Abstracting to function because I may need to add health checks to it
def send_get_request(query_url, headers):
    response = requests.get(query_url, headers=headers)
    return response


def get_access_token(client_id, client_secret, url):
    headers = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=headers)

    access_token = response.json()['access_token']
    if access_token == '':
        log.warning('Bad access token')

    return access_token


def form_auth_headers(client_id, access_token):
    headers = {
        'client-id': client_id,
        'Authorization': 'Bearer ' + access_token
    }
    return headers
