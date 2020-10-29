import random
import requests


def get_random_query():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    words = response.content.splitlines()
    return random.choice(words).decode('UTF-8')
