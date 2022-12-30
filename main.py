import sys
from driver import * 

if __name__ == '__main__':

    # Get File
    fileLoc = sys.argv[1]
    # Call and run the driver program
    run_analysis(fileLoc)
    print('Done')




