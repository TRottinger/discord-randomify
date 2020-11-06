import re


# Function to build a url for http request
# Expects args to be in the format of header=value (str)
def build_url(url, *argv):
    """
    Builds a url with query
    Expects format of key=value
    :param url:
    :param argv:
    :return:
    """
    if len(argv) == 0:
        return url
    url += '?'
    
    # start building http request
    for arg in argv:
        if re.fullmatch("^[^=]*=[^=]*$", arg) is not None:
            url += arg
            url += '&'
    url = url[:-1]
    
    return url


def build_url_kwargs(url, **kwargs):
    """
    Builds a url with query and kwargs
    Expects kwargs to be in the format of key=value
    :param url:
    :param kwargs:
    :return:
    """
    if len(kwargs) == 0:
        return url
    url += '?'
    for key, val in kwargs.items():
            url += key + '=' + val
            url += '&'
    url = url[:-1]

    return url


def build_twitch_streams_url(url, first, game_id, after):
    """
    Builds streams url for Twitch based on different parameters
    :param url:
    :param first:
    :param game_id:
    :param after:
    :return:
    """
    return_url = ''
    if game_id != '0':
        if after != '0':
            return_url = build_url(url, "first=" + first, "game_id=" + game_id, "after=" + after)
        else:
            return_url = build_url(url, "first=" + first, "game_id=" + game_id)
    else:
        if after != '0':
            return_url = build_url(url, "first=" + first, "after=" + after)
        else:
            return_url = build_url(url, "first=" + first)

    return return_url
