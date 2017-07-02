# Std lib
import urllib.request
import urllib.parse
import threading

# Modules
from parse import Parse

class BFSNode:
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

    def thread_explore(self, fixUrl, seedLink, linkSets, searchTerms, maxLinks, discoveredLinks):
        for link in linkSets:
            if fixUrl == 'true':
                link = urllib.parse.urljoin(seedLink, link)
            rawData = self.go_to(link)

            if rawData != None:
                parsedResult = self.parse(rawData)

                self.process_data(parsedResult['data'], searchTerms, link)
                discoveredLinks.extend(parsedResult['links'][:maxLinks])

        return None 

    def explore(self, params):
        discoveredLinks = []
        seedLink = params['seedLink']
        searchTerms = params['searchTerms']
        self.interestingLinks = params['interestingLinks']
        maxLinks = params['maxLinks']
        fixUrl = params['fixUrl']
        newLinks = params['newLinks']
        noOfThreads = params['noOfThreads']

        threadedLinks = []
        x = 0
        while x < len(newLinks):
            head = x*noOfThreads
            tail = head + noOfThreads - 1
            threadedLinks.append(newLinks[head:tail])
            x += 1
        
        print(threadedLinks)
        threads = []
        for linkSets in threadedLinks:
            t = threading.Thread(target=self.thread_explore, args=(fixUrl, seedLink, linkSets, searchTerms, maxLinks, discoveredLinks))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return discoveredLinks

