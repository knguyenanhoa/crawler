from parser import ParseWebContent

class Analyser:
    def __init__(self): 
        return None

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
                elif params['keyPhrase'] != '' and parser.match(d, params['keyPhrase']):
                    return {'isTargetLink': True, 'result': currentLink}
                else:
                    continue

        result = self.interesting(interest, params,)
        if result:
            return {'isTargetLink': False, 'result': currentLink}
        else:
            return {'isTargetLink': False, 'result': None}
