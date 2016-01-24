import re
from mispellings import *
from cinnamon import syn

def special_search(needle, haystack, lst):
    if needle in ["address"] + first_pass("address") + second_pass("address") + syn["address"]:
        lst.update({(haystack[x.start():x.end()-2], x.start()) for x in re.finditer(' [1-9]+ [a-zA-Z-]+ \W*(?i)(blvd\.|st\.|rd\.|cr\.|ln\.)(?i)\W*( |\?|\.|,|!)', " " + haystack + " ")})

def direct_search(needle, haystack):
    lst = {}
    lst.update({(needle, x.start()) for x in re.finditer(" " + needle + "( |\?|\.|,|!)", " " + haystack + " ")})
    special_search(needle, haystack, lst)
    return lst

def search(needle, haystack):
    needles = [needle.lower()] + first_pass(needle) + second_pass(needle) + syn[needle.lower()]
    lst = {}
    for n in needles:lst.update(direct_search(n, haystack.lower()))
    return lst

if __name__ == '__main__':
    print(search("address", "That test 95 fifth st. life! direction! 17 Mason St. lool"))