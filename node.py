import urllib.request
import nltk

import node
from parse import Parse

class Node:
    interestingLinks = []

    def __init__(self):
        return None

    def go_to(self, url):
        try:
            return urllib.request.urlopen(url)
        except ValueError:
            print('ValueError')
            return None
        except urllib.error.HTTPError:
            print('HTTPError')
            return None


    def parse(self, rawData):
        parser = Parse(rawData)
        return parser.get_links()




    def process_data(self, data, searchTerms, currentLink):
        interest = 0
        for d in data:
            tokens = nltk.word_tokenize(d)
            for t in tokens:
                for term in searchTerms: 
                    if t.strip() == term:
                        interest += 1
                    else:
                        continue

        if interest > 0:
            self.interestingLinks.append(currentLink)
            


    def explore(self, params):
        searchTerms = params['searchTerms']
        depth = params['depth']
        maxDepth = params['maxDepth']
        currentLink = params['currentLink']

        if depth >= maxDepth:
            return None

        else:
            depth += 1
            rawData = self.go_to(currentLink)

            if rawData != None:
                parsedResult = self.parse(rawData)

                self.process_data(parsedResult['data'], searchTerms, currentLink)


                for link in parsedResult['links']:
                    nextParams = {}
                    nextParams['depth'] = depth
                    nextParams['maxDepth'] = maxDepth
                    nextParams['currentLink'] = link
                    nextParams['searchTerms'] = searchTerms

                    self.explore(nextParams)

            else:
                return None

