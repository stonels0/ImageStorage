# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-25 13:53:23
# @Last Modified by:   Lishi
# @Last Modified time: 2018-01-12 16:41:57
import os
import sys
''' 将需要的文件包路径，加入文件路径'''
sys.path.insert(0,'../core')  # 插入环境变量中;

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
currentPath = os.path.dirname(__file__)
