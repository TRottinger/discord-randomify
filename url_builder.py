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
