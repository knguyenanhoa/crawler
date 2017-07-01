import urllib.request
from parse import Parse


def explore(url):
    return urllib.request.urlopen(url)


# Main
url = 'https://www.google.com'

raw_data = explore(url)
parser = Parse(raw_data)
links = parser.get_links()


