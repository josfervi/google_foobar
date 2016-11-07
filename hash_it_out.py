# CONTENTS
# - HOW TO CRACK THE HASH
# - def answer(digest):
# - solution
# - test cases

# ================HOW TO CRACK THE HASH================
#                           ____
#    (msg[i-1], msg[i]) -> |hash| -> dig[i]
#                           ----
#
#    dig[i] = ((129*msg[i]) xor msg[i-1]) % 256
#     msg[-1] = 0
#     xor denotes bitwise XOR 
#
#     - A % 256 is equivalent to truncating A to 8 bits
#     - bitwise XOR is a bitwise operation
#     - therefore:
#       - % 256 distributes over xor
#       - (A xor B) % 256 = (A % 256) xor (B % 256)
#    
#    dig[i] = ((129*msg[i]) % 256) xor (msg[i-1] % 256)
#           = ((129*msg[i]) % 256) xor msg[i-1]
#
#     - 129 = 0b10000001
#     - 129*A = 128 * A + A
#             = (2^7)*A + A
#             = A<<7    + A
#
#    dig[i] = ((msg[i]<<7 + msg[i]) % 256) xor msg[i-1]
#
#     - Let b =  msg[i]
#     - Let c = (msg[i]<<7 + msg[i]) % 256
#
#     - Let b7 b6 b5 b4 b3 b2 b1 b0 be the bits of  msg[i] and
#     - Let c7 c6 c5 c4 c3 c2 c1 c0 be the bits of (msg[i]<<7 + msg[i]) % 256
#     - then 
#           b7 b6 b5 b4 b3 b2 b1 b0
#         + b0  0  0  0  0  0  0  0
#        --------------------------
#        c8 c7 c6 c5 c4 c3 c2 c1 c0
#
#     The picture above lets us express the forward lookup in another way.
#     Forward Lookup: Given b we can get c in the following way:
#     if b0 = 0            (i.e. if b is even)
#      then c = b          {c is even}
#     if b0 = 1 and b7 = 0 (i.e. if b is odd and b <  128)
#      then c = b + 128    {c is odd and c >= 128,          note: c < 256} 
#     if b0 = 1 and b7 = 1 (i.e. if b is odd and b >= 128, note: b < 256)
#      then c = b - 128    {c is odd and c < 128}
#
#     Using the curly bracket {} conditions we can get a reverse lookup.
#     Reverse Lookup: Given c we can get b in the following way:
#     if c is even
#      then b = c
#     if c is odd and c >= 128
#      then b = c - 128
#     if c is odd and c < 128
#      then b = c + 128
#     
#     Reverse Lookup (Predicated Version
#       no conditionals - no branching - no branch predicting):
#
#           c7 c6 c5 c4 c3 c2 c1 c0
#         + c0  0  0  0  0  0  0  0
#        --------------------------
#        b8 b7 b6 b5 b4 b3 b2 b1 b0
#
#        Where again b7 b6 ... b0 are the bits of b 
#
#    Rewriting:
#    dig[i] = c xor msg[i-1]
#
#     - using A xor B xor B = A
#
#    dig[i] xor msg[i-1] = c
#
#    In summary,
#    For dig[i]
#     if we know the previous message, msg[i-1]
#     then we can get c
#     then we can use the Reverse Lookup to get b, msg[i]!
#
#    For dig[0], we know the previous message, msg[-1] = 0!
#    Thus c = dig[i] xor 0 = dig[i].
#    Thus we can get msg[0].
#
#    For dig[1], we now know the previous message, msg[0]!
#    Thus we can get msg[1].
#
#    Etc. our knowledge of msg[-1]
#         allows us to unravel the whole digest!
# ================end HOW TO CRACK THE HASH================

def answer(digest):
    return solution(digest)
    
def solution(digest):
    size= len(digest)
    
    message= [0 for i in range(size)]
    # note: message[-1] equals 0 as desired!
        
    for i in range(size):
        c= digest[i] ^ message[i-1]
        b= 0
        if (c % 2 == 0): # c is even
            b= c
        elif c >= 128:   # c is odd and c >= 128
            b= c - 128
        else:            # c is odd and c <  128
            b= c + 128
        message[i]= b
    return message

# test cases (uncomment)
digest=  [0, 129, 3, 129, 7, 129, 3, 129,
          15, 129, 3, 129, 7, 129, 3, 129]
message= [0, 1, 2, 3, 4, 5, 6, 7, 8, 
          9, 10, 11, 12, 13, 14, 15]
print answer(digest) == message

digest= [0, 129, 5, 141, 25, 137, 61, 149,
         113, 145, 53, 157, 233, 185, 109, 165]
message= [0, 1, 4, 9, 16, 25, 36, 49, 64,
          81, 100, 121, 144, 169, 196, 225]
print answer(digest) == message