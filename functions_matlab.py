# Need Matlab installed to work
import matlab.engine
from utility_functions import *

# Function calling and testing DFA algorithm
def runDFA(train, column, n_min, n_max, n_length, plotOption):
    # Starts the matlab engine that integrates python and matlab
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    a, r2, out_a, out_l = eng.dfa(column, n_min, n_max, n_length, plotOption, nargout =4)
    writeToFileDFA(a,r2, out_a, out_l, column)
    eng.quit()

def runEntSamp_M(train, m, r, column):
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    r = matlab.double(r)
    output = eng.Ent_Samp(column,m, r)
    writeToFile(output, column, 'SampEnt')
    eng.quit()

def runEntAp_M(train, m, r, column):
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    r = matlab.double(r)
    output = eng.Ent_Ap(column,m, r)
    writeToFile(output, column, 'Ent_Ap')
    eng.quit()

def runEntMSPlus_M(train,tau,m,r,column):
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    r = matlab.double(r)
    output = eng.Ent_MS_Plus(column,tau,m,r)
    # print(output)
    writeToFile(output, column, 'Ent_MS_Plus')
    eng.quit()

def runEntPermu_M(train, dim, tau, column):
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    output = eng.Ent_Permu(dim,tau)
    writeToFile(output, column, 'EntPermu')
    eng.quit()

def runEntSymbolic_M(train, L, column):
    print('Matlab code contains errors. Fix and uncomment part in functions_matlab to run')
    # eng = matlab.engine.start_matlab()
    # eng.addpath('matlab_codes')
    # output = eng.Ent_Symbolic(train, L)
    # writeToFile(output, column, 'Ent_Symbolic')
    # eng.quit()
    
    
def runEntXSamp_M(x,y,m,R,norm,column1, column2):
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(x)
    createMatLabData2(y)
    r = matlab.double(R)
    output = eng.Ent_xSamp(m,r,norm)
    column = column1 + ' and ' + column2
    writeToFile(output, column, 'Ent_xSamp')
    eng.quit()

def runRQA_M(train, tau, dim, column, norm, type_, zScore, setParameter, setValue, plotOption):
    # Starts the matlab engine that integrates python and matlab
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    rp, output = eng.RQA(tau, dim, column, norm, type_, zScore, setParameter, setValue, plotOption,nargout = 2)
    outs = [rp, output]
    writeToFile(outs, column, 'RQA')
    eng.quit()

# Function calling and using AMI_Stergio algorithm
def runAMI_Stergio_M(train, column, n):
    # Starts the matlab engine that integrates python and matlab
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    output = eng.AMI_Stergiou('Results/Data/s1.csv',n)
    writeToFile(output, column, 'AMI_Stergio')
    eng.quit()
    if not output:
        return 0
    else:
        return(output[0][0])

# Function calling and using FNN algorithm
def runFNN_M(train, column, tau, MaxDim, Rtol, Atol, speed):
    # Starts the matlab engine that integrates python and matlab
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    output = eng.FNN('Results/Data/s1.csv',tau,MaxDim,Rtol,Atol,speed, nargout = 2)
    writeToFile(output, column, 'FNN')
    eng.quit()
    return output[0]
    
# Function calling and using LyE_W algorithm
def runLyE_R_M(train, column, tau, dim, sampling_frequency, plotOption):
    # Add Mean Period Slove Values Here
    slope = [0,0,0,0]
    meanPeriod = 1
    # Starts the matlab engine that integrates python and matlab
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    output = eng.LyE_R('Results/Data/s1.csv',sampling_frequency,tau,dim)
    # Need to fix slope and meanPeriod recieving in MatLab
    # output = eng.LyE_R('Results/Data/s1.csv',sampling_frequency,tau,dim,slope, meanPeriod, plotOption)
    writeToFile(output, column, 'LyE_R')
    eng.quit()

# Function calling and using LyE_W algorithm
def runLyE_W_M(train, column, tau, dim, sampFrequency, evolve):
    # Starts the matlab engine that integrates python and matlab
    print('Matlab code contains errors. Fix and uncomment part in functions_matlab to run')
    # eng = matlab.engine.start_matlab()
    # eng.addpath('matlab_codes')
    # createMatLabData(train)
    # output = eng.LyE_W('Results/Data/s1.csv',sampFrequency,tau,dim,evolve)
    # writeToFile(output, column, 'LyE_W')
    # eng.quit()

# Function calling and using AMI_Thomas algorithm
def runAMI_Thomas_M(train, column):
    # Starts the matlab engine that integrates python and matlab
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    output = eng.AMI_Thomas('Results/Data/s1.csv',35)
    writeToFile(output, column, 'AMI_Thomas')
    eng.quit()
    return(output[0][0])

# Function calling and using MyAlgorithm algorithm
# def runMyAlgorithm_M(train,column,tau,dim):
#     # Starts the matlab engine that integrates python and matlab
#     eng = matlab.engine.start_matlab()
#     eng.addpath('matlab_codes')
#     createMatLabData(train)
#     output = eng.MyAlgorithm('Results/Data/s1.csv',200,tau,dim,10)
#     writeToFile(output, column, 'MyAlgorithm')
#     eng.quit()
