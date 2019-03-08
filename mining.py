# -*- coding: UTF-8 -*-

import os
import pandas as pd
from tabulate import tabulate
# import numpy as np
# import json
# from pymongo import MongoClient

if os.name == 'nt':  # windows platform
    separator = '\\'
    # line_break = '\r\n'
    line_break = '\n'
else:
    separator = '/'  # unix like platform
    line_break = '\n'

coding = 'UTF-8'
#
working_folder = os.getcwd()
# setting working folder to cwd for markdown
# working_folder = '.{}'.format(separator)
data_folder_name = 'Data'
avatar_folder_name = 'Avatar'
mechanical_factory_folder_name = 'Map'
excel_fmt = '<table><img src={} width=275 height=163>'
data_path = '{}{}{}'.format(working_folder, separator, data_folder_name)
avatar_folder = '{}{}{}'.format(data_path, separator, avatar_folder_name)  # source folder
map_folder = '{}{}{}'.format(data_path, separator, mechanical_factory_folder_name)  # source folder

pig_info_filename = 'pig_info.csv'  # source file, gbk
area_info_filename = 'area_info.csv'  # source file, utf-8
pig2area_filename = 'pig2area.csv'  # output file, utf-8
# abs file path
pig_info_file = '{}{}{}'.format(data_path, separator, pig_info_filename)
area_info_file = '{}{}{}'.format(data_path, separator, area_info_filename)
pig2area_file = '{}{}{}'.format(data_path, separator, pig2area_filename)

README = 'README.md'


def normalize_gem_info():
    """
    this function is deprecated
    :return:
    """
    print('this function was used before but now is deprecated!')
    # file_name_list = os.listdir(mining_folder)
    # # mongodb = MongoClient()['mole']['gll']
    # gem_info_dict_list = []
    # # print(file_name_list)
    # with open(gem_info_file, 'w', encoding=coding) as fo:
    #     # '''矿区,特产宝石,开采等级,耗费能量,开采时间'''
    #     fo.writelines('矿区,特产宝石,开采等级,耗费能量,开采时间{}'.format(line_break))
    #     for l in file_name_list:
    #         gem_info_list = l.strip()[:-4].split('-')
    #         level = gem_info_list[0]
    #         location = gem_info_list[1]
    #         gem = gem_info_list[2]
    #         energy_usage = gem_info_list[3]
    #         time_usage = gem_info_list[4]
    #         pics = '{}{}{}'.format(mining_folder, separator, l)
    #
    #         gem_info = dict()
    #         gem_info['gem'] = gem
    #         gem_info['location'] = location
    #         gem_info['level'] = level
    #         gem_info['energy_usage'] = energy_usage
    #         gem_info['time_usage'] = time_usage
    #         gem_info['pics'] = pics
    #
    #         gem_info_dict_list.append(gem_info)
    #         # '''矿区,特产宝石,开采等级,耗费能量,开采时间'''
    #         fo.writelines('{},{},{},{},{}{}'.format(location, gem,  level, energy_usage, time_usage, line_break))
    #         # fo.writelines((json.dumps(gem_info, ensure_ascii=False) + line_break).encode(coding).decode(coding))
    #         # mongodb.insert_one(gll)
    #         # gem2location2level_list.append(gll)
    # return gem_info_dict_list


# def get_gem_info(gem_info_list, gem):
#     for l in gem_info_list:
#         if gem.strip() == l.get('gem').strip():
#             return l
#     raise Exception('no such gem:{}'.format(gem))
#
#
# def find_map(area):
#     pass
#
#
# def find_avatar(pig_name):
#     name_list = os.listdir(avatar_folder)
#     for name in name_list:
#         if pig_name in name:
#             return '{}{}{}'.format(avatar_folder, separator, name)


def merge_areas_and_pigs():
    with open(pig_info_file, 'r') as f_pig, open(area_info_file, 'r', encoding=coding) as f_area:
        pig_csv = pd.read_csv(f_pig)
        area_csv = pd.read_csv(f_area)
        # 青绿猫眼、蓝宝石、钻石无对应的猪种，全部对应特种猪
        merge_key = '宝石'
        # print(pig_header, area_header)
        area_csv = area_csv.sort_values(by='开采时间')
        pig2area = pd.merge(area_csv, pig_csv,  on=merge_key, how='outer')
        # sort rows
        pig2area = pig2area[['矿区', '宝石', '开采等级', '耗费能量', '开采时间', '猪种', '其他获取方式', '是否有勋章']]
        # rename rows
        pig2area.rename(columns={'宝石': '特产宝石', '猪种': '优势猪种'}, inplace=True)
        # markdown
        md = tabulate(pig2area, tablefmt='pipe', headers="keys")
        with open(README, 'w', encoding=coding) as fo:
            fo.writelines('摩尔庄园肥肥馆攻略{}### 机械工坊{}无图表格，有图表格见Data文件夹下的excel{}{}'.
                          format(line_break, line_break, line_break, line_break))
            fo.writelines(md)

        # add pics
        pig2area_dict = pig2area.T.to_dict()  # 先转置矩阵再转换成字典
        maps = os.listdir(map_folder)
        avatars = os.listdir(avatar_folder)
        for index, pig2area_info in pig2area_dict.items():
            # print(index, json.dumps(pig2area_info, indent=4, ensure_ascii=False))
            pig_name = pig2area_info.get('优势猪种')
            map_name = pig2area_info.get('矿区')
            # print(str(pig_name), str(map_name))
            try:
                avatar_path = '{}{}{}'.format(avatar_folder, separator, next(i for i in avatars if str(pig_name) in i))
                map_path = '{}{}{}'.format(map_folder, separator, next(i for i in maps if str(map_name) in i))
                pig2area_dict[index]['猪种档案图'] = excel_fmt.format(avatar_path)
                pig2area_dict[index]['矿区图'] = excel_fmt.format(map_path)
            except (TypeError, StopIteration):
                print((pig_name, map_name))

        # print(json.dumps(pig2area_dict, indent=4, ensure_ascii=False))
        df = pd.DataFrame(pig2area_dict).T
        df = df[['矿区', '特产宝石', '开采等级', '耗费能量', '开采时间', '矿区图', '优势猪种',
                 '猪种档案图', '其他获取方式', '是否有勋章']]

        df.to_csv(pig2area_file)



def convert_core_pandas_to_dict(core_pandas, keys):
    result = dict()
    for key in keys:
        result[key] = core_pandas.__getattribute__(key)
    return result


if __name__ == '__main__':
    merge_areas_and_pigs()
    # normalize_gem_info()
    # generate_md()
    # generate_csv()
    # print(json.dumps(fmt, indent=4))
