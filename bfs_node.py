# Std lib
import urllib.request
import urllib.parse

# Modules
from parse import Parse

class BFSNode:
    interestingLinks = []

    def __init__(self):
        return None

    def go_to(self, url):
        print(url)
        try:
            return urllib.request.urlopen(url)
        except ValueError as error:
            print(error)
            return None
        except urllib.error.HTTPError:
            print('HTTPError')
            return None

    def parse(self, rawData):
        parser = Parse()
        return parser.get_links(rawData)

    def process_data(self, data, searchTerms, currentLink):
        parser = Parse()
        interest = 0
        for d in data:
            for term in searchTerms: 
                if parser.match(d, term):
                    interest += 1
                else:
                    continue

        if interest > 0 and currentLink not in self.interestingLinks:
            self.interestingLinks.append(currentLink)

    def explore(self, params):
        discoveredLinks = []

        seedLink = params['seedLink']
        searchTerms = params['searchTerms']
        self.interestingLinks = params['interestingLinks']
        maxLinks = params['maxLinks']
        fixUrl = params['fixUrl']
        newLinks = params['newLinks']

        for link in newLinks:
            if fixUrl == 'true':
                link = urllib.parse.urljoin(seedLink, link)
            rawData = self.go_to(link)

            if rawData != None:
                parsedResult = self.parse(rawData)

                self.process_data(parsedResult['data'], searchTerms, link)
                discoveredLinks.extend(parsedResult['links'][:maxLinks])

        return discoveredLinks

