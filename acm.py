# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 09:04:56 2021

@author: Uday Velakur
"""

#node object
class Node:
    def __init__(self):
        self.Balance = 0
        self.runningMachine = None
        self.Day = 0
        self.Buy = None
        self.Keep = None
        
#machine object contains day buy and sell price and running profit
class Machine:
    def __init__(self, Di, Pi, Ri, Gi):
        self.Di = Di
        self.Pi = Pi
        self.Ri = Ri
        self.Gi = Gi

#case class initialized with case details. Creates the tree and maximizes the profit        
class Case:
    def __init__(self, N, C, D, machine_list):
        self.N = N
        self.C = C
        self.D = D
        self.machine = machine_list
        self.Tree = self.BuildTree()
        
    
    # buy branch sells machine and buys new machine and returns balance
    def buyBranch(self, fork, machine):
        profit = 0
        salePrice = 0
        if fork.runningMachine:
            salePrice = fork.runningMachine.Ri
            profit = fork.runningMachine.Gi * (machine.Di - fork.Day -1)
            
        if machine.Pi <= (fork.Balance + profit + salePrice):
            return fork.Balance + profit + salePrice - machine.Pi 
        else: 
            return fork.Balance 
    # keep branch keeps the current machine and balance and returns machine
    def keepBranch(self, fork, machine):
        try:
            return fork.Balance + fork.runningMachine.Gi*(machine.Di - fork.Day)
        except AttributeError:
            return fork.Balance
            
    #build the tree with given case and machine list    
    def BuildTree(self):
        fork = Node()
        fork.Balance = self.C

        this_row = [fork]
        
        for thisMachine in self.machine:
            new_row = []
            
            for thisFork in this_row:
                thisFork.Buy = Node()
                thisFork.Keep = Node()
                thisFork.Buy.Day = thisMachine.Di
                thisFork.Keep.Day = thisMachine.Di
                
                #Buy branch
                thisFork.Buy.Balance = self.buyBranch(thisFork, thisMachine) 
                if thisFork.Buy.Balance!=thisFork.Balance:
                    thisFork.Buy.runningMachine = thisMachine
                    new_row.append(thisFork.Buy)
                    
                #Keep branch
                thisFork.Keep.Balance = self.keepBranch(thisFork, thisMachine)
                thisFork.Keep.runningMachine = thisFork.runningMachine
                new_row.append(thisFork.Keep)
                      
            this_row = new_row   
        
        return this_row
    
    #maximize the profit in the last row of the tree
    def Maximize(self):
        max_profit = 0
        for thisFork in self.Tree:
           try:
               profit = thisFork.Balance + thisFork.runningMachine.Gi*(self.D - thisFork.Day) + thisFork.runningMachine.Ri
           except AttributeError:
               profit = thisFork.Balance
           if profit>max_profit:
               max_profit = profit
               
        return max_profit
     
#method to read the case and machine list (also sort) from text file
def CaseList(filename):
    Cases = []
    i = 0
    with open(filename) as f:
        data = f.readline().strip().split(" ")
        
        while data!= ["0","0","0"]:
            machine_list = []
            case = list(map(int,data))
            Cases.append(case)
            N = case[0]
            for _ in range(N):
                machine = f.readline().strip().split(" ")
                machine_list.append(list(map(int,machine)))
            machine_list.sort()   
            Cases[i].append([Machine(*machine) for machine in machine_list])    
            data = f.readline().strip().split(" ")
            i+=1
    
    return Cases
                           
def main():
    for i,case in enumerate(CaseList("snapshot_input.txt"), start=1):
        profit = Case(*case).Maximize()
        print("Case %d: %d " %(i,profit))
     
if __name__== "__main__":
    main()