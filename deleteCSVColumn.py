import csv
import os


def remove_first_column_if_ones(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # 检查第一列是否全部为1
    if all(row[0] == '1' for row in rows):
        # 删除第一列
        modified_rows = [row[1:] for row in rows]

        # 保存修改后的文件
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(modified_rows)


# 指定目录
# directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\prem_13.csv'

# 遍历目录下的所有CSV文件
# for filename in os.listdir(directory):
#     if filename.endswith('.csv'):
#         csv_path = os.path.join(directory, filename)
#         remove_first_column_if_ones(csv_path)
#         print(f'Processed {filename}')
csv_path = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\prem_13.csv'
remove_first_column_if_ones(csv_path)