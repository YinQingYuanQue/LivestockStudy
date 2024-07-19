
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = gpd.read_file(r'Origin_Data\799_HMMSup_FZ.shp')
df = pd.DataFrame(df)
df['MT Time'] = pd.to_datetime(df['MT Time'])
df = df.set_index('MT Time')

df = df.between_time('8:00:00','7:00:00')
df = df.reset_index()
aug_df = df[df['MT Time'].dt.month == 8]
sep_df = df[df['MT Time'].dt.month == 9]
oct_df = df[df['MT Time'].dt.month == 10]
combination = []
all_p = range(0,3**12)
for i in all_p:
    Tri = []
    quotient = int(i/3)
    remainder = i % 3
    Tri.append(remainder)
    while quotient != 0:
        remainder = quotient % 3
        Tri.append(remainder)
        quotient = int(quotient/3)
    combination.append(Tri)
combination = np.array(combination)
comb = []
for i in combination:
    j = i[:]
    l = len(j)
    while l != 16:
        j.append(0)
        l = l + 1
    comb.append(j)
comb = np.array(comb)
comb
df = df.reset_index()
aug_day = 31
sep_day = 30
oct_day = 31
def get_cum(df,days,month):
    newdf = pd.DataFrame(index = pd.date_range(df.loc[df.index[0],'MT Time'].date(), df.loc[df.index[-1],'MT Time'].date(),freq='1D'))
    newdf['s'] = None
    C_r = []
    C_p = []
    run = 0
    num_days = range(1,days)
    for x in num_days:
        print('Running day {} of {}'.format(x,days))
        test_me = df[df['MT Time'].dt.day == x]
        if ~test_me.empty:
            print(test_me)
            if test_me.shape[0] > 11:
                n_df = df[df['MT Time'] != pd.to_datetime(month +' ' + str(x) + ' 2021')]
                MCDA = n_df['MCDDA'].to_numpy()
                low = n_df['Low_activi'].to_numpy()
                high = n_df['High_activ'].to_numpy()
                rest = n_df['Resting'].to_numpy()
        for i in comb[0:3**12]:
            n = df.index[0]
            s = 0
            p = 1
            for j in np.arange(0,12):
                if i[j] == 0:
                    s = s + MCDA[n] * 0.4
                    p = p * (low[n]/(low[n] + high[n] + rest[n]))
                elif i[j] == 1:
                    s = s + MCDA[n] * 0.2
                    p = p * (rest[n]/(low[n] + high[n] + rest[n]))
                elif i[j] == 2:
                    s = s + MCDA[n] * 0.4
                    p = p + (high[n]/(high[n] + rest[n] + low[n]))
                n +=1 
            C_r.append(s)
            C_p.append(p)
            print(run/(3**12))
            run += 1
        c = pd.DataFrame(data = {'C_r':C_r, 'C_p':C_p})
        c['s'] = c["C_r"] * c['C_p']
        newdf.loc[pd.to_datetime(month + ' ' + str(x) + ' 2021'),'s'] = c['s'].sum()
        del c 
    return(newdf)
oct = get_cum(oct_df, oct_day, 'October')
aug = get_cum(aug_df, aug_day, 'August')
sep = get_cum(sep_df, sep_day, 'September')

df = pd.concat([oct,aug,sep])
df = gpd.GeoDataFrame(df, geometry = 'geometry')
df.to_file('799CumExp.shp')