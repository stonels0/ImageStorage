# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2018-06-08 19:39:32
# @Last Modified by:   Lishi
# @Last Modified time: 2018-06-14 20:53:12
import os,os.path
import sys
from PIL import Image                       # 载入图像处理包，用于图像文件的读入和保存;
import _init_paths                          # 载入_init_paths.py 路径文件;
import scipy.io as scio
import numpy as np
import json,subprocess 
from easydict import EasyDict as edict
from xml2json import *                      # xml2json.py 文件，进行xml==》json;
from file_utils import *                    # file_utils.py 文件，进行文件相关操作;
from submit2center_test2 import *                 # submit2center_test.py 文件，进行与数据库交互的功能;
import pdb
import threading,time
import string
##---------------------------------------------------------------------------------------------------------
#提取srcAnn
def extract_ann(srcforder):
    assert os.path.isdir(srcforder)
    fordername = os.path.basename(srcforder)
    filepath = './synset.txt'
    syn_map = loadmap(filepath)
    tag = syn_map.get(fordername)
    filelist = getfolderlist_current(filepath)
#提取信息
def extract_info(filepath,d = None):
    d = edict()
    d.name,_ = os.path.basename(filepath).split('.')
    d.srcext,d.dstext = normalize(filepath)
    d.hashID = sha256(filepath)
    flag = False
    try:
        img = Image.open(filepath)
        d.mode = img.mode
        d.size = np.array(img).shape
        flag = True
    except:
        pass
        # print ('the file cannt be import to the program, error!!!')# 文件不能读取
    return d,flag

def get_info(size):
    if not size:
        return None,None,None
    if len(size)>2:
        return size[0],size[1],size[2]
    else:
        return size[0],size[1],1

# 操作文件夹;
def manipulate_from_folders(imgRoot,annRoot):
    ''' image operation：extract info and Annotation, forming the information into the database'''
    #   input：filepath
    #   output：

    srcDataset = 'OpenImage'     # 存储数据集名称;
    query = formsql()       # sqlquery Template
    imgroot = imgRoot
    annroot = annRoot
    desroot = 'E:/Lishi/Datasets/DataSets_release/OpenImage/complete_Image'
    #把已经入库的图像放到这个文件夹里面
    parentFolders = getfolderlist_current(imgroot)
    num_parent_folders = len(parentFolders)

    flag_num = 0#用来计数入库数量

    for pIdx,pFolder in enumerate(parentFolders):
        forder_path = os.path.join(imgroot,pFolder)

        folders = getfolderlist_current(forder_path)
        num_sub_folders = len(folders)

        for sIdx,sFolder in enumerate(folders):
            imgfolder = os.path.join(forder_path,sFolder)
            imglist = getAllImgs(imgfolder)
           #pdb.set_trace()
            nums_img = len(imglist)
            sum_files = 0
            
            if nums_img == 0:
                try:
                    os.removedirs(imgfolder)#删除空文件夹
                    print("already delete current empty folder!")
                except Exception as e:
                    continue
            else:
                print("current is: " + imgfolder)

                for jdx,filepath in enumerate(imglist):
                    filename,_ = os.path.basename(filepath).split('.')

                    ann_path = os.path.join(annroot,pFolder,sFolder,filename+'_meta.json')
                    if not os.path.exists(ann_path): # 若标注文件未生成，则跳过;
                        continue

                    with open(ann_path,'r') as f:
                        json_file = json.load(f)
                    jsonstr = json.dumps(json_file)#得到srcAnn这个信息

                    info_dict,flag_info = extract_info(filepath)
                    if not flag_info:
                        # pdb.set_trace()
                        continue
                    info_img = get_info(info_dict.get('size'))
                    # pdb.set_trace()

                    values = [srcDataset, info_dict.get('name'), info_dict.get('srcext'),jsonstr,info_dict.get('hashID'),info_dict.get('dstext'), info_img[1], info_img[0], info_img[2],info_dict.get('mode')]
                    despath = os.path.join(desroot,pFolder,sFolder)

                    try:
                        if not os.path.exists(despath):
                            os.makedirs(despath)
                    except Exception as e:
                        continue

                    if not os.path.exists(despath):
                        os.makedirs(despath)

                    # flag = movefile(filepath,despath)
                    # if not flag:
                    #     continue

                    flag_insert = insertdata(query,values)
                    if not flag_insert:
                        # despath_flip = os.path.join(despath,os.path.basename(filepath))
                        # filepath_flip = os.path.dirname(filepath)
                        # flag = movefile(despath_flip,filepath_flip)
                        print ('Warning, please debug the program, there are some bugs!')
                        # pdb.set_trace()
                    else:
                        flag = movefile(filepath,despath)
                        if not flag:
                            with open('log_YFCC100M_shouldMove.txt','a') as f:
                                f.write("{}\n".format(filepath))
                        sum_files+=1

                        flag_num += 1
                        print(flag_num)

                        sys.stdout.write(' '*100 + '\r')
                        sys.stdout.flush()
                        sys.stdout.write("insert data into {} | {}\r".format(jdx+1,nums_img))
                        sys.stdout.flush()

                if sum_files == nums_img: 
                    try:
                        os.removedirs(imgfolder)#删除空文件夹
                        print("operate all image, current folder is empty,delete!")
                    except Exception as e:
                        continue
                #if sum_files != nums_img:
                else:
                    pass
                    # print('the all image can not been insert! ')
                    # with open('log_YFCC100M.txt','a') as f:
                    #     f.write("folder:{}\t{}|{}\n".format(subfolder, sum_files, nums_img))

       

