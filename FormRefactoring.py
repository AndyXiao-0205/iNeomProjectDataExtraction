import pandas as pd

# 载入Excel文件
file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\test.xlsx'  # 替换为你的文件路径
data = pd.read_excel(file_path, header=None, usecols=[0])  # 读取第一列，没有标题行

# 创建新的DataFrame，第一列包含奇数行数据，第二列包含偶数行数据
new_data = pd.DataFrame()
new_data[0] = data.iloc[::2].values.flatten()  # 奇数行数据
new_data[1] = data.iloc[1::2].values.flatten()  # 偶数行数据

# 保存到新的Excel文件中
new_file_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\test2.xlsx'  # 新文件的名称
new_data.to_excel(new_file_path, index=False, header=False)  # 不包含索引和标题行