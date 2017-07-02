# Std lib
import urllib.request
import urllib.parse

# Modules
from parse import Parse

class DFSNode:
    interestingLinks = []
    parser = Parse()

    def __init__(self):
        return None

    def go_to(self, url):
        try:
            return urllib.request.urlopen(url)
        except ValueError as error:
            print(error)
            return None
        except urllib.error.HTTPError:
            print('HTTPError')
            return None

    def parse(self, rawData):
        return self.parser.get_links(rawData)

    def process_data(self, data, searchTerms, currentLink):
        interest = 0
        for d in data:
            for term in searchTerms: 
                if self.parser.match(d, term):
                    interest += 1
                else:
                    continue

        if interest > 0 and currentLink not in self.interestingLinks:
            self.interestingLinks.append(currentLink)

    def link_check_fail(self, link, currentLink):
        if self.parser.skip_link(link):
            return True
        if link == currentLink:
            return True
        return False

    def explore(self, params):
        searchTerms = params['searchTerms']
        depth = params['depth']
        maxDepth = params['maxDepth']
        currentLink = params['currentLink']
        maxLinks = params['maxLinks']
        fixUrl = params['fixUrl']

        if depth >= maxDepth:
            return None

        else:
            depth += 1
            rawData = self.go_to(currentLink)

            if rawData != None:
                parsedResult = self.parse(rawData)

                self.process_data(parsedResult['data'], searchTerms, currentLink)

                links = parsedResult['links'][:maxLinks]
                if len(links) > 0:
                    for link in links:
                        if self.link_check_fail(link, currentLink):
                            continue

                        if fixUrl == 'true':
                            link = urllib.parse.urljoin(currentLink, link)

                        nextParams = {}
                        nextParams['depth'] = depth
                        nextParams['maxDepth'] = maxDepth
                        nextParams['currentLink'] = link
                        nextParams['searchTerms'] = searchTerms
                        nextParams['maxLinks'] = maxLinks
                        nextParams['fixUrl'] = fixUrl

                        self.explore(nextParams)
                else:
                    return None

            else:
                return None

