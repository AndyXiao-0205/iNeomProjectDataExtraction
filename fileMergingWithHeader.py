import pandas as pd
import os
import glob


def merge_and_deduplicate(csv_list, outputfile):
    # 初始化一个空的DataFrame用于合并数据
    merged_data = pd.DataFrame()
    for inputfile in csv_list:
        # 读取每个CSV文件
        try:
            data = pd.read_csv(inputfile)
            # 将读取的数据追加到merged_data
            merged_data = pd.concat([merged_data, data], ignore_index=True)
        except pd.errors.ParserError as e:
            print(f'解析错误：文件{inputfile}在处理时遇到问题。详细信息：{e}')
        except UnicodeDecodeError as e:
            print(f'编码错误：文件{inputfile}无法使用UTF-8编码读取。详细信息：{e}')

    # 对合并后的数据进行去重
    merged_data.drop_duplicates(inplace=True)

    # 将去重后的数据写入到输出文件
    merged_data.to_csv(outputfile, index=False)
    print(f'完成合并和去重: {outputfile}')


if __name__ == '__main__':
    root_directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\spo2\\fileAfterClassify\\withHeader'  # 请修改为你的CSV文件所在的根目录路径

    for subdir, dirs, files in os.walk(root_directory):
        # 获取当前子目录的名称
        folder_name = os.path.basename(subdir)
        # 查找当前子目录下的所有CSV文件
        csv_files = glob.glob(os.path.join(subdir, '*.csv'))
        if csv_files:  # 如果当前子目录下有CSV文件
            # 输出文件的名称与文件夹名称一致，扩展名为.csv，保存在当前子目录下
            output_csv_path = os.path.join(subdir, f'{folder_name}.csv')
            merge_and_deduplicate(csv_files, output_csv_path)
