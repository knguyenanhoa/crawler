from html.parser import HTMLParser

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
    def __init__(self, rawData):
        self.rawData = rawData

    def get_links(self):
        charset = self.rawData.headers.get_content_charset()
        if charset != None:
            processedData = self.rawData.read().decode(charset)
        else:
            processedData = self.rawData.read().decode('utf-8')

        responseParser = HTMLResponseParser()
        responseParser.feed(processedData)

        # first 10 links only please...
        return {'links': responseParser.links[:20], 'data': responseParser.data}
