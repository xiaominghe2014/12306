#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
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
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get_tel_code():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    response = requests.get(url, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    tel_code_map = {}
    map(lambda x: tel_code_map.setdefault(x[0], x[1]), stations)
    return tel_code_map


def query_train_url(tel_code, from_station, to_station, date):
    query_url = 'https://kyfw.12306.cn/otn/leftTicket/query?' \
                'leftTicketDTO.train_date=%s' \
                '&leftTicketDTO.from_station=%s' \
                '&leftTicketDTO.to_station=%s' \
                '&purpose_codes=ADULT'
    return query_url % (date,
                        tel_code.get(from_station.decode('utf-8')),
                        tel_code.get(to_station.decode('utf-8')))


def get_rains_list_and_place_map(g_from_station, g_to_station, date):
    s = requests.session()
    tel_code = get_tel_code()
    resp = json.loads(s.get(query_train_url(tel_code, g_from_station, g_to_station, date),
                            stream=True, verify=False).text)
    data = resp.get('data', '')
    train_list_r = data.get('result', '{}')
    place_map_r = data.get('map', '{}')
    return train_list_r, place_map_r


'''
@param train_list:
        13.日期
        3.车次
        4.起点站
        5.终点站
        6,7.过站
        8.出发时间
        9.到达时间
        10.历时

        32.商务座
        31.一等座
        30.二等座
        21.高级软卧
        23.软卧
        33.动卧
        28.硬卧
        24.软座
        29.硬座
        26.无座
@param place_map: 站点代号和名称对应等map
@:return: 可购买的数据list,0 车次 1 商务座 2 一等座 3 二等座 4 高级软卧 5 软卧 6 动卧 7 硬卧 8 软座 9 硬座 10 无座
'''


def print_query_result(train_list, place_map):
    q_buy_list = []
    for raw_train in train_list:
        raw_train_list = raw_train.split('|')
        for idx in range(len(raw_train_list)):
            if not raw_train_list[idx]:
                raw_train_list[idx] = '--'
        for i in range(4):
            raw_train_list[4 + i] = place_map.get(raw_train_list[4 + i], '')

        print '日期:{0[13]} 车次:{0[3]} 起点:{0[4]} 终点:{0[5]} 过:{0[6]},{0[7]} ' \
              '始发:{0[8]} 到达:{0[9]} 历时:{0[10]}'.format(raw_train_list)
        print '商务座:{0[32]} 一等座:{0[31]} 二等座:{0[30]} 高级软卧:{0[21]} 软卧:{0[23]} 动卧:{0[33]} 硬卧:{0[28]} ' \
              '软座:{0[24]} 硬座:{0[29]} 无座:{0[26]}'.format(raw_train_list)
        print '-----------------------------------------------' \
              '-----------------------------------------------'
        buy_list_item = [raw_train_list[3]]
        list_idx = [32, 31, 30, 21, 23, 33, 28, 24, 29, 26]
        for i in range(len(list_idx)):
            if raw_train_list[list_idx[i]] == '--':
                raw_train_list[list_idx[i]] = '0'
            buy_list_item.append(raw_train_list[list_idx[i]])
        q_buy_list.append(buy_list_item)
    return q_buy_list


def sort_train_list(raw_train1, raw_train2):
    train_list1 = raw_train1.split('|')
    train_list2 = raw_train2.split('|')
    word_map = {'D': 1, 'G': 2, 'T': 3, 'Z': 4, 'K': 5, 'L': 6}
    k1, k2 = train_list1[3][0], train_list2[3][0]
    v1, v2 = 100, 100
    if k1 in word_map:
        v1 = word_map[k1]
    if k2 in word_map:
        v2 = word_map[k2]
    return v1-v2


def query_trains(from_station_q, to_station_q, date):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    train_list, place_map = get_rains_list_and_place_map(from_station_q, to_station_q, date)
    train_list.sort(sort_train_list)
    return print_query_result(train_list, place_map)


if __name__ == '__main__':
    lens = len(argv)
    from_station = '上海'
    to_station = '杭州'
    train_date = strftime('%Y-%m-%d', time.localtime(time.time()))
    buy_list = query_trains(lens > 1 and argv[1] or from_station, lens > 2 and argv[2] or to_station,
                            lens > 3 and argv[3] or train_date)