def test_insertdata():
    srcroot = 'E:/DataSet_Download/ImageNet'
    dstroot = 'E:/DataSet_Download/1-Image'
    filepath1 = 'E:/0557.jpg'
    filepath2 = 'E:/FeiGe/results/pascal_car/cmyk.JPEG'

    synset_file = './synset.txt'
    synset_map = loadmap(synset_file)                   # 以字典形式存储Imagenet对应的语义标签;
    xml1 = 'E:/DataSet_Download/ImageNet/Annotation/Annotation/n01322604/n01322604_3.xml'
    xml2 = '../2007_000063.xml'                         # multiple object test; perfect;
    foldername = os.path.dirname(xml1).split('/')[-1]   # n01322604 对应的文件夹，即Imagenet中的标号;
    tag = synset_map.get(foldername)                    # Imagenet标号对应的语义标签;
    jsonstr = createmeta(xml2, tag)                     # 最终转化为对应的json字符串;

    srcAnn1 = jsonstr
    # pdb.set_trace()

    d1 = extract_info(filepath1)                        # 从图像中提取信息，保存到字典d1中;
   
    srcDataset = 'ImageNet'

    info1 = get_info(d1.get('size'))                    # 从字典 d1 中提取图像尺寸信息;
    # pdb.set_trace()
    query = formsql()                                   # 组合图像的标注信息和其他信息，组合为sql语句形式;
    values = [srcDataset, d1.name, d1.srcext,srcAnn1,d1.dstext,d1.dstext, info1[1], info1[0], info1[2],d1.mode]
    insertdata(query,values)                            # 插入操作;

def test_xml_jsonstr():
    filename = './synset.txt'
    synset_map = loadmap(filename)     # 以字典形式存储Imagenet对应的语义标签;
    xml1 = 'E:/DataSet_Download/ImageNet/Annotation/Annotation/n01322604/n01322604_3.xml'
    xml2 = '../2007_000063.xml'        # multiple object test; perfect;
    foldername = os.path.dirname(xml1).split('/')[-1]  # n01322604 对应的文件夹，即Imagenet中的标号;
    tag = synset_map.get(foldername)                   # Imagenet标号对应的语义标签;
    jsonstr = createmeta(xml2, tag)                    # 最终转化为对应的json字符串;
    print type(jsonstr)
    print jsonstr        
"""
def demo_OpenImage(dirpath, annroot, demandlist):
    #demandlist = [folder for folder in folderlist if folder.startswith('img') and os.path.isdir(os.path.join(dirpath,folder))]
    #demandlist = [folder for folder in folderlist if folder.startswith('img') and os.path.isdir(os.path.join(dirpath,folder))]
    sum_folders = len(demandlist)
    print 'the folderlist number is:%s ' %(sum_folders)

    for id,folder in enumerate(demandlist):
        print('{}:{} {}\n'.format(id+1,sum_folders,folder))
        # pdb.set_trace()
        imgroot = os.path.join(dirpath,folder)
       	manipulate_from_folders(imgroot,annroot) # 操作文件夹;
"""
def demo_OpenImage():

    annroot = 'E:/Lishi/Datasets/DataSets_release/OpenImage/metadata/test'

    dirpath = 'E:/Lishi/Datasets/DataSets_release/OpenImage/images'
    folderlist = ['test1']
    #folderlist = os.listdir(dirpath)
    #demandlist = [folder for folder in folderlist if folder.startswith('img') and os.path.isdir(os.path.join(dirpath,folder))]
    # demandlist = ['img3']

    sum_folders = len(folderlist)
    print 'the folderlist number is:%s ' %(sum_folders)

    for id,folder in enumerate(folderlist):
        print('{}:{} {}\n'.format(id+1,sum_folders,folder))
        pdb.set_trace()
        imgroot = os.path.join(dirpath,folder)
        manipulate_from_folders(imgroot,annroot) # 操作文件夹;

if __name__ == '__main__':
    #main()
    instance_idAnn_Map = {}
    
    cap_idAnn_Map = {}

    keypoints_idAnn_Map = {}

    categories_map = {}

    liences_map = {}
    demo_OpenImage()
    #annroot = 'E:/Lishi/Datasets/DataSets_release/OpenImage/metadata/test'

    #dirpath = 'E:/Lishi/Datasets/DataSets_release/OpenImage/images/test1'
    #folderlist = os.listdir(dirpath)
    #demandlist1 = ['img331', 'img332', 'img333', 'img334']
    #pdb.set_trace()
    #task1 = threading.Thread(target = demo_OpenImage, args = (dirpath, annroot, folderlist,))
    #task1.start()
"""
def testcode():
    #test_xml_jsonstr()                 # 测试代码 xml 转化为 json 字符串;
    #test_insertdata()                  # 测试代码 向数据库插入数据;
    demo_YFCC100M()           

def main():
    instance_idAnn_Map = {}
    
    cap_idAnn_Map = {}

    keypoints_idAnn_Map = {}

    categories_map = {}

    liences_map = {}
    testcode()
"""
#if __name__ == '__main__':
    #main()