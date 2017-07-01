import io
import node

global searchTerms


# Main
searchTerms = []

with open('input.txt','r') as file:
    for line in file:
        searchTerms.append(line.strip())

url = searchTerms[0]
searchTerms.pop(0)

params = {}
params['depth'] = 0
params['maxDepth'] = 2
params['currentLink'] = url
params['interestingLinks'] = []
params['searchTerms'] = searchTerms

rootNode = node.Node()
rootNode.explore(params)


# CHECK
print(rootNode.interestingLinks)
