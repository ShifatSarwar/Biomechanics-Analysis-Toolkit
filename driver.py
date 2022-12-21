from functions import *
from functions_Matlab import *
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import random
import time

def addLine(name, line):
    with open(name, 'a') as f:
       f.write(line)
       f.write("\n")
    f.close()

def runAlgorithm(t1, column, algorithm, param_array):    
    
    # DFA
    if algorithm == 2:
        # Change parameter values from default
        plotOption = 1
        n_min = 16 # minimum box size 
        n_max = len(t1)/9 # maximum box size
        n_length = 18 # number of points to sample best fit
        if len(param_array) == 1:
            n_min = param_array[0]
        elif len(param_array) == 2:
            n_min = param_array[0]
            n_max = param_array[1]
        elif len(param_array) == 3:
            n_min = param_array[0]
            n_max = param_array[1]
            n_length = param_array[2]
        elif len(param_array) == 4:
            n_min = param_array[0]
            n_max = param_array[1]
            n_length = param_array[2]
            plotOption = param_array[3]            

        runDFA(t1, column)
    
    # Ent_Sample
    elif algorithm == 7: #Code to run Ent_Sample
        r = getR(t1)
        dim = param_array[0]
        if(len(param_array)) == 2:
            r = param_array[1]

        runEntSamp_M(t1, dim, r, column)
        # runEnt_Samp(t1, dim, column)

    # AMI_Stergio 
    elif algorithm == 3:
        n = 200
        if len(param_array) == 1:
            n = param_array[0]
        tau = int(runAMI_Stergio_M(t1, column))
    
    # FNN
    elif algorithm == 4:
        MaxDim, Rtol, Atol, speed = 10,15,2,0
        if len(param_array) == 4:
            MaxDim = param_array[0]
            Rtol = param_array[1]
            Atol = param_array[2]
            speed = param_array[3]

        dim = int(runFNN(t1, column, tau))
    
    else:

        if param_array[0] == 1:
            n = 200 # maximal lag
            # tau = runAMIThomas(t1, column)
            tau = int(runAMI_Stergio_M(t1, column))
            MaxDim, Rtol, Atol, speed = 10,15,2,0 
            dim = int(runFNN(t1, column, tau))
            
        # RQA
        if algorithm == 1:   #Code to run RQA 
            
            if len(param_array) == 6:
                if param_array[0] != 1:
                    print("Select 1 or give tau and dim values manually")
                    return
                zScore = param_array[1]
                norm = param_array[2]
                setParam = param_array[3]
                setValue = param_array[4]
                plotOption = param_array[5]

            elif len(param_array) == 8:
                tau = param_array[1]
                dim = param_array[2]
                zScore = param_array[3]
                norm = param_array[4]
                setParam = param_array[5]
                setValue = param_array[6]
                plotOption = param_array[7]

            else:
                if param_array == 1:
                    runRQA(t1, tau, dim, column)
                else:
                    print("Select 1 or give tau and dim values manually")
                    return
            
        # LyE_W
        elif algorithm == 5: #Code to run LyE_W
            sampFrequency = 200
            evolve = 0.2

            if len(param_array) == 3:
                if param_array[0] != 1:
                    print("Select 1 or give tau and dim values manually")
                    return
                sampFrequency = param_array[1]
                evolve = param_array[2]
            
            elif len(param_array) == 5:
                tau = param_array[1]
                dim = param_array[2]
                sampFrequency = param_array[3]
                evolve = param_array[4]
            
            else:
                if param_array[0] == 1:
                    runLYE_W(t1, column,tau, dim)
                    # runLyE_W_M(t1, column,tau,dim)
                else:
                    print("Select 1 or give tau and dim values manually")
                    return

        # LyE_R
        elif algorithm == 6: #Code to run LyE_R
            sampFrequency = 200

            if len(param_array) == 2:
                sampFrequency = param_array[1]
            elif len(param_array) == 4:
                tau = param_array[1]
                dim = param_array[2]
                sampFrequency = param_array[3]
            
            else:
                if param_array[0] == 1:
                    runLyE_R_M(t1, column, tau, dim)
                else:
                    print("Select 1 or give tau and dim values manually")
                    return        
        
        # Ent_Ap
        elif algorithm == 8: #Code to run Ent_Ap
            tolerance_r = 0.2

            if len(param_array) == 3:
                dim = param_array[1]
                tolerance_r = param_array[2]
            elif len(param_array) == 2:
                if param_array[0] == 1:
                    tolerance_r = param_array[1]
                else:
                    dim = param_array[1]
            else:
                if param_array[0] == 1:
                    runEntAp(t1, dim, tolerance_r, column)
                else:
                    print("Change First Parameter to 1 if dim needs to be calculated before analysis")
                    return

        # Ent_MS_Plus
        elif algorithm == 9: #Code to run Ent_MS_Plus
            
            m = 2 # Length of vectors to be compared
            r = getR(t1) # Radius for accepting matches
            
            if len(param_array) == 4:
                tau = param_array[1]
                m = param_array[2]
                r = param_array[3]
        
            elif len(param_array) == 3:
                if param_array[0] == 1:
                    m = param_array[1]
                    r = param_array[2]
                else:
                    tau = param_array[1]
                    m = param_array[2]
            
            elif param_array[0] != 1:
                print("Change First Parameter to 1 if dim needs to be calculated before analysis")
                return
            
            elif len(param_array) == 2:
                m = param_array[1]

            # runEntMSPlus(t1,tau2,m,r,column)
            runEntMSPlus_M(t1,tau,m,r,column)

        # Ent_Permu
        elif algorithm == 10: #Code to run Ent_Permu
            m = 2 # Length of vectors to be compared
            tau = 0 # Radius for accepting matches
            
            if len(param_array) == 3:
                tau = param_array[1]
                m = param_array[2]
            
            elif param_array[0] != 1:
                print("Change First Parameter to 1 if dim needs to be calculated before analysis")
                return
            
            elif len(param_array) == 2:
                m = param_array[1]

            runEntPermu(t1, dim, tau, column)

        # Ent_Symbolic
        elif algorithm == 11:
            x = t1 # 1D binary array of data column
            # x = convertTo1D(t1)
            l = len(t1) # Word Length
            runEntSymbolic(t1,l,column)

        # Ent_xSamp
        elif algorithm == 12:
            x = t1 # first data series
            y = t1 # second data series
            m = 2 # vector length for matching
            R = getR(t1) # tolerance for finding matches
            norm = 1 
            runEntXSamp(x,y,m,R,norm,column)
            
