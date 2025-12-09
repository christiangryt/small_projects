import copy

def ruller(arr):

    height = len(arr)
    width = len(arr[0])

    directions = [
        [-1,0],
        [-1, 1],
        [-1, -1],
        [0,1],
        [1,1],
        [1,0],
        [1,-1],
        [0,-1]
    ]
    
    accessable = 0
    max_nabo = 4
    flere_endre = True
    
    iter_liste = []
    for row in arr:
        iter_liste += row
    
    while flere_endre:
        
        flere_endre = False

        for k, i in enumerate(iter_liste):

            nabo_teller = 0
            tegn = i
            print (f"{tegn}")
            
            xx = k // height
            yy = k % width

            if tegn == "@":
                
                for dir in directions:
                    x = xx + dir[0]
                    y = yy + dir[1]
                    
                    if x < 0 or y < 0 or x >= height or y >= width:
                        continue

                    nabo = arr[x][y]
                    if nabo == "@":
                        nabo_teller += 1

                    print (f"   Ser på {x} {y}. {nabo}")
                    
                if nabo_teller < max_nabo:
                    #print (f"{k} {k} fjernet")k
                    accessable += 1
                    arr[xx][yy] = "."
                    iter_liste.pop(k)
                    flere_endre = True
            
            else:
                iter_liste.pop(k)
                
    print (accessable)

    for jj in arr:
        print (jj)

def parse_input(matrise, linje):

    matrise.append(linje)
    
with open("data-test.txt") as f:
    
    matrise = []

    while (rad := f.readline().strip()):
        rad = list(rad)
        parse_input(matrise, rad)
    
    print (matrise)
    ruller(matrise)