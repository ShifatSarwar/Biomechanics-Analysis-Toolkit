from utility_functions import *
from functions_matlab import *
from functions_python import *

# This is the main code block that determines which tecngnique to use and 
# calls them for processing. It takes 5 arguments.
# t1 : time series or data column
# column : name of the columns like ""
# algorithm : Number of the user chosen algorithm from options
# autoCalc : A boolean value that determines if users wants to automatically calculate
#            tau and dim values or use given values.
# runPref : running preference either Python or Matlab
# param_array : An array with all the paramters for running a particular algorithm.
def runAlgorithm(t1, column, algorithm, autoCalc, runPref, param_array):     
    # DFA
    if algorithm == 2:
        # Change parameter values from default
        plotOption = 1
        n_min = 16 # minimum box size 
        n_max = len(t1)/9 # maximum box size
        n_length = 18 # number of points to sample best fit
        # If user given parameters than apply those
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
        # Calls the DFA algorithm 
        runDFA(t1, column,n_min, n_max, n_length, plotOption)

    # AMI_Stergio 
    elif algorithm == 3:
        n = 200
        if len(param_array) == 1:
            if param_array[0] != -1:
                n = param_array[0]
        if runPref == 1:
            tau = int(runAMIStergio(t1, column, n))
        tau = int(runAMI_Stergio_M(t1, column,n))
    
    # FNN
    elif algorithm == 4:
        MaxDim, Rtol, Atol, speed = 10,15,2,0
        if autoCalc:
            # Change n value Here
            tau = find_ami_value(column)
            if tau == None:
                tau = runAMI_Stergio_M(t1, column, 200)
            tau = int(tau)
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

        if runPref == 2:
            dim = int(runFNN_M(t1, column, tau, MaxDim, Rtol, Atol, speed))
        dim = int(runFNN(t1, column, tau, MaxDim, Rtol, Atol, speed)) 
    
    # Ent_Symbolic
    elif algorithm == 11:
        x = t1 # 1D binary array of data column
        x = convertTo1D(t1)
        l = 1 # Word Length
        if len(param_array) == 1:
            if param_array[0] != -1:
                l = param_array[0]
        
        if runPref == 2:
            runEntSymbolic_M(x, int(l), column)
        runEntSymbolic(x,int(l),column)

    
    else:
        if not autoCalc:
            if algorithm != 8 and algorithm != 7:
                tau = int(input("Enter tau Value: "))
            if algorithm != 9:
                dim = int(input("Enter dim Value: "))
        else:
            n = 200 # maximal lag
            # tau = runAMIThomas(t1, column)
            tau = find_ami_value(column)
            if tau == None:
                tau = runAMI_Stergio_M(t1, column, 200)
            tau = int(tau)
            if algorithm != 9:
                MaxDim, Rtol, Atol, speed = 10,15,2,0 
                dim = find_dim_value(column)
                if tau == None:
                    dim = runFNN(t1, column, tau, MaxDim, Rtol, Atol, speed)
                dim = int(dim)
                
            
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
            if runPref == 1:
                runRQA(t1, tau, dim, column, norm, type_, zScore, setParameter, setValue, plotOption)
            runRQA_M(t1, tau, dim, column, norm, type_, zScore, setParameter, setValue, plotOption)
            
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
            
            if runPref == 2:
                runLyE_W_M(t1, column,tau,dim, sampFrequency, evolve)
            runLYE_W(t1, column,tau,dim, sampFrequency, evolve)
            
        # LyE_R
        elif algorithm == 6: #Code to run LyE_R
            sampFrequency = 200
            plotOption = 1
            if len(param_array) >= 1:
                if param_array[0] != -1:
                    sampFrequency = param_array[0]
                if param_array[1] != -1:
                    plotOption = param_array[1]
            if runPref == 2:
                runLyE_R_M(t1, column, tau, dim, sampFrequency, plotOption)
            runLYE_R(t1, column, tau, dim, sampFrequency, plotOption)

        # Ent_Sample
        elif algorithm == 7: #Code to run Ent_Sample
            r = getR(t1)

            if runPref == 1:
                runEntSamp(t1, dim, r, column)
            runEntSamp_M(t1, dim, r, column)
                   
        # Ent_Ap
        elif algorithm == 8: #Code to run Ent_Ap
            tolerance_r = 0.2
            if len(param_array) >= 1:
                if param_array[0] != -1:
                    tolerance_r = param_array[0]
            
            if runPref == 2:
                runEntAp_M(t1, dim, tolerance_r, column)
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
            
            if runPref == 1:
                runEntMSPlus(t1,tau,m,r,column)
            runEntMSPlus_M(t1,tau,m,r,column)  

        # Ent_Permu
        elif algorithm == 10: #Code to run Ent_Permu
            if not autoCalc:
                if tau == -1:
                    tau = 0 # Time Delay
                if dim == -1:
                    dim = 2 # Embedding Dimension
            
            if runPref == 2:
                runEntPermu_M(t1, dim, tau, column)
            runEntPermu(t1, dim, tau, column)
        
        # My Algorithm
        # elif algorithm == 13: #Code to run MyAlgorithm
        #     if not autoCalc:
        #         if tau == -1:
        #             tau = 0 # Time Delay
        #         if dim == -1:
        #             dim = 2 # Embedding Dimension
            
        #     if runPref == 2:
        #         runMyAlgorithm_M(t1, dim, tau, column)
        #     runMyAlgorithm(t1, dim, tau, column)
            

