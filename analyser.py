from parser import ParseWebContent

class Analyser:
    def __init__(self):
        pass

    def interesting(self, interest, params,):
        if interest < 0:
            return False
        if params['currentLink'] in params['interestingLinks']:
            return False
        if params['currentLink'] == params['seedLink']:
            return False
        return True

    def analyse(self, data, params,):
        currentLink = params['currentLink']
        seedLink = params['seedLink']
        parser = ParseWebContent()

        interest = 0
        for d in data:
            for term in params['searchTerms']: 
                if parser.match(d, term):
                    interest += 1
                else:
                    continue

        if self.interesting(interest, params,):
            return currentLink
        else:
            return None
