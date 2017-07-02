# Std lib
import urllib.request
import urllib.parse
from multiprocessing import Process, Manager

# Modules
from parse import Parse

class BFSNode:
    man = Manager()
    discoveredLinks = man.list()
    interestingLinks = man.list()

    def __init__(self): return None

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

        if interest > 0 and (not (currentLink in self.interestingLinks)):
            self.interestingLinks.append(currentLink)

    def compile_process_sets(self, newLinks, noOfProcesses):
        process_sets = []
        x = 0
        
        if len(newLinks) < noOfProcesses:
            linksPerProcess = len(newLinks)
        else:
            linksPerProcess = round(len(newLinks)/noOfProcesses)

        while x < noOfProcesses:
            head = x*linksPerProcess
            tail = head + linksPerProcess
            process_sets.append(newLinks[head:tail])
            x += 1
            
        return process_sets

    def process_explore(self, newLinks, fixUrl, seedLink, searchTerms, maxLinks):
        for link in newLinks:
            if fixUrl == 'true':
                link = urllib.parse.urljoin(seedLink, link)
            rawData = self.go_to(link)

            if rawData != None:
                parsedResult = self.parse(rawData)

                self.process_data(parsedResult['data'], searchTerms, link)
                self.discoveredLinks.extend(parsedResult['links'][:maxLinks])

    def explore(self, params):
        seedLink = params['seedLink']
        searchTerms = params['searchTerms']
        self.interestingLinks = self.man.list(params['interestingLinks'])
        maxLinks = params['maxLinks']
        fixUrl = params['fixUrl']
        newLinks = params['newLinks']
        noOfProcesses = params['noOfProcesses']

        processSets = self.compile_process_sets(newLinks, noOfProcesses)

        for set in processSets:
            p = Process(target=self.process_explore, args=(set, fixUrl, seedLink, searchTerms, maxLinks))
            p.start()
            p.join()
            
        return None

