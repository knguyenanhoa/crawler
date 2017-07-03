import io

class ReadWrite:
    def __init__(self):
        pass

    def reader(self, filePath):
        searchTerms = []
        with open(filePath,'r') as file:
            for line in file:
                searchTerms.append(line.strip())
        return searchTerms

    def writer(self, filePath, data):
        with open(filePath, 'w') as file:
            for datum in data:
                file.write("%s\n" % datum)
        return None
