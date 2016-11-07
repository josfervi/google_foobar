# I wrote this solution using many function definitions
# to promote code readability, modularity and demonstrate
# problem decomposition; however, Python has a large function
# call overhead. If performance is preferred, the solution
# code can be rewritten in inline form thus forgoing many
# function calls.

from fractions import gcd

def answer(vertices):
    return picks_theorem(vertices)

def picks_theorem(vertices):
    #  Pick's Theorem aplies here perfectly.
    #  It says:
    #    Given a lattice polygon, P, (not nec. a triangle)
    #    (a polygon whose vertices are integer points - i.e. have integer coordinates),
    #    the area, A, of the P can be found by using:
    #    A = i + b/2 - 1     [eq. 1]
    #    where
    #      A is the area of P
    #      i is the number of int pts within P
    #      b is the number of int pts on the boundary of P
    #
    #  Thus manipulating [eq. 1] to solve for i, I get:
    #  i= A - b/2 + 1
    
    two_a= ara(vertices)
    b=     num_int_pts_on_triangle_boundary(vertices)
    i=     ( (two_a - b) >> 1) + 1                  # a>>1 equals a/2 (/ is int div)
    return i

# Returns two times the area of the triangle formed by vertices.
def ara(vertices):
    # Let pts. A, B, C be the vertices of triangle P
    # Let AB be the vector formed by going from pt A to pt B
    # Let AC be the vector formed by going from pt A to pt C
    # The magnitude of the cross product, AB x AC,
    # gives the area of the parallelogram with adjacent sides AB, AC.
    # Importantly, this area is also twice the area of triangle P.
    x=0
    y=1
    [a, b, c]= vertices
                # The magnitude of AB x AC
    return abs(   a[x] * ( b[y] - c[y] )
                + b[x] * ( c[y] - a[y] )
                + c[x] * ( a[y] - b[y] )  )
                
def num_int_pts_on_triangle_boundary(vertices):
    [a, b, c]= vertices
    return num_int_pts_on_line(a, b) + \
           num_int_pts_on_line(b, c) + \
           num_int_pts_on_line(c, a) - 3 # Each vertex of the triangle
                                         # gets counted two times, so
                                         # subtract 3 to account for
                                         # the double counting.

def num_int_pts_on_line(pt0, pt1):
    # Let L be the line segment from pt0 to pt1.
    # Let m = rise/run be the slope of L.
    # Let ri/ru be the reduced fraction of the fraction rise/run.
    #  Then ri = rise/gcd(rise,run) and
    #       ru =  run/gcd(rise,run).
    #  Furthermore ri and ru are integers.
    # Let a 'jump' be defined as:
    #              going ru units to the right and then 
    #              going ri units up,
    # Now starting at pt0, a grid pt),
    #  each time we do a jump,
    #  we land on the next int pt that is within L.
    #
    # Starting at pt0, an int pt,
    #  we make n = rise/ri jumps.
    #   n = rise/ri
    #     = rise/(rise/gcd(rise,run))
    #     = gcd(rise,run)
    #  On the nth jump we are at pt1
    #  and have covered n+1=gcd(rise,run)+1 int pts.
    x=0
    y=1
    rise= pt1[y] - pt0[y]
    run=  pt1[x] - pt0[x]
    return gcd( abs(rise), abs(run) ) + 1
  
# TEST CASES
#print( answer( [ [-1, -1],
#                 [ 1,  0],
#                 [ 0,  1]  ] ) == 1)
                    
#print answer( [ [2,    3], 
#                [6,    9], 
#                [10, 160]  ] )#  ==  289
                
#print answer( [ [ 91207,  89566],
#                [-88690, -83026],
#                [ 67100,  47194]  ] )  ==  1730960165