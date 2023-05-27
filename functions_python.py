import python_codes.ami_stergio
import python_codes.ami_thomas
import python_codes.entPermu
import python_codes.fnn
import python_codes.lye_W
import python_codes.lye_R
import python_codes.ent_Ap
import python_codes.ent_Samp
import python_codes.entMSPlus
import python_codes.ent_symbolic
import python_codes.ent_xSamp
import python_codes.rqa
from utility_functions import *

# Function calling and testing AMI_Stergio algorithm
def runAMIStergio(train, column, n):
    output = python_codes.ami_stergio.AMI_Stergiou(train, n)
    writeToFile(output, column, 'AMI_Stergio')
    if(len(output[0] != 0)):
        return(output[0][0][0])
    return 0

def runAMIThomas(train):
    output = python_codes.ami_thomas.AMI_Thomas(train, 35)
    print(output)

# Function calling and testing FNN algorithm
def runFNN(train, column, tau, MaxDim, Rtol, Atol, speed):
    output = python_codes.fnn.FNN(train, tau, MaxDim, Rtol, Atol, speed)
    writeToFile(output, column, 'FNN')
    return output[1]

# Function calling and testing LyE_R algorithm
# Manually change slope and Mean Period values
def runLYE_R(train, column, tau, dim, sample_frequency, plotOption):
    slope = [0,0,0,0]
    meanPeriod = 1
    # Add Mean Period Slove Values Here
    output = python_codes.lye_R.LyE_R(train, column, sample_frequency,tau,dim,slope,meanPeriod,plotOption)
    writeToFile(output, column, 'LyE_R')
    
# Function calling and testing LyE_W algorithm
def runLYE_W(train, column, tau, dim, sampFrequency, evolve):
    output = python_codes.lye_W.LyE_W(train,sampFrequency,tau,dim,evolve)
    writeToFile(output, column, 'LyE_W')

def runEntAp(train, dim, r, column):
    output = python_codes.ent_Ap.Ent_Ap(train,dim,r)
    writeToFile(output, column, 'Ent_Ap')


def runEntMSPlus(train, tau, m, r, column):
    print('Python code contains errors. Fix and uncomment part in functions_python to run')
    # output = python_codes.entMSPlus.Ent_MS_Plus(train,tau,m,r)
    # writeToFile(output, column, 'Ent_MS_Plus')

def runEntPermu(train, dim, tau, column):
    output = python_codes.entPermu.Ent_Permu(train,dim,tau)
    writeToFile(output, column, 'EntPermu')

def runEntSymbolic(train, L, column):
    output = python_codes.ent_symbolic.Ent_Symbolic(train,L)
    writeToFile(output, column, 'Ent_Symbolic')

def runEntSamp(train, m, r, column):
    output = python_codes.ent_Samp.Ent_Samp(train, m, r)
    writeToFile(output, column, 'SampEnt')

def runEntXSamp(x,y,m,R,norm,column1, column2):
    output = python_codes.ent_xSamp.Ent_xSamp(x,y,m,R,norm)
    column = column1 + ' and ' + column2
    writeToFile(output, column, 'Ent_xSamp')

def runRQA(train, tau, dim, column, norm, type_, zScore, setParameter, setValue, plotOption):
    # Change lineLength value here
    lineLength = None
    # print('Matlab code contains errors. Fix and uncomment part in functions_matlab to run')
    rp, output = python_codes.rqa.RQA(train, type_, tau, dim, zScore, norm, lineLength, setParameter, setValue, plotOption, column, 2)
    outs = [rp, output]
    writeToFile(outs, column, 'RQA')
    


