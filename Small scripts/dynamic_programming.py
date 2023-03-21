
p = [2,3,2,1,4]
len_p = len(p)-1
C = 5 



def N(C,i,p): 
    if C == 0: 
        return 1
    if C < 0 or i < 0 : 
        return 0
    return N(C,i-1,p) + N(C-p[i], i-1,p)
    
print("N:", N(C, len_p ,p))




def mem_N(C,i,r): 
    if r[C-1][i-1] >= 0: 
        return r[C-1][i-1]
    if C==0 : 
        return 1  
    if C<0 or i < 0 : 
        return 0  
    else: 
        q = mem_N(C-p[i], i-1,r) + mem_N(C,i-1,r) 
        r[C-1][i-1] = q
        return q 

r = [[-1] * (len_p+1) for i in range (len_p+1)]
print("Memoization N:", mem_N(C, len_p ,r))





def comb (a,n,C): 
    r = [[0] * (C+1) for i in range (len_p)]
    r[0][0] = 1 

    for i in range(1,n+1): 
        for j in range(C+1): 

            if a[i-1] <= j : 
                r[i][j] = r[i-1][j] + r[i-1][j-a[i-1]]
            else: 
                r[i][j] = r[i-1][j]
    #print(r)
    return r[n][C]

#print("comb: ",comb(p,len(p), 5))





r = [-1 for x in range(len(p))]


def rod(p,m,r): 

    if m==0 : 
        return 0 
    else: 
        q = -1
        for i in range(1,m+1): 
            q = max(q,p[i] + rod(p,m-i,r))
    r[m] = q 
    return q 

#print("\n\nrod =  ",rod(p,len(p)-1,r))




def mem_rod(p,m,r): 
    if r[m] >= 0: 
        return r[m]

    if m==0 : 
        q = 0 
    else: 
        q = -1
        for i in range(1,m+1): 

            q = max(q,p[i] + mem_rod(p,m-i,r))

    r[m] = q 
    return q 
#print("\n\nMem_rod =  ",mem_rod(p,len(p)-1,r))


