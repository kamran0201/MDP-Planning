import numpy as np
import matplotlib.pyplot as plt
import sys, os, argparse, random, time
from math import *
from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable, PULP_CBC_CMD

# abs diff
def abs_diff(vt_1,vt):
    sum=0
    for i in range(len(vt)):
        sum+=abs(vt[i]-vt_1[i])
    return sum

# value iteration
def vi(ns, na, ends, transitions, mdptype, discount):
    vt=[0.0]*ns
    pit=[0]*ns
    for i in range(ns):
        if i in ends:
            continue
        avail_actions=[transition[1] for transition in transitions if transition[0]==i]
        avail_actions=sorted(list(set(avail_actions)))
        pit[i]=avail_actions[0]
    while True:
        vt_1=vt[:]
        for i in range(ns):
            if i in ends:
                continue
            maxsum=0
            avail_actions=[transition[1] for transition in transitions if transition[0]==i]
            avail_actions=sorted(list(set(avail_actions)))
            for j in avail_actions:
                avail_trans=[transition for transition in transitions if transition[0]==i and transition[1]==j]
                sum=0
                for k in range(len(avail_trans)):
                    sum+=avail_trans[k][4]*(avail_trans[k][3]+discount*vt[avail_trans[k][2]])
                if sum>maxsum:
                    pit[i]=j
                    maxsum=sum
            vt[i]=maxsum
        if abs_diff(vt_1,vt) < 1e-7:
            break
    vt=[format(i,'.6f') for i in vt]
    return [vt, pit]

# policy iteration
def pi(ns, na, ends, transitions, mdptype, discount):
    pit=[0]*ns
    vpi=[0.0]*ns
    for i in range(ns):
        if i in ends:
            continue
        avail_actions=[transition[1] for transition in transitions if transition[0]==i]
        avail_actions=sorted(list(set(avail_actions)))
        pit[i]=avail_actions[0]
    while True:
        pit_1=pit[:]
        a_mat=[[0.0]*ns for i in range(ns)]
        b=[0.0]*ns
        for i in range(ns):
            avail_trans=[transition for transition in transitions if transition[0]==i and transition[1]==pit[i]]
            a_mat[i][i]+=1
            for k in range(len(avail_trans)):
                a_mat[i][avail_trans[k][2]]-=avail_trans[k][4]*discount
                b[i]+=avail_trans[k][4]*avail_trans[k][3]
        vpi=np.linalg.solve(a_mat,b)
        qpi=[[0.0]*na for i in range(ns)]
        for i in range(ns):
            if i in ends:
                continue
            avail_actions=[transition[1] for transition in transitions if transition[0]==i]
            avail_actions=sorted(list(set(avail_actions)))
            for j in avail_actions:
                avail_trans=[transition for transition in transitions if transition[0]==i and transition[1]==j]
                sum=0
                for k in range(len(avail_trans)):
                    sum+=avail_trans[k][4]*(avail_trans[k][3]+discount*vpi[avail_trans[k][2]])
                qpi[i][j]=sum
    
        for i in range(ns):
            if i in ends:
                continue
            avail_actions=[transition[1] for transition in transitions if transition[0]==i]
            avail_actions=sorted(list(set(avail_actions)))
            for j in avail_actions:
                if qpi[i][j]>vpi[i]+1e-4:
                    pit[i]=j
                    break
        if pit_1==pit:
            break
    vpi=[format(i,'.6f') for i in vpi]
    return[vpi, pit]

# linear programming
def lp(ns, na, ends, transitions, mdptype, discount):
    pit=[0]*ns
    model = LpProblem(name="mdp-problem", sense=LpMaximize)
    v = {i: LpVariable(name=f"v{i}") for i in range(ns)}
    vsum=0
    for i in range(ns):
        vsum-=v[i]
    model += vsum
    for i in range(ns):
        for j in range(na):
            avail_trans=[transition for transition in transitions if transition[0]==i and transition[1]==j]
            sum=0
            for k in range(len(avail_trans)):
                sum+=avail_trans[k][4]*(avail_trans[k][3]+discount*v[avail_trans[k][2]])
            model += (v[i] >= sum)
    model.solve(solver=PULP_CBC_CMD(msg=False))
    vpi=[0.0]*ns
    for var in model.variables():
        vpi[int(var.name[1:])]=var.value()
    for i in range(ns):
        if i in ends:
            continue
        maxsum=0
        avail_actions=[transition[1] for transition in transitions if transition[0]==i]
        avail_actions=sorted(list(set(avail_actions)))
        pit[i]=avail_actions[0]
        for j in avail_actions:
            avail_trans=[transition for transition in transitions if transition[0]==i and transition[1]==j]
            if len(avail_trans)==0:
                continue
            sum=0
            for k in range(len(avail_trans)):
                sum+=avail_trans[k][4]*(avail_trans[k][3]+discount*vpi[avail_trans[k][2]])
            if sum>maxsum:
                pit[i]=j
                maxsum=sum
    vpi=[format(i,'.6f') for i in vpi]
    return[vpi, pit]

# main
mdp=None
algorithm="lp"
inp=sys.argv
inplen=len(inp)
for i in range(1,(inplen+1)//2):
    if inp[2*i-1] == "--mdp":
        mdp=inp[2*i]
    elif inp[2*i-1] == "--algorithm":
        algorithm=inp[2*i]

file=open(mdp,"r")
alls=file.readlines()
numalls=len(alls)
alls=[(all.rstrip().split())[1:] for all in alls]
ns=int(alls[0][0])
na=int(alls[1][0])
ends=alls[2]
ends=[int(end) for end in ends]
transitions=alls[3:numalls-2]
transitions=[[int(transition[0]), int(transition[1]), int(transition[2]), float(transition[3]), float(transition[4])] for transition in transitions]
mdptype=alls[numalls-2][0]
discount=float(alls[numalls-1][0])
file.close()

if algorithm == "vi":
    vtpit=vi(ns,ns,ends,transitions,mdptype,discount)
    vt=vtpit[0]
    pit=vtpit[1]
    for i in range(len(vt)):
        print(vt[i]+' '+str(pit[i]))
elif algorithm == "hpi":
    vtpit=pi(ns,ns,ends,transitions,mdptype,discount)
    vt=vtpit[0]
    pit=vtpit[1]
    for i in range(len(vt)):
        print(vt[i]+' '+str(pit[i]))
elif algorithm == "lp":
    vtpit=lp(ns, na, ends, transitions, mdptype, discount)
    vt=vtpit[0]
    pit=vtpit[1]
    for i in range(len(vt)):
        print(vt[i]+' '+str(pit[i]))
