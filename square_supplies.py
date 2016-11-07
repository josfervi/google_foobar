# This file is missing part of my submission.

# CONTENTS
#  - notes
#  - answer
#  - make_change

#=========NOTES=========
# The problem can be reformulated as:
# 
# "Square" coins are square because they
# are always worth a square number of cents,
# e.g. 1 cent, 4 cents, 9 cents, ..,.10000 cents.
# Make n cents of change using
# the fewest number of "square" coins.
#=======END-NOTES=======

# xrange() is deprecated in Python3

from math import sqrt

def answer(n):
    # largest integer p s.t. p**2 <= n
    p= int(sqrt(n))
    
    if   p**2     == n: return 1
    elif p**2 + 1 == n: return 2
    
    coins= [i**2 for i in xrange(p+1)]
    # e.g. if n=26 then p=5 and
    #      coins=[0, 1, 4, 9, 16, 25]
    
    return make_change(coins, n)

# make n cents of change using
# the fewest number of coins
#
# PRECONDITIONS:
# coins[0] must equal 0
# coins[1] must equal 1
# coins[2] must be >= 4
def make_change(coins, n):
    
    if n<4: return n
    
    m= [[None, 1, 2, 3] + [0]*(n-3) for a in xrange(len(coins))]
    
    m[0]= [None]*(n+1)
    m[1]= [None]+ range(1,n+1)

    for c in range(2, len(coins)):
        coin= coins[c]
    
        for i in range(4, n+1):
            if   coin==i:   m[c][i]= 1
            elif coin+1==i: m[c][i]= 2
            elif coin > i:  m[c][i]=       m[c-1][i]
            else:           m[c][i]= min(  m[c-1][i],
                                        1+m[c][i-coin] )
    
    # coins[p] is the last coin
    p= len(coins)-1
    return m[p][n]

# TEST CASES
#                                            *                       *
#idx  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18    
#ans= [0, 1, 2, 3, 1, 2, 3, 4, 2, 1,  2,  3,  3,  2,  3,  4,  1,  2,  2]
#passed= True
#for idx, an in enumerate(ans):
#    passed&= answer(idx) == an
#passed&= answer(24)  == 3
#passed&= answer(160) == 2
#if(passed): print ":) Passed all tests!"
#else:       print ":( Failed at least one test."