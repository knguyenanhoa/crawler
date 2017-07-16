# Std lib
import logging
import urllib.request
import urllib.parse
from multiprocessing import Process, Manager, Pool, Event

# Modules
from parser import ParseWebContent
from analyser import Analyser

class BFSNode:
    man = Manager()
    analyser = Analyser()
    discoveredLinks = man.list()
    interestingLinks = man.list()
    visitedLinks = man.list()
    kill = Event()

    def __init__(self): 
        return None

    def visited(self, url):
        if url in self.visitedLinks:
            return True
        else:
            self.visitedLinks.append(url)
            return False

    def go_to(self, url):
        # logger init here as multiprocess not supported
        logger = logging.getLogger(__name__)
        try:
            return urllib.request.urlopen(url)
        except (ValueError, urllib.error.URLError, urllib.error.HTTPError) as e:
            logger.error(e)
            return None
        except:
            logger.error('Unknown error')

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

    def pool_explore(self, processSet, params,):
        seedLink = params['seedLink']
        searchTerms = params['searchTerms']
        maxLinks = params['maxLinks']
        fixUrl = params['fixUrl']
        newLinks = params['newLinks']
        noOfProcesses = params['noOfProcesses']

        for link in processSet:
            if self.visited(link):
                continue

            if self.kill.is_set():
                return None

            if fixUrl == 'true':
                link = urllib.parse.urljoin(seedLink, link)
            rawData = self.go_to(link)

            if rawData != None:
                parsedResult = self.parse(rawData)
                params['currentLink'] = link

                analysedResult = self.analyser.analyse(parsedResult['data'], params,)
                if analysedResult['isTargetLink']:
                    print("First encounter: %s" % analysedResult['result'])
                    self.kill.set()
                else:
                    self.interestingLinks.append(analysedResult['result'])
                    self.discoveredLinks.extend(parsedResult['links'][:maxLinks])

    def explore(self, params):
        self.interestingLinks = self.man.list(params['interestingLinks'])

        processSets = self.compile_process_sets(params['newLinks'], params['noOfProcesses'])

        self.visitedLinks = self.man.list()
        with Pool(params['noOfProcesses']) as p:
            multi_result = [p.apply_async(self.pool_explore, (set, params,)) for set in processSets]
            [result.get() for result in multi_result]

        return None
