# -*- coding: UTF-8 -*-
# from pymongo import MongoClient
import os
import json

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
mechanical_factory_folder_name = 'MechanicalFactory'
excel_fmt = '<table><img src={} width=275 height=163>'
data_path = '{}{}{}'.format(working_folder, separator, data_folder_name)
avatar_folder = '{}{}{}'.format(data_path, separator, avatar_folder_name)  # source folder
mining_folder = '{}{}{}'.format(data_path, separator, mechanical_factory_folder_name)  # source folder

pig_info_filename = 'pig_info.csv'  # source file
gem_info_filename = 'gem_info.csv'  # output file
pig4gem_filename = 'pig4gem.csv'  # output file
# abs file path
pig_info_file = '{}{}{}'.format(data_path, separator, pig_info_filename)
gem_info_file = '{}{}{}'.format(data_path, separator, gem_info_filename)
pig4gem_file = '{}{}{}'.format(data_path, separator, pig4gem_filename)

fmt = {
    'kinds': '福仔',
    'favorite_gem': u'黑曜石',
    'access': '无',
    'avatar': '{}{}'.format(avatar_folder, '福仔'),
    'favorite_gem_mining_location':  '{}{}'.format(mining_folder, '福仔'),
    'favorite_gem_mining_level': 'primary'
}


def normalize_gem_info():
    file_name_list = os.listdir(mining_folder)
    # mongodb = MongoClient()['mole']['gll']
    gem_info_dict_list = []
    # print(file_name_list)
    with open(gem_info_file, 'w', encoding=coding) as fo:

        for l in file_name_list:
            gem_info_list = l.strip()[:-4].split('-')
            level = gem_info_list[0]
            location = gem_info_list[1]
            gem = gem_info_list[2]
            energy_usage = gem_info_list[3]
            time_usage = gem_info_list[4]
            pics = '{}{}{}'.format(mining_folder, separator, l)

            gem_info = dict()
            gem_info['gem'] = gem
            gem_info['location'] = location
            gem_info['level'] = level
            gem_info['energy_usage'] = energy_usage
            gem_info['time_usage'] = time_usage
            gem_info['pics'] = pics

            gem_info_dict_list.append(gem_info)
            # '''宝石，产地，开采等级，耗费能量，开采时间，图'''
            fo.writelines('{},{},{},{},{},{}{}'.format(gem, location, level, energy_usage, time_usage, pics, line_break))
            # fo.writelines((json.dumps(gem_info, ensure_ascii=False) + line_break).encode(coding).decode(coding))
            # mongodb.insert_one(gll)
            # gem2location2level_list.append(gll)
    return gem_info_dict_list


def get_gem_info(gem_info_list, gem):
    for l in gem_info_list:
        if gem.strip() == l.get('gem').strip():
            return l
    raise Exception('no such gem:{}'.format(gem))


def find_avatar(pig_name):
    name_list = os.listdir(avatar_folder)
    for name in name_list:
        if pig_name in name:
            return '{}{}{}'.format(avatar_folder, separator, name)


