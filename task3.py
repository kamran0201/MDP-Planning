import numpy as np
import matplotlib.pyplot as plt
import sys, os, argparse, random, time, subprocess
from math import *

# main
statesfile1="./data/attt/states/states_file_p1.txt"
statesfile2="./data/attt/states/states_file_p2.txt"
policyfile1="./data/attt/policies/p1_policy1.txt"
policyfile2="./data/attt/policies/p2_policy1.txt"

check_folder=os.path.isdir("task3")
if check_folder:
    print("Folder task3 already exists","\n")
else:
    os.makedirs("task3")
    print("Folder task3 created","\n")

# generating successive policies

for i in range(10):
    cmd_encoder="python","encoder.py","--policy",policyfile2,"--states",statesfile1
    print(f"Generating 1.{i} MDP encoding using encoder.py","\n")
    f=open(f"./task3/task3mdp1.{i}.txt","w")
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    cmd_planner="python","planner.py","--mdp",f"./task3/task3mdp1.{i}.txt"
    print(f"Generating 1.{i} Value Policy file using planner.py","\n")
    f=open(f"./task3/task3vnp1.{i}.txt",'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    cmd_decoder="python","decoder.py","--value-policy",f"./task3/task3vnp1.{i}.txt","--states",statesfile1,"--player-id","1"
    print(f"Generating 1.{i} Decoded Policy file using decoder.py","\n")
    f=open(f"./task3/task3policy1.{i}.txt","w")
    subprocess.call(cmd_decoder,stdout=f)
    f.close()

    policyfile1=f"./task3/task3policy1.{i}.txt"

    cmd_encoder="python","encoder.py","--policy",policyfile1,"--states",statesfile2
    print(f"Generating 2.{i} MDP encoding using encoder.py","\n")
    f=open(f"./task3/task3mdp2.{i}.txt","w")
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    cmd_planner="python","planner.py","--mdp",f"./task3/task3mdp2.{i}.txt"
    print(f"Generating 2.{i} Value Policy file using planner.py","\n")
    f=open(f"./task3/task3vnp2.{i}.txt",'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    cmd_decoder="python","decoder.py","--value-policy",f"./task3/task3vnp2.{i}.txt","--states",statesfile2,"--player-id","2"
    print(f"Generating 2.{i} Decoded Policy file using decoder.py","\n")
    f=open(f"./task3/task3policy2.{i}.txt","w")
    subprocess.call(cmd_decoder,stdout=f)
    f.close()

    policyfile2=f"./task3/task3policy2.{i}.txt"

# comparing successive policies
cmd_compare="diff","./data/attt/policies/p1_policy1.txt","./task3/task3policy1.0.txt"
f=open(f"./task3/diff.txt","w")
subprocess.call(cmd_compare,stdout=f)
f.close()
f=open(f"./task3/diff.txt","r")
lines=f.readlines()
length=len(lines)
print(f"diff output for p1_policy1.txt and task3policy1.0.txt has {length} lines","\n")
f.close()

for i in range(9):
    cmd_compare="diff",f"./task3/task3policy1.{i}.txt",f"./task3/task3policy1.{i+1}.txt"
    f=open(f"./task3/diff.txt","w")
    subprocess.call(cmd_compare,stdout=f)
    f.close()
    f=open(f"./task3/diff.txt","r")
    lines=f.readlines()
    length=len(lines)
    print(f"diff output for task3policy1.{i}.txt and task3policy1.{i+1}.txt has {length} lines","\n")
    f.close()

cmd_compare="diff","./data/attt/policies/p2_policy1.txt","./task3/task3policy2.0.txt"
f=open(f"./task3/diff.txt","w")
subprocess.call(cmd_compare,stdout=f)
f.close()
f=open(f"./task3/diff.txt","r")
lines=f.readlines()
length=len(lines)
print(f"diff output for p2_policy1.txt and task3policy2.0.txt has {length} lines","\n")
f.close()

for i in range(9):
    cmd_compare="diff",f"./task3/task3policy2.{i}.txt",f"./task3/task3policy2.{i+1}.txt"
    f=open(f"./task3/diff.txt","w")
    subprocess.call(cmd_compare,stdout=f)
    f.close()
    f=open(f"./task3/diff.txt","r")
    lines=f.readlines()
    length=len(lines)
    print(f"diff output for task3policy2.{i}.txt and task3policy2.{i+1}.txt has {length} lines","\n")
    f.close()
