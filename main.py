# Std lib
import time

# Other
import io
import node


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

inputFile = reader('io/input.txt')

params['searchTerms'] = inputFile[12:]
params['depth'] = 0
params['maxDepth'] = int(inputFile[5])
params['maxLinks'] = int(inputFile[7])
params['fixUrl'] = inputFile[9]
params['currentLink'] = inputFile[1]
params['interestingLinks'] = []


# MAIN
searchSpace = params['maxLinks'] ** params['maxDepth'] 
print("Search space %s" % searchSpace)

if searchSpace <= 1000:
    rootNode = node.Node()
    rootNode.explore(params)
    result = rootNode.interestingLinks
else:
    print("Search space exceeds 1000 - Terminate")
    result = None

# Output
if result != None:
    writer('io/output.txt', rootNode.interestingLinks)

print("Exec in %s seconds" % (time.time() - startTime)) # log time
