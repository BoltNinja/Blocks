import sys; args = sys.argv[1:]
numbers = args
if "x" in numbers[0]:
    s = numbers[0].split("x")
    container = (int(s[0]),int(s[1]))
    numbers = numbers[1:]
elif "X" in numbers[1]:
    s = numbers[0].split("X")
    container = (int(s[0]),int(s[1]))
    numbers = numbers[1:]
else:
    container = (int(numbers[0]),int(numbers[1]))
    numbers = numbers[2:]
rectangles = []
for i in numbers:
    splitted = []
    if "x" in i:
        splitted = i.split("x")
    elif "X" in i:
        splitted = i.split("X")
    if splitted!=[]:
        rectangles.append((int(splitted[0]),int(splitted[1])))
new = []
for i in numbers:
    if "x" not in i and "X" not in i:
        new.append(i)
for i in range(int(len(new)/2)):
    rectangles.append((int(new[i*2]),int(new[i*2+1])))
rectangles = sorted(rectangles, key=lambda x: x[0] * x[1], reverse=True)
def find_block_placements(puzzle_height, puzzle_width, block_height, block_width):
    placements = []
    for i in range(puzzle_height - block_height + 1):
        for j in range(puzzle_width - block_width + 1):
            placement = []
            for y in range(block_height):
                for x in range(block_width):
                    index = (i + y) * puzzle_width + (j + x)
                    placement.append(index)
            placements.append(sorted(placement))
    block_height, block_width = block_width, block_height
    for i in range(puzzle_height - block_height + 1):
        for j in range(puzzle_width - block_width + 1):
            placement = []
            for y in range(block_height):
                for x in range(block_width):
                    index = (i + y) * puzzle_width + (j + x)
                    placement.append(index)
            placements.append(sorted(placement))
    return placements
PSBLS = [[] for _ in range(len(rectangles))]
for index, rectangle in enumerate(rectangles):
   for i in range(1+container[1]-rectangle[1]):
       for j in range(1+container[0]-rectangle[0]):
           set1 = set()
           number = j*container[1]+i
           for a in range(number,number+container[1]*rectangle[0],container[1]):
               set1 = set1|{z for z in range(a,a+rectangle[1])}
           PSBLS[index].append(sorted(list(set1)))
   other = (rectangle[1],rectangle[0])#reverse
   for i in range(1+container[1]-other[1]):
       for j in range(1+container[0]-other[0]):
           set1 = set()
           number = j*container[1]+i
           for a in range(number,number+container[1]*other[0],container[1]):
               set1 = set1|{z for z in range(a,other[1]+a)}
           PSBLS[index].append(sorted(list(set1)))#sort both
area = container[0]*container[1]
puzzle = "."*area
alphabet = "abcdefghijklmnopqrstuvwxyz"
DECOMP = dict()
def bruteForce(pzl,psbls,setOfChoices,assignments):
    used = []#invalid
    for i in assignments:
        if i in used:
            return ""
    used.append(i)
    passed = True#return solved
    for i in psbls:
        if i != []:
            passed = False
    if passed: return pzl
    for num, choice in enumerate(setOfChoices):
       if len(choice) == 0:continue
       letter = ""
       locations = []
       for x in alphabet:
           if not x in pzl:
               letter = x
               break
       for j in psbls[num]:
            notpsbl = psbls[num]
            period = [True for i in j if pzl[i] == "."]
            if len(period) < choice[0]*choice[1]: continue
            elif all(period): p = j[0]
            for j in notpsbl:
                if j[0] == p:
                    locations.append(set(j))
            for a in locations:
                subPzl = pzl
                for i in a:
                   subPzl = subPzl[:i] + letter + subPzl[i+1:]
                   DECOMP[letter]= choice
                psbls[num] = []
                assignments[num] = list(a)
                setOfChoices[num] = []
                solve = bruteForce(subPzl,psbls,setOfChoices,assignments)
                if solve: return solve
                setOfChoices [num] = choice
                assignments[num] = []
                psbls[num] = notpsbl
       return ""     
if sum([i[0]*i[1] for i in rectangles])<=container[0]*container[1]:
    solved = bruteForce(puzzle, PSBLS, rectangles, [[] for _ in range(len(rectangles))])
    finalD = []
    lookedThroughAlr = set()
    for i in solved:
        if i==".":
            finalD.append((1,1))
        else:
            if i not in lookedThroughAlr:
                finalD.append(DECOMP[i])
                lookedThroughAlr.add(i) 
    print("Decomposition:", finalD)
else:
    print("No Solution")
# print(DECOMP)
#Aarav Gupta, pd 4, 2025