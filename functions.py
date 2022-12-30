import pandas as pd
import csv
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


import numpy
import matlab.engine

# Calculates the Entropy_Sample Radius Value for Accepting Matches
def getR(t1):
    std = t1.std()
    r = 0.2*std
    return r

# Depending on the file format fethes the  required time series
# from the csv/parquet files respectively. 
def getFile(a):
    if a.endswith('.csv'):
        # a = '/home/pki371_04/shifu/S002_G01_D01_B01_T01.csv'
        train = pd.read_csv(a, error_bad_lines=False)
        lines = readFiles(1)
    else:
        # a = '/home/pki371_04/shifu/S001_G01_D02_B02_T01.parquet'
        train = pd.read_parquet(a)
        lines = readFiles(0)

    train = train.iloc[3:]
    train = train.drop(columns=['Activity', 'Marker'])
    return train, lines

# Function that reads the column that needs to be analyzed
# Specify required columns in columns.txt file
def readFiles(fileType):
    if fileType == 0:
        with open('columns.txt') as f:
            lines = f.readlines()
        return lines
    else:
        with open('columnCSV.txt') as f:
            lines = f.readlines()
        return lines

# Writes the output to each txt file
def writeToFile(output, column, name):
    f1 = 'Results/'+name+'.txt'
    with open(f1, 'a') as f:
        f.write(column)
        f.write('\n')
        if name == 'AMI_Stergio':
            if not output:
                s = 'tau, first minimum in AMI: 0'
                f.write(s)
                f.write('\n')
            else:
                s = 'tau, first minimum in AMI: '+ str(output[0][0])
                f.write(s)
                f.write('\n')
                if(len(output[0]) > 1):
                    s = 'V_AMI: '+ str(output[0][1])
                    f.write(s)
                    f.write('\n')
        elif (name == 'FNN'):
            s = 'dE: '+ str(output[0])
            f.write(s)
            f.write('\n')
            s = 'dim: '+ str(output[1])
            f.write(s)
        elif (name == 'LyE_W'):
            s = 'out matrix: ' + str(output[0])
            f.write(s)
            f.write('\n')
            s = 'LyE: '+ str(output[1])
            f.write(s)
        elif (name == 'RQA'):
            s = 'rp: ' + str(output[0])
            f.write(s)
            f.write('\n')
            s = 'output: '+ str(output[1])
            f.write(s)
        elif (name == 'Ent_Ap'):
            s = 'ApEn: ' + str(output)
            f.write(s)
        elif (name == 'EntPermu'):
            s = 'permEnt: ' + str(output[0])
            f.write(s)
            f.write('\n')
            s = 'histogram: '+ str(output[1])
            f.write(s)
        elif (name == 'SampEnt'):
            s = 'Output: ' + str(output)
            f.write(s)
        elif (name == 'Ent_MS_Plus'):
            s = 'RCMSE: ' + str(output[0])
            f.write(s)
            f.write('\n')
            s = 'CMSE: '+ str(output[1])
            f.write(s)
            f.write('\n')
            s = 'MSE: ' + str(output[2])
            f.write(s)
            f.write('\n')
            s = 'MSFE: '+ str(output[3])
            f.write(s)
            f.write('\n')
            s = 'GMSE: '+ str(output[4])
            f.write(s)
        elif (name == 'Ent_Symbolic'):
            s = 'Output: ' + str(output)
            f.write(s)
        elif (name == 'Ent_xSamp'):
            s = 'SE: ' + str(output)
            f.write(s)
        f.write('\n')
        f.write('---------------------------------------')
        f.write('\n')


def writeToFileDFA(a,r2, out_a, out_l, column):
    f1 = 'Results/DFA.txt'
    with open(f1, 'a') as f:
        f.write(column)
        f.write('\n')
        s = 'a: '+ str(a)
        f.write(s)
        f.write('\n')
        s = 'r2: '+ str(r2)
        f.write(s)
        f.write('\n')
        s = 'out_a: '+ str(out_a)
        f.write(s)
        f.write('\n')
        s = 'out_l: '+ str(out_l)
        f.write(s)
        f.write('\n')
        f.write('---------------------------------------')
        f.write('\n')


# Function calling and testing AMI_Stergio algorithm
def runAMIStergio(train, column):
    output = python_codes.ami_stergio.AMI_Stergiou(train, 200)
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
def runLYE_R(train, column, tau, dim, sample_frequency):
    # Add Mean Period Slove Values Here
    output = python_codes.lye_R.LyE_R(train,sample_frequency,tau,dim,[0,0,0,0],1,1)
    writeToFile(output, column, 'LyE_R')
    
# Function calling and testing LyE_W algorithm
def runLYE_W(train, column, tau, dim, sampFrequency, evolve):
    output = python_codes.lye_W.LyE_W(train,sampFrequency,tau,dim,evolve)
    writeToFile(output, column, 'LyE_W')

def runEntAp(train, dim, r, column):
    output = python_codes.ent_Ap.Ent_Ap(train,dim,r)
    writeToFile(output, column, 'Ent_Ap')

def runEntMSPlus(train, tau, m, r, column):
    output = python_codes.entMSPlus.Ent_MS_Plus(train,tau,m,r)
    writeToFile(output, column, 'Ent_MS_Plus')

def runEntPermu(train, dim, tau, column):
    output = python_codes.entPermu.Ent_Permu(train,dim,tau)
    writeToFile(output, column, 'EntPermu')

def runEntSymbolic(train, L, column):
    train = train.to_numpy()
    # train = pd.get_dummies(train)
    train = train.tobytes()
    output = python_codes.ent_symbolic.Ent_Symbolic(train,L)
    writeToFile(output, column, 'Ent_Symbolic')

def runEntSamp(train, m, r, column):
    output = python_codes.ent_Samp.Ent_Samp(train, m, r)
    writeToFile(output, column, 'SampEnt')

def runEntXSamp(x,y,m,R,norm,column):
    output = python_codes.ent_xSamp.Ent_xSamp(x,y,m,R,norm)
    writeToFile(output, column, 'Ent_xSamp')

def convertTo1D(train):
    t2 = []
    for x in train:
        t2.append(bin(x))
    return t2

