from html.parser import HTMLParser
import re

class HTMLResponseParser(HTMLParser):
    links = []
    data = []

    def handle_starttag(self, tag, attrs):
        links = []
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

    def handle_data(self, data):
        self.data.append(data)


class Parse:
    link_ignore_patterns = []

    def __init__(self):
        with open('ignore.txt', 'r') as file:
            for line in file:
                self.link_ignore_patterns.append(line.strip())
        self.link_ignore_patterns = self.link_ignore_patterns[1:]

    def get_links(self, rawData):
        charset = rawData.headers.get_content_charset()
        if charset != None:
            processedData = rawData.read().decode(charset)
        else:
            processedData = rawData.read().decode('utf-8')

        responseParser = HTMLResponseParser()

        # dunno why this needs to happen
        responseParser.links = []
        responseParser.data = []

        responseParser.feed(processedData)

        return {'links': responseParser.links, 'data': responseParser.data}

    def match(self, rawData, searchTerm):
        template = re.compile(searchTerm)
        if template.search(rawData):
            return True
        else:
            return False

    def skip_link(self, link):
        for pattern in self.link_ignore_patterns:
            template = re.compile(pattern)
            if template.search(link):
                return True
            else:
                continue
        return False
        
