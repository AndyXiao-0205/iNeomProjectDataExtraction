import pandas as pd
import os
import re

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

def calculate_oxygen_deficiency_ratios(data, file_name):
    conditions = {
        'SpO2<80': (data['SpO2'] < 80),
        '95>SpO2>=90': (data['SpO2'] >= 90) & (data['SpO2'] < 95),
        'SpO2<90': (data['SpO2'] < 90),
        'SpO2>95': (data['SpO2'] >= 95)
    }
    results = {}
    total_valid_records = len(data[data['SpO2'].notnull() & (data['SpO2'] > 40)])

    for key, mask in conditions.items():
        valid_data_points = data.loc[mask].shape[0]
        results[key] = valid_data_points

    results['file'] = file_name
    results['total_valid_points'] = total_valid_records
    return results

def calculate_oxygen_HR_coincide_deficiency_ratios(data, file_name):
    data['HR'] = pd.to_numeric(data['HR'], errors='coerce')
    conditions = {
        'SpO2<80 & HR<100': (data['SpO2'] < 80) & (data['HR'] < 100),
        'SpO2<90 & HR<100': (data['SpO2'] < 90) & (data['HR'] < 100),
        'SpO2<85 & HR<100': (data['SpO2'] < 85) & (data['HR'] < 100)
    }
    results = {}
    total_valid_records = len(data[data['SpO2'].notnull() & (data['SpO2'] > 40) & data['HR'].notnull()])

    for key, mask in conditions.items():
        valid_data_points = data.loc[mask].shape[0]
        results[key] = valid_data_points

    results['file'] = file_name
    results['total_valid_points'] = total_valid_records
    return results


def calculate_heart_rate_incidents(data):
    data['HR'] = pd.to_numeric(data['HR'], errors='coerce')
    data['below_100'] = data['HR'] < 100
    data['shifted'] = data['below_100'].shift(1).fillna(False)

    # 识别心率小于100的连续区段
    data['group'] = (data['below_100'] & (data['below_100'] != data['shifted'])).cumsum()
    # 计算连续区段大小
    group_sizes = data.groupby('group').size()
    # 只考虑连续至少3次记录的区段
    valid_groups = group_sizes[(data.groupby('group')['below_100'].first()) & (group_sizes >= 3)]

    total_incidents = valid_groups.count()  # 总连续事件数
    total_data_below_100 = data['below_100'].sum()  # 小于100的总记录数

    return total_incidents, total_data_below_100

def calculate_and_export_oxygen_deficiency(file_path, output_path):
    file_name = os.path.basename(file_path)
    data = pd.read_csv(file_path, header=None, sep=None, usecols=[1, 2, 3, 4], engine="python")
    data.columns = ['Date', 'Time', 'SpO2', 'HR']
    data['SpO2'] = pd.to_numeric(data['SpO2'], errors='coerce')
    data['Datetime'] = data.apply(lambda row: try_parse_datetime(f"{row['Date']} {row['Time']}"), axis=1)
    data = data.dropna(subset=['SpO2', 'Datetime'])

    daily_results = {}
    daily_heart_rate_results = {}
    for date, group in data.groupby(data['Datetime'].dt.date):
        daily_results[str(date)] = calculate_oxygen_deficiency_ratios(group, file_name)
        daily_heart_rate_results[str(date)] = calculate_heart_rate_incidents(group)

    overall_results = calculate_oxygen_deficiency_ratios(data, file_name)
    overall_results_coincide = calculate_oxygen_HR_coincide_deficiency_ratios(data, file_name)
    overall_heart_rate_results = calculate_heart_rate_incidents(data)

    # 写入Excel
    with pd.ExcelWriter(output_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        # Oxygen deficiency points per day
        daily_df = pd.DataFrame(daily_results).T
        daily_df.insert(0, 'File Name', file_name)
        daily_df['HR Incidents < 100'] = pd.Series(daily_heart_rate_results).apply(lambda x: x[0])
        daily_df['HR Data Points < 100'] = pd.Series(daily_heart_rate_results).apply(lambda x: x[1])
        daily_df.reset_index(inplace=True)
        daily_df.rename(columns={'index': 'Date'}, inplace=True)
        daily_df.to_excel(writer, sheet_name='Daily Ratios', index=False, startrow=writer.sheets['Daily Ratios'].max_row)

        # Overall results
        overall_df = pd.DataFrame([overall_results], index=['Overall'])
        overall_df.insert(0, 'File Name', file_name)
        overall_df['HR Incidents < 100'] = overall_heart_rate_results[0]
        overall_df['HR Data Points < 100'] = overall_heart_rate_results[1]
        overall_df.to_excel(writer, sheet_name='Overall Ratios', index=False, startrow=writer.sheets['Overall Ratios'].max_row)

        overall_df_coincide = pd.DataFrame([overall_results_coincide], index = ['Overall_coincided'])
        overall_df_coincide.to_excel(writer, sheet_name='Coincide', index=False, startrow=writer.sheets['Coincide'].max_row)



def process_folder(folder_path, output_path, start_from = 1):
    pattern = re.compile(r'cleaned_prem_(\d+)\.csv')
    files = sorted(
        (f for f in os.listdir(folder_path) if pattern.match(f)),
        key=lambda x: int(pattern.search(x).group(1))
    )
    for file_name in files:
        file_number = int(pattern.search(file_name).group(1))
        print(f"Processing file number {file_number}")
        if file_number >= start_from:
            file_path = os.path.join(folder_path, file_name)
            calculate_and_export_oxygen_deficiency(file_path, output_path)
    print("All data processed and written to Excel.")

# 示例用法
file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\cleaned_prem_1.csv'
folder_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\FiO2lessThan0.22\\'# 替换为实际文件路径
output_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\Ratio_3.xlsx'
process_folder(folder_path, output_path)