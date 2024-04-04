import os
import shutil

# 指定要遍历的目录路径
source_directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\withHeader'
# 指定目标目录路径
target_directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify'
# 指定文件的扩展名
file_extension = '.csv'

for subdir, dirs, files in os.walk(source_directory):
    for dir_name in dirs:
        # 构建期望的文件名和路径
        expected_file_name = dir_name + file_extension
        expected_file_path = os.path.join(subdir, dir_name, expected_file_name)

        # 检查文件是否存在
        if os.path.exists(expected_file_path):
            # 构建目标路径
            target_file_path = os.path.join(target_directory, expected_file_name)

            # 移动文件
            shutil.move(expected_file_path, target_file_path)
            print(f"Moved: {expected_file_path} to {target_file_path}")

# 注意：此脚本会将找到的文件移动到目标目录，替换任何已存在的同名文件。
