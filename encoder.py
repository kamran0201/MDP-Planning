import numpy as np
import matplotlib.pyplot as plt
import sys, os, argparse, random, time
from math import *

# main
policyfile=None
statesfile=None
inp=sys.argv
inplen=len(inp)
for i in range(1,(inplen+1)//2):
    if inp[2*i-1] == "--policy":
        policyfile=inp[2*i]
    elif inp[2*i-1] == "--states":
        statesfile=inp[2*i]

na=9
file=open(policyfile,"r")
policys=file.readlines()
policys=[policy.rstrip().split() for policy in policys]
rival_player=policys[0][0]
policys=policys[1:]
numpolicys=len(policys)
rival_states=[policy[0] for policy in policys]
probabs=[[float(pb) for pb in policy[1:]] for policy in policys]
file.close()

own_player=None
if rival_player=="1":
    own_player="2"
elif rival_player=="2":
    own_player="1"

file=open(statesfile,"r")
own_states=file.readlines()
own_states=[own_state.rstrip() for own_state in own_states]
ns=len(own_states)
file.close()

print(f"numStates {(ns+1)}")
print(f"numActions {(na)}")
print(f"end {ns}")

for i in range(ns):
    currstate=own_states[i]
    psbl_a=[i for i, ch in enumerate(currstate) if ch=="0"]
    for j in psbl_a:
        tempstate=currstate[:j]+own_player+currstate[j+1:]
        if tempstate not in rival_states:
            print(f"transition {i} {j} {ns} 0.0 1.0")
            continue
        tempidx=rival_states.index(tempstate)
        for k in range(na):
            if probabs[tempidx][k] == 0:
                continue
            nextstate=tempstate[:k]+rival_player+tempstate[k+1:]
            if nextstate not in own_states:
                print(f"transition {i} {j} {ns} 1.0 {probabs[tempidx][k]}")
                continue
            nextidx=own_states.index(nextstate)
            print(f"transition {i} {j} {nextidx} 0.0 {probabs[tempidx][k]}")

print("mdptype episodic")
print("discount 1.0")
