from functions import writeToFileDFA, writeToFile
import python.ami_stergio
import python.ami_thomas
import python.entPermu
import python.fnn
import python.lye_W
import python.lye_E
import python.ent_Ap
import python.ent_Samp


# Function calling and testing AMI_Stergio algorithm
def runAMIStergio(train, column):
    output = python.ami_stergio.AMI_Stergiou(train, 200)
    writeToFile(output, column, 'AMI_Stergio')
    if(len(output[0] != 0)):
        return(output[0][0][0])
    return 0

def runAMIThomas(train):
    output = python.ami_thomas.AMI_Thomas(train, 200)
    print(output)

# Function calling and testing FNN algorithm
def runFNN(train, column, tau):
    output = python.fnn.FNN(train, tau, 10, 15, 2, 0)
    # writeToFile(output, column, 'FNN')
    return output[1]

# Function calling and testing LyE_R algorithm
def runLYE_R(train, column, tau, dim):
    output = python.lye_E.LyE_R(train,200,tau,dim,[0,0,0,0],1,1)
    writeToFile(output, column, 'LyE_R')
    
# Function calling and testing LyE_W algorithm
def runLYE_W(train, column, tau, dim):
    output = python.lye_W.LyE_W(train,200,12,5,10)
    writeToFile(output, column, 'LyE_W')

def runEntAp(train, dim, column):
    output = python.ent_Ap.Ent_Ap(train,dim,0.2)
    writeToFile(output, column, 'EntAp')

def runEntPermu(train, dim, tau, column):
    output = python.entPermu.Ent_Permu(train,dim,tau)
    print(output)
    # writeToFile(output, column, 'EntPermu')

def runEntSamp(train, m, r, column):
    output = python.ent_Samp.Ent_Samp(train, m, r)
    writeToFile(output, column, 'SampEnt')
