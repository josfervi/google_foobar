# STRUCTURE
# - answer(chunk, word):
#   - isCyclic(word):
#   - isSingleCharactered(word):
#   - acyclic_word_case(chunk, word):
#   - cyclic_word_case(chunk, word):
#     - indexAll(str, substr):

# CONTENTS
# ***word is cyclic if word can be written
#    as ABA where A is a non-empty string
#    and B is a string
#    e.g. "lol"    is cyclic (A="l",   B="o")
#    e.g. "abcabc" is cyclic (A="abc", B="")
# NOTES
#     how acyclic_word_case was developed
# Function Definitions
#     isCyclic
#     isSingleCharactered
#     acyclic_word_case
#           (Solves the problem only for
#            the special case where word
#            is acyclic and is faster than
#            cyclic_word_case in this special
#            case)
#       indexAll
#     cyclic_word_case
#           (Solves the problem in the
#            the general case, but is slower
#            than acyclic_word_case in the case
#            where word is acyclic. Must be used
#            when word is cyclic because
#            acyclic_word_case is not guaranteed
#            to solve the problem when word is
#            cyclic)
#   answer
#
# Test cases
#  test cases fpr isCyclic
#  test cases for isSingleCharactered
#  test cases for indexAll
#  test cases for answer
#       (tests acyclic_word_case and
#               cyclic_word_case as well)


# ========NOTES========
# When word is cyclic, there can be overlap
# between instances of word in chunk.
# Take for example the chunk "lololo" and
# the word "lol". The first match of "lol"
# in "lololo" is "LOLolo" (starting at index
# 0 and capitalized for clarity) overlaps 
# the second match of "lol" in "lololo"
# (starting at index 2).
#
# 
#===How acyclic_word_case was developed===
#
# [1] When word is acyclic, there cannot be any
#     overlap between instances of word in chunk.
# [2] If m1 and m2 are two non-overlap 
#     instances/matches of word in chunk.
#                         m2
#                        vvv
#     (e.g. "goo" in "googoo")
#                     ^^^
#                      m1
#     The operation of removing m1 and then 
#     removing m2 is equivalent to the
#     operation of removing m2 and then
#     removing m1.
# Frpm [1] and [2], conclude that [3] in the case
# where word is acyclic, the matches of word in
# chunk can be removed from chunk in any order
# to always give the answer.
# Programatically, the most efficient procedure is
# to remove the matches as they appear. This is what
# I have done in acyclic_word_case.
# ========END-NOTES========


# ========Function Definitions========

# returns "word can be written as ABA where A is a nonempty string and B is a string."
# e.g.
#    isCyclic("lol")   returns True    (A="l",  B="o")
#    isCyclic("lolo")  returns True    (A="lo", B="")
#    isCyclic("o")     returns False
#    isCyclic("goo")   returns False
#    isCyclic("llooll" returns True    (A="ll", B="oo")
#                                   or (A="l",  B="lool")
#    isCyclic("oooo")  returns True    (A="o",  B="oo")
#                                   or (A="oo", B="")
def isCyclic(word):
    for i in range(1, len(word)/2 + 1):
        if (word[:i] == word[-i:]):
            return True
    return False

# isSingleCharactered("o")  returns True
# isSingleCharactered("oo") returns True
def isSingleCharactered(word):
    c= word[0]
    for i in range(1, len(word)):
        if word[i] != c:
            return False
    return True

def acyclic_word_case(chunk, word):
    rc= chunk # the remaining chunk
    while True:
        try:
            # this finds the first occurrence of word in rc 
            # this first occurence may even be an occurrence
            # that was created after the previous removal
            i= rc.index(word)
            # remove the first occurrence of
            # word from rc, the remaining chunk
            rc= rc[:i] + rc[i+len(word):]
        except:
            # no more occurences of word in rc
            return rc

# index all occurrences of substr in str
# returns a list of indexes
# where substr is found inside str
# see test cases for examples
def indexAll(str, substr):
    j= []
    i= 0
    while i <= len(str) - len(substr):
        try:
            i= str.index(substr, i)
            j.append(i)
            i+= 1
        except:
            break
    return j

memo= {} # use dictionary to memoize completed work

def cyclic_word_case(chunk, word):
    global memo
    
    try:
        return memo[chunk]
    except:
        pass # continue onto line 91
    
    wd_len=  len(word)
    if(len(chunk) < wd_len):
        return chunk
    
    matches= indexAll(chunk, word)
    
    if (matches == []):
        memo[chunk]= chunk
        return chunk
    
    candidates= []
    for m in matches:
        # remove matched word from the chunk
        rc= chunk[:m] + chunk[m+wd_len:] # factor into a function?
        candidate= cyclic_word_case(rc, word)
        candidates.append(candidate)
    
    result=      min(candidates, key= lambda s: (len(s), s))
    memo[chunk]= result
    return result
    
def answer(chunk, word):
    global memo
    if (not isCyclic(word)) or isSingleCharactered(word):
        return acyclic_word_case(chunk, word)
    else:
        # each request statrts with an empty dictionary,
        # which is used to memoize completed work
        memo= {}
        return  cyclic_word_case(chunk, word)


# ========Test Cases========

# test cases for isCyclic(word)    
print isCyclic("lol")    == True
print isCyclic("lolo")   == True
print isCyclic("o")      == False
print isCyclic("goo")    == False
print isCyclic("llooll") == True
print isCyclic("oooo")   == True

# test cases for isSinglecharactered(word)
print isSingleCharactered("o")  == True
print isSingleCharactered("oo") == True

# tests cases for indexAll(str, substr)
#====trigger the break inside the except block====
print( indexAll("lololololo", "goo")
           == [])
print( indexAll("lololololo", "lol")
           == [0, 2, 4, 6])
print ( indexAll("lollolalolaalolaaalol", "lol")
           == [0, 3, 7, 12, 18])
#====fall out of the while loop============
#====because i > len(str) - len(substr)====
print( indexAll("lololololol", "lol")
           == [0, 2, 4, 6, 8])
print( indexAll("goo", "goo") == [0])
print( indexAll("googooagooaagooaaagoo", "goo")
           == [0, 3, 7, 12, 18])
print( indexAll("fooaaafooaafooafoofoo", "foo")
            == [0, 6, 11, 15, 18] )

# test cases for answer(word)
#====acyclic, 0 levels of nesting====
print answer("goodgooogoogfogoood", "goo") == "dogfood"
#====acyclic, 1 level of nesting====
print answer("ggoooo_gogooo", "goo") == "_"
#====acyclic, 2 levels of nesting====
print answer("gggoooooo", "goo") == ""
#====cyclic, 0 levels of nesting====
print answer("caba", "aba") == "c"
print answer("lololololo", "lol") == "looo"
print answer("ololololol", "lol") == "oloo"
print answer("ababababab", "bab") == "aaab"
#====cyclic, 1 level of nesting====
print answer("caababa", "aba") == "c"
print answer("allolololl", "lol") == "a"