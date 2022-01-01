from os import sched_get_priority_max, stat
import os
import sys
import time
import tracemalloc
import argparse
from types import prepare_class
import psutil

GAP_PENALTY = 30
COST_ARRAY = [[0,110,48,94],
              [110,0,118,48],
              [48,118,0,110],
              [94,48,110,0]]

def cost(charA,charB):
    char_idx = {'A':0,'C':1,'G':2,'T':3}
    return COST_ARRAY[char_idx[charA]][char_idx[charB]]

def createStrings(base,idx):
    str1 = base
    for i in idx:
        # can we make this more efficient?
        # I think python will be creating a new string copying everything.
        # That will make this a linear operation instead of O(1)
        #Alternative 1 : Working faster for small inp, need to check diff for large ones
        #str1 = ''.join([str1[:i+1] , str1 , str1[i+1:]])
        str1 = str1[:i + 1] + str1 + str1[i + 1:]
    return str1

'''
Reverses the strings and calls space effecient matching.
'''
def sequenceAlignmentSpaceEfficientBack(str1,str2,res=None):
    return sequenceAlignmentSpaceEfficient(str1[::-1],str2[::-1],res)

'''
Uses mx2 space. This returns only the optimized cost.
Since this is space optimized it loses on information
required to generate the matched strings.
'''
def sequenceAlignmentSpaceEfficient(str1,str2,res=None):
    n = len(str1)
    m = len(str2)

    dp = [[float('inf')] * (m+1) for _ in range(2)]
    
    #base case
    dp[0][0] = 0
    for i in range(1,m+1):
        dp[0][i] = dp[0][i-1]+GAP_PENALTY
    dp[1][0] = GAP_PENALTY
    
    #bottom up
    pos = 1
    for i in range(1,n+1):
        dp[pos%2][0] = dp[(pos-1)%2][0] + GAP_PENALTY
        for j in range(1,m+1):
            dp[pos%2][j] = min(dp[pos%2][j-1] + GAP_PENALTY,
                               dp[(pos-1)%2][j] + GAP_PENALTY,
                               dp[(pos-1)%2][j-1] + cost(str1[i-1], str2[j-1]))
        pos += 1
    if res != None:
        res += dp[(pos-1)%2]
    return dp[(pos-1)%2][m]

    
'''
The internal attribute is used by the D&C algo
to output the string indexes instead of actual strings.
'''
def sequenceAlignment(str1, str2,internal=False):
    n = len(str1)
    m = len(str2)

    '''
    We create an array of size m+1 * n+1 because we also need to consider the
    case when we compare all of str1 with none of str2. Thus do[0][1] means we
    are calculating the cost for matching the first character of str2 with none
    of str1.
    '''
    dp = [[float('inf')]* (m+1) for _ in range(n+1)]

    #base case

    dp[0][0] = 0
    for i in range(1,n+1):
        dp[i][0] = dp[i-1][0] + GAP_PENALTY

    for j in range(1,m+1):
        dp[0][j] = dp[0][j-1] + GAP_PENALTY

    # bottom up
    for i in range(1,n+1):
        for j in range(1,m+1):
            dp[i][j] = min(dp[i][j-1] + GAP_PENALTY, dp[i-1][j] + GAP_PENALTY, dp[i-1][j-1] + cost(str1[i-1],str2[j-1]))

    # top down
    i,j = n,m
    res_str1 = ""
    res_str2 = ""
    points = []
    while i>0 and j>0:
        if dp[i][j] == dp[i][j-1] + GAP_PENALTY:
            res_str1 = '_' +res_str1
            res_str2 = str2[j-1] + res_str2
            #res_str1 = str1[i-1]+res_str1
            #res_str2 = '_' + res_str2
            if internal:
                points.append([i-1,j-2])
            j -= 1
        elif dp[i][j] == dp[i-1][j] + GAP_PENALTY:
            res_str1 = str1[i-1]+res_str1
            res_str2 = '_' + res_str2
            #res_str2 = str2[j-1] + res_str2
            #res_str1 = '_' + res_str1
            if internal:
                points.append([i-2,j-1])
            i-=1
        else:
            res_str1 = str1[i-1] + res_str1
            res_str2 = str2[j-1] + res_str2
            if internal:
                points.append([i-2,j-2])
            i-=1
            j-=1
    while i>0:
        res_str1 = str1[i-1] + res_str1
        res_str2 = '_' + res_str2
        if internal:
            points.append([i-2,j-1])
        i-=1

    while j>0:
        res_str2 = str2[j-1] + res_str2
        res_str1 = '_' + res_str1
        if internal:
            points.append([i-1,j-2])
        j -= 1
    if internal:
        return points
    return [res_str1,res_str2, dp[n][m]]

