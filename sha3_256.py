"""
Created on Sat Dec 4 16:12:35 2021

@author: Batel Oved
"""

### Constants ###

b = 1600
r = 1088
c = b-r
w = 64
d = 256
rounds = 24

ROT =  [[0,36,3,41,18],
        [1,44,10,45,2],
        [62,6,43,15,61],
        [28,55,25,21,56],
        [27,20,39,8,14]]

RC = [0]*rounds
RC[0]  = 0x0000000000000001
RC[1]  = 0x0000000000008082
RC[2]  = 0x800000000000808A
RC[3]  = 0x8000000080008000
RC[4]  = 0x000000000000808B
RC[5]  = 0x0000000080000001
RC[6]  = 0x8000000080008081
RC[7]  = 0x8000000000008009
RC[8]  = 0x000000000000008A
RC[9]  = 0x0000000000000088
RC[10] = 0x0000000080008009
RC[11] = 0x000000008000000A
RC[12] = 0x000000008000808B
RC[13] = 0x800000000000008B
RC[14] = 0x8000000000008089
RC[15] = 0x8000000000008003
RC[16] = 0x8000000000008002
RC[17] = 0x8000000000000080
RC[18] = 0x000000000000800A
RC[19] = 0x800000008000000A
RC[20] = 0x8000000080008081
RC[21] = 0x8000000000008080
RC[22] = 0x0000000080000001
RC[23] = 0x8000000080008008


def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        bits = bits[::-1]
        result.extend([int(b) for b in bits])
    return result

def fromBitsToHex(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        byte = byte[::-1]
        chars.append("{:02x}".format(int(''.join([str(bit) for bit in byte]), 2)))
    return '0x' + ''.join(chars)

def rotate(l, n):
    return l[-n:] + l[:-n]

def strToStateArray(S):
    A = [[[0 for z in range(w)] for x in range(5)] for y in range(5)]
    for x in range(5):
        for y in range(5):
            for z in range(w):
                A[x][y][z] = S[w*(5*y+x)+z]
    return A
    
def stateArrayToStr(A):
    S = [0 for i in range(b)]
    for x in range(5):
        for y in range(5):
            for z in range(w):
                S[w*(5*y+x)+z] = A[x][y][z]
    return S
    
##### Implementation #####

def PreProccessing(m):
    lenB_m = len(m)*8
    M = toBits(m)
    N = M + [0,1]
    P = N + [1] + [0 for i in range((-4-lenB_m)%r)] + [1]
    n = len(P)//r
    P = [P[i*r:r+i*r] for i in range(n)]
    return P,n

def Theta(A):
    B = [[0 for z in range(w)] for x in range(5)]
    C = [[0 for z in range(w)] for x in range(5)]
    D = [[0 for z in range(w)] for x in range(5)]
    for x in range(5):
        for z in range(w):
            C[x][z] = A[x][0][z] ^ A[x][1][z] ^ A[x][2][z] ^ A[x][3][z] ^ A[x][4][z]
    
    for x in range(5):
        B[x] = rotate(list(C[x]),1)
    
    for x in range(5):
        for z in range(w):
            D[x][z] = C[(x-1)%5][z] ^ B[(x+1)%5][z]
       
    for x in range(5):
        for y in range(5):
            for z in range(w):
                A[x][y][z] = A[x][y][z] ^ D[x][z]   
    return A
        
def Rho(A):
    for x in range(5):
        for y in range(5):
            A[x][y] = rotate(A[x][y],ROT[x][y])
    return A

def Pi(A):
    B = [[[0 for z in range(w)] for x in range(5)] for y in range(5)]
    for x in range(5):
        for y in range(5):
            B[x][y] = A[(x+3*y)%5][x]
    return B
    
def Chi(A):
    B = [[[0 for z in range(w)] for x in range(5)] for y in range(5)]
    for x in range(5):
        for y in range(5):
            for z in range(w):
                B[x][y][z] = A[x][y][z] ^ ((A[(x+1)%5][y][z] ^ 1) & A[(x+2)%5][y][z])
    return B
    
def Iota(A,r):
    rc = list(format((RC[r]),'064b'))
    rc = [int(rc[i]) for i in range(w)]
    rc = rc[::-1]
    for z in range(w):
        A[0][0][z] = A[0][0][z] ^ rc[z]
    return A
    
def Rnd(A, ir):
    return Iota(Chi(Pi(Rho(Theta(A)))),ir)

def f(s):
    A = strToStateArray(s)
    for ir in range(rounds):
        A = Rnd(A, ir)
    s = stateArrayToStr(A)
    s = s[:d]
    return s
    
def Sponge(P,n):
    s = [0 for i in range(b)]
    for i in range(n):
        Pb = P[i] + [0 for i in range(c)]
        s = f([a^b for a,b in zip(s,Pb)])
    return s
    
def SHA3_256(m):
    P,n = PreProccessing(m)
    return fromBitsToHex(Sponge(P,n))


print(SHA3_256('Hello'))





    