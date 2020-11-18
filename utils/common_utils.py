import random
import requests


def setup_words(url=None):
    response = requests.get(url)
    words = response.content.splitlines()
    return words


class RandomQuery:
    def __init__(self, url=None, strict_url=None, first_name_url=None):
        if url is None:
            url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        if strict_url is None:
            strict_url = "https://www.mit.edu/~ecprice/wordlist.10000"
        if first_name_url is None:
            first_name_url = "https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.txt"
        self.words = setup_words(url)
        self.strict_words = setup_words(strict_url)
        self.first_names = setup_words(first_name_url)

    def get_random_query(self):
        """
        Returns a random word to use in search queries.
        :param url:
        :return:
        """
        if len(self.words) == 0:
            return "random"
        else:
            return random.choice(self.words).decode('UTF-8')

    def get_random_query_strict(self):
        """
        Returns a random word to use in search queries from the strictly words list
        :return:
        """
        if len(self.strict_words) == 0:
            return "random"
        else:
            return random.choice(self.strict_words).decode('UTF-8')

    def get_random_first_name(self):
        if len(self.strict_words) == 0:
            return "Tim"
        else:
            return random.choice(self.first_names).decode('UTF-8')

