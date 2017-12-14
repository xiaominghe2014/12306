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

# 禁用安全请求警告
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

# 查询忽略价格,便于快速查询
price_ignore = True


def enum(**enums):
    return type('Enum', (), enums)


submit_order_des = 'var ticket_submit_order={' \
                   'ticket_type:{adult:"1",child:"2",student:"3",disability:"4"},' \
                   'ticket_type_name:{"1":"成人票","2":"孩票","3":"学生票","4":"伤残军人票"},' \
                   'tour_flag:{dc:"dc",wc:"wc",fc:"fc",gc:"gc",lc:"lc",lc1:"l1",lc2:"l2"},' \
                   'passenger_type:{adult:"1",child:"2",student:"3",disability:"4"},' \
                   'passenger_card_type:{two:"1",one:"2",tmp:"3",passport:"B",work:"H",hongkong_macau:"C",taiwan:"G"},' \
                   'request_flag:{isAsync:"1"},ticket_query_flag:{query_commom:"00",query_student:"0X00"},' \
                   'seatType:{yz_type:"1"},special_areas:{lso:"LSO",dao:"DAO",ado:"ADO",nqo:"NQO",tho:"THO"}};'

# 站点代号查询get地址
url_station = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
# 登录时验证的图像生成get地址
url_verify_img = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
# 登录验证图post验证地址
url_verify_img_check = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
# 登录请求post地址
# @return Set-Cookie:uamtk
url_login = 'https://kyfw.12306.cn/passport/web/login'
# 登录成功返回newapptk
url_get_newapptk = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
# apptk验证
# post tk
# @return result_code 0 验证通过
url_check_tk = 'https://kyfw.12306.cn/otn/uamauthclient'
# 预订时请求验证用户post地址
# @return data.flag true 已登录，false 需要重新登录
url_check_usr = 'https://kyfw.12306.cn/otn/login/checkUser'
# 订单请求 需要post
# 字段 secretStr, train_date, back_train_date, tour_flag(dc--单程),
# purpose_codes(ADULT or 0x00) query_from_station_name query_to_station_name,undefined
url_get_order = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
# 获取token
# return 需要从页面获取js字段 globalRepeatSubmitToken 正则 ^var globalRepeatSubmitToken = ‘(.*?)’;$
# key_check_isChange 'key_check_isChange:'value'
url_get_token = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
# 乘客信息查询
# @post 字段_json_att，REPEAT_SUBMIT_TOKEN
# @return data.normal_passengers{
# address
# born_date
# code
# country_code
# email
# first_letter
# index_id
# mobile_no
# passenger_flag
# passenger_id_no 身份证
# passenger_id_type_code
# passenger_id_type_name
# passenger_name
# passenger_type
# passenger_type_name
# phone_no
# postalcode
# recordCount
# sex_code
# sex_name
# total_times
# }
url_passengerDTOs = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
# 拉去买票验证码
url_get_buy_img = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew??module=passenger&rand=randp'
# 订单验证地址
# cancel_flag:2
# bed_level_order_num:000000000000000000000000000000
# passengerTicketStr: seatType,0,票类型（成人票填1),乘客名,passenger_id_type_code,passenger_id_no,mobile_no,’N’
# oldPassengerStr:乘客名,passenger_id_type_code,passenger_id_no,passenger_type+’_’
# tour_flag:dc
# randCode:
# _json_att:
# REPEAT_SUBMIT_TOKEN
# @return ifShowPassCode”:”Y(需要验证码) or N” status:true成功 or false
url_check_order = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
# 准备排队
# train_date:Wed Dec 20 2017 00:00:00 GMT+0800 (CST)
# train_no,stationTrainCode,seatType,fromStationTelecode,toStationTelecode,
# leftTicket,purpose_codes=00,train_location,_json_att,REPEAT_SUBMIT_TOKEN
url_getQueueCount = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
# 买票验证码提交
# randCode rand=randp json_att, REPEAT_SUBMIT_TOKEN
url_post_buy_code = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
# 确认购买
# passengerTicketStr oldPassengerStr randCode purpose_codes key_check_isChange leftTicketStr
# train_location choose_seats seatDetailType:000 roomType:00 dwAll:N _json_att REPEAT_SUBMIT_TOKEN
# @return data.submitStatus = true 成功 or false
url_post_buy = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
# 不断请求订单 get random参数是当前秒数*1000+毫秒数
# @return 有orderId 则表示成功
url_get_order_no = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?' \
                   'random=%s&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=%s'
# 订单查询地址
url_post_order = 'https://kyfw.12306.cn/otn//payOrder/init?random=%s'

# 浏览器代理设置
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.84 Safari/537.36'}

# ==========================================================================
# 查询列车数据返回的相应索引
# mark 备注，no 车编号, name 车次,
# start_station 始发站, end_station 终点站
# from_station  to_station 过站
# from_time 出发时间, to_time 到站时间, total_time 历时
# mark_code 备注代码, leftTicket 相应字段-订单需要
# date 日期 secretStr 需要URLDecode
# from_station_no to_station_no seat_types 出发站,目的站,座位类型 查询票价需要
# seat_SW 商务座 seat_1 一等座 seat_2 二等座 seat_GJRW 高级软卧 seat_RW 软卧
# seat_DW 动卧 seat_YW 硬卧 seat_RZ 软座 seat_YZ 硬座 seat_WZ 无座
# ==========================================================================
e_train = enum(secretStr=0,
               mark=1,
               no=2,
               name=3,
               start_station=4,
               end_station=5,
               from_station=6,
               to_station=7,
               from_time=8,
               to_time=9,
               total_time=10,
               mark_code=11,
               leftTicket=12,
               date=13,
               train_location=15,
               from_station_no=16,
               to_station_no=17,
               seat_GJRW=21,
               seat_RW=23,
               seat_RZ=24,
               seat_WZ=26,
               seat_YW=28,
               seat_YZ=29,
               seat_2=30,
               seat_1=31,
               seat_SW=32,
               seat_DW=33,
               seat_types=35)

'''A1	硬座  
   A2	软座   
   A3	硬卧   
   A4	软卧   
   A6	高级软卧 
   A9	商务座  
   F	动卧  
   M	一等座  
   O	二等座  
   WZ	无座   
'''
e_seat = enum(SW='A9', ONE='M', TWO='O',
              GJRW='A6', RW='A4', DW='F',
              YW='A3', RZ='A2', YZ='A1', WZ='WZ')


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
