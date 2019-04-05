import pandas as pd
import numpy as np
# import json
from matplotlib import pyplot as plt
from matplotlib import rcParams
from tabulate import tabulate
import math

rcParams['font.sans-serif'] = ['SimHei']
benefit_file_path = 'Data/成长收益.csv'


def load_file():
    filename = benefit_file_path
    # 猪种,初始值,加工收益,材料价格,单价,成长
    # breed, init_value, proportion, price, growth = 0
    pig_info_list = []
    with open(filename, 'r', encoding='utf-8') as fi:
        df = pd.read_csv(fi)
        # df.sort_values(by='寿命')
        # df = df.sort_values(by='培育价格')
        df_dict = df.T.to_dict()
        # print(json.dumps(df_dict, indent=4, ensure_ascii=False))
        for number, pig_info in df_dict.items():
            pig_info_list.append(pig_info)
        # for pig_info in pig_info_list:
        #     print(pig_info)
    return pig_info_list


def calculate(pig_info, breading_days=20, feed_time=2, play_time=3, oxytocin_flag=True, nutrient_flag=True,
              pk_flag=True):
    """
    计算养猪的收益
    :param pig_info: 猪种信息
    :param breading_days: 养育天数，默认为 20，体重、魅力计算时换算成小时
    :param feed_time: 每日喂养（玉米）次数，默认为 2 次
    :param play_time: 每日逗逗猪的次数，默认为 3（上限） 次
    :param oxytocin_flag: 是否催产
    :param nutrient_flag: 是否喂营养液
    :param pk_flag: 美美猪pk
    :return: 猪种与净利润
    """
    net_profit = 0  # 初始净利润
    oxytocin_price = 600  # 催产针价格
    nutrient_price = 200  # 营养液价格
    feed_price = 30  # 上等玉米价格
    life_extend = 10000  # 延寿 10 天

    breed = pig_info.get('猪种')
    init_value = pig_info.get('初始值')
    breed_price = pig_info.get('培育价格')
    proportion = round(pig_info.get('加工收益'), 2)
    material_cost = pig_info.get('材料价格')
    price = pig_info.get('单价')
    growth = pig_info.get('成长')
    life_time = pig_info.get('寿命')

    # 育种费用
    net_profit -= breed_price

    # 使用催产针
    if oxytocin_flag:
        # 提前出生 12 小时
        weight_or_charm = init_value + 12 * growth
        net_profit -= oxytocin_price
    else:
        weight_or_charm = init_value + 24 * growth

    # 喂猪费用
    net_profit -= feed_price * feed_time * breading_days
    # 成长值
    weight_or_charm += breading_days * (growth * 2 * 24 + play_time * 2)

    if nutrient_flag:
        # 每日喂五次营养液
        weight_or_charm += 5 * 3
        net_profit -= 5 * nutrient_price

    if breading_days <= 20:
        # 每日锻炼，最多 20 天
        weight_or_charm += breading_days * 10
    else:
        weight_or_charm += 20 * 10

    if int(growth) == 1:
        # 美美猪
        if pk_flag:
            # 开启PK，每日最多加 50 魅力
            weight_or_charm += 5 * 10 * breading_days
            # 高级美美屋摩尔豆奖励
            net_profit += (1200 + 2000) * 5 / 3
    else:
        # 肥肥猪，需要 2 天成年才可加工
        if breading_days <= 2:
            proportion = 1

    if breading_days > life_time:
        # 延寿
        net_profit -= life_extend * math.ceil(float(breading_days - life_time) / 10)

    # 净利润
    net_profit = proportion * weight_or_charm * price - material_cost
    net_profit = round(net_profit, 2)
    # profit_per_day = round(net_profit / breading_days, 2)
    # return {'breed': breed, 'net_profit': net_profit, 'profit_per_day': profit_per_day}
    return {'breed': breed, 'net_profit': net_profit}


# def cmp(breading_days=20, feed_time=2, play_time=3, oxytocin_flag=True, nutrient_flag=True, pk_flag=True):
#     pig_info_list = load_file()
#     net_profit_list = []
#     for pig_info in pig_info_list:
#         net_profit_list.append(calculate(pig_info, breading_days=breading_days, feed_time=feed_time,
#                                          play_time=play_time, oxytocin_flag=oxytocin_flag,
#                                          nutrient_flag=nutrient_flag, pk_flag=pk_flag))
#         # print(calculate(pig_info, breading_time=breading_time))
#     # net_profit_list = sorted(net_profit_list, key=lambda i: i['net_profit'], reverse=True)
#     net_profit_list = sorted(net_profit_list, key=lambda i: i['net_profit'], reverse=True)
#     return net_profit_list


