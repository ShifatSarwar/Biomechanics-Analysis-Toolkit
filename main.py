from functions import getFile, readFiles, runAlgorithm, getStrides, getR
from functions_Matlab import *
from functionsPython import *

def runAlgorithm(t1, column, num):  
    if num == 2:
        runDFA(t1, column)
    else:    
        # tau = runAMIThomas(t1, column)
        tau = int(runAMI_Stergio_M(t1, column))
        dim = int(runFNN(t1, column, tau))
        
        if num == 1:   #Code to run RQA 
            runRQA(t1, tau, dim, column)
            
        elif num == 3: #Code to run LyE_W
            # runLYE_W(t1, column,tau, dim)
            runLyE_W_M(t1, column,tau,dim)
        elif num == 4: #Code to run LyE_R
            runLyE_R_M(t1, column, tau, dim)
        elif num == 5: #Code to run Ent_Ap
            # runEnt_Ap(t1, dim, column)
            runEntAp(t1, dim, column)
        elif num == 6:
            # runEnt_Permu(t1, dim, tau, column)
            runEntPermu(t1, dim, tau, column)
        elif num == 7:
            r = getR(t1)
            runEntSamp(t1, dim, r, column)


if __name__ == '__main__':
    #Choose Algorithm
    # RQA         : 1
    # DFA         : 2
    # LyE_W       : 3
    # LyE_R       : 4
    # Ent_Ap      : 5
    # Ent_Permu   : 6
    # Ent_Samp    : 7
    num = 1

    # Get the trained file
    # 0 for parquet and 1 for csv file
    train = getFile(0)
    # Get the number and names of colums
    lines = readFiles(train)
    # Loop through columns
    for x in lines:
        column = x.strip('\n')
        if (x != ''):
            t1 = train[column]
            if (column == 'LTContact' or column == 'RTContact'):
                t2 = train['time']
                t3 = train['LTContact']
                t1 = getStrides(t1,t2)
            runAlgorithm(t1, column, num)

















