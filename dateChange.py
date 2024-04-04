import csv
import os
from datetime import datetime

# 用于将月份缩写转换为数字的字典
month_to_num = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}

def convert_date_format(date_str):
    # 尝试将日期从[月份缩写].[日期].[年份]格式转换为mm/dd/yyyy
    try:
        parts = date_str.split('.')
        if len(parts) == 3 and parts[0] in month_to_num:
            return f"{month_to_num[parts[0]]}/{parts[1]}/{parts[2]}"
    except ValueError:
        pass
    # 如果日期已经是目标格式或者无法识别，直接返回原始字符串
    return date_str

def process_csv(file_path):
    modified_rows = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # 自动检测日期列（这里假设日期列的数据包含'.'，用于简化示例）
            date_col_index = next((i for i, v in enumerate(row) if '.' in v), None)
            if date_col_index is not None:
                row[date_col_index] = convert_date_format(row[date_col_index])
            modified_rows.append(row)

    # 写回CSV文件
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(modified_rows)

# 遍历指定文件夹中的所有CSV文件
for file_name in os.listdir('D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify'):
    if file_name.endswith('.csv'):
        process_csv(os.path.join('D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify', file_name))
