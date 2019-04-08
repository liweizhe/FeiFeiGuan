import pandas as pd
import numpy as np
# import json
from matplotlib import pyplot as plt
from matplotlib import rcParams
from tabulate import tabulate
import math

rcParams['font.sans-serif'] = ['SimHei']
benefit_file_path = 'Data/成长收益.csv'


def load_file(filename=benefit_file_path):
    # 猪种,初始值,加工收益,材料价格,单价,成长,限量,种类
    # breed, init_value, proportion, price, growth, limited, p_type
    pig_info_list = []
    with open(filename, 'r', encoding='utf-8') as fi:
        df = pd.read_csv(fi)
        df_dict = df.T.to_dict()
        # print(json.dumps(df_dict, indent=4, ensure_ascii=False))
        for number, pig_info in df_dict.items():
            pig_info_list.append(pig_info)
        # for pig_info in pig_info_list:
        #     print(pig_info)
    return pig_info_list


def calculate(pig_info, breeding_days=20, feed_time=2, play_time=3, oxytocin_flag=True, nutrient_flag=True,
              pk_flag=True):
    """
    计算养猪的收益
    :param pig_info: 猪种信息
    :param breeding_days: 养育天数，默认为 20，体重、魅力计算时换算成小时
    :param feed_time: 每日喂养（玉米）次数，默认为 2 次
    :param play_time: 每日逗逗猪的次数，默认为 3（上限） 次
    :param oxytocin_flag: 是否催产
    :param nutrient_flag: 是否喂营养液
    :param pk_flag: 美美猪pk
    :return: 猪种与净利润
    """
    cost = 0  # 初始花费
    oxytocin_price = 600  # 催产针价格
    nutrient_price = 200  # 营养液价格
    feed_price = 30  # 上等玉米价格
    life_extend = 10000  # 10000 延寿 10 天

    breed = pig_info.get('猪种')
    p_type = int(pig_info.get('种类'))  # 1代表肥肥猪，0代表美美猪
    init_value = pig_info.get('初始值')
    breed_price = pig_info.get('培育价格')
    proportion = round(pig_info.get('加工收益'), 2)
    material_cost = pig_info.get('材料价格')
    price = pig_info.get('单价')
    growth = pig_info.get('成长')
    life_time = pig_info.get('寿命')

    # 育种费用
    cost += breed_price

    # 使用催产针
    if oxytocin_flag:
        # 提前出生 12 小时
        weight_or_charm = init_value + 12 * growth
        cost += oxytocin_price
    else:
        weight_or_charm = init_value + 24 * growth

    # 喂猪费用
    cost += feed_price * feed_time * breeding_days
    # 双倍成长值 + 逗逗猪
    weight_or_charm += (2 * growth * 24 + play_time * 2) * breeding_days

    if nutrient_flag:
        # 每日喂五次营养液，单次加 3 体重或魅力
        weight_or_charm += 5 * 3 * breeding_days
        cost += 5 * nutrient_price * breeding_days

    if breeding_days <= 20:
        # 每日锻炼，最多 20 天，每天加 10 体重或魅力
        weight_or_charm += 10 * breeding_days
    else:
        weight_or_charm += 10 * 20

    if breeding_days > life_time:
        # 延寿
        cost += life_extend * math.ceil(float(breeding_days - life_time) / 10)

    if p_type == 0:
        # 美美猪
        if pk_flag:
            # 开启PK，每日最多5次，单次获胜加10魅力
            weight_or_charm += 5 * 10 * breeding_days
            # 演出和PK获胜收益
            pk_profit = 5 * (1200 + 2000) * breeding_days / 3
        else:
            pk_profit = 0
        net_profit = weight_or_charm * price - cost + pk_profit
    else:
        # 肥肥猪，需要 2 天成年才可加工
        if breeding_days <= 2:
            proportion = 1
        # 直接售出价格
        sell_profit = weight_or_charm * price - cost
        # 加工价格
        plant_profit = proportion * weight_or_charm * price - material_cost - cost
        if sell_profit > plant_profit:
            net_profit = sell_profit
        else:
            net_profit = plant_profit
    return {'breed': breed, 'net_profit': net_profit}


