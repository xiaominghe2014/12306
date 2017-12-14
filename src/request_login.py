#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: request_login.py
@time: 2017/12/13 下午2:27

"""

from get_trains_data import *
import json
import getpass


class Login12306(object):
    def __init__(self):
        self.request_img = True
        self.session = requests.session()
        self.tk = ''

    def get_verify_img(self):
        if self.request_img:
            resp = self.session.get(url=url_verify_img, headers=headers, verify=False)
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
        cont = self.session.post(url=url_verify_img_check, data=data, headers=headers, verify=False)
        dic = json.loads(cont.content)
        print dic
        code = dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        # self.request_img = '7' == code
        return '4' == code

    def get_apptk(self, cb):
        data = {'appid' : 'otn'}
        resp = self.session.post(url_get_newapptk, headers=headers, data=data)
        if 200 == resp.status_code:
            result = json.loads(resp.text)
            print(result.get("result_message"))
            self.tk = result.get("newapptk")
            cb()

    def check_apptk(self):
        data = {'tk': self.tk}
        resp = self.session.post(url_check_tk, headers=headers, data=data)
        if 200 == resp.status_code:
            print(resp.text)

    def login(self):
        name = raw_input('用户名:')
        pwd = getpass.getpass('密码:')
        data = {'username': name, 'password': pwd, 'appid': 'otn'}
        result = self.session.post(url=url_login, data=data, headers=headers, verify=False)
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
        return True

    def get_order(self):
        return True

    def get_token(self):
        return True

    def get_passenger(self):
        return True

    def check_order(self):
        return True

    def get_queue_count(self):
        return True

    def post_buy(self):
        return True

    def get_order_no(self):
        pass

    def auto_req_order(self, trains):
        print trains
        res = self.check_user()
        if res:
            submit_success = self.get_order()
            if submit_success:
                is_get = self.get_token()
                if is_get:
                    get_pass = self.get_passenger()
                    if get_pass:
                        is_checked = self.check_order()
                        if is_checked:
                            if self.get_queue_count():
                                if self.post_buy():
                                    self.get_order_no()


if __name__ == '__main__':
    Login12306().req_login()