def draw_table(net_file='net_profit.csv', perday_file='perday_profit.csv', output_folder='Data',
               max_breading_days=20, feed_time=2, play_time=3,
               oxytocin_flag=True, nutrient_flag=True, pk_flag=True):
    pig_info_list = load_file()
    net_file = '{}/{}_days_{}'.format(output_folder, max_breading_days, net_file)
    perday_file = '{}/{}_days_{}'.format(output_folder, max_breading_days, perday_file)
    with open(net_file, 'w', encoding='utf-8') as fn, open(perday_file, 'w', encoding='utf-8') as fp:
        days = range(1, max_breading_days + 1)
        fn.writelines('猪种\\天数')
        fp.writelines('猪种\\天数')
        for day in days:
            fn.writelines(',{}'.format(day))
            fp.writelines(',{}'.format(day))
        fn.writelines('\n')
        fp.writelines('\n')
        for pig_info in pig_info_list:
            breed = pig_info.get('猪种', 'error')

            fn.writelines('{}'.format(breed))
            fp.writelines('{}'.format(breed))

            net_profit_lst = [breed]
            perday_profit_lst = [breed]
            for day in days:
                result = calculate(pig_info=pig_info, breading_days=day, feed_time=feed_time,
                                   play_time=play_time, oxytocin_flag=oxytocin_flag,
                                   nutrient_flag=nutrient_flag, pk_flag=pk_flag)
                net_profit = result.get('net_profit')
                perday_profit = round(net_profit/day, 2)
                net_profit_lst.append(net_profit)
                perday_profit_lst.append(perday_profit)

                fn.writelines(',{}'.format(net_profit))
                fp.writelines(',{}'.format(perday_profit))
            fn.writelines('\n')
            fp.writelines('\n')
    print('*-*' * 30)


def np_csv(np_array, filename='profit.csv', output_folder='Data'):
    net_file = '{}/{}'.format(output_folder, filename)
    np.savetxt(net_file, np_array, delimiter=',', fmt='%s', encoding='utf-8')


def sort_and_get(np_array, sorted_column, first_n=10, reverse=True):
    if reverse:
        np_array = np_array[np_array[:, sorted_column].argsort()[::-1][:first_n]]
    else:
        np_array = np_array[np_array[:, sorted_column].argsort()[:first_n]]
    return np_array


def gen_profits(max_breading_days=20, feed_time=2, play_time=3, oxytocin_flag=True,
                nutrient_flag=True, pk_flag=True, t_flag=False):

    pig_info_list = load_file()

    days = range(1, max_breading_days + 1)
    fn_array = []
    fp_array = []
    for pig_info in pig_info_list:
        breed = pig_info.get('猪种', 'error')
        net_profit_lst = [breed]
        perday_profit_lst = [breed]

        for day in days:
            result = calculate(pig_info=pig_info, breading_days=day, feed_time=feed_time,
                               play_time=play_time, oxytocin_flag=oxytocin_flag,
                               nutrient_flag=nutrient_flag, pk_flag=pk_flag)
            net_profit = result.get('net_profit')
            perday_profit = net_profit/day
            net_profit_lst.append(int(net_profit))
            perday_profit_lst.append(int(perday_profit))
        # print(type(net_profit_lst[0]), type(net_profit_lst[1]))
        fn_array.append(net_profit_lst)
        fp_array.append(perday_profit_lst)

    if t_flag:
        # 转置
        fn_array = np.array(fn_array, dtype=object).T
        fp_array = np.array(fp_array, dtype=object).T
    else:
        # 不转置
        fn_array = np.array(fn_array, dtype=object)
        fp_array = np.array(fp_array, dtype=object)

    # print(fn_array)
    # md = tabulate(fn_array, tablefmt='pipe', headers="keys")
    # print(md)
    # print(type(fn_array), type(fn_array[0]), type(fn_array[0][0]), type(fn_array[0][1]))
    print('*-*' * 30)
    return fn_array, fp_array


def show(net_profit_list, num=10):
    for _ in net_profit_list:
        print(_)
    print('-*-' * 30)
    plt.title("收益排行榜前{}".format(num))
    plt.xlabel("猪种")
    plt.ylabel("净利润")
    bread = [i['breed'] for i in net_profit_list[:num]]
    net_profit = [i['net_profit'] for i in net_profit_list[:num]]
    plt.plot(bread, net_profit, 'ro')
    # plt.axis(0, 10, 0, 1000000)
    plt.show()


def cmp():
    breading_days = 60
    sorted_column = 20
    first_n = 10
    fn, fp = gen_profits(max_breading_days=breading_days)
    fn = sort_and_get(fn, sorted_column=sorted_column, first_n=first_n)
    fp = sort_and_get(fp, sorted_column=sorted_column, first_n=first_n)
    # fn = sort_and_get(fn, 20, reverse=False)
    with open('README.md', 'w', encoding='utf-8') as fo:
        fo.writelines('#肥肥馆收益计算\n\n### 肝向\n\n5次pk+营养液+逗猪\n\n根据第{}天总收益排行前{}的猪种\n\n前{}天每天的总收益:\n\n'.
                      format(sorted_column, first_n, breading_days))
        md_n = tabulate(fn, tablefmt='pipe', headers="keys")
        fo.writelines(md_n)
        fo.writelines('\n前{}天平均到每天的收益:\n\n'.format(breading_days))
        md_p = tabulate(fp, tablefmt='pipe', headers='keys')
        fo.writelines(md_p)


if __name__ == '__main__':
    # draw_table()
    # draw_table(max_breading_days=10)
    cmp()
    print('-*-' * 30)
