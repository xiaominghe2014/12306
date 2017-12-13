#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: request_data.py
@time: 2017/12/13 下午2:35

"""

import re
import requests

# 站点代号查询get地址
url_station = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
# 登录时验证的图像生成get地址
url_verify_img = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
# 登录验证图post验证地址
url_verify_img_check = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
# 登录请求post地址
url_login = 'https://kyfw.12306.cn/passport/web/login'
# 预订时请求验证用户post地址
url_check_usr = 'https://kyfw.12306.cn/otn/login/checkUser'
# 订单验证地址
url_check_order = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
# 订单确认地址
url_post_order = 'https://kyfw.12306.cn/otn//payOrder/init?random=1513152638649'
# 浏览器代理设置
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.84 Safari/537.36'}


def get_tel_code():
    url = url_station
    response = requests.get(url, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    tel_code_map = {}
    map(lambda x: tel_code_map.setdefault(x[0], x[1]), stations)
    return tel_code_map


def query_train_url(tel_code, from_s, to_s, date):
    query_url = 'https://kyfw.12306.cn/otn/leftTicket/query?' \
                'leftTicketDTO.train_date=%s' \
                '&leftTicketDTO.from_station=%s' \
                '&leftTicketDTO.to_station=%s' \
                '&purpose_codes=ADULT'
    return query_url % (date,
                        tel_code.get(from_s.decode('utf-8')),
                        tel_code.get(to_s.decode('utf-8')))


def query_train_price_url(train_no, from_station_no, to_station_no, seat_types, train_date):
    query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?' \
                'train_no=%s' \
                '&from_station_no=%s' \
                '&to_station_no=%s' \
                '&seat_types=%s' \
                '&train_date=%s'
    return query_url % (train_no, from_station_no, to_station_no, seat_types, train_date)
