from html.parser import HTMLParser

class HTMLLinkParser(HTMLParser):
    links = []

    def handle_starttag(self, tag, attrs):
        links = []
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])


class Parse:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def get_links(self):
        charset = self.raw_data.headers.get_content_charset()
        processed_data = self.raw_data.read().decode(charset)

        link_parser = HTMLLinkParser()
        link_parser.feed(processed_data)
        links = link_parser.links

        print(links)