'''
Wrapper function to avoid passing str1 and str2 by value
'''
def sequenceAlignmentDC(str1, str2, res, i, j, x, y):
    '''
    Divide and Conquer recurrsion function.
    i,j are starting and ending indices for str1.
    x,y are starting and ending indices for str2.
    '''
    def sequenceAlignmentDC_inner(i, j, x, y):
        # Base case. Solve using vanilla sequence alignment algorithm.
        if j-i+1 <= 2 or y-x+1<=2:
            tmp = sequenceAlignment(str1[i:j+1],str2[x:y+1],True)
            for p in tmp:
                res.append([i+p[0],x+p[1]])
            return
    
        n = y-x +1
        m = (j-i+1)//2
        minValue = float('inf')
        minIndex = 0
        space_k_fwd = []
        space_k_bwd = []
        A = sequenceAlignmentSpaceEfficient(str1[i:i+m],str2[x:y+1],space_k_fwd)
        B = sequenceAlignmentSpaceEfficientBack(str1[i+m:j+1],str2[x:y+1], space_k_bwd)
        for k in range(n+1):
            A = space_k_fwd[k]
            B = space_k_bwd[k]
            if A+B < minValue:
                minValue = A+B
                minIndex = k
        sequenceAlignmentDC_inner(i,i+m-1,x,x+minIndex-1)
        sequenceAlignmentDC_inner(i+m,j,x+minIndex,y)
    sequenceAlignmentDC_inner(i, j, x, y)
    return sequenceAlignmentSpaceEfficient(str1, str2)

'''
Get the cost for matching str1 with str2
'''
def getScore(str1,str2):
    p = 0
    c = 0
    assert(len(str1) == len(str2))
    while p<len(str1) and p < len(str2):
        if str1[p] == '_' or str2[p] == '_':
            c += GAP_PENALTY
            p+=1
            continue
        if str1[p] != str2[p]:
            c += cost(str1[p],str2[p])
            p+=1
            continue
        p+=1
    return c

def writeOutput(str1, str2, time_taken, mem, opt_val = 0):
    with open('output.txt', 'w') as f:
        print(str1[:50] + " " + str1[-50:], file=f)
        print(str2[:50] + " " + str2[-50:], file=f)
        print(str(opt_val), file=f)
        print(str(time_taken), file=f)
        print(str(mem), file=f)

'''
Used to create the string matching from the points
array populated by the divide and conquer algorithm.
'''
def getStrfromPoints(points,str1,str2):
    points.sort()
    res1 = ""
    res2 = ""
    prev_i = points[0][0]
    prev_j = points[0][1]
    for i,j in points[1:]:
        if i == prev_i:
            res1 += '_'
        else:
            res1 += str1[i]
            prev_i = i
        if j == prev_j:
            res2 += '_'
        else:
            res2 += str2[j]
            prev_j = j
    return [res1,res2]

'''
Output verification by calculating the
cost for the matched string output.
'''
def test(str1,str2,opt):
    if getScore(str1,str2) == opt:
        print("TestPassed")
    else:
        print("Failed")
        print(str1)
        print(str2)
        print(opt)
        print(getScore(str1,str2))

def startStat():
    start = time.time()
    tracemalloc.start()
    return start

def endStat(start):
    #end time
    end = time.time()
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    '''
    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)
    '''
    res = [] # list containing [total_time, memory_used]
    res.append(end-start)
    res.append((top_stats[0].size*1.0/1024))
    return res

def main():
    parser = argparse.ArgumentParser(description='$python3 '+sys.argv[0]+'.py <path to input file> <op_code>')
    parser.add_argument('file',
                    help='Test input file path')
    parser.add_argument('--stat', action='store_true',
                    help='Enable memory and performance stat collection')
    parser.add_argument('--space', action='store_true',
                    help='Use space efficient algorithm')
    parser.add_argument('--dc', action='store_true',
                    help='Use divide and conquer algorithm')
    parser.add_argument('--test', action='store_true',
                    help='run validation test')
    args = parser.parse_args()

    start = startStat()

    str1_idx = []
    str2_idx = []
    str1 = ""
    str2 = ""
    with open(args.file,'r') as fd:
        lines = fd.readlines()
        str1 = lines[0].strip()
        idx_str1 = True
        for l in lines[1:]:
            if l[0].isdigit():
                if idx_str1:
                    str1_idx.append(int(l))
                else:
                    str2_idx.append(int(l))
            else:
                str2 = l.strip()
                idx_str1 = False

    str1 = createStrings(str1,str1_idx)
    str2 = createStrings(str2,str2_idx)
   
    if args.dc:
        res = []
        value = sequenceAlignmentDC(str1,str2,res,0,len(str1)-1,0,len(str2)-1)
        res.append([len(str1)-1,len(str2)-1])
        match = getStrfromPoints(res,str1,str2)
        stats = endStat(start)
        writeOutput(match[0], match[1], stats[0], psutil.Process(os.getpid()).memory_info().rss/1024, value)
        if args.test:
            test(match[0],match[1],sequenceAlignmentSpaceEfficient(str1,str2))
    elif args.space:
        res = sequenceAlignmentSpaceEfficient(str1,str2)
        stats = endStat(start)
        writeOutput("", "", stats[0], psutil.Process(os.getpid()).memory_info().rss/1024, res)
    else:
        res = sequenceAlignment(str1,str2)
        stats = endStat(start)
        if args.test:
            test(res[0],res[1],res[2])
        writeOutput(res[0], res[1], stats[0], psutil.Process(os.getpid()).memory_info().rss/1024, res[2])
    


    #printing the memory allocated - current and peak. Check if tracemalloc peak is the size we need to show?
    if args.stat:
        print(tracemalloc.get_traced_memory())

if __name__ == '__main__':
    main()