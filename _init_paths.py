# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-25 13:53:23
# @Last Modified by:   anchen
# @Last Modified time: 2017-07-25 13:56:15
import os
import sys
sys.path.insert(0,'core')
sys.path.insert(0,'tools')
def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
currentPath = os.path.dirname(__file__)
lib_path = os.path.join(currentPath, 'core')
add_path(lib_path)