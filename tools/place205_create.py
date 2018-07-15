# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-25 10:52:03
# @Last Modified by:   Lishi
# @Last Modified time: 2017-08-14 22:24:35
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

def createmeta(xmlfile=None,label=None):
    ''' generate the jsonstr for insert into the database'''
    d = {}
    if label:
        tag = {}
        tag['label']=label
        d = tag.copy()

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
    srcDataset = 'Places205'
    query = formsql()       # sqlquery Template
    imgroot = 'E:/Lishi/Datasets/99-Source/Places 205 Database/Images'
    pdb.set_trace()
    folderlist = getfolderlist_current(imgroot)

    nums_folder = len(folderlist)

    ann_arg = edict()
    pdb.set_trace()

    for i, folder_root in enumerate(folderlist):
        folderpath = os.path.join(imgroot,folder_root)
        subfolderlist = getfolderlist_current(folderpath)

        nums_subfolder = len(subfolderlist)
        for idx,subfolder in enumerate(subfolderlist):

            imgfolder = os.path.join(folderpath, subfolder)

            imglist = getAllImgs(imgfolder)
            nums_img = len(imglist)
            print ('{}: {} | {} |{} will be insert into the database.'.format(subfolder, idx+1, nums_subfolder,nums_img))

            sum_files = 0
            ann_arg.label = subfolder

            for jdx,filepath in enumerate(imglist):
                #filename = os.path.basename(filepath)

                #jsonstr = createmeta(xmlfile,label) # srcAnn
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
                    sys.stdout.write("insert data into {} | {}\r".format(jdx+1,nums_img))
                    sys.stdout.flush()
            if sum_files != nums_img:
                with open('log_imagenet.txt','a') as f:
                    f.write("folder:{}\t{}|{}\n".format(subfolder, sum_files, nums_img))

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