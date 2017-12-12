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
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable


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


def pretty_sort(train_list, place_map):
    trains = PrettyTable()
    trains.field_names = ['车次', '起点', '终点', '开始', '结束', '历时',
                          '商务', '一等', '二等', '高级软卧', '软卧', '动卧', '硬卧',
                          '软座', '硬座', '无座']
    for raw_train in train_list:
        raw_train_list = raw_train.split('|')
        for idx in range(len(raw_train_list)):
            if not raw_train_list[idx]:
                raw_train_list[idx] = '--'
        for i in range(4):
            raw_train_list[4 + i] = place_map.get(raw_train_list[4 + i], '')
        if raw_train_list[4]:
            raw_train_list[4] = '(始)' + raw_train_list[4]
        else:
            raw_train_list[4] = '(过)' + raw_train_list[6]
        if raw_train_list[5]:
            raw_train_list[5] = '(终)' + raw_train_list[5]
        else:
            raw_train_list[5] = '(过)' + raw_train_list[7]
        trains.add_row([raw_train_list[3], raw_train_list[4], raw_train_list[5],
                        raw_train_list[8], raw_train_list[9], raw_train_list[10],
                        raw_train_list[32], raw_train_list[31], raw_train_list[30], raw_train_list[21],
                        raw_train_list[23], raw_train_list[33], raw_train_list[28], raw_train_list[24],
                        raw_train_list[29], raw_train_list[26]])
    return trains


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
    return pretty_sort(train_list, place_map)


if __name__ == '__main__':
    lens = len(argv)
    from_station = '上海'
    to_station = '杭州'
    train_date = strftime('%Y-%m-%d', time.localtime(time.time()))
    print query_trains(lens > 1 and argv[1] or from_station,
                       lens > 2 and argv[2] or to_station,
                       lens > 3 and argv[3] or train_date)