# The main function calls this algorithm to ask the user their choices
# It only takes the location of the file as input when main.py is called
def run_analysis(fileLoc):
    print("Choose Number Corresponding to Algorithm"+'\n'
           +"to Analyze Data:"+'\n'
           +"[1. RQA] [2. DFA] [3. AMI_Stergio] [4. FNN] [5. LyE_W]"+'\n'
           +"[6. LyE_R] [7. Ent_Sample] [8. Ent_Ap] [9. Ent_MS_Plus] [10. Ent_Permu]"+'\n'
           +"[11. Ent_Symbolic] [12. Ent_xSamp]")

    while True:
        num = input("Enter a number between 1 and 12: ")
        if num.isdigit():
            num = int(num)
            if 1 <= num <= 12:
                break
        print("Invalid input. Please enter a number between 1 and 12.")

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
    
    if num != 2:
        print("Do you want to run on the default choice (0) or specifically on python (1) or matlab (2)? Choose (0 , 1 or 2)")
        while True:
            algoChoice = int(input("Your Choice: "))
            if algoChoice in [0, 1, 2]:
                break
            else:
                print("Invalid input. Please enter 0, 1, or 2.")
        
        
    elif num == 2:
        algoChoice = 0
            
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
            print('LyE_R(tau, dim, sampling_frequency, plotOption)')
            print('Manually change slope and mean period values in functions_python.py/functions_matlab.py run_LyE_R method')
            param_array.append(int(input("sample_frequency: ")))
            param_array.append(int(input("plotOption: ")))

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

        # Add your algorithm call here
        # elif num == 13:
            #print('MyAlgorithm(parameters)')
            # param_array.append(TYPE(input("p, parameter 1: ")))
            # param_array.append(int(input("m, Vector length: ")))

    
    if num != 12:

        # FileType determines type of file "Parquet" or "CSV"
        train,lines = getFile(fileLoc, 1)
        # Loop through columns in the file
        for x in lines:
            column = x.strip('\n')
            if (x != ''):
                try:
                    t1 = train[column]  # Attempt to access the column data
                # Perform further operations with the column data
                except KeyError as e:
                    print(f"Fix Column Name. KeyError occurred for column'{column}': {str(e)}")
                    continue  # Proceed to the next key
                t1 = train[column]
                if (column == 'LT Contact' or column == 'RT Contact'):
                    t2 = train['time']
                    t1 = getStrides(t1,t2)
                else:
                    # s = time.time()

                    print('Running algorithm on '+ column)
                    runAlgorithm(t1, column, num, autoCalc, algoChoice, param_array)
                    # print(time.time()-s)

    # Directly calls xSamp because it takes different input columns than the rest
    elif num == 12:
        # FileType determines type of file "Parquet" or "CSV"
        train,lines = getFile(fileLoc, 2)
        lines1 = lines[0]
        lines2 = lines[1]
        for idx, x in enumerate(lines1):
            column1 = x.strip('\n')
            column2 = lines2[idx].strip('\n')
            if (x!='' and lines2[idx]!=''):
                try:
                    t1 = train[column1]  # Attempt to access the column data
                # Perform further operations with the column data
                except KeyError as e:
                    print(f"Fix Column Name. KeyError occurred for column'{column1}': {str(e)}")
                    continue  # Proceed to the next key
                try:
                    t2 = train[column2]  # Attempt to access the column data
                # Perform further operations with the column data
                except KeyError as e:
                    print(f"Fix Column Name. KeyError occurred for column'{column2}': {str(e)}")
                    continue  # Proceed to the next key
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
                
                if algoChoice == 2:
                    runEntXSamp_M(t1, t2, m, r, norm, column1, column2)
                runEntXSamp(t1, t2, m, r, norm, column1, column2)
                


            
            
            
