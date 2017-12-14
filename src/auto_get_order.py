#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@des: 自动抢单
@file: auto_get_order.py
@time: 2017/12/14 下午4:31

Usage:
    auto_get_order.py [-f] FROM_STATION [-t] TO_STATION [-d] DATE [-c] TRAIN_CODE [-s] SEAT_TYPE


Arguments:
    FROM_STATION 出发站点(eg. 北京)
    TO_STATION   目的站点(eg. 上海)
    DATE         出发日期(eg. 2017-12-25)
    TRAIN_CODE   列车类型(eg. D,G,T,Z,K,L)
    SEAT_TYPE    座位型号(eg. 0)---[0 商务, 1 一等, 2 二等, 3 高级软卧, 4 软卧, 5 动卧, 6 硬卧, 7 软座, 8 硬座, 9 无座]


Options:
    -h --help       show this
    -f --from       start station
    -t --to         to station
    -d --date       start off date
    -c --code       train code
    -s --seat       seat type


Example:
    auto_get_order.py -f 上海 -t 成都 -d 2017-12-25 -c DGTZK -s 012345678
"""
from docopt import docopt
from request_login import *
from query_trains import *


def get_train_info(arg_from_station, arg_to_station, arg_date):
    return query_trains(arg_from_station, arg_to_station, arg_date)


def filter_train_info(arg_trains_info, arg_code, arg_seat):
    arg_code_list = map(lambda x: arg_code[x], range(len(arg_code)))
    arg_seat_list = map(lambda x: e_seat_idx[int(arg_seat[x])], range(len(arg_seat)))
    print arg_code_list, arg_seat_list
    return arg_trains_info


if __name__ == '__main__':
    args = docopt(__doc__)
    from_station = args['FROM_STATION']
    to_station = args['TO_STATION']
    date = args['DATE']
    code = args['TRAIN_CODE']
    seat = args['SEAT_TYPE']
    train_info = filter_train_info(get_train_info(from_station, to_station, date), code, seat)
    if 0 < len(train_info):
        Login12306().auto_req_order(train_info)