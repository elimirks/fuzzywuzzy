#Synonym module
import json
import re

#a class structure might be overkill
#but then again not... 
class Synonyms():
    def __init__(self,load_file):
        with open(load_file) as data_file:    
            self.synonyms = json.load(data_file)
        
    def __getitem__(self,s):
        #return synonyms matching s
        if s in self.synonyms:
            return self.synonyms[s]
        else:
            return []
        
    def __len__(self):
        return len(self.synonyms)
    
    def index(self, q, t):
        #   q: query, initial search query
        #   t: text, body of text to search in
        indices = {}
        for s in (self.synonyms[q]+[q]):
            if s in t:
                indices[s] = [m.start() for m in re.finditer(s, t)]
        return indices
            
syn = Synonyms('static/cinnamon.json')
if __name__ == '__main__':
    print(syn['hover'])





    
