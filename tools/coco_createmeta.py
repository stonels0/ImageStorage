# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-26 18:51:18
# @Last Modified by:   Lishi
# @Last Modified time: 2017-12-12 20:40:06
import json
import sys
import os,os.path
import copy
from string import Template
import subprocess
import pdb
'''
   图像数据库入库工作；
'''
# 改变运行目录==>脚本所在目录；避免相对位置出错;
scriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(scriptPath)

def split_str(s, n):
    length = len(s)
    return [ s[i:i+n] for i in range(0, length, n) ]

def extract_metadata_ann(image_id):
    global imgAnnIdsMap
    global keypoint_map
    global cap_map
    
    flag_instance=None
    flag_key=None
    flag_cap=None
    # 此种方式，如果键值不存在，报异常;
    #item_instance = imgAnnIdsMap[image_id]
    item_instance = imgAnnIdsMap.get(image_id) # 返回值为item 数据；
    item_key = keypoint_map.get(image_id) # 返回值为item 数组 
    item_cap = cap_map.get(image_id) # 返回值为元素
    d = {}
    if item_instance:
        flag_instance = True
        instance = extract_metadata_instance(item_instance)
        d = instance.copy()
    if item_key:
        flag_key = True
        person_key = extract_metadata_keypoint(item_key)
        d.update(person_key)
    if item_cap:
        flag_cap = True
        caption = extract_metadata_caption(item_cap)
        d.update(caption)

    return flag_instance,flag_key,flag_cap,d

def extract_metadata_image(elems):
    if len(elems)<8: return None
    global liences_map
    d = dict()
    d['file_name'] = elems['file_name']
    d['width'] = elems['width']
    d['height'] = elems['height']
    d['coco_url'] = elems['coco_url']
    d['flickr_url'] = elems['flickr_url']
    d['date_captured'] = elems['date_captured']
    d['license'] = liences_map[ elems['license'] ]
    
    return d

def extract_metadata_image_trainval(elems):
    if len(elems)<8: return None
    global liences_map
    d = dict()
    d['file_name'] = elems['file_name']
    d['width'] = elems['width']
    d['height'] = elems['height']
    d['coco_url'] = elems['coco_url']
    d['flickr_url'] = elems['flickr_url']
    d['date_captured'] = elems['date_captured']
    d['license'] = liences_map[ elems['license'] ]
    
    return d

def extract_metadata_imagetest(elems):
    if len(elems)<7: return None
    global liences_map
    d = dict()
    d['file_name'] = elems['file_name']
    d['width'] = elems['width']
    d['height'] = elems['height']
    d['coco_url'] = elems['coco_url']

    d['date_captured'] = elems['date_captured']
    d['license'] = liences_map[ elems['license'] ]
    
    return d

def extract_metadata_instance(elems): # elems 为数组;
    global categores_map
    d = dict() # 一对多的问题，需要更改：
    for elem in elems:
        if len(elem)<7:
            print 'this is error places, please check the file or program!!!'
            print 'the length of the file: %d ' % len(elem)
            pdb.set_trace()
            return None
        item_cat = categores_map.get(elem['category_id'])
        category = [item_cat['supercategory'], item_cat['name'] ]
        d.setdefault('categories',[])
        d['categories'].append(category)
        d.setdefault('segmentations',[]).append(elem['segmentation'])
        d.setdefault('bboxs', []).append(elem['bbox'])
        d.setdefault('areas',[]).append(elem['area'])
        d.setdefault('iscrowds', []).append(elem['iscrowd'])
    return d

def extract_metadata_keypoint(elems):
    d = dict()
    for elem in elems:
        if len(elem)<9:
            print 'this is error places, please check the file or program!!!'
            print 'the length of the file: %d ' % len(elem)
            pdb.set_trace()
            return None
        d.setdefault('num_keypoints',[]).append(elem['num_keypoints'])
        d.setdefault('keypoints',[]).append(elem['keypoints'])
    return d

def extract_metadata_caption(elems):
    d = dict()
    for elem in elems:
        if len(elem)<3:
            print 'this is error places, please check the file or program!!!'
            print 'the length of the file: %d ' % len(elem)
            pdb.set_trace()
            return None
        d.setdefault('captions',[]).append(elem['caption'])
    return d

captions_train2014 = './captions_train2014.json'
captions_val2014 = './captions_val2014.json'
image_info_test2014 =  './image_info_test2014.json'
image_info_test2015 =  './image_info_test2015.json'
image_info_testdev2015 =  './image_info_test-dev2015.json'
instances_train2014 = './instances_train2014.json'
instances_val2014 = './instances_val2014.json'
person_keypoints_train2014 = './person_keypoints_train2014.json'
person_keypoints_val2014= './person_keypoints_val2014.json'

# 读入文件：
with open(captions_train2014,'r') as f:
    captions_train2014 = json.load(f)