def getStrides(t1,t2):
    aStart = []
    sTime = []
    aEnd = []
    eTime = []
    index = 0
    down = True
    aStart.append(index)
    sTime.append(index)
    for x in t1:
        if x == 1000.0:
            if(down):
                index=index+1
            else:
                aStart.append(index)
                sTime.append(t2[index])
                down = True
        elif x == 0.0:
            if (down):
                aEnd.append(index-1)
                eTime.append(t2[index-1])
                down = False
            else:
                index=index+1
    
    # index = 0
    # down = True
    # a2Start = []
    # s2Time = [] 
    # a2End = []
    # e2Time = []
    # a2Start.append(index)
    # s2Time.append(index)
    # for x in t3:
    #     if x == 1000.0:
    #         if(down):
    #             index=index+1
    #         else:
    #             a2Start.append(index)
    #             s2Time.append(t2[index])
    #             down = True
    #     elif x == 0.0:
    #         if (down):
    #             a2End.append(index-1)
    #             e2Time.append(t2[index-1])
    #             down = False
    #         else:
    #             index=index+1
    divided_a =[]
    for x in aStart:
        divided_a.append(x/10.0)
    
    strideDiff = []
    index = 0
    # # while index < len(aStart):
    # #     x = sTime[index]-s2Time[index]
    # #     strideDiff.append(abs(x))
    # #     index+=1
    while index < len(aStart)-1:
        strideDiff.append(divided_a[index+1]-divided_a[index])
        index+=1
    pathF = 'Results/Datas/s2.csv'
    addLine(pathF, column)
    for x in strideDiff:
        addLine(pathF, str(x))
    del sTime[-1]
    plt.plot(sTime, strideDiff)
    
    # giving a title to my graph
    plt.title(column)
    plt.savefig(column+'.png')
    
    
    df = pd.read_csv(pathF)
    return df


