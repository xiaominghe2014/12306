#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: 0.0.0
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@todo: 详情见代码列表
@software: PyCharm
@file: request_login.py
@time: 2017/12/13 下午2:27

"""

from get_trains_data import *
import json
import getpass
import datetime
import time
from time import strftime

class Login12306(object):

    def __init__(self):
        self.request_img = True
        self.session = requests.session()
        self.tk = ''
        self.train_map = None
        self.token = ''
        self.key_check_isChange = ''
        self.passengers = []
        # todo 根据相应的列车信息筛选座位类型
        self.seatType = '1'

    def get(self, arg_url):
        return self.session.get(url=arg_url, headers=headers, verify=False)

    def post(self, arg_url, data):
        return self.session.post(url=arg_url, data=data, headers=headers, verify=False)

    def get_verify_img(self):
        if self.request_img:
            resp = self.get(url_verify_img)
            with open('../img/img.jpg', 'wb') as f:
                f.write(resp.content)
                # self.request_img = False
        verify_res = raw_input('请输入验证码位置(1-8):')
        return verify_res

    def check_verify_img(self, verify_res):
        img_area = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']
        answer_list = []
        for i in range(len(verify_res)):
            answer_list.append(img_area[int(verify_res[i])-1])
        answer = ','.join(answer_list)
        data = {'login_site': 'E', 'rand': 'sjrand', 'answer': answer}
        cont = self.post(url_verify_img_check, data)
        dic = json.loads(cont.content)
        code = dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        # self.request_img = '7' == code
        return '4' == code

    def get_apptk(self, cb):
        data = {'appid' : 'otn'}
        resp = self.post(url_get_newapptk, data)
        if 200 == resp.status_code:
            result = json.loads(resp.text)
            print(result.get("result_message"))
            self.tk = result.get("newapptk")
            cb()

    def check_apptk(self):
        data = {'tk': self.tk}
        resp = self.post(url_check_tk, data)
        if 200 == resp.status_code:
            print(resp.text)

    def login(self):
        name = raw_input('用户名:')
        pwd = getpass.getpass('密码:')
        data = {'username': name, 'password': pwd, 'appid': 'otn'}
        result = self.post(url_login, data)
        dic = json.loads(result.content)
        print dic
        result = dic['result_code']
        if 0 != result:
            self.login()
        else:
            self.get_apptk(self.check_apptk)

    def req_login(self):
        is_verify = self.check_verify_img(self.get_verify_img())
        if is_verify:
            self.login()
        else:
            self.req_login()

    def check_user(self):
        data = {'_json_att': ''}
        resp = self.post(url_check_usr, data)
        if 200 == resp.status_code:
            result = json.loads(resp.text)
            return result['data']['flag']
        return False

    def get_order(self, arg_train):
        if not self.train_map:
            self.train_map = get_tel_code()
        data = {
            'secretStr': arg_train[e_train.secretStr],
            'train_date': datetime.strptime(arg_train[e_train.date], '%Y-%m-%d'),
            'back_train_date': '2017-12-25',
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': self.train_map[arg_train[e_train.from_station]],
            'query_to_station_name': self.train_map[arg_train[e_train.to_station]],
            'undefined': ''
        }
        resp = self.post(url_get_order, data)
        return 200 == resp.status_code

    def get_token(self):
        data = {'_json_att': ''}
        resp = self.post(url_get_token, data)
        if 200 == resp.status_code:
            token_txt = get_txt_by_re(resp.text, r'var globalRepeatSubmitToken = \'(.*?)\'')
            self.token = token_txt.group(1)
            check_txt = get_txt_by_re(resp.text, r'\'key_check_isChange\':\'(.*?)\'')
            self.key_check_isChange = check_txt.group(1)
            return True
        return False

    def get_passenger(self):
        data = {'_json_att': '', 'REPEAT_SUBMIT_TOKEN': self.token}
        resp = self.post(url_passengerDTOs, data)
        if 200 == resp.status_code:
            js = json.loads(resp.text)
            self.passengers = js['data']['normal_passengers']
            return True
        return False

    def get_buy_img(self):
        if self.request_img:
            resp = self.get(url_get_buy_img)
            with open('../img/img.jpg', 'wb') as f:
                f.write(resp.content)
        return True

    def check_buy_img(self):
        verify_res = raw_input('请输入验证码位置(1-8):')
        img_area = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']
        answer_list = []
        for i in range(len(verify_res)):
            answer_list.append(img_area[int(verify_res[i])-1])
        answer = ','.join(answer_list)
        data = {'rand': 'randp', 'randCode': answer, 'json_att': '', 'REPEAT_SUBMIT_TOKEN': self.token}
        cont = self.post(url_post_buy_code, data)
        js = json.loads(cont.content)
        code = js['data']['result']
        return '1' == code

    def get_passenger_ticket(self):
        passenger = self.passengers[0]
        return '%s,0,1,%s,%,%s,%s,N' % (self.seatType, passenger['passenger_name'], passenger['passenger_id_type_code'],
                                        passenger['passenger_id_no'], passenger['mobile_no'])

    def get_old_passenger(self):
        passenger = self.passengers[0]
        return '%s,%s,%s,%s_' % (passenger['passenger_name'], passenger['passenger_id_type_code'],
                                 passenger['passenger_id_no'], passenger['passenger_type'])

    def check_order(self):
        data = {
            'cancel_flag': 2,
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': self.get_passenger_ticket(),
            'oldPassengerStr': self.get_old_passenger(),
            'tour_flag': 'dc',
            'randCode': '',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        resp = self.post(url_check_order, data)
        if 200 == resp.status_code:
            # todo 此处根据ifShowPassCode添加验证是否需要验证码
            return True
        return False

    def get_queue_count(self, arg_train):
        train_date = strftime('%a %b %d %Y %H:%M:%S GMT+0800 (CST)', time.strptime(arg_train[e_train.date], '%Y%m%d'))
        data = {
            'train_date': train_date,
            'train_no': arg_train[e_train.no],
            'stationTrainCode': arg_train[e_train.name],
            'seatType': self.seatType,
            'fromStationTelecode': arg_train[e_train.from_station],
            'toStationTelecode': arg_train[e_train.to_station],
            'leftTicket': arg_train[e_train.leftTicket],
            'purpose_codes': '00',
            'train_location': arg_train[e_train.train_location],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        resp = self.post(url_getQueueCount, data)
        if 200 == resp.status_code:
            return True
        return False

    def post_buy(self, arg_train):
        data = {'passengerTicketStr': self.get_passenger_ticket(),
                'oldPassengerStr': self.get_old_passenger(),
                'randCode': '',
                'purpose_codes': '00',
                'key_check_isChange': self.key_check_isChange,
                'leftTicketStr': arg_train[e_train.leftTicket],
                'train_location': arg_train[e_train.train_location],
                'choose_seats': '',
                'seatDetailType': '000',
                'roomType': '00',
                'dwAll': '',
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': self.token
                }
        resp = self.post(url_post_buy, data)
        if 200 == resp.status_code:
            return True
        return False

    def get_order_no(self):
        get_url = url_get_order_no % ('1513307920803',self.token)
        resp = self.get(get_url)
        if 200 == resp.status_code:
            js = json.loads(resp.text)
            order_id = js['data']['orderId']
            if 'null' != order_id and order_id:
                print '订票成功,请及时到网站支付...\n' \
                      '订单号:%s' % order_id
                return True
            else:
                return self.get_order_no()
        return False

    def auto_req_order(self, trains):
        print trains
        res = self.check_user()
        if res:
            submit_success = self.get_order(trains[0])
            if submit_success:
                is_get = self.get_token()
                if is_get:
                    get_pass = self.get_passenger()
                    if get_pass:
                        is_checked = self.check_order()
                        if is_checked:
                            if self.get_queue_count(trains[0]):
                                if self.post_buy():
                                    self.get_order_no()
        else:
            self.req_login()
            self.auto_req_order(trains)


if __name__ == '__main__':
    Login12306().req_login()