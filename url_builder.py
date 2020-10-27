# Function to build a url for http request
# Expects args to be in the format of header=value (str)

def build_url(url, *argv):
    if len(argv) == 0:
        return url

    # start building http request
    first = True
    url_builder = url + '?'
    for arg in argv:
        if not first:
            url_builder += '&'
        else:
            first = False
        url_builder += arg

    return url_builder


def build_twitch_streams_url(url, first, game_id, after):
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