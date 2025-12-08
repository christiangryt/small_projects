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

    for i in range(height):

        for j in range(width):

            nabo_teller = 0
            tegn = arr[i][j]
            print (f"[{i} {j}]. {tegn}")

            if tegn == "@":
                
                for dir in directions:
                    x = i + dir[0]
                    y = j + dir[1]
                    
                    try:
                        if x < 0 or y < 0:
                            continue

                        nabo = arr[x][y]
                        if nabo == "@":
                            nabo_teller += 1

                        print (f"   Ser på {x} {y}. {nabo}")
                    
                    except:

                        continue

                if nabo_teller < max_nabo:
                    print ("Good")
                    accessable += 1
                    continue
            
    print (accessable)

def parse_input(matrise, linje):

    matrise.append(linje)

eksempel =  [
    [".", "@", ".", "@", "@"],
    [".", "@", "@", ".", "@"],
    [".", ".", ".", ".", "@"],
    ["@", "@", "@", ".", "@"],
    [".", "@", "@", ".", "@"],
    [".", ".", "@", "@", "@"],
    ["@", "@", ".", "@", "@"],
    [".", "@", ".", ".", "@"],
]

#ruller(eksempel)

with open("data-test.txt") as f:
    
    matrise = []

    while (rad := f.readline().strip()):
        rad = list(rad)
        parse_input(matrise, rad)
    
    print (matrise)
    ruller(matrise)