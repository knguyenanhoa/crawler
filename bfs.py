# Std lib
import time

# Other
import bfs_node
from read_write import ReadWrite


# Input
startTime = time.time() # log time

io = ReadWrite()
inputFile = io.reader('io/bfs_input.txt')
depth = 0

params = {}
params['seedLink'] = inputFile[1]
params['newLinks'] = [inputFile[1]]
params['maxDepth'] = int(inputFile[5])
params['maxLinks'] = int(inputFile[7])
params['fixUrl'] = inputFile[9]
params['noOfProcesses'] = int(inputFile[11])
params['keyPhrase'] = inputFile[15]
params['searchTerms'] = inputFile[18:]
params['interestingLinks'] = []


# MAIN
searchSpace = params['maxLinks'] ** params['maxDepth']
print("Search space %s" % searchSpace)

while depth < params['maxDepth']:
    depth += 1
    if depth == params['maxDepth']:
        print("Depth --- %s MAX" % depth)
    else:
        print("Depth --- %s" % depth)

    rootNode = bfs_node.BFSNode()
    rootNode.explore(params)
    params['newLinks'] = rootNode.discoveredLinks
    params['interestingLinks'] = rootNode.interestingLinks

# Output
if params['interestingLinks'] != None:
    io.writer('io/bfs_output.txt', params['interestingLinks'])

print("Exec in %s seconds" % (time.time() - startTime)) # log time
