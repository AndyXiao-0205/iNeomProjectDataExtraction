import os
import shutil

# 设置你的CSV文件所在的目录和目标目录的根路径
source_directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2'
target_root_directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify'

# 遍历source_directory中的所有文件
for filename in os.listdir(source_directory):
    if filename.startswith('prem') and filename.endswith('.csv'):
        # 分析文件名以找到编号
        parts = filename.split('_')
        prem_number = parts[1]

        # 创建目标文件夹路径
        target_directory = os.path.join(target_root_directory, f'prem_{prem_number}')

        # 如果目标文件夹不存在，则创建它
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # 构建源文件和目标文件的完整路径
        source_file = os.path.join(source_directory, filename)
        target_file = os.path.join(target_directory, filename)

        # 移动文件
        shutil.move(source_file, target_file)
        print(f'Moved "{filename}" to "{target_directory}"')

print('All applicable files have been moved.')
