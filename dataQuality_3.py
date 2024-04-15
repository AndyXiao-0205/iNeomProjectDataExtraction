import pandas as pd
import os
from scipy.stats import iqr


def try_parse_datetime(date_time_str):
    date_formats = [
        '%b. %d. %Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%b.%d.%Y %H:%M:%S',
        '%d-%b-%Y %H:%M:%S'
    ]
    for date_format in date_formats:
        try:
            return pd.to_datetime(date_time_str, format=date_format)
        except ValueError:
            continue
    return pd.NaT


def calculate_statistics(data, spo2_column_index):
    data = pd.to_numeric(data.iloc[:, spo2_column_index], errors='coerce')
    data = data.dropna()
    data = data[data >= 40]
    if data.empty:
        return {}

    statistics = {
        'Max': data.max(),
        'Min': data.min(),
        'Mean': data.mean(),
        'Median': data.median(),
        'IQR': iqr(data),
        'Total Valid Data Points': len(data)
    }
    return statistics


def append_to_excel(output_path, df, sheet_name):
    if not os.path.exists(output_path):
        mode = 'w'
    else:
        mode = 'a'
    with pd.ExcelWriter(output_path, mode=mode, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


def process_and_output(file_path, output_path):
    bed_number = os.path.splitext(os.path.basename(file_path))[0]
    data = pd.read_csv(file_path, header=None, sep=';', on_bad_lines='skip')
    data['Datetime'] = data.apply(lambda row: try_parse_datetime(f"{row[1]} {row[2]}"), axis=1)

    spo2_column_index = 3
    statistics = calculate_statistics(data, spo2_column_index)
    stats_df = pd.DataFrame([statistics])

    append_to_excel(output_path, stats_df, 'Overall Statistics')


# 示例用法
file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\prem_73.csv'
output_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\outcome_73.xlsx'
process_and_output(file_path, output_path)
