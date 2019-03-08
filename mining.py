# -*- coding: UTF-8 -*-
# from pymongo import MongoClient
import os
import json
import pandas as pd
# import random
import numpy as np

if os.name == 'nt':  # windows platform
    separator = '\\'
    # line_break = '\r\n'
    line_break = '\n'
else:
    separator = '/'  # unix like platform
    line_break = '\n'

coding = 'UTF-8'
working_folder = os.getcwd()
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


def normalize_gem_info():
    """
    this function is deprecated
    :return:
    """
    print('this function was used before and is deprecated now')
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


def get_gem_info(gem_info_list, gem):
    for l in gem_info_list:
        if gem.strip() == l.get('gem').strip():
            return l
    raise Exception('no such gem:{}'.format(gem))


def find_map(area):
    pass


def find_avatar(pig_name):
    name_list = os.listdir(avatar_folder)
    for name in name_list:
        if pig_name in name:
            return '{}{}{}'.format(avatar_folder, separator, name)


def load_file():
    with open(pig_info_file, 'r') as f_pig, open(area_info_file, 'r', encoding=coding) as f_area:
        pig_csv = pd.read_csv(f_pig)
        area_csv = pd.read_csv(f_area)
        # 青绿猫眼、蓝宝石、钻石无对应的猪种，全部对应特种猪
        # pig_csv.loc[pig_csv['宝石'] == '无', '宝石'] = '钻石'  # 把无宝石爱好的猪全部改钻石
        # for row in pig_csv.itertuples():
        #     if row[2] == '无':
        #         print(row[2])
        merge_key = '宝石'
        # print(pig_header, area_header)
        area_csv = area_csv.sort_values(by='开采时间')
        pig2area = pd.merge(area_csv, pig_csv,  on=merge_key, how='outer')
        # pig2area.append(area_csv.loc[area_csv['宝石']])
        # pig2area = pig2area
        # print(pig2area)
        pig2area_dict = pig2area.T.to_dict()  # 先转置矩阵再转换成字典
        maps = os.listdir(map_folder)
        avatars = os.listdir(avatar_folder)
        for index, pig2area_info in pig2area_dict.items():
            # print(index, json.dumps(pig2area_info, indent=4, ensure_ascii=False))
            pig_name = pig2area_info.get('猪种')
            map_name = pig2area_info.get('矿区')
            # print(str(pig_name), str(map_name))
            try:
                avatar_path = '{}{}{}'.format(avatar_folder, separator, next(i for i in avatars if str(pig_name) in i))
                map_path = '{}{}{}'.format(map_folder, separator, next(i for i in maps if str(map_name) in i))
                pig2area_dict[index]['档案图'] = excel_fmt.format(avatar_path)
                pig2area_dict[index]['矿区图'] = excel_fmt.format(map_path)
            except (TypeError, StopIteration):
                print((pig_name, map_name))

        # print(json.dumps(pig2area_dict, indent=4, ensure_ascii=False))
        df = pd.DataFrame(pig2area_dict).T
        df = df[['矿区', '宝石', '开采等级', '耗费能量', '开采时间', '矿区图', '猪种',
                 '档案图', '其他获取方式', '是否有勋章']]
        df.rename(columns={'宝石': '特产宝石', '猪种': '优势猪种', '档案图': '猪种档案图'}, inplace=True)
        df.to_csv(pig2area_file)
        # pig2area.to_csv(pig2area_file)


def convert_core_pandas_to_dict(core_pandas, keys):
    result = dict()
    for key in keys:
        result[key] = core_pandas.__getattribute__(key)
    return result


