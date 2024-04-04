import pandas as pd

def try_parse_datetime(date_time_str):
    date_formats = [
        '%b. %d. %Y %H:%M:%S',  # "Jan. 1. 2020 12:00:00"
        '%m/%d/%Y %H:%M:%S',    # "12/25/2020 12:00:00"
        '%b.%d.%Y %H:%M:%S',  # "Jan. 1. 2020 12:00:00"
    ]
    for date_format in date_formats:
        try:
            return pd.to_datetime(date_time_str, format=date_format)
        except ValueError:
            continue
    return pd.NaT

def calculate_daily_ratio(data):
    # 确保数据按日期时间排序
    data.sort_values('Datetime', inplace=True)

    # 计算相邻时间点之间的时间差（秒）
    data['Time Diff'] = data['Datetime'].diff().dt.total_seconds()

    # 将SpO2值转换为数值
    data.iloc[:, 3] = pd.to_numeric(data.iloc[:, 3], errors='coerce')

    # 计算总时间和SpO2小于95的时间
    total_time = data['Time Diff'].sum()
    under_condition_time = data.loc[data.iloc[:, 3] < 95, 'Time Diff'].sum()

    return under_condition_time, total_time

def calculate_overall_ratio(file_path):
    data = pd.read_csv(file_path, header=None, sep=',', on_bad_lines='skip')
    data['Datetime'] = data.apply(lambda row: try_parse_datetime(f"{row[1]} {row[2]}"), axis=1)
    data = data.dropna(subset=['Datetime'])

    overall_under_condition_time = 0
    overall_total_time = 0

    for date, group in data.groupby(data['Datetime'].dt.date):
        under_condition_time, total_time = calculate_daily_ratio(group)
        overall_under_condition_time += under_condition_time
        overall_total_time += total_time

    # 计算整体比例
    ratio = overall_under_condition_time / overall_total_time if overall_total_time > 0 else 0
    return ratio



# 示例用法
file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\prem_1.csv'  # 替换为实际文件路径
overall_ratio = calculate_overall_ratio(file_path)
print(f"Overall ratio of time with SpO2 under 95: {overall_ratio:.2%}")
