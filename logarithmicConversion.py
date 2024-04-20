import numpy as np
import pandas as pd
from scipy import stats
# 假设 df 是包含你数据的 pandas DataFrame，并且 'value' 是你需要转换的列
df = pd.read_excel('D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\test.xlsx', sheet_name='Sheet3')

df['SpO2<90_2'], best_labmda = stats.boxcox(df['SpO2<90'])
df['SpO2<85_2'], best_labmda = stats.boxcox(df['SpO2<85'])
df['HR Data Points < 100_2'], best_labmda = stats.boxcox(df['HR Data Points < 100'])

print(df['SpO2<90_2'], df['SpO2<85_2'], df['HR Data Points < 100_2'])
with pd.ExcelWriter('D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\test.xlsx',mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet3', startrow=0)