def generate_csv():
    # mongodb = MongoClient()['mole']['pigs']
    gem_info_list = normalize_gem_info()
    pig2location_list = []
    try:
        # with open('Data/pig_info.csv', 'r') as fi, open('{}{}pig_file.txt'.format(data_path, separator), 'w') as fo:
        with open(pig_info_file, 'r') as fi, open(pig4gem_file, 'w', encoding=coding) as fo:
            fo.writelines('矿区,特产宝石,开采等级,耗费能量,耗费时间,矿区地图,优势猪种,猪猪档案,其他获取方式,是否有勋章{}'.format(line_break))
            for l in fi:
                pig_info = l.strip().split(',')
                pig_name = pig_info[0]
                gem = pig_info[1]
                access = pig_info[2]
                medal = pig_info[3]

                pig4gem = dict()
                pig4gem['pig'] = pig_name
                pig4gem['gem'] = gem
                pig4gem['access'] = access
                pig4gem['medal'] = medal
                pig4gem['avatar'] = find_avatar(pig_name)
                if gem != str('无'):
                    gem_info = get_gem_info(gem_info_list, gem)
                else:
                    gem = '钻石'
                    gem_info = get_gem_info(gem_info_list, gem)

                pig4gem['location'] = gem_info.get('location')
                pig4gem['level'] = gem_info.get('level')
                pig4gem['energy_usage'] = gem_info.get('energy_usage')
                pig4gem['time_usage'] = gem_info.get('time_usage')
                pig4gem['pics'] = gem_info.get('pics')

                pig2location_list.append(pig4gem)
                # '''矿区,特产宝石,开采等级,耗费能量,耗费时间,矿区地图,优势猪种,猪猪档案,其他获取方式,是否有勋章'''
                fo.writelines('{},{},{},{},{},{},{},{},{},{}{}'.format(pig4gem['location'],
                                                                       gem,
                                                                       pig4gem['level'],
                                                                       pig4gem['energy_usage'],
                                                                       pig4gem['time_usage'],
                                                                       excel_fmt.format(pig4gem['pics']),
                                                                       pig_name,
                                                                       excel_fmt.format(pig4gem['avatar']),
                                                                       access,
                                                                       medal,
                                                                       line_break))
                # fo.writelines((json.dumps(pig4gem, ensure_ascii=False) + line_break).encode(coding).decode(coding))
                # mongodb.insert(pig4gem)
    except IOError:
        raise Exception('没有猪猪和宝石兴趣的映射文件哦。')


def generate_md():  # deprecated
    """
    this function is deprecated, use it carefully.
    :return:
    """
    # mongodb = MongoClient()['mole']['pigs']
    gem_info_list = normalize_gem_info()
    pig2location_list = []
    try:
        # with open('Data/pig_info.csv', 'r') as fi, open('{}{}pig_file.txt'.format(data_path, separator), 'w') as fo:
        with open(pig_info_file, 'r') as fi, open('pig_file.md', 'w', encoding=coding) as fo:
            # fo.writelines("""<style>img{width: 60%;padding-left: 20%;}</style>\r\n""")
            fo.writelines('|猪种|档案图|喜爱宝石|矿区|开采等级|其他获取方式|是否有勋章|{}'.format(line_break))
            fo.writelines('|:----:' * 7 + '|{}'.format(line_break))
            for l in fi:
                pig_info = l.strip().split(',')
                pig_name = pig_info[0]
                gem = pig_info[1]
                access = pig_info[2]
                medal = pig_info[3]

                pig4gem = dict()
                pig4gem['pig'] = pig_name
                pig4gem['gem'] = gem
                pig4gem['access'] = access
                pig4gem['medal'] = medal
                pig4gem['avatar'] = find_avatar(pig_name)
                if gem != str('无'):
                    gem_info = get_gem_info(gem_info_list, gem)
                    pig4gem['location'] = gem_info.get('location')
                    pig4gem['level'] = gem_info.get('level')
                    pig4gem['map'] = gem_info.get('map')
                else:
                    pig4gem['location'] = '无'
                    pig4gem['level'] = '无'
                    pig4gem['map'] = '无'

                pig2location_list.append(pig4gem)
                # """|猪种|档案图|喜爱宝石|矿区|开采等级|其他获取方式|是否有勋章|"""
                fo.writelines('|{}|{}|{}|{}|{}|{}|{}|{}'.format(pig_name,
                                                                '![avatar]({})'.format(pig4gem['avatar']),
                                                                gem,
                                                                '![location]({})'.format(pig4gem['map']),
                                                                pig4gem['level'],
                                                                access,
                                                                medal,
                                                                line_break))

                # fo.writelines((json.dumps(pig4gem, ensure_ascii=False) + line_break).encode(coding).decode(coding))
                # mongodb.insert(pig4gem)
    except IOError:
        raise Exception('没有猪猪和宝石兴趣的映射文件哦。')


if __name__ == '__main__':
    generate_md()
    generate_csv()
    # print(json.dumps(fmt, indent=4))
