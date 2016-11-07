S=                  None
even_s_candidate=   None
closest_even_less_= 0
closest_even_more=  None
closest_odd_less_=  1
closest_odd_more=   None
l=      0
r=      None
l_odd_= 1
r_even= None

# The answer,   s, lies in [l...r     ] inclusive
# If s is even, s  lies in [l...r_even] inclusive
# If s is odd,  s  lies in [l_odd...r ] inclusive

def answer(str_S):
    
    global S, r, r_even, closest_even_more, closest_odd_more
    
    S= int(str_S)
    R= {0:1, 1:1, 2:2, 3:3, 4:7, 5:4}
    
    if S >= 148:
        r= r_even= closest_even_more= 2*( (S+1)/4 )
        closest_odd_more= r+1
    
    # Let s be the answer
    # { s is in [l...r] inclusive }
    
    k= 4
    while (2*k)+1 < r:
        
        a= R[2*k - 2]= R[k-1] + R[k  ] + (k-1)
        b= R[2*k - 1]= R[k-2] + R[k-1] +  1
        c= R[2*k    ]= R[k  ] + R[k+1] +  k
        d= R[2*k + 1]= R[k-1] + R[k  ] +  1
        
        updateBounds([a,b,c,d], 2*k-2)
        
        k*= 2

    del a,b,c,d, k
    
    mid= (l+r)/2
    
    k= ( (mid+1)/4 ) * 4
    
    flags= []
    while k > 6:
        flag= k % 4 == 0
        flags.append(flag)
        k= k/2 if flag else (k-2)/2
    
    flags.reverse()
    
    for flag in flags:
        
        if flag:
            a= R[2*k - 2]= R[k-1] + R[k  ] + (k-1)
            b= R[2*k - 1]= R[k-2] + R[k-1] +  1
            c= R[2*k    ]= R[k  ] + R[k+1] +  k
            d= R[2*k + 1]= R[k-1] + R[k  ] +  1
            e= R[2*k + 2]= R[k+1] + R[k+2] + (k+1)
            f= R[2*k + 3]= R[k  ] + R[k+1] +  1
            
            updateBounds([a,b,c,d,e,f], 2*k-2)
            
            k*= 2
        else:
            a= R[2*k    ]= R[k  ] + R[k+1] +  k
            b= R[2*k + 1]= R[k-1] + R[k  ] +  1
            c= R[2*k + 2]= R[k+1] + R[k+2] + (k+1)
            d= R[2*k + 3]= R[k  ] + R[k+1] +  1
            e= R[2*k + 4]= R[k+2] + R[k+3] + (k+2)
            f= R[2*k + 5]= R[k+1] + R[k+2] +  1
            
            updateBounds([a,b,c,d,e,f], 2*k)
            
            k= k*2 + 2
    
def updateBounds(A, first_index):
    
    # { A = [R[i] for i in xrange(first_index, first_index+len(A))]
    
    global l, l_odd_, r, r_even, even_s_candidate, \
           closest_even_less_, closest_even_more,  \
           closest_odd_less_,  closest_odd_more 
    
    i= first_index + len(A) -2
    for a in reversed(A[:: 2]):
        
        # { i is even }
        even_n= i
        
        # { a = R[even_n] }
        if a < S:
            closest_even_less_= max(closest_even_less_, even_n)
            l=      max(l, even_n +1)
            l_odd_= max(l_odd_, l if l%2==1 else l+1)
            if l<l_odd_ and l%2==1:
                l+= 1
            break
        elif a > S:
            closest_even_more= min(closest_even_more, even_n)
            r_even= min(r_even, even_n -1 -1)
            if r_even<r and r%2==0:
                r-= 1
        else:
            closest_even_less_= closest_even_more= even_n
            even_s_candidate= even_n
            l=      max(l,     even_n   )
            l_odd_= max(l_odd_, even_n +1)
            if l<l_odd_ and l%2==1:
                l+= 1
            r_even= min(r_even, even_n  )
            if r_even<r and r%2==0:
                r-= 1
        
        i-= 2
        
    i= first_index + len(A) -1
    for a in A[::-2]: # equivalent to [ A[3], A[1] ]       when len(A) = 4
                      # equivalent to [ A[5], A[3], A[1] ] when len(A) = 6
        # { i is odd }
        odd_n= i
        
        # { a = R[odd_n] }
        if a < S:
            closest_odd_less_= max(closest_odd_less_, odd_n)
            l_odd_= max(l_odd_, odd_n +1 +1)
            if l<l_odd_ and l%2==1:
                l+= 1
            break
        elif a > S:
            closest_odd_more= min(closest_odd_more, odd_n)
            r= min(r, odd_n -1)
        else:
            closest_odd_less_= closest_odd_more= odd_n
            l= l_odd_= r= odd_n
            s= odd_n
            return s
        
        i+= 2

str_S= "148"
answer(str_S)