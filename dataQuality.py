import pandas as pd
import os


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

def clean_and_convert_to_numeric(data, column_index, min_value):
    # 将SpO2列中的非数字字符替换并尝试转换为数值，错误转换为NaN
    data.iloc[:, column_index] = pd.to_numeric(data.iloc[:, column_index], errors='coerce')
    # 过滤掉SpO2值小于设定的最小值的记录
    data = data[data.iloc[:, column_index] > min_value]
    return data

def calculate_metrics_and_intervals(data, bed_number):
    # 将SpO2值转换为数值，并移除NaN值
    spo2_column_index = 3
    data = clean_and_convert_to_numeric(data, spo2_column_index, 20)
    valid_data = data.dropna(subset=[spo2_column_index, 'Datetime'])

    results = []
    intervals = []

    # 对每日数据进行分组计算
    for date, group in valid_data.groupby(valid_data['Datetime'].dt.date):
        stats = {
            'Bed Number': bed_number,
            'Date': date,
            'Median': group.iloc[:, spo2_column_index].median(),
            'Mean': group.iloc[:, spo2_column_index].mean(),
            'Max': group.iloc[:, spo2_column_index].max(),
            'Min': group.iloc[:, spo2_column_index].min(),
            'Range': group.iloc[:, spo2_column_index].max() - group.iloc[:, spo2_column_index].min(),
            'Standard Deviation': group.iloc[:, spo2_column_index].std(),
            'Variance': group.iloc[:, spo2_column_index].var()
        }
        results.append(stats)

    # 计算有效数据间的时间间隔
    for i in range(len(results) - 1):
        end_of_day = valid_data[valid_data['Datetime'].dt.date == results[i]['Date']]['Datetime'].max()
        start_of_next_day = valid_data[valid_data['Datetime'].dt.date == results[i + 1]['Date']]['Datetime'].min()
        interval = (start_of_next_day - end_of_day).total_seconds() / 3600  # 转换为小时
        intervals.append(
            {'Bed Number': bed_number, 'Date': results[i]['Date'], 'Interval to Next Day (hours)': interval})

    return results, intervals


def append_to_excel(output_path, df, sheet_name):
    if not os.path.exists(output_path):
        mode = 'w'
    else:
        mode = 'a'
    with pd.ExcelWriter(output_path, mode=mode, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


def process_and_output(file_path, output_path):
    # 从文件路径提取床位号（文件名）
    bed_number = os.path.splitext(os.path.basename(file_path))[0]

    data = pd.read_csv(file_path, header=None, sep=';', on_bad_lines='skip')
    data['Datetime'] = data.apply(lambda row: try_parse_datetime(f"{row[1]} {row[2]}"), axis=1)

    # 计算统计值和时间间隔
    stats, intervals = calculate_metrics_and_intervals(data, bed_number)
    stats_df = pd.DataFrame(stats)
    intervals_df = pd.DataFrame(intervals)

    # 输出统计值和时间间隔到不同的工作表
    append_to_excel(output_path, stats_df, 'Statistics')
    append_to_excel(output_path, intervals_df, 'Intervals')

# 示例用法
file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\prem_99.csv'
output_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\output_99.xlsx'
process_and_output(file_path, output_path)