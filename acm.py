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
        
       
    def BuildTree(self):
        fork = Node()
        fork.Balance = self.C

        this_row = [fork]
        if self.N == 0: return this_row
            
        for i,thisMachine in enumerate(self.machine):
            new_row = []
                
            for thisFork in this_row:
                thisFork.Buy = Node()
                thisFork.Keep = Node()
                thisFork.Buy.Day = thisMachine.Di
                thisFork.Keep.Day = thisMachine.Di
                
    
                profit = 0
                salePrice = 0
                if thisFork.runningMachine:
                    salePrice = thisFork.runningMachine.Ri
                    profit = thisFork.runningMachine.Gi * (thisMachine.Di - thisFork.Day -1)
            
                if thisMachine.Pi <= (thisFork.Balance + profit + salePrice):
                    thisFork.Buy.Balance = thisFork.Balance + profit + salePrice - thisMachine.Pi 
                    thisFork.Buy.runningMachine = thisMachine
                    new_row.append(thisFork.Buy)
                                
                #Keep branch
                thisFork.Keep.runningMachine = thisFork.runningMachine
                try:
                    thisFork.Keep.Balance = thisFork.Balance + thisFork.runningMachine.Gi*(thisMachine.Di - thisFork.Day)
                except AttributeError:
                    thisFork.Keep.Balance = thisFork.Balance
                new_row.append(thisFork.Keep)
            this_row = new_row
              
        return this_row
    
    # def Check_Profit(self, row):
    #     running_profits = [thisFork.Balance + thisFork.runningMachine.Gi*(self.C - thisFork.Day) + thisFork.runningMachine.Ri for thisFork in row if thisFork.runningMachine]
    #     if not running_profits: return [row[-1]] 
    #     maxprofit = max(running_profits)
    #     row_profit = [thisFork for thisFork in row if thisFork.runningMachine and thisFork.Balance + thisFork.runningMachine.Gi*(self.C - thisFork.Day) + thisFork.runningMachine.Ri == maxprofit]
    #     row_profit.append(row[-1])
    #     return row_profit

    
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
      for i,case in enumerate(CaseList("works.in.txt"), start=1):
          profit = Case(*case).Maximize()
          print("Case %d: %d " %(i,profit))
         
if __name__== "__main__":
    main()