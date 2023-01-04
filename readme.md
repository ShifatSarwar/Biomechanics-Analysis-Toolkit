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
Following this link will helpd guide installing the MATLAB api for PYTHON: 
<https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html>




