import re
from backend.mispellings import *
from backend.cinnamon import syn

def special_search(needle, haystack, lst):
    similarNeedles = ["address"] + syn["address"]
    if needle in similarNeedles:
        lst += [(haystack[x.start()-1:x.end()-1], x.start()-1) for x in re.finditer('(?<=\W)[1-9]+ [a-zA-Z-]+ \W*(?i)(blvd\.|st\.|rd\.|cr\.|ln\.)(?i)\W*(?=\W|$)', " "+haystack.lower())]
    similarNeedles = ["phone number"] +  syn["phone number"]
    if needle in similarNeedles:
        lst += [(haystack[x.start()-1:x.end()-1], x.start()-1) for x in re.finditer('(?<=\W)(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})(?=\W|$)', " "+haystack.lower())]
    similarNeedles = ["date"] +  syn["date"]
    if needle in similarNeedles:
        lst += [(haystack[x.start()-1:x.end()-1], x.start()-1) for x in re.finditer('(?<=\W)(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])(?=\W|$)', " "+haystack.lower())]
        lst += [(haystack[x.start()-1:x.end()-1], x.start()-1) for x in re.finditer('(?<=\W)(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])(?=\W|$)', " "+haystack.lower())]

def direct_search(needle, haystack):
    regex = "(?<=\W)" + re.escape(needle) + "(?=\W|$)"
    regexMatches = re.finditer(regex, " "+haystack.lower())
    lst = [(haystack[x.start()-1:x.end()-1], x.start()-1) for x in regexMatches]
    special_search(needle, haystack, lst)
    return lst

def search(needle, haystack):
    needles = set(
        [needle.lower()] +
        first_pass(needle) +
        second_pass(needle) +
        syn[needle.lower()]
    )
    lst = []
    for n in needles:
        print(n)
        lst += (direct_search(n.lower(), haystack))
    return lst

if __name__ == '__main__':
    print(search("phone number", "Hello my naem is Michael! My pone number is 416-528-8624 :)"))
