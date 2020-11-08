import random
import requests


def get_random_query(url=None):
    """
    Returns a random word to use in search queries.
    :param url:
    :return:
    """
    if url is None:
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    else:
        word_site = url
    response = requests.get(word_site)
    words = response.content.splitlines()
    if len(words) == 0:
        return "random"
    else:
        return random.choice(words).decode('UTF-8')
