import pandas as pd
import numpy as np


def calculate_rScO2_ratio(file_path):
    # 读取Excel文件
    data = pd.read_excel(file_path)

    # 将第一列的日期时间转换为datetime格式
    data.iloc[:, 0] = pd.to_datetime(data.iloc[:, 0], format='%m/%d/%y %H:%M:%S')

    # 计算相邻时间点之间的时间差（秒）
    data['Time Diff'] = data.iloc[:, 0].diff().dt.total_seconds()

    # 跳过第一个时间差计算结果为NaN的行
    data = data.iloc[1:, :]

    # 将rScO2值转换为数值类型，并将值为0的视为NaN
    data.iloc[:, 1] = pd.to_numeric(data.iloc[:, 1], errors='coerce').replace(0, np.nan)

    # 计算总时间
    total_time = data['Time Diff'].sum()

    # 假设我们关注的条件是rScO2小于某个阈值，这里以70为例
    threshold = 70
    under_condition_time = data.loc[data.iloc[:, 1] < threshold, 'Time Diff'].sum()

    # 计算比例
    ratio = under_condition_time / total_time if total_time > 0 else 0

    return ratio


# 示例用法
file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\nirs\\fileAfterClassify\\prem_13.xlsx'  # 替换为实际文件路径
rScO2_ratio = calculate_rScO2_ratio(file_path)
print(f"Overall ratio of time with rScO2 under threshold: {rScO2_ratio:.2%}")