def generate_csv():
    # mongodb = MongoClient()['mole']['pigs']
    print('deprecated')
    return
    # gem_info_list = normalize_gem_info()
    # pig2location_list = []
    # try:
    #     # with open('Data/pig_info.csv', 'r') as fi, open('{}{}pig_file.txt'.format(data_path, separator), 'w') as fo:
    #     with open(pig_info_file, 'r') as fi, open(pig2area_file, 'w', encoding=coding) as fo:
    #         fo.writelines('矿区,特产宝石,开采等级,耗费能量,耗费时间,矿区地图,优势猪种,猪猪档案,其他获取方式,是否有勋章{}'.format(line_break))
    #         for l in fi:
    #             pig_info = l.strip().split(',')
    #             pig_name = pig_info[0]
    #             gem = pig_info[1]
    #             access = pig_info[2]
    #             medal = pig_info[3]
    #
    #             pig4gem = dict()
    #             pig4gem['pig'] = pig_name
    #             pig4gem['gem'] = gem
    #             pig4gem['access'] = access
    #             pig4gem['medal'] = medal
    #             pig4gem['avatar'] = find_avatar(pig_name)
    #             if gem != str('无'):
    #                 gem_info = get_gem_info(gem_info_list, gem)
    #             else:
    #                 gem = '钻石'
    #                 gem_info = get_gem_info(gem_info_list, gem)
    #
    #             pig4gem['location'] = gem_info.get('location')
    #             pig4gem['level'] = gem_info.get('level')
    #             pig4gem['energy_usage'] = gem_info.get('energy_usage')
    #             pig4gem['time_usage'] = gem_info.get('time_usage')
    #             pig4gem['pics'] = gem_info.get('pics')
    #
    #             pig2location_list.append(pig4gem)
    #             # '''矿区,特产宝石,开采等级,耗费能量,耗费时间,矿区地图,优势猪种,猪猪档案,其他获取方式,是否有勋章'''
    #             fo.writelines('{},{},{},{},{},{},{},{},{},{}{}'.format(pig4gem['location'],
    #                                                                    gem,
    #                                                                    pig4gem['level'],
    #                                                                    pig4gem['energy_usage'],
    #                                                                    pig4gem['time_usage'],
    #                                                                    excel_fmt.format(pig4gem['pics']),
    #                                                                    pig_name,
    #                                                                    excel_fmt.format(pig4gem['avatar']),
    #                                                                    access,
    #                                                                    medal,
    #                                                                    line_break))
    #             # fo.writelines((json.dumps(pig4gem, ensure_ascii=False) + line_break).encode(coding).decode(coding))
    #             # mongodb.insert(pig4gem)
    # except IOError:
    #     raise Exception('没有猪猪和宝石兴趣的映射文件哦。')


def generate_md():  # deprecated
    """
    this function is deprecated, use it carefully.
    :return:
    """
    print('this function is deprecated')
    # mongodb = MongoClient()['mole']['pigs']
    # gem_info_list = normalize_gem_info()
    # pig2location_list = []
    # try:
    #     # with open('Data/pig_info.csv', 'r') as fi, open('{}{}pig_file.txt'.format(data_path, separator), 'w') as fo:
    #     with open(pig_info_file, 'r') as fi, open('pig_file.md', 'w', encoding=coding) as fo:
    #         # fo.writelines("""<style>img{width: 60%;padding-left: 20%;}</style>\r\n""")
    #         fo.writelines('|猪种|档案图|喜爱宝石|矿区|开采等级|其他获取方式|是否有勋章|{}'.format(line_break))
    #         fo.writelines('|:----:' * 7 + '|{}'.format(line_break))
    #         for l in fi:
    #             pig_info = l.strip().split(',')
    #             pig_name = pig_info[0]
    #             gem = pig_info[1]
    #             access = pig_info[2]
    #             medal = pig_info[3]
    #
    #             pig4gem = dict()
    #             pig4gem['pig'] = pig_name
    #             pig4gem['gem'] = gem
    #             pig4gem['access'] = access
    #             pig4gem['medal'] = medal
    #             pig4gem['avatar'] = find_avatar(pig_name)
    #             if gem != str('无'):
    #                 gem_info = get_gem_info(gem_info_list, gem)
    #                 pig4gem['location'] = gem_info.get('location')
    #                 pig4gem['level'] = gem_info.get('level')
    #                 pig4gem['map'] = gem_info.get('map')
    #             else:
    #                 pig4gem['location'] = '无'
    #                 pig4gem['level'] = '无'
    #                 pig4gem['map'] = '无'
    #
    #             pig2location_list.append(pig4gem)
    #             # """|猪种|档案图|喜爱宝石|矿区|开采等级|其他获取方式|是否有勋章|"""
    #             fo.writelines('|{}|{}|{}|{}|{}|{}|{}|{}'.format(pig_name,
    #                                                             '![avatar]({})'.format(pig4gem['avatar']),
    #                                                             gem,
    #                                                             '![location]({})'.format(pig4gem['map']),
    #                                                             pig4gem['level'],
    #                                                             access,
    #                                                             medal,
    #                                                             line_break))
    #
    #             # fo.writelines((json.dumps(pig4gem, ensure_ascii=False) + line_break).encode(coding).decode(coding))
    #             # mongodb.insert(pig4gem)
    # except IOError:
    #     raise Exception('没有猪猪和宝石兴趣的映射文件哦。')


if __name__ == '__main__':
    load_file()
    # normalize_gem_info()
    # generate_md()
    # generate_csv()
    # print(json.dumps(fmt, indent=4))
