#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: 0.0.0
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: query_trains.py
@time: 2017/12/10 下午10:19

"""
import sys
from sys import argv
import time
from time import strftime
import json
from get_trains_data import *
from prettytable import PrettyTable
from urllib import unquote


def get_rains_list_and_place_map(g_from_station, g_to_station, date):
    s = requests.session()
    tel_code = get_tel_code()
    resp = json.loads(s.get(query_train_url(tel_code, g_from_station, g_to_station, date),
                            stream=True, verify=False).text)
    data = resp.get('data', '')
    train_list_r = data.get('result', '{}')
    place_map_r = data.get('map', '{}')
    return train_list_r, place_map_r


def pretty_sort(train_list_pretty, place_map, list_price):
    train_list = train_list_pretty
    trains = PrettyTable(['车次', '起点', '终点', '开始', '结束', '历时',
                          '商务', '一等', '二等', '高级软卧', '软卧', '动卧', '硬卧',
                          '软座', '硬座', '无座'])
    for ldx, raw_train in enumerate(train_list):

        raw_train_list = raw_train.split('|')
        raw_train_list[0] = unquote(raw_train_list[0])
        for idx in range(len(raw_train_list)):
            if not raw_train_list[idx]:
                raw_train_list[idx] = '--'
            elif '无'== raw_train_list[idx]:
                raw_train_list[idx] = '--'
            # print idx, raw_train_list[idx]
        for i in range(4):
            raw_train_list[4 + i] = place_map.get(raw_train_list[4 + i], '')
        trains.add_row([raw_train_list[e_train.name], (raw_train_list[4] and '(始)' or '(过)') + raw_train_list[6],
                        (raw_train_list[5] and '(终)' or '(过)') + raw_train_list[7], raw_train_list[8],
                        raw_train_list[9], raw_train_list[10],
                        raw_train_list[32]+list_price[ldx][0], raw_train_list[31]+list_price[ldx][1],
                        raw_train_list[30]+list_price[ldx][2], raw_train_list[21]+list_price[ldx][3],
                        raw_train_list[23]+list_price[ldx][4], raw_train_list[33]+list_price[ldx][5],
                        raw_train_list[28]+list_price[ldx][6], raw_train_list[24]+list_price[ldx][7],
                        raw_train_list[29]+list_price[ldx][8], raw_train_list[26]+list_price[ldx][9]])
    return trains


def get_trains(train_list):
    data_trains = []
    for ldx, raw_train in enumerate(train_list):
        raw_train_list = raw_train.split('|')
        raw_train_list[0] = unquote(raw_train_list[0])
        for idx in range(len(raw_train_list)):
            if not raw_train_list[idx]:
                raw_train_list[idx] = '--'
            elif '无'== raw_train_list[idx]:
                raw_train_list[idx] = '--'
        for i in e_seat_idx:
            if '--' != raw_train_list[i]:
                data_trains.append(raw_train_list)
                break
    return data_trains


def sort_train_list(raw_train1, raw_train2):
    train_list1 = raw_train1.split('|')
    train_list2 = raw_train2.split('|')

    word_map = {'D': 1, 'G': 2, 'T': 3, 'Z': 4, 'K': 5, 'L': 6}
    k1, k2 = train_list1[3][0], train_list2[3][0]
    v1, v2 = word_map.get(k1, 100), word_map.get(k2, 100)
    return v1-v2


def query_trains(from_station_q, to_station_q, date):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    train_list, place_map = get_rains_list_and_place_map(from_station_q, to_station_q, date)
    train_list.sort(sort_train_list)
    print pretty_sort(train_list, place_map, query_price(train_list, date))
    return get_trains(train_list)


def query_per_price(raw_train_list, date):
    keys = [e_seat.SW, e_seat.ONE, e_seat.TWO, e_seat.GJRW, e_seat.YW,
            e_seat.DW, e_seat.YW, e_seat.RZ, e_seat.YZ, e_seat.WZ]
    if price_ignore:
        return map(lambda x: '', range(10))
    s = requests.session()
    resp = s.get(query_train_price_url(raw_train_list[2], raw_train_list[16], raw_train_list[17],
                                       raw_train_list[35], date), headers=headers, stream=True, verify=False)

    try:
        data = json.loads(resp.text)['data']
        price = []
        for i in range(len(keys)):
            price.append(data.get(keys[i], ''))
        return price
    except Exception as e:
        print e
        # query_per_price(raw_train_list, date)
        return map(lambda x: '', range(10))


def query_price(train_list_price, date):
    price = []
    train_list = train_list_price
    for raw_train in train_list:
        raw_train_list = raw_train.split('|')
        price.append(query_per_price(raw_train_list, date))
    return price


if __name__ == '__main__':
    lens = len(argv)
    from_station = '上海'
    to_station = '杭州'
    train_date = strftime('%Y-%m-%d', time.localtime(time.time()))
    trains_data = query_trains(lens > 1 and argv[1] or from_station,
                               lens > 2 and argv[2] or to_station,
                               lens > 3 and argv[3] or train_date)
    # for item in trains_data:
    #     print item

