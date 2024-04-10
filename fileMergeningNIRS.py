import pandas as pd
import os
import glob


def merge_and_deduplicate_xlsx(xlsx_list, outputfile):
    merged_data = pd.DataFrame()
    for inputfile in xlsx_list:
        try:
            # 读取每个Excel文件的第一个工作表
            data = pd.read_excel(inputfile, sheet_name=0)
            merged_data = pd.concat([merged_data, data], ignore_index=True)
        except Exception as e:
            print(f'处理文件{inputfile}时遇到错误：{e}')

    # 对合并后的数据进行去重
    merged_data.drop_duplicates(inplace=True)

    # 将去重后的数据写入到输出Excel文件
    merged_data.to_excel(outputfile, index=False)
    print(f'完成合并和去重: {outputfile}')


if __name__ == '__main__':
    root_directory = 'D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\nirs\\fileAfterClassify'  # 请修改为你的Excel文件所在的根目录路径

    for subdir, dirs, files in os.walk(root_directory):
        folder_name = os.path.basename(subdir)
        xlsx_files = glob.glob(os.path.join(subdir, '*.xlsx'))
        if xlsx_files:
            output_xlsx_path = os.path.join(root_directory, f'{folder_name}.xlsx')
            merge_and_deduplicate_xlsx(xlsx_files, output_xlsx_path)
