import re
from backend.mispellings import *
from backend.cinnamon import syn

def special_search(needle, haystack, lst):
    if needle in ["address"] + first_pass("address") + second_pass("address") + syn["address"]:
        lst += [(haystack[x.start() -1:x.end()-1], x.start()) for x in re.finditer('(?<=\W)[1-9]+ [a-zA-Z-]+ \W*(?i)(blvd\.|st\.|rd\.|cr\.|ln\.)(?i)\W*(?=\W|$)', " "+haystack.lower())]

def direct_search(needle, haystack):
    lst = [(haystack[x.start()-1:x.end()-1], x.start()) for x in re.finditer("(?<=\W)" + needle.replace('.', '\\.') + "(?=\W|$)", " "+haystack.lower())]
    print(needle + " ||| "  + str(lst))
    special_search(needle, haystack, lst)
    return lst

def search(needle, haystack):
    needles = set([needle.lower()] + first_pass(needle) + second_pass(needle) + syn[needle.lower()])
    lst = []
    for n in needles:lst += (direct_search(n.lower(), haystack))
    return lst

if __name__ == '__main__':
    print(search("hello", "Hello my naem is Michael!"))
