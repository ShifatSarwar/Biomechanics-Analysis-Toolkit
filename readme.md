### Analysis toolkit

- Download and extract the zip file on specified folder. 
- Open the ToolKit Folder from command line. 
- Find the 'ColumnParquet.txt' or 'ColumnCSV.txt' file and write the list of columns to be analyzed.

- Execute Analysis with command: 

```
python3 main.py "File Location"
```
This starts the execution and user is asked with a question about the Algorithm
```
Choose Number Corresponding to the Algorithm to Analyze Data:
[1. RQA] [2. DFA] [3. AMI_Stergio] [4. FNN] [5. LyE_W]
[6. LyE_R] [7. Ent_Sample] [8. Ent_Ap] [9. Ent_MS_Plus] [10. Ent_Permu]
[11. Ent_Symbolic] [12. Ent_xSamp]

Your Choice: 
```
After user makes choice about algorithm they are asked if they would like to calculate tau and dim if chosen algorithm requires them.

```
Do you want tau and dim values to be calculated? Choose (y/n)

Your Choice: 
```
User gets an additional choice to choose if they want to run the algorithm in Python(1) or MatLab(2). A default choice(0) is also avialble that represesnts the most up to date and properly tested algorithms from Python or MatLab. 
```
Do you want to run on the default choice (0) or specifically on python (1) or matlab (2)? Choose (0 , 1 or 2)

Your Choice: 
```
Finally user gives the parameters.
```
Use default parameters? Choose (y/n)

Your Choice: n

Use -1 if you would like to skip some paramters
-----------------------------------------------
RQA(tau, dim, NORM, TYPE, ZSCORE, SETPARA, SETVALUE, plotOption)
NORM: 
```
The results are generated on the Results folder containing .txt files for each algorithms.
Genered figures can be found inside the Figures folder and the algorithm subfolders with proper names corresponding to the labels.


# Change Default Parameters
Default Parameters are found in driver.py file inside the runAlgorithm method. Each parameter and their description are given as guide. If you would like to change workings inside algorithm take a look inside function.py and functions_Matlab.py files. 

# Running MATLAB and PYTHON
Following this link will helpd guide installing the MATLAB Engine API for PYTHON: 
<https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html>

Step 1: Install MATLAB Application on your device. (Make sure it is activated)

Step 2: Locate the Matlabroot folder and go to MATLAB/extern/engines/python on Terminal.
You will need sudo access to access the folder on MAC or run the next line on Linux Systems Terminal.

Step 3: Run the command below to allow matlab engine working in python. 
```
python setup.py install
```

# Adding new Algorithms
To add new or custom algorithms to enhance the capabilities of this toolkit follow this methods:

Step 1: Add the algorithm in either python_codes or matlab_codes.

## For Python Codes
Step 2: Check parameters and add call mechanism on functions_python.py

Step 3: Add your call method like this:
```
def runMyAlgorithm(data, parameters, column):
    output = python_codes.myAlgorithm.Main_Function(data, parameters)
    writeToFile(output, column, 'MyAlgorithm')
```

Step 4: Add write mechanism in utility_functions.py like this by updating the block below, it is also available inside the writeToFile function:
```
# Add your write option here
    elif (name == 'MyAlgorithm'):
        s = 'Output Identifier: ' + str(output)
        f.write(s)
```

Step 5: Add function call in driver.py along with user choosing mechanism.

- Step 5.1: Add name of Technique to run_analysi method 
```
[13. MyAlgorithm]
```
- Step 5.2: Add the commands for choosing option 13 and its parameters by updating the following code block.
```
# Add your algorithm call here
    elif num == 13:
        print('MyAlgorithm(parameters)')
        param_array.append(TYPE(input("p, parameter 1: ")))
        param_array.append(int(input("m, Vector length: ")))
```
- Step 5.3: Fix any issues with autoCalc, agloChoice if they need their tau and dim values automatically generated or have booth python and matlab codes available for choice.

Step 6: Provide default paramters or just make the call from runAlgorith method inside driver.py by updating the following block of code.
```
# My Algorithm
    elif algorithm == 13: #Code to run MyAlgorithm
        if not autoCalc:
            if tau == -1:
                tau = 0 # Time Delay
            if dim == -1:
                dim = 2 # Embedding Dimension
        
        if runPref == 2:
            runMyAlgorithm_M(t1, dim, tau, column)
        runMyAlgorithm(t1, dim, tau, column)
```

## For Matlab

Step 2: Add location to data Column generated for MatLab codes. They will be automatically generated. Just need to add their location to .m files and convert them to be suitable for processing by MatLab. Make sure to covert data into matlab specific types from given prameters by python.
```
dataLoc = 'Results/Datas/s1.csv';
name = convertCharsToStrings(name);
DATA = readtable(dataLoc, 'PreserveVariableNames', true);
DATA = table2array(DATA);
```

Step 3: Add call mechnaism to functions_matlab.py. Use _M after run command to avoid confusion with call name for equivalent python algorithm. The code block is already available just add the name of the algorithm and appropriate parameters.
```
# Function calling and using MyAlgorithm algorithm
def runMyAlgorithm_M(train,column,tau,dim):
    # Starts the matlab engine that integrates python and matlab
    eng = matlab.engine.start_matlab()
    eng.addpath('matlab_codes')
    createMatLabData(train)
    output = eng.MyAlgorithm('Results/Data/s1.csv',200,tau,dim,10)
    writeToFile(output, column, 'MyAlgorithm')
    eng.quit()
```

Step 4 - 6 are same as Python 


