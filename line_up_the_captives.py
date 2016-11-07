from itertools import combinations
from math      import factorial
 
def answer(x,y,n):
    # Let X (capital x) denote the guard that sees x number of rabbits
    # Let Y (capital y) denote the guard that sees y number of rabbits
    
    if   x+y >  n+1: return 0
    elif x+y == n+1: return   nCr(n-1, x-1)
    elif x+y == n  : return ( nCr(n-2, x-1) * (n-1) * (n-2) ) >> 1
    elif x+y <= 2  : return 0
    elif [x,y] == [1,2] or [x,y] == [2,1]: return factorial(n-2)
    
    h= (n + 1) - (x + y) # h is the number of unseen rabbits
    m= n-1 # because it's used in many places
    prods= [0]*h
    prev_s= [0]*h
    acc= 0
    
                             # [1, ..., n-2]
    # for s in combinations( range(1, m  ), h):
    #     same_so_far= True
    #     prod= 1
    #     i= 0
    #     for prev_s_i, s_i in zip(prev_s, s):
    #         if (same_so_far and s_i == prev_s_i): prod= prods[i]
    #         else:
    #             same_so_far= False
    #             prod*= m - s_i
    #             prods[i]= prod
    #         i+= 1
    #     prev_s= s
    #     acc+= prod
        
                         # [1, ..., n-2]
    for s in combinations( range(1, m  ), h):
        prod= 1
        for s_i in s:
            prod*= m - s_i
        acc+= prod
        #acc+= reduce(lambda p, s_i: p*(m-s_i), s, 1)
    
    return nCr(m-h, x-1) * acc

# credit to dheerosaur on StackExchange
# http://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
def nCr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(mul, xrange(n, n-r, -1))
    denom = reduce(mul, xrange(1, r+1))
    return numer/denom
    
print answer(2,2,4) == 6
print answer(1,3,4) == 3
print answer(1,2,6) == 24
print answer(2,2,3) == 2
print answer(2,2,5)