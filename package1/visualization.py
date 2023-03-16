import os
import pandas as pd
import datetime as dt
import missingno as msno
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from scipy import stats

# Функция визуализации годовой динамики
def get_dynamics_year(df, year):
    # Группируем продажи по месяцам
    df_month = df.groupby('Month').agg({'Value (in 1000 rub)': 'sum'})
    # Формируем динамику в %
    for i in df_month.index:
        if i > 1:
            df_month.at[i, 'Dynamics'] = \
            round(((df_month['Value (in 1000 rub)'].values[i-1] -\
            df_month['Value (in 1000 rub)'].values[i-2]) /\
            df_month['Value (in 1000 rub)'].values[i-2]) * 100, 2)
    # Строим графики продаж и динамики
    fig, axs = plt.subplots(figsize=(15, 6), ncols=1, nrows=2)
    axs[0].set_title(f"Продажи по месяцам {year} года, млн.руб.")
    axs[0].plot(df_month.index, df_month['Value (in 1000 rub)'], color='green')
    axs[0].grid()
    axs[1].set_title(f"Динамика продаж по месяцам {year} года, %")
    axs[1].stem([x for x in range(1, len(df_month.index)+1)],  df_month['Dynamics'],
                basefmt='g-', linefmt="--", markerfmt="o", bottom=0)
    axs[1].grid();
