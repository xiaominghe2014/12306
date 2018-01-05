#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: 0.0.0
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@software: PyCharm
@file: setup.py
@time: 2017/12/12 下午5:40

"""

from setuptools import setup, find_packages

setup(
    name='py_12306',
    version='0.0.0',
    description=u'查询火车票',
    author='Ximena',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'docopt',
        'prettytable',
        'email',
    ]
)
