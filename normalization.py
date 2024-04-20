import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# 使用pandas的read_excel函数读取Excel文件
# 假设Excel文件名为'data.xlsx'，并且数据位于第一个工作表，列名包括'Variable1'和'Variable2'
df = pd.read_excel('D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\test.xlsx', sheet_name='Sheet2')

# 显示前几行数据以确认数据已正确读取
print(df.head())
# 创建一个新的图形
fig = plt.figure()

# 添加一个3D坐标轴
plt.figure(figsize=(10, 6))
sns.scatterplot(x='SpO2_2', y='HR_2', data=df)

# 添加数据点

# 设置轴标签
plt.xlabel('SpO2')
plt.xlabel('HR')


# 显示图形
plt.show()