# def draw_table(net_file='net_profit.csv', per_day_file='per_day_profit.csv', output_folder='Data',
#                max_breeding_days=20, feed_time=2, play_time=3,
#                oxytocin_flag=True, nutrient_flag=True, pk_flag=True):
#     pig_info_list = load_file()
#     net_file = '{}/{}_days_{}'.format(output_folder, max_breeding_days, net_file)
#     per_day_file = '{}/{}_days_{}'.format(output_folder, max_breeding_days, per_day_file)
#     with open(net_file, 'w', encoding='utf-8') as fn, open(per_day_file, 'w', encoding='utf-8') as fp:
#         days = range(1, max_breeding_days + 1)
#         fn.writelines('猪种\\天数')
#         fp.writelines('猪种\\天数')
#         for day in days:
#             fn.writelines(',{}'.format(day))
#             fp.writelines(',{}'.format(day))
#         fn.writelines('\n')
#         fp.writelines('\n')
#         for pig_info in pig_info_list:
#             breed = pig_info.get('猪种', 'error')
#
#             fn.writelines('{}'.format(breed))
#             fp.writelines('{}'.format(breed))
#
#             net_profit_lst = [breed]
#             per_day_profit_lst = [breed]
#             for day in days:
#                 result = calculate(pig_info=pig_info, breeding_days=day, feed_time=feed_time,
#                                    play_time=play_time, oxytocin_flag=oxytocin_flag,
#                                    nutrient_flag=nutrient_flag, pk_flag=pk_flag)
#                 net_profit = result.get('net_profit')
#                 per_day_profit = round(net_profit/day, 2)
#                 net_profit_lst.append(net_profit)
#                 per_day_profit_lst.append(per_day_profit)
#
#                 fn.writelines(',{}'.format(net_profit))
#                 fp.writelines(',{}'.format(per_day_profit))
#             fn.writelines('\n')
#             fp.writelines('\n')
#     print('*-*' * 30)


def np_csv(np_array, filename='profit.csv', output_folder='Data'):
    net_file = '{}/{}'.format(output_folder, filename)
    np.savetxt(net_file, np_array, delimiter=',', fmt='%s', encoding='utf-8')


def sort_and_get(df, sorted_column, first_n=10, reverse=True):
    # print(type(np_array), type(np_array[0]), type(np_array[0][0]), type(np_array[0][1]))
    df = df.drop_duplicates().values
    if first_n >= df.size:
        first_n = df.size
    if reverse:
        df = df[df[:, sorted_column].argsort()[::-1][:first_n]]
    else:
        df = df[df[:, sorted_column].argsort()[:first_n]]
    return df


def gen_profits(max_breeding_days=20, feed_time=2, play_time=3, oxytocin_flag=True,
                nutrient_flag=True, pk_flag=True, remove_limited=True, t_flag=False):

    pig_info_list = load_file()

    days = range(1, max_breeding_days + 1)
    net_profit_df = []
    per_day_profit_df = []

    for pig_info in pig_info_list:
        breed = pig_info.get('猪种', 'error')
        p_type = int(pig_info.get('种类'))  # 1代表肥肥猪，0代表美美猪
        limited = pig_info.get('限量')
        if remove_limited and limited:
            # 去除限量或绝版猪的计算
            # print(breed)
            continue
        if pk_flag and p_type == 0:
            # 逗猪的次数、是否 pk 、是否使用营养液
            status = '{}{}{}'.format(play_time, int(pk_flag), int(nutrient_flag))
        else:
            # 肥肥猪无法参与 pk
            status = '{}{}{}'.format(play_time, 0, int(nutrient_flag))
        net_profit_lst = [breed, status]
        per_day_profit_lst = [breed, status]

        for day in days:
            result = calculate(pig_info=pig_info, breeding_days=day, feed_time=feed_time,
                               play_time=play_time, oxytocin_flag=oxytocin_flag,
                               nutrient_flag=nutrient_flag, pk_flag=pk_flag)
            net_profit = result.get('net_profit')
            per_day_profit = net_profit/day
            net_profit_lst.append(int(net_profit))
            per_day_profit_lst.append(int(per_day_profit))
        # print(type(net_profit_lst[0]), type(net_profit_lst[1]))
        net_profit_df.append(net_profit_lst)
        per_day_profit_df.append(per_day_profit_lst)

    if t_flag:
        # 转置
        net_profit_df = pd.DataFrame(net_profit_df, dtype=object).T
        per_day_profit_df = pd.DataFrame(per_day_profit_df, dtype=object).T
    else:
        # 不转置
        net_profit_df = pd.DataFrame(net_profit_df, dtype=object)
        per_day_profit_df = pd.DataFrame(per_day_profit_df, dtype=object)

    # print(type(net_profit_df), type(net_profit_df[0]),
    # type(net_profit_df[0][0]), type(net_profit_df[0][1]))
    # print('*-*' * 30)
    return net_profit_df, per_day_profit_df


