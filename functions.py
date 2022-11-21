import matplotlib.pyplot as plt
# import time
import pandas as pd

def getR(t1):
    std = t1.std()
    r = 0.2*std
    return r

def addLine(name, line):
    with open(name, 'a') as f:
       f.write(line)
       f.write("\n")
    f.close()

 
def getStrides(t1,t2, column):
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

    # df = pd.DataFrame(strideDiff)
    # tau = int(runAMI_Stergio_M(df, column))    
    # dim = int(runFNN(df, column, tau))

# Depending on the file format fethes the  required time series
# from the csv/parquet files respectively. 
# getFile(1) for CSV (To use csv change column names in column.txt based on csv file columns)
# getFile(0) for Parquet 
def getFile(a):
    train = ''
    if a==1:
        train = pd.read_csv('/home/pki371_04/shifu/S001_G01_D01_B01_T01.csv')   
    else:
        train = pd.read_parquet('/home/pki371_04/shifu/S001_G01_D02_B02_T01.parquet')
    train = train.iloc[3:]
    train = train.head(60)
    # train = train.drop(columns=['Activity', 'Marker', 'time'])
    train = train.drop(columns=['Activity', 'Marker'])
    # train = train['Pelvis Accel Sensor X (mG)']
    return train

# Function that reads the column that needs to be analyzed
# Specify required columns in columns.txt file
def readFiles(train):
    with open('columns.txt') as f:
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
        elif (name == 'EntAp'):
            s = 'ApEn: ' + str(output)
            f.write(s)
        elif (name == 'EntPermu'):
            s = 'ApEn: ' + str(output)
            f.write(s)
        elif (name == 'SampEnt'):
            s = 'Output: ' + str(output)
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
