import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 读取CSV文件
df = pd.read_csv('D:\\Desktop\\BUPT\\Final Project\\test.csv')


specific_bed = 'UCN14'  # 根据需要修改床位
specific_data_type = 'SpO2'  # 根据需要修改数据类型
filtered_df = df[(df['cama'] == specific_bed) & (df['dato'] == specific_data_type)]

# 确保时间戳列是datetime类型，以便绘图
filtered_df['horaRegistro'] = pd.to_datetime(filtered_df['horaRegistro'])

# 对数据按时间排序
filtered_df.sort_values('horaRegistro', inplace=True)

# 限制输出数据的最大数量
# max_data_points = 500  
# if len(filtered_df) > max_data_points:
#     filtered_df = filtered_df.tail(max_data_points)

# 限定时间范围
# start_date = '2021-02-11 06:00:00'  # 设置开始时间
# end_date = '2021-02-11 09:00:00'    # 设置结束时间
# filtered_df = filtered_df[(filtered_df['horaRegistro'] >= start_date) & (filtered_df['horaRegistro'] <= end_date)]


# 绘制数据变化图
plt.figure(figsize=(10, 6))
plt.plot(filtered_df['horaRegistro'], filtered_df['valor'], marker='o', linestyle='-')
plt.title(f'Changes in {specific_data_type} data overtime for bed {specific_bed} ')
plt.xlabel('time')
plt.ylabel('value')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # 根据数据密集程度调整时间间隔
plt.gcf().autofmt_xdate()  # 自动调整日期倾斜
plt.tight_layout()
plt.show()
