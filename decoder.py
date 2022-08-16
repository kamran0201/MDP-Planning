import numpy as np
import matplotlib.pyplot as plt
import sys, os, argparse, random, time
from math import *

# main
valuepolicyfile=None
statesfile=None
playerid=None
inp=sys.argv
inplen=len(inp)
for i in range(1,(inplen+1)//2):
    if inp[2*i-1] == "--value-policy":
        valuepolicyfile=inp[2*i]
    elif inp[2*i-1] == "--states":
        statesfile=inp[2*i]
    elif inp[2*i-1] == "--player-id":
        playerid=inp[2*i]

print(playerid)

file=open(statesfile,"r")
own_states=file.readlines()
own_states=[own_state.rstrip() for own_state in own_states]
ns=len(own_states)
file.close()

file=open(valuepolicyfile,"r")
actions=file.readlines()
actions=[action.rstrip().split()[1] for action in actions]
file.close()

for i in range(ns):
    probab=[0]*9
    probab[int(actions[i])]=1
    print(f"{own_states[i]} {probab[0]} {probab[1]} {probab[2]} {probab[3]} {probab[4]} {probab[5]} {probab[6]} {probab[7]} {probab[8]}")




