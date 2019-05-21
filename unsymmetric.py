
## ungeschlagener Weltmeister auf (n+1,n) und (n,n+1) Boards
def unsymmetric(m,n, move):
    i, j = move
    if m < n:
##      Fall 2   
        if n-(m+1) >= 2:
##          if move aus Left        
            if Left(i, j, m):
                return ((m-1)-j, m-i)
##          if move aus Right        
            elif Right(i, j, m):
                return (m-j, (m-1)-i)
##          Fall 2, da gerade Anzahl an Stripes            
            if Case2(i, j, m, n):
##          if m gerade, so beginnt Stripe bei ungeraden indizes
##          if j gerade, so ist move aus RightStripe
##          if m ungerade, so beginnt Stripe bei geraden indizes                    
##          if j gerade, so ist move aus RightStripe
                return Stripe(i, j, m)
##          Fall 3                    
            elif Case3(i, j, m, n):
##          if letzte Spalte, so war move im extra Stripe                
                if j == n-1:
##          if m gerade, gibt es keine freie Stelle                    
                    if m%2 == 0:
                        if i%2 == 0:
                            return (i+1, j)
                        else:
                            return (i-1, j)
                    else:
                        if i != m-1:  
                            if i%2 == 0:
                                return (i+1, j)
                            else:
                                return (i-1, j)
##          move war freie Stelle
                        else:
                            pass
                return Stripe(i, j, m)
##      Fall 1 und {TODO4}
        else:
            return Case1(i, j, m)
    else:
        if m-(n+1) >= 2:
            if Left(j, i, n):
                return (n-j, (n-1)-i)        
            elif Right(j, i, n):
                return ((n-1)-j, n-i)
            if i >= n+1 and (m-(n+1))%2 == 0:
                if n%2 == 0:
                    if i%2 == 0:
                        return (i-1, j)
                    else:
                        return (i+1, j)
                else:
                    if i%2 == 0:
                        return (i+1, j)
                    else:
                        return (i-1, j)
            elif n+1 <= i <= m-1 and (m-(n+1))%2 != 0:
                if i == m-1:
                    if n%2 == 0:
                        if j%2 == 0:
                            return (i, j+1)
                        else:
                            return (i, j-1)
                    else:
                        if j != n-1:  
                            if j%2 == 0:
                                return (i, j+1)
                            else:
                                return (i, j-1)
                        else:
                            pass
                if n%2 == 0:
                    if i%2 == 0:
                        return (i-1, j)
                    else:
                        return (i+1, j)
                else:
                    if i%2 == 0:
                        return (i+1, j)
                    else:
                        return (i-1, j)
        else:
            if 0 <= i <= (n-1) and i+j < n:
                return (n-j, (n-1)-i)        
            elif 1 <= i <= n and i+j >= n:
                return ((n-1)-j, n-i)
##TODO Fall 4
def Case1(i, j, m):
##      if move aus Left        
        if Left(i, j, m):
            return ((m-1)-j, m-i)
##      if move aus Right        
        elif Right(i, j, m):
            return (m-j, (m-1)-i)
    
def Case2(i, j, m, n):
    if m+1 <= j <= n-1 and (n-(m+1))%2 == 0:
        return True
    else:
        return False
            
def Case3(i, j, m, n):
    if m+1 <= j <= n-1 and (n-(m+1))%2 != 0:
        return True
    else:
        return False
    
def Left(i, j, m):
    if 0 <= j <= (m-1) and i+j < m:
        return True
    else:
        return False
    
def Right(i, j, m):
    if 1 <= j <= m and i+j >= m:
        return True
    else:
        return False
    
def Stripe(i, j, m):
    if m%2 == 0:            
        if j%2 == 0:
            return (i, j-1)
        else:
            return (i, j+1)
    else:                    
        if j%2 == 0:                        
            return (i, j+1)
        else:
            return (i, j-1)
        
