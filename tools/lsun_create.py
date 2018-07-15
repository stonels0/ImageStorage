# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-28 10:52:03
# @Last Modified by:   Lishi
# @Last Modified time: 2018-01-12 17:37:30
# 

import os,os.path
import sys
from PIL import Image
import _init_paths
import numpy as np
import json,subprocess 
from easydict import EasyDict as edict
from xml2json import *
from file_utils import *
from submit2center import *
import pdb

def extract_info(filepath,d = None):
    d = edict()
    d.name,_ = os.path.basename(filepath).split('.')
    d.srcext,d.dstext = normalize(filepath)
    d.hashID = sha256(filepath)
    try:
        img = Image.open(filepath)
        d.mode = img.mode
        d.size = np.array(img).shape
    except:
        print ('the file cannt be import to the program, error!!!')
    return d

def get_info(size):
    if not size:
        return None,None,None
    if len(size)>2:
        return size[0],size[1],size[2]
    else:
        return size[0],size[1],1

def manipulate_from_folders():
    ''' image operation：extract info and Annotation, forming the information into the database'''
    #   input：filepath
    #   output：
    srcDataset = 'LSUN-SCLS'
    query = formsql()       # sqlquery Template
    folder_root = 'E:/Lishi/Datasets/DataSets_release/LSUN Challenge/SCENE CLASSIFICATION/Images'


    folderlist_subroot = getfolderlist_current(folder_root)

    
    hasAnn = ['train','validation']         # test 入库特殊处理;

    for i, folder in enumerate(folderlist_subroot):             # 遍历 子文件夹，即（train，validation，test）
        sub_folder_root = os.path.join(folder_root,folder)
        folderlist = getfolderlist_current(sub_folder_root)     # 对应文件夹下的文件类别，sofa。。。
        nums_subfolder = len(folderlist)
        flag_ann = False
        if folder in hasAnn:
            flag_ann = True

        for idx,subfolder in enumerate(folderlist):
            subfolder_path = os.path.join(sub_folder_root,subfolder)
            if not flag_ann:
                jsonstr = None
            else:
                ann = {}
                ann['label'] = subfolder
                jsonstr = json.dumps(ann)
            filelist = getAllImgs(subfolder_path)
            nums_img = len(filelist)
            sum_files = 0

            for j,filepath in enumerate(filelist):
                #jsonstr = createmeta(**ann_arg)

                info_dict = extract_info(filepath)
                info_img = get_info(info_dict.get('size'))
                values = [srcDataset, info_dict.get('name'), info_dict.get('srcext'),jsonstr,info_dict.get('hashID'),info_dict.get('dstext'), info_img[1], info_img[0], info_img[2],info_dict.get('mode')]
                flag_insert = insertdata(query,values)

                if not flag_insert:
                    print ('Warning, please debug the program, there are some bugs!')
                    pdb.set_trace()
                else:
                    sum_files+=1
                    sys.stdout.write(' '*100 + '\r')
                    sys.stdout.flush()
                    sys.stdout.write("insert data into {} | {}\r".format(j+1,nums_img))
                    sys.stdout.flush()
            if sum_files != nums_img:
                with open('log_lsun.txt','a') as f:
                    f.write("folder:{}\t{}|{}\n".format(subfolder_path, sum_files, nums_img))

if __name__ == '__main__':
    manipulate_from_folders()
