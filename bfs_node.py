# Std lib
import urllib.request
import urllib.parse
from multiprocessing import Process, Manager

# Modules
from parser import ParseWebContent
from analyser import Analyser

class BFSNode:
    man = Manager()
    analyser = Analyser()
    discoveredLinks = man.list()
    interestingLinks = man.list()

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
        parser = ParseWebContent()
        return parser.get_links(rawData)


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

    def process_explore(self, processSet, params,):
        seedLink = params['seedLink']
        searchTerms = params['searchTerms']
        maxLinks = params['maxLinks']
        fixUrl = params['fixUrl']
        newLinks = params['newLinks']
        noOfProcesses = params['noOfProcesses']

        for link in processSet:
            if fixUrl == 'true':
                link = urllib.parse.urljoin(seedLink, link)
            rawData = self.go_to(link)

            if rawData != None:
                parsedResult = self.parse(rawData)

                params['currentLink'] = link
                self.interestingLinks.append(self.analyser.analyse(parsedResult['data'], params,))
                self.discoveredLinks.extend(parsedResult['links'][:maxLinks])

    def explore(self, params):
        self.interestingLinks = self.man.list(params['interestingLinks'])

        processSets = self.compile_process_sets(params['newLinks'], params['noOfProcesses'])

        for set in processSets:
            p = Process(target=self.process_explore, args=(set, params,))
            p.start()
            p.join()

        return None
