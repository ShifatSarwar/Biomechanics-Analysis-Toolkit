import pandas as pd
import csv
import rqa
import lye_E
train = pd.read_csv('/home/pki371_04/shifu/S001_G01_D01_B01_T01.csv')
# train = pd.read_parquet('/home/pki371_04/shifu/S001_G01_D02_B02_T01.parquet')

if __name__ == '__main__':
    # train = train.iloc[3:]
    train = train.drop(columns=['Activity', 'Marker', 'time'])
    train = train['Pelvis Accel Sensor X (mG)']
    # x = rqa.RQA(train.PelvisAccelSensorX_mG_, 'RQA', 1, 1, 0, 'euc', None, 'radius', 2.5, 1, 1)
    # x = rqa.RQA(train, 'RQA', 1, 1, 0, 'euc', None, 'radius', 2.5, 1, 1)
    y = lye_E.LyE_R(train,200,1,1,[0,0,0,0],1,1)
    # print(x)
    print(y)





