def show(net_profit_list, num=10):
    for _ in net_profit_list:
        print(_)
    print('-*-' * 30)
    plt.title("收益排行榜前{}".format(num))
    plt.xlabel("猪种")
    plt.ylabel("净利润")
    breed = [i['breed'] for i in net_profit_list[:num]]
    net_profit = [i['net_profit'] for i in net_profit_list[:num]]
    plt.plot(breed, net_profit, 'ro')
    # plt.axis(0, 10, 0, 1000000)
    plt.show()


def cmp():
    breeding_days = 60
    sorted_column = 20
    first_n = 40

    # fn = sort_and_get(fn, 20, reverse=False)
    with open('README.md', 'w', encoding='utf-8') as fo:
        headers = ['猪种', '肝度值'] + ['第{}天'.format(i) for i in range(1, breeding_days + 1)]
        n_results = pd.DataFrame()
        p_results = pd.DataFrame()

        # # 逗猪 + 5次pk + 喂营养液
        # n_df, p_df = gen_profits(max_breeding_days=breeding_days)
        # n_results = n_results.append(n_df)
        # p_results = p_results.append(p_df)
        # 逗猪 + 无pk + 喂营养液
        n_df, p_df = gen_profits(max_breeding_days=breeding_days, pk_flag=False)
        n_results = n_results.append(n_df)
        p_results = p_results.append(p_df)
        # 逗猪 + 无pk + 无营养液
        n_df, p_df = gen_profits(max_breeding_days=breeding_days, pk_flag=False, nutrient_flag=False)
        n_results = n_results.append(n_df)
        p_results = p_results.append(p_df)
        # 不逗猪 + 无pk + 无营养液
        n_df, p_df = gen_profits(max_breeding_days=breeding_days, pk_flag=False, nutrient_flag=False, play_time=0)
        n_results = n_results.append(n_df)
        p_results = p_results.append(p_df)

        n_results = sort_and_get(n_results, sorted_column=sorted_column, first_n=first_n)
        p_results = sort_and_get(p_results, sorted_column=sorted_column, first_n=first_n)

        n_results = pd.DataFrame(n_results, columns=headers)
        p_results = pd.DataFrame(p_results, columns=headers)
        md_n = tabulate(n_results, tablefmt='pipe', headers="keys")
        md_p = tabulate(p_results, tablefmt='pipe', headers='keys')
        fo.writelines('\n\n#肥肥馆收益计算\n\n'
                      '统计了 {} 天的数据。\n\n'
                      '##总收益排行前 {}\n\n'
                      '根据第 {} 天收益排行\n\n'
                      '肝度值分别代表：逗猪的次数、是否 pk (肥肥猪均为 0)、是否使用营养液，\n\n'
                      '如：如肝度值311，代表每天逗 3 次，参与高级美美猪PK（且5次全胜），喂营养液（五次）\n\n'.
                      format(breeding_days, first_n, sorted_column))
        fo.writelines(md_n)
        fo.writelines('\n\n###平均到每天的收益\n\n')
        fo.writelines(md_p)
        fo.writelines('\n\n')


if __name__ == '__main__':
    # draw_table()
    # draw_table(max_breeding_days=10)
    cmp()
    print('----finish{}line----'.format('-*-' * 20))
