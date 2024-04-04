import pandas as pd

# 替换为您的CSV文件路径
file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\prem_2.csv'

data = pd.read_csv(file_path, header=None, sep=";", on_bad_lines='skip')

# 指定行号和列号，注意Python是从0开始计数的
row_index = 0  # 第3行
column_index = 0  # 第2列

# 输出指定行和列的内容
specific_value = data.iloc[row_index, column_index]
print(specific_value)