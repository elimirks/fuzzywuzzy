import re
from mispellings import *
from cinnamon import syn

def direct_search(needle, haystack):
    return {(needle, x.start()) for x in re.finditer(" " + needle + "( |\?|\.|,|!)", " " + haystack + " ")}

def search(needle, haystack):
    needles = [needle.lower()] + first_pass(needle) + second_pass(needle) + syn[needle.lower()]
    lst = []
    for n in needles:lst+=direct_search(n, haystack.lower())
    return lst

if __name__ == '__main__':
    print(search("Test", "That test life! direction!"))