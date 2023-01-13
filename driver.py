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

def runAlgorithm(t1, column, algorithm, autoCalc, param_array):     
    # DFA
    if algorithm == 2:
        # Change parameter values from default
        plotOption = 1
        n_min = 16 # minimum box size 
        n_max = len(t1)/9 # maximum box size
        n_length = 18 # number of points to sample best fit
        if len(param_array) > 1:
            for i, x in enumerate(param_array):
                if x != -1:
                    if i == 0:
                        n_min = x
                    elif i == 1:
                        n_max = x
                    elif i == 2:
                        n_length = x
                    elif i == 3:
                        plotOption = x           

        runDFA(t1, column,n_min, n_max, n_length, plotOption)

    # AMI_Stergio 
    elif algorithm == 3:
        n = 200
        if len(param_array) == 1:
            if param_array[0] != -1:
                n = param_array[0]
        tau = int(runAMI_Stergio_M(t1, column,n))
    
    # FNN
    elif algorithm == 4:
        MaxDim, Rtol, Atol, speed = 10,15,2,0
        if autoCalc:
            # Change n value Here
            tau = int(runAMI_Stergio_M(t1, column, 200))
        else:
            tau = int(input('Enter tau Value: '))
        if len(param_array) > 1:
            for i, x in enumerate(param_array):
                if x != -1:
                    if i == 0:
                        MaxDim = x
                    elif i == 1:
                        Rtol = x
                    elif i == 2:
                        Atol = x
                    elif i == 3:
                        speed = x   

        dim = int(runFNN(t1, column, tau, MaxDim, Rtol, Atol, speed)) 
    
    # Ent_Symbolic
    elif algorithm == 11:
        x = t1 # 1D binary array of data column
        x = convertTo1D(t1)
        l = len(t1) # Word Length
        if len(param_array) == 1:
            if param_array[0] != -1:
                l = param_array[0]

        runEntSymbolic(x,int(l),column)
    
    # Ent_xSamp
    elif algorithm == 12:
        x = t1 # first data series
        y = t1 # second data series
        m = 2 # vector length for matching
        R = getR(t1) # tolerance for finding matches
        norm = 1 
        runEntXSamp(x,y,m,R,norm,column)
    
    else:
        if not autoCalc:
            if algorithm != 8 and algorithm != 7:
                tau = int(input("Enter tau Value: "))
            if algorithm != 9:
                dim = int(input("Enter dim Value: "))
        else:
            n = 200 # maximal lag
            # tau = runAMIThomas(t1, column)
            tau = int(runAMI_Stergio_M(t1, column,200))
            if algorithm != 9:
                MaxDim, Rtol, Atol, speed = 10,15,2,0 
                dim = int(runFNN(t1, column, tau, MaxDim, Rtol, Atol, speed))
            
        # RQA
        if algorithm == 1:   #Code to run RQA     
            norm = 'MAX'
            type_ = 'RQA'
            zScore = 0
            setParameter = 'recurrence'
            setValue = 2.5
            plotOption = 1
            if len(param_array) >= 1:
                for i, x in enumerate(param_array):
                    if x != -1 or x != '-1':
                        if i == 0:
                            norm = x
                        elif i == 1:
                            type_ = x
                        elif i == 2:
                            zScore = x
                        elif i == 3:
                            setParameter = x
                        elif i == 4:
                            setValue = x
                        elif i == 5:
                            plotOption = x        
            
            runRQA(t1, tau, dim, column, norm, type_, zScore, setParameter, setValue, plotOption)
            
        # LyE_W
        elif algorithm == 5: #Code to run LyE_W
            sampFrequency = 200
            evolve = int(0.05*sampFrequency)
            if len(param_array) >= 1:
                if param_array[0] != -1:
                    sampFrequency = param_array[0]
                if param_array[1] != -1:
                    evolve = param_array[1]
                else:
                    evolve = int(0.05*sampFrequency)

            runLYE_W(t1, column,tau,dim, sampFrequency, evolve)
            
        # LyE_R
        elif algorithm == 6: #Code to run LyE_R
            sampFrequency = 200
            if len(param_array) >= 1:
                if param_array[0] != -1:
                    sampFrequency = param_array[0]
    
            runLYE_R(t1, column, tau, dim, sampFrequency)

        # Ent_Sample
        elif algorithm == 7: #Code to run Ent_Sample
            r = getR(t1)
            runEntSamp_M(t1, dim, r, column)
            # runEnt_Samp(t1, dim, column)
                   
        # Ent_Ap
        elif algorithm == 8: #Code to run Ent_Ap
            tolerance_r = 0.2
            if len(param_array) >= 1:
                if param_array[0] != -1:
                    tolerance_r = param_array[0]

            runEntAp(t1, dim, tolerance_r, column)
        
        # Ent_MS_Plus
        elif algorithm == 9: #Code to run Ent_MS_Plus
            m = 2 # Length of vectors to be compared
            r = getR(t1) # Radius for accepting matches
            if len(param_array) >= 1:
                if param_array[0] != -1:
                    m = param_array[0]
                if param_array[1] != -1:
                    r = param_array[1]
            # runEntMSPlus(t1,tau2,m,r,column)
            runEntMSPlus_M(t1,tau,m,r,column)  

        # Ent_Permu
        elif algorithm == 10: #Code to run Ent_Permu
            if not autoCalc:
                if tau == -1:
                    tau = 0 # Time Delay
                if dim == -1:
                    dim = 2 # Embedding Dimension
            
            runEntPermu(t1, dim, tau, column)
            
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

    num = int(input("Your Choice: "))
    if num != 2 and num != 3 and num != 11 and num != 12:
        print("Do you want tau and/or dim values to be calculated? Choose (y/n)")
        autoCalc = input("Your Choice: ")
        while autoCalc != 'y' and autoCalc != 'n':
            print("Invalid Selection. Try Again.")
            autoCalc = input("Your Choice: ")
        
        if autoCalc == 'y':
            autoCalc = True
        elif autoCalc == 'n':
            autoCalc = False
    else:
        autoCalc = False
    
    if num != 10:
        print('Use default parameters? Choose (y/n)')
        dParams = input("Your Choice: ")
        while dParams != 'y' and dParams != 'n':
            print("Invalid Selection. Try Again.")
            dParams = input("Your Choice: ")
    else:
        dParams = 'y'
    
    param_array = []
    if dParams == 'n':
        print('Use -1 if you would like to skip one or more parameters')
        print('--------------------------------------------------------')

        if num == 1:
            print('RQA(tau, dim, NORM, TYPE, ZSCORE, SETPARA, SETVALUE, plotOption)')
            param_array.append(input("NORM: "))
            param_array.append(input("TYPE: "))
            param_array.append(int(input("ZSCORE: ")))
            param_array.append(input("SETPARA: "))
            param_array.append(float(input("SETVALUE: ")))
            param_array.append(int(input("plot_Option (0(False)/1(True)): ")))
        
        elif num == 2:
            print('DFA(n_min, n_max, n_length, plotOption)')
            param_array.append(float(input("n_min, minimum box size: ")))
            param_array.append(float(input("n_max, maximum box size: ")))
            param_array.append(int(input("n_length, numbers of points of sample for best fit: ")))
            param_array.append(int(input("plot_Option, plot log F vs. log n? (0(False)/1(True)): ")))
        
        elif num == 3:
            print('AMI_Stergio(n)')
            param_array.append(int(input("n, maximal lag: ")))

        elif num == 4:
            print('FNN(tau, MaxDim, Rtol, Atol, speed)')
            param_array.append(int(input("MaxDim, Maximum Embedding Dimension: ")))
            param_array.append(int(input("Rtol, threshold for the first criterion: ")))
            param_array.append(int(input("Atol, threshold for the second criterion: ")))
            param_array.append(int(input("speed, pa 0 for the code to calculate to the MaxDim"+'\n'
                                           + "or a 1 for the code to finish once a minimum is found: ")))

        elif num == 5:
            print('LyE_W(tau, dim, sample_frequency, evolve)')
            param_array.append(int(input("sample_frequency: ")))
            param_array.append(int(input("evolve: ")))

        elif num == 6:
            print('LyE_R(tau, dim, sampling_frequency)')
            param_array.append(int(input("sample_frequency: ")))

        elif num == 7:
            print('Ent_Sample(dim, r)') 
            param_array.append(float(input("r, radius for accepting matches: ")))

        elif num == 8:
            print('Ent_Ap(dim, r)') 
            param_array.append(float(input("tolerance_r: ")))

        elif num == 9:
            print('Ent_MS_Plus(m,r)')
            param_array.append(int(input("m, length of vectors to be compared: ")))
            param_array.append(float(input("r, radius for accepting matches: ")))

        elif num == 11:
            print('Ent_Symbolic(L)')
            param_array.append(int(input("L, Word Length: ")))

        elif num == 12:
            print('Ent_xSamp(m,R,norm)')
            param_array.append(int(input("m, Vector length for matching: ")))
            param_array.append(float(input("R, radius for accepting matches: ")))
            param_array.append(int(input("norm, 1 for MAX, 2 for Mean/ZScore: ")))
    
    if num != 11 and num != 12:

        # FileType determines type of file "Parquet" or "CSV"
        train,lines = getFile(fileLoc, 1)

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
                    print('Running algorithm on '+ column)
                    runAlgorithm(t1, column, num, autoCalc, param_array)
                    # print(time.time()-s)
    else:
        if num == 11:
            pass
        elif num == 12:
            # FileType determines type of file "Parquet" or "CSV"
            train,lines = getFile(fileLoc, 2)
            lines1 = lines[0]
            lines2 = lines[1]
            for idx, x in enumerate(lines1):
                column1 = x.strip('\n')
                column2 = lines2[idx].strip('\n')
                if (x!='' and lines2[idx]!=''):
                    t1 = train[column1]
                    t2 = train[column2]
                    print('Running algorithm on '+column1+" and "+column2)
                    m = 2
                    r = getTolerance(t1,t2)
                    norm = 1
                    if len(param_array) > 1:
                        for i, x in enumerate(param_array):
                            if x != -1:
                                if i == 0:
                                    m = x
                                elif i == 1:
                                    r = x
                                elif i == 2:
                                    norm = x
                    
                    runEntXSamp(t1, t2, m, r, norm, column1, column2)
                    


            
            
            
