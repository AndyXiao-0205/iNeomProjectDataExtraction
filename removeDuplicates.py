import pandas as pd
import os
import re

# 指定包含CSV文件的文件夹路径
folder_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify'


# 正则表达式模式，匹配 'prem_[床位号].csv'
pattern = re.compile(r'cleaned_prem_(\d+)\.csv')
start_file = 'cleaned_prem_104.csv'  # 修改为你的起始文件名
start_processing = False
# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if pattern.match(filename):  # 检查文件名是否匹配
        if filename == start_file:
            start_processing = True  # 找到起始文件，开始处理文件
        if start_processing:
            print(f"正在处理文件：{filename}")  # 打印当前处理的文件名
            # 构建完整的文件路径
            file_path = os.path.join(folder_path, filename)
            # 读取CSV文件
            df = pd.read_csv(file_path)
            # 去除重复的数据行
            df = df.drop_duplicates(keep='first')
            # 构建新的文件名
            new_file_path = os.path.join(folder_path, 'cleaned_' + filename)
            # 保存处理后的数据到新的CSV文件
            df.to_csv(new_file_path, index=False)

print("已处理所有符合格式的文件，并保存到了同一文件夹中。")

