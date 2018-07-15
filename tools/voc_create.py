# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-25 10:52:03
# @Last Modified by:   Lishi
# @Last Modified time: 2017-12-12 22:51:31
import os,os.path
import sys
from PIL import Image
import _init_paths
import scipy.io as scio
import numpy as np
import json,subprocess 
from easydict import EasyDict as edict
from xml2json import *
from file_utils import *
from submit2center import *
import pdb
'''
    voc2012 数据集数据解析并入库;
'''

def loadmap(filepath):
    synsetmap = {}
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        while True:
            lines = f.readline()
            if not lines:
                break
                pass
            p_key = lines.strip().split(' ')[0]
            p_value = lines[len(p_key):].strip()
            synsetmap[p_key]=p_value
    return synsetmap

def createmeta(xmlfile=None,segClass=None,segObject=None):
    ''' generate the jsonstr to insert into the database'''
    pdb.set_trace()
    d = {}
    if segClass:
        tag = {}
        tag['segClass']=sha256(segClass)
        d = tag.copy()
    if segObject:
        tag={}
        tag['segObject']=sha256(segObject)
        d.update(tag)

    if xmlfile and os.path.exists(xmlfile):
        xml = open(xmlfile, 'r').read()
        result = Xml2Json(xml).result # dict
        d.update(result) # 把字典result的键/值对更新到d里
    if not d:
        jsonstr = None
    else:
        jsonstr = json.dumps(d)

    return jsonstr;

def extract_ann(srcforder):
    assert os.path.isdir(srcforder)
    fordername = os.path.basename(srcforder)
    filepath = './synset.txt'
    syn_map = loadmap(filepath)
    tag = syn_map.get(fordername)
    filelist = getfolderlist_current(filepath)

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
    # output：
    srcDataset = 'VOC2012'
    query = formsql()       # sqlquery Template
    folder_root = 'E:/Lishi/Datasets/DataSets_release/VOC12'
    imgroot = os.path.join(folder_root,'JPEGImages')
    annroot = os.path.join(folder_root,'Annotations')
    segmentationClass_folder = os.path.join(folder_root,'SegmentationClass')
    segmentationObject_folder = os.path.join(folder_root,'SegmentationObject')

    imglist = getAllImgs(imgroot)
    nums_img = len(imglist)

    #print ('{}: {} | {} |{} will be insert into the database.'.format(folder, i+1, nums_folder,nums_img))

    sum_files = 0
    ann_arg = edict()

    for idx,filepath in enumerate(imglist):
        filename = os.path.basename(filepath)
        shortname,_ = os.path.splitext(filename)
        xmlfile = os.path.join(annroot,shortname + '.xml')
        segClass = os.path.join(segmentationClass_folder,shortname+'.png')
        segObject = os.path.join(segmentationObject_folder,shortname+'.png')
        if os.path.exists(xmlfile):
            ann_arg.xmlfile = xmlfile
        if os.path.exists(segClass):
            ann_arg.segClass = segClass
        if os.path.exists(segObject):
            ann_arg.segObject = segObject

        jsonstr = createmeta(**ann_arg)

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
            sys.stdout.write("insert data into {} | {}\r".format(idx+1,nums_img))
            sys.stdout.flush()
    if sum_files != nums_img:
        with open('log_imagenet.txt','a') as f:
            f.write("folder:{}\t{}|{}\n".format(folder, sum_files, nums_img))

def test_insertdata():
    srcroot = 'E:/DataSet_Download/ImageNet'
    dstroot = 'E:/DataSet_Download/1-Image'
    filepath1 = 'E:/0557.jpg'
    filepath2 = 'E:/FeiGe/results/pascal_car/cmyk.JPEG'

    synset_file = './synset.txt'
    synset_map = loadmap(synset_file)
    xml1 = 'E:/DataSet_Download/ImageNet/Annotation/Annotation/n01322604/n01322604_3.xml'
    xml2 = '../2007_000063.xml' # multiple object test; perfect;
    foldername = os.path.dirname(xml1).split('/')[-1]
    tag = synset_map.get(foldername)
    jsonstr = createmeta(xml2, tag) 

    srcAnn1 = jsonstr
    pdb.set_trace()

    d1 = extract_info(filepath1)
   
    srcDataset = 'ImageNet'

    info1 = get_info(d1.get('size'))  
    pdb.set_trace()
    query = formsql()
    values = [srcDataset, d1.name, d1.srcext,srcAnn1,d1.dstext,d1.dstext, info1[1], info1[0], info1[2],d1.mode]
    insertdata(query,values)  

def test_xml_jsonstr():
    filename = './synset.txt'
    synset_map = loadmap(filename)
    xml1 = 'E:/DataSet_Download/ImageNet/Annotation/Annotation/n01322604/n01322604_3.xml'
    xml2 = '../2007_000063.xml' # multiple object test; perfect;
    foldername = os.path.dirname(xml1).split('/')[-1]
    tag = synset_map.get(foldername)
    jsonstr = createmeta(xml2, tag)
    print type(jsonstr)
    print jsonstr        
def testcode():
    #test_xml_jsonstr()
    #test_insertdata()
    manipulate_from_folders()

def main():
    testcode()

if __name__ == '__main__':
    main()