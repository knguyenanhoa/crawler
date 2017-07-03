# Std lib
import time

# Other
import io
import bfs_node


# Functions
def reader(filePath):
    searchTerms = []
    with open(filePath,'r') as file:
        for line in file:
            searchTerms.append(line.strip())
    return searchTerms

def writer(filePath, data):
    with open(filePath, 'w') as file:
        for datum in data:
            file.write("%s\n" % datum)

# Input
startTime = time.time() # log time

params = {}

inputFile = reader('io/bfs_input.txt')

searchTerms = inputFile[14:]
depth = 0
seedLink = inputFile[1]
maxDepth = int(inputFile[5])
maxLinks = int(inputFile[7])
fixUrl = inputFile[9]
noOfProcesses = int(inputFile[11])


# MAIN
searchSpace = maxLinks ** maxDepth
print("Search space %s" % searchSpace)

params['searchTerms'] = searchTerms
params['fixUrl'] = fixUrl
params['interestingLinks'] = []
params['maxLinks'] = maxLinks
params['newLinks'] = [seedLink]
params['seedLink'] = seedLink
params['noOfProcesses'] = noOfProcesses

while depth < maxDepth:
    depth += 1

    rootNode = bfs_node.BFSNode()
    rootNode.explore(params)
    params['newLinks'] = rootNode.discoveredLinks
    params['interestingLinks'].extend(rootNode.interestingLinks)

# Output
if params['interestingLinks'] != None:
    writer('io/bfs_output.txt', params['interestingLinks'])

print("Exec in %s seconds" % (time.time() - startTime)) # log time
