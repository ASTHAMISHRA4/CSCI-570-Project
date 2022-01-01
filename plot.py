
import os
import random
from matplotlib import pyplot
import math
import test

INP_SIZE = 10
INP_STEP = 100
INP_POINTS = 30

def genNums(count):
    nums = []
    sz = 4
    for i in range(count):
        nums.append(int(random.random()*sz))
        sz*=2
    return nums

def getBase():
    genes = {0:'A', 1:'C', 2:'T', 3:'G'}
    str1 = str2 = ""
    for i in range(4):
        str1+=genes[int(random.random()*2)]
    for i in range(4):
        str2+=genes[int(random.random()*2)]
    return [str1,str2]

input_size = []
time_points_normal = []
time_points_eff = []
memory_points_normal = []
memory_points_eff = []

#for inp_size in range(4,INP_POINTS*INP_STEP,INP_STEP):
for inp_size in range(INP_SIZE):
    input_str = getBase()
    nums_str1 = genNums(inp_size)
    nums_str2 = genNums(inp_size)
#    nums_str1 = test.random_string(inp_size)
#    nums_str2 = test.random_string(inp_size)
    total_input_size = len(input_str) * 2 ** len(nums_str1) + len(input_str) * 2 ** len(nums_str2)
 #   total_input_size = len(nums_str1) + len(nums_str2)
    print(total_input_size)
    with open('inp.txt', 'w') as f:
        print(input_str[0], file=f)
        for i in range(inp_size):
            print(nums_str1[i], file=f)
        print(input_str[1], file=f)
        for i in range(inp_size):
            print(nums_str2[i], file=f)

    #Normal version
    os.system('python3 SequenceAlignment.py inp.txt')
    with open('output.txt', 'r') as f:
        lines = f.readlines()
        time_taken = float(lines[-2])
        mem_taken = float(lines[-1])
    input_size.append(total_input_size)
    time_points_normal.append(time_taken)
    memory_points_normal.append(mem_taken)

    #Memory Efficient version
    os.system('python3 SequenceAlignment.py --dc inp.txt')
    with open('output.txt', 'r') as f:
        lines = f.readlines()
        time_taken = float(lines[-2])
        mem_taken = float(lines[-1])
    time_points_eff.append(time_taken)
    memory_points_eff.append(mem_taken)

with open('data','w') as f:
    for i in range(INP_SIZE):
        f.write("%d, %f, %f\n" %(input_size[i], time_points_normal[i], time_points_eff[i]))
        f.write("%d, %f, %f\n" %(input_size[i], memory_points_normal[i], memory_points_eff[i]))

pyplot.xlabel("Input size")
pyplot.ylabel("Time : Normal(red) & Efficient (blue) in seconds", fontsize=10)
pyplot.plot(input_size,time_points_normal,label='normal')
pyplot.plot(input_size,time_points_eff,label='efficient')
pyplot.legend()
pyplot.savefig('graph_time.png')

pyplot.clf()
pyplot.xlabel("Input size")
pyplot.ylabel("Memory : Normal(red) & Efficient (blue) in kb")
pyplot.plot(input_size,memory_points_normal,label='normal')
pyplot.plot(input_size,memory_points_eff,label='efficient')
pyplot.legend()
pyplot.savefig('graph_memory.png')
    
