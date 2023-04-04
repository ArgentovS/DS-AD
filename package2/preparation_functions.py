import os
import pandas as pd
import datetime as dt
import missingno as msno
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from scipy import stats
from tqdm import tqdm


### Функция обработки датасета
def get_fraud_df(indexs):
    print(len(indexs[0]), len(indexs[1]))
    chrono_fraud_index = []
    for userid in tqdm(indexs[0]):
        chrono_fraud_index.extend(chekc_stage(indexs[1][indexs[1].user_id == userid]))
    return chrono_fraud_index


### Функция форми
def chekc_stage(df_start):
    
    # Список индексов записей, не прошедших проверку
    index_fraud = []
    
    # Пройдёмся по всем каналам, через которые был трафик пользователя с уникальным id
    for channel in list(df_start.ad_channel.unique()):
        
        # Зададим нормальную матрицу воронки продаж для проверки реальных воронок на адекватность времени эапов
        df_norma = pd.DataFrame({'funnel_stage': ['interest', 'consideration', 'intent', 'purchase'],
                             'timestamp': [999999999, 999999999, 999999999, 999999999]})
        
        # Пройдёмся по всем имеющимся в воронке этапам и зафиксируем их время
        for stage in ['interest', 'consideration', 'intent', 'purchase']:
            if stage in list(df_start[df_start.ad_channel == channel].funnel_stage):
                df_norma['timestamp'].loc[df_norma['funnel_stage'] == stage] =\
                        df_start['timestamp'].loc[(df_start['funnel_stage'] == stage) &\
                                                   (df_start['ad_channel'] == channel)].values[0]
        
        # Проверяем полноту этапов и адекватность времени наступления
        # каждого следующего этапа воронки продаж
        times = list(df_norma['timestamp'])
        if (times[1] - times[0] < 0) or (times[2] - times[1] < 0) or (times[3] - times[2] < 0):
            index_fraud.extend(df_start[df_start.ad_channel == channel].index)
            
    return index_fraud
