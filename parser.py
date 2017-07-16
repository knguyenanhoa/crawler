from html.parser import HTMLParser
import re
import logging

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


class ParseWebContent:
    link_ignore_patterns = []
    logger = logging.getLogger(__name__)

    def __init__(self):
        with open('ignore.txt', 'r') as file:
            for line in file:
                self.link_ignore_patterns.append(line.strip())
        self.link_ignore_patterns = self.link_ignore_patterns[1:]

    def get_links(self, rawData):
        self.logger.info('got here')
        processedData = ''
        charset = rawData.headers.get_content_charset()
        try:
            if charset == None:
                processedData = rawData.read().decode('utf-8')
            else:
                processedData = rawData.read().decode(charset)

        except UnicodeDecodeError as e:
            self.logger.error(e)

        responseParser = HTMLResponseParser()

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
        
