import pandas as pd
import re
import matplotlib.pyplot as plt

# Calculates the Entropy_Sample Radius Value for Accepting Matches
def getR(t1):
    std = t1.std()
    r = 0.2*std
    return r

# Depending on the file format fethes the  required time series
# from the csv/parquet files respectively. 
def getFile(a, numFiles):
    if a.endswith('.csv'):
        train = pd.read_csv(a, error_bad_lines=False)
        lines = readFiles(1)
    else:
        train = pd.read_parquet(a)
        lines = readFiles(0)
    
    if numFiles == 2 and a.endswith('.csv'):
        line1 = readFiles(2)
        line2 = readFiles(3)
        lines = [line1,line2]
    elif numFiles == 2:
        line1 = readFiles(4)
        line2 = readFiles(5)
        lines = [line1,line2]

    train = train.iloc[3:]
    train = train.drop(columns=['Activity', 'Marker'])
    return train, lines

# Function that reads the column that needs to be analyzed
# Specify required columns in columns.txt file
def readFiles(fileType):
    if fileType == 0:
        with open('ColumnNames/columns.txt') as f:
            lines = f.readlines()
    elif fileType == 1:
        with open('ColumnNames/columnCSV.txt') as f:
            lines = f.readlines()
    elif fileType == 2:
        with open('ColumnNames/columnCSVxSamp1.txt') as f:
            lines = f.readlines()
    elif fileType == 3:
        with open('ColumnNames/columnCSVxSamp2.txt') as f:
            lines = f.readlines()
    elif fileType == 4:
        with open('ColumnNames/columnxSamp1.txt') as f:
            lines = f.readlines()
    elif fileType == 5:
        with open('ColumnNames/columnxSamp2.txt') as f:
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
            if isinstance(output, list) and len(output) > 0:
                s = 'permEnt: ' + str(output[0])
                f.write(s)
                f.write('\n')
                s = 'histogram: '+ str(output[1])
                f.write(s)
            else:
                s = 'permEnt: ' + str(output)
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
        # Add your write option here
        # elif (name == 'MyAlgorithm'):
            # s = 'Output Identifier: ' + str(output)
            # f.write(s)
        f.write('\n')
        f.write('---------------------------------------')
        f.write('\n')
        
        

# Specifically writes DFA output
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

# Coverts the data column to 1 Dimension for certain nonlinear analysis
def convertTo1D(train):
    m = train.mean()
    t2 = []
    for x in train:
        if x > m:
            t2.append(1)
        else:
            t2.append(0)
    return t2

# Creates a data file that can be easily interpreted by Matlab.
def createMatLabData(train):
#   train = train.head(10)
    train.to_csv('Results/Data/s1.csv', index = False)

def createMatLabData2(train):
#   train = train.head(10)
    train.to_csv('Results/Data/s2.csv', index = False)

# Calculates a tolerance value using a basic formulae
def getTolerance(t1, t2):
    stdT1 = t1.std()
    stdT2 = t2.std()
    # print(stdT1, stdT2)
    r = stdT2/stdT1
    return r

# Adds Output Line 
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
    pathF = 'Results/Data/s2.csv'
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

# Attempst to find AMI values from preexisting AMI values if user chooses auto calculation
# It saves a lot of computation time. 
def find_ami_value(name):
    data_file = 'Results/AMI_Stergio.txt'
    with open(data_file, 'r') as file:
        content = file.read()

    pattern = r'{}[\s\S]*?first minimum in AMI: (\d+\.\d+)'.format(re.escape(name))
    match = re.search(pattern, content)

    if match:
        ami_value = float(match.group(1))
        return ami_value
    else:
        return None

# Attempts to find DIM values from preexisting DIM values if user chooses auto calculation
# It saves a lot of computation time. 
def find_dim_value(name):
    data_file = 'Results/FNN.txt'
    with open(data_file, 'r') as file:
        content = file.read()

    pattern = r'{}[\s\S]*?dim: (\d+)'.format(re.escape(name))
    match = re.search(pattern, content)

    if match:
        dim_value = int(match.group(1))
        return dim_value
    else:
        return None
