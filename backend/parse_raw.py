import nltk
import re
import json

debug = False
blacklist = [(r'and the .*;',','),(r'the .*;',','),(r'\(.*\)',''),(r'synonyms and antonyms',''),(r'\[.*\]',''),(r'\[\w*\s*',''),(r'\s{2,}','')]

#READ
f = open('static/raw_cinnamon.txt','r')
lines = []

for line in f:
    lines.append(line.strip().lower())
    
#PARSE
#try to store each word as itself, 
#with a list of synonyms as it's value
synonyms = {}

def remove_trailing_hyph(s):
    #there's a better way...
    #but remove hyphens somehow stuck in the second last place in a word
    #can't possibly be a real hyphenation
    matches = re.findall(r'\w*-\w{1}',s)
    for m in matches:
        e = s.index(m) + len(m)
        s = s[:e-2]+s[e-1:]
    return s
        
def clean_line(line):
    if line != "" and line[-1] == '-':
        line = line[:-1]
    else:
        line +=" " 
    return line
    
def parse_group(group):
    for r,o in blacklist:
        group = re.sub(r,o,group)
    group = remove_trailing_hyph(group)
    group = group.replace(';',',')
    group = group.replace('.',',')
    
    words = group.split(',')
    words = [w.strip() for w in words if w.strip() != ""]
    for w in words:
        if w not in synonyms:
            synonyms[w] = [s for s in words if s!=w]
        else:
            og = synonyms[w]
            synonyms[w] = list(set([s for s in words if s!=w] + og))
    
    return group

word_group = ""
ant = False
started = False
for line in lines:
    written = False
    #first build up each paragraph into one long line
    if not started and word_group == "" and line != "":
        #first line of word-group
        parts = line.split('.')
        if len(parts) > 1:
            #START
            started = True
            if parts[0]=='ant':
                ant=True
            word_group = clean_line(line)
            written = True
    
    if started and '.' not in line:
        word_group += clean_line(line)
        written = True
        
    if started and line != "" and line[-1] == '.':
        #END
        if not written:
            word_group += clean_line(line)
            
        parse_group(word_group)
        if not ant and debug:
            print ('GROUP',word_group)
        ant = False
        started = False
        word_group = ""
        
with open('static/cinnamon.json', 'w') as outfile:
    json.dump(synonyms, outfile)
        
