import requests


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
