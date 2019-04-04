import pandas as pd
# import json
from matplotlib import pyplot as plt
from matplotlib import rcParams
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


def calculate(pig_info, breading_time=20, feed_time=2, play_time=3, oxytocin_flag=True, nutrient_flag=True,
              pk_flag=True):
    """
    计算养猪的收益
    :param pig_info: 猪种信息
    :param breading_time: 养育时间，单位是天，默认为 20
    :param feed_time: 每日喂养（玉米）次数，默认为 2 次
    :param play_time: 每日逗逗猪的次数，默认为 3（上限） 次
    :param oxytocin_flag: 是否催产
    :param nutrient_flag: 是否喂营养液
    :param pk_flag: 美美猪pk
    :return: 猪种与净利润（摩尔豆）
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
    # born status
    if oxytocin_flag:
        weight_or_charm = init_value + 12 * 3 * growth
        net_profit -= oxytocin_price
    else:
        weight_or_charm = init_value + 24 * growth

    if nutrient_flag:
        # 每日最多喂五次营养液
        weight_or_charm += breading_time * (growth * 2 * 24 + play_time * 2) + 5 * 3
        net_profit -= 5 * nutrient_price
    else:
        weight_or_charm += breading_time * (growth * 2 * 24 + play_time * 2)

    if breading_time <= 20:
        # 每日锻炼两次，最多 20 次
        weight_or_charm += breading_time * 10
    else:
        weight_or_charm += 20 * 10

    if pk_flag and int(growth) == 1:
        # 美美猪 PK，每日最多加 50 魅力
        weight_or_charm += 5 * 10 * breading_time
        # 高级美美屋摩尔豆奖励
        net_profit += 2000 * 5 / 3

    if breading_time > life_time:
        # 延寿
        net_profit -= life_extend * math.ceil(float(breading_time - life_time)/10)
    # 喂猪费用
    net_profit -= feed_price * feed_time * breading_time
    # 净利润
    net_profit = proportion * weight_or_charm * price - material_cost - breed_price
    net_profit = round(net_profit, 2)
    profit_per_day = round(net_profit/breading_time, 2)
    return {'breed': breed, 'net_profit': net_profit, 'profit_per_day': profit_per_day}


def show(breading_time=20, feed_time=2, play_time=3, oxytocin_flag=True, nutrient_flag=True, pk_flag=True):
    pig_info_list = load_file()
    net_profit_list = []
    for pig_info in pig_info_list:
        net_profit_list.append(calculate(pig_info, breading_time=breading_time, feed_time=feed_time,
                                         play_time=play_time, oxytocin_flag=oxytocin_flag,
                                         nutrient_flag=nutrient_flag, pk_flag=pk_flag))
        # print(calculate(pig_info, breading_time=breading_time))
    # net_profit_list = sorted(net_profit_list, key=lambda i: i['net_profit'], reverse=True)
    net_profit_list = sorted(net_profit_list, key=lambda i: i['net_profit'], reverse=True)[:10]
    for _ in net_profit_list:
        print(_)
    print('-*-' * 30)
    plt.title("培育天数:{}".format(breading_time))
    plt.xlabel("猪种")
    plt.ylabel("净利润")
    bread = [i['breed'] for i in net_profit_list]
    net_profit = [i['net_profit'] for i in net_profit_list]
    plt.plot(bread, net_profit, 'ro')
    # plt.axis(0, 10, 0, 1000000)
    plt.show()


if __name__ == '__main__':
    show()
    show(60)
    # show(pk_flag=False)
    # show(60, pk_flag=False)
