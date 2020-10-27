# Function to build a url for http request
# Expects args to be in the format of header=value (str)

def build_url(url, *argv):
    if len(argv) == 0:
        return url
    url += '?'
    
    # start building http request
    for arg in argv:
        url += arg
        url += '&'
    url = url[:-1]
    
    return url


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