def run_analysis(fileLoc):
    print("Choose Number Corresponding to Algorithm"+'\n'
           +"to Analyze Data:"+'\n'
           +"[1. RQA] [2. DFA] [3. AMI_Stergio] [4. FNN] [5. LyE_W]"+'\n'
           +"[6. LyE_R] [7. Ent_Sample] [8. Ent_Ap] [9. Ent_MS_Plus] [10. Ent_Permu]"+'\n'
           +"[11. Ent_Symbolic] [12. Ent_xSamp]")

    num = input("Your Choice: ")

    print("Do you want tau and dim values to be calculated or provide the values yourself? Choose (y/n)")

    autoCalc = input("Your Choice: ")
    while autoCalc != 'y' or autoCalc != 'n':
        print("Invalid Selection. Try Again.")
        autoCalc = input("Your Choice: ")
    
    if autoCalc == 'y':
        autoCalc = 1
    elif autoCalc == 'n':
        autoCalc = 0
    

    print("Add Parameters for your Algorithm")
    param_array = list(map(int, input("Enter Parameter: ").split(',')))

    
    # FileType determines type of file "Parquet" or "CSV"
    train = getFile(fileLoc)
    lines = readFiles(fileLoc)

    # Loop through columns in the file
    for x in lines:
        column = x.strip('\n')
        if (x != ''):
            t1 = train[column]
            if (column == 'LT Contact' or column == 'RT Contact'):
                t2 = train['time']
                t1 = getStrides(t1,t2)
            else:
                # s = time.time()
                runAlgorithm(t1, column, num, autoCalc, param_array)
                # print(time.time()-s)
                # break


    # df = pd.DataFrame(strideDiff)
    # tau = int(runAMI_Stergio_M(df, column))    
    # dim = int(runFNN(df, column, tau))
    
    # train2 = train['Pelvis Accel Sensor X (mG)']
    # print(train2.head(5))
    # train = pd.read_csv('Results/Datas/sine.csv')
    # t1 = train['Wave']
    # tau = int(runAMIStergio(t1, 'Wave'))
    # dim = runFNN(t1, 'Wave', tau)
    # runLYE_W(t1, 'Wave', tau, dim)
    
    # fileLoc = '/home/pki371_04/shifu/s1.csv'
    # train.to_csv(fileLoc, index=False)
    # rp, output = eng.RQA(nargout = 2)
    # print(output)
    # tS = '/home/pki371_04/shifu/s1.csv'
    # 
    # x = rqa.RQA(train, 'RQA', 1, 1, 0, 'euc', None, 'radius', 2.5, 1, 1)
    # y = lye_E.LyE_R(train,200,13,5,[0,0,0,0],1,1)
    # print(x)
    # print(y)
    # output = ami_stergio.AMI_Stergiou(train, 35)
    # tau = output[1][1][0]
    # output = fnn.FNN(train, 28, 10, 15, 2, 0)
    # print(output[0])
    # print(output[1])
    # output = lye_E.LyE_R(train,200,28,5,[0.996539,92914283,0.49280859,0.18828235,0.17224157,0.19505927,0.24233192,0.31718892,0.42754704,0.57112659])
    # print(output)


# def runRQA_Wrong():
#     train = pd.read_csv('/home/pki371_04/shifu/s2.csv')
#     x = rqa.RQA(train, 'RQA', 0.99730564, 5, 0, 'max', 2, 'recurrence', 2.5, 1, 1)
#     print(x)