with open(captions_val2014,'r') as f:
    captions_val2014 = json.load(f)

with open(image_info_test2014,'r') as f:
    image_info_test2014 = json.load(f)

with open(image_info_test2015,'r') as f:
    image_info_test2015 = json.load(f)

with open(image_info_testdev2015,'r') as f:
    image_info_testdev2015 = json.load(f)

with open(instances_train2014,'r') as f:
    instances_train2014 = json.load(f)

with open(instances_val2014,'r') as f:
    instances_val2014 = json.load(f)

with open(person_keypoints_train2014,'r') as f:
    person_keypoints_train2014 = json.load(f)

with open(person_keypoints_val2014,'r') as f:
    person_keypoints_val2014 = json.load(f)


metadir = './meta'

# 似乎没有必要，直接 以此为遍历对象即可；
#instances_map = {}
# install the map for image_id -- item
#for item in instances_train2014['images']:
    #instances_map[item['id']] = item
#for item in instances_val2014['images']:
    #instances_map[item['id']] = item

imgAnnIdsMap = {}
# 1：N   (one picture vs multiple labels;)
for item in instances_train2014['annotations']:
    # sefdefault,同get()方法，如不存在，将会添加键，并将至设为默认值；
    #                         如存在，返回该键对应的值，否则返回该键设置的值；
    imgAnnIdsMap.setdefault(item['image_id'], [])
    imgAnnIdsMap[item['image_id']].append(item)
for item in instances_val2014['annotations']:
    imgAnnIdsMap.setdefault(item['image_id'], []).append(item)

categores_map = {}
# install the map for category_id -- item
for item in instances_train2014['categories']:
    categores_map[item['id']] = item

liences_map = {}
for item in instances_train2014['licenses']:
    liences_map[item['id']] = item


cap_map = {}
for item in captions_train2014['annotations']:
    cap_map.setdefault(item['image_id'],[]).append(item)
for item in captions_val2014['annotations']:
    cap_map.setdefault(item['image_id'],[]).append(item)

keypoint_map = {}
for item in person_keypoints_train2014['annotations']:
    keypoint_map.setdefault(item['image_id'], [])
    keypoint_map[item['image_id']].append(item)
for item in person_keypoints_val2014['annotations']:
    keypoint_map.setdefault(item['image_id'], [])
    keypoint_map[item['image_id']].append(item)

json_dir = metadir
for instance_item in image_info_testdev2015['images']:
    filename = instance_item['file_name']
    image_id = instance_item['id']      # 索引 其他存在的 map（如标注，执照等）
    json_path = os.path.join(json_dir, filename.strip().split('.')[0]+'_meta.json')
    if os.path.isfile(json_path) and os.path.getsize(json_path):
        print 'file name: %s metadata already exists, skip.' % filename
        continue
    print 'file name %s metadata creating...' % filename
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    # form JSON data and write it to a file
    json_data = dict()
    json_data['image'] = extract_metadata_imagetest(instance_item)

    instance,keypoint,caption,annotations = extract_metadata_ann(image_id)
    func = lambda x,y:x if y in x else x + [y]
    if 'categories' in annotations.keys():
        tag=reduce(func,[[],]+annotations['categories'])
    else:
        tag = None
    json_data['tag'] = tag
    
    if instance:
        json_data.setdefault('annType',[]).append('instance')
    if keypoint:
        json_data.setdefault('annType',[]).append('keypoint')
    if caption:
        json_data.setdefault('annType',[]).append('caption')
    json_data.setdefault('annType',None)

    if annotations:
        json_data['annotations'] = annotations
    json_data['info'] = image_info_testdev2015['info']

    with open(json_path, 'wb') as fout:
        # json 缩进参数和排序;
        json.dump(json_data, fout, sort_keys=True, indent=4)

'''
file_paths = {
    'captions_train2014':'./captions_train2014.json',
    'image_info_test2014': './image_info_test2014.json',
    'instances_val2014': './instances_val2014.json',
    'person_keypoints_train2014': './person_keypoints_train2014.json',
    'person_keypoints_val2014' : './person_keypoints_val2014.json'
}

pdb.set_trace()
for k,v in file_paths.iteritems():
    with open(v,'r') as f:
        exec(k+'=json.load(f)') # 可以用exec解释字符串形式的程序，字符串内可以替换变量。但最好还是用字典。

LS的应该把'abc'换成s吧 abc = 5
>>> s='abc'
>>> exec(s+'=5') # exec('abc'+'=5')
>>> abc
5

import os
import sys
#运行目录
CurrentPath = os.getcwd()
print CurrentPath
#当前脚本目录
print "##################################################"
print os.path
print sys.argv[0]
print os.path.split( os.path.realpath( sys.argv[0] ) )
print "##################################################"
ScriptPath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
print ScriptPath

'''