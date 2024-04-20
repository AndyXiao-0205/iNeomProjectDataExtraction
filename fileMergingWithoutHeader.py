import pandas as pd
import os
import glob


def merging_without_headers(csv_list, outputfile):
    first_file = True
    for inputfile in csv_list:
        try:
            # 尝试使用UTF-8编码读取
            data = pd.read_csv(inputfile, header=None, encoding='utf-8', on_bad_lines='skip')
        except UnicodeDecodeError:
            try:
                # 如果UTF-8失败，尝试使用ISO-8859-1编码
                data = pd.read_csv(inputfile, header=None, encoding='ISO-8859-1', on_bad_lines='skip')
            except Exception as e:
                print(f'读取文件{inputfile}时遇到错误：{e}')
                continue  # 处理下一个文件

        if first_file:
            data.to_csv(outputfile, mode='w', index=False, header=False)
            first_file = False
        else:
            data.to_csv(outputfile, mode='a', index=False, header=False)

    print(f'完成合并: {outputfile}')

if __name__ == '__main__':
    root_directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\noHeader\\prem_64'  # 修改为你的CSV文件所在的根目录路径

    # 遍历根目录下的每个子目录
    for subdir, dirs, files in os.walk(root_directory):
        folder_name = os.path.basename(subdir)
        # 查找当前子目录下的所有CSV文件
        csv_files = glob.glob(os.path.join(subdir, '*.csv'))
        if csv_files:  # 如果当前子目录下有CSV文件
            # 输出文件的名称与文件夹名称一致，扩展名为.csv，保存在当前子目录下
            output_csv_path = os.path.join(subdir, f'{folder_name}.csv')
            merging_without_headers(csv_files, output_csv_path)
