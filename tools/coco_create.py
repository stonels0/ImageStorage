# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-25 10:52:03
# @Last Modified by:   Lishi
# @Last Modified time: 2018-01-12 17:31:24
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
from submit2center import *                 # submit2center.py 文件，进行与数据库交互的功能;
import pdb

def extract_metadata_ann(image_id):
    # 将定义的全局变量模块导入
    global instance_idAnn_Map               #            
    global keypoints_idAnn_Map
    global cap_idAnn_Map
    
    flag_instance=None
    flag_key=None
    flag_cap=None
    # 此种方式，如果键值不存在，报异常;
    #item_instance = instance_idAnn_Map[image_id]
    item_instance = instance_idAnn_Map.get(image_id) # 返回值为item 数据；
    item_key = keypoints_idAnn_Map.get(image_id) # 返回值为item 数组 
    item_cap = cap_idAnn_Map.get(image_id) # 返回值为元素
    d = {}
    if item_instance:
        flag_instance = True
        instance = extract_metadata_instance(item_instance)
        #d = instance.copy()
        d['instances'] = instance
    if item_key:
        flag_key = True
        person_key = extract_metadata_keypoint(item_key)
        #d.update(person_key)
        d['person_key'] = person_key
    if item_cap:
        flag_cap = True
        caption = extract_metadata_caption(item_cap)
        d.update(caption)
        #d['captions'] = caption

    return flag_instance,flag_key,flag_cap,d
'''
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
'''
##----------------------------------------------------------
## extract the base image information;
def extract_metadata_image_trainval(elems):
    if len(elems)<8: return None
    global liences_map
    d = dict()
    d['file_name'] = elems['file_name']
    d['width'] = elems['width']
    d['height'] = elems['height']
    d['coco_url'] = elems['coco_url']
    d['flickr_url'] = elems['flickr_url'] # 多一个 ‘flickr_url’ 属性
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
##---------------------------------------------------
## 提取三类标注信息;
def extract_metadata_instance(elems): # elems 为数组;
    global categories_map
    d = dict() # 一对多的问题，需要更改：
    for elem in elems:
        if len(elem)<7:
            print 'this is error places, please check the file or program!!!'
            print 'the length of the file: %d ' % len(elem)
            pdb.set_trace()
            return None
        item_cat = categories_map.get(elem['category_id'])
        category = [item_cat['supercategory'], item_cat['name'] ]
        ## 去掉了id 和 imageid;
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
        # categories allways the person;
        d.setdefault('segmentations',[]).append(elem['segmentation'])
        d.setdefault('num_keypoints',[]).append(elem['num_keypoints'])
        d.setdefault('areas',[]).append(elem['area'])
        d.setdefault('iscrowds', []).append(elem['iscrowd'])
        d.setdefault('keypoints',[]).append(elem['keypoints'])
        d.setdefault('bboxs', []).append(elem['bbox'])
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
##---------------------------------------------------------------------------------------------------------
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

# 操作文件夹;
def manipulate_from_folders():
    ''' image operation：extract info and Annotation, forming the information into the database'''
    #   input：filepath
    #   output：
    # 将定义的全局变量模块导入
    global instance_idAnn_Map 
    
    global cap_idAnn_Map

    global keypoints_idAnn_Map

    global categories_map
    global liences_map

    liences_map = {}
    srcDataset = 'COCO'     # 存储数据集名称;
    query = formsql()       # sqlquery Template
    imgroot = 'E:/Lishi/Datasets/DataSets_release/MS_COCO/coco-master/images'
    annroot = 'E:/Lishi/Datasets/DataSets_release/MS_COCO/coco-master/annotations'


    image_info_test2015 = os.path.join(annroot,'image_info_test2015.json')
    image_info_testdev2015 = os.path.join(annroot,'image_info_test-dev2015.json')

    image_info_test2014 = os.path.join(annroot,'image_info_test2014.json')
    
    with open(image_info_test2014,'r') as f:
        image_info_test2014 = json.load(f)

    with open(image_info_test2015,'r') as f:
        image_info_test2015 = json.load(f)

    with open(image_info_testdev2015,'r') as f:
        image_info_testdev2015 = json.load(f)
  
    captions_train2014 = os.path.join(annroot,'captions_train2014.json')
    captions_val2014 = os.path.join(annroot,'captions_val2014.json')

    instances_train2014 = os.path.join(annroot,'instances_train2014.json')
    instances_val2014 = os.path.join(annroot,'instances_val2014.json')
    
    person_keypoints_train2014 = os.path.join(annroot,'person_keypoints_train2014.json')
    person_keypoints_val2014= os.path.join(annroot,'person_keypoints_val2014.json')

    # 读入文件：
    with open(captions_train2014,'r') as f:
        captions_train2014 = json.load(f)

    with open(captions_val2014,'r') as f:
        captions_val2014 = json.load(f)

    with open(instances_train2014,'r') as f:
        instances_train2014 = json.load(f)

    with open(instances_val2014,'r') as f:
        instances_val2014 = json.load(f)

    with open(person_keypoints_train2014,'r') as f:
        person_keypoints_train2014 = json.load(f)

    with open(person_keypoints_val2014,'r') as f:
        person_keypoints_val2014 = json.load(f)

    ## coco组织方式：
    # 分为两年发布：2014 和 2015；
    # 每年的图像基本信息相同(test(7) 和 train/val(8) 少一个'flickr_url'属性)，存储在三种标注方式的images标签中(当然也分为train、val和test)
    # test15/14标注中，相同标注：lienses\categories，info（基于年份）略有不同
    # 14版本中，三类标注图像基本信息为同一个；images、info、liences相同
    # caption不包含类别（categories）信息，instance 和 person_keypoint 类别信息不同；
    # 14 的 标注信息，三类当然肯定不同啦~·~
    # 
    # 第一级: info, images, annType, tag
    # 第二级:
    ## 插入数据库方式
    # 按照各个年份的images 基本信息，同时分为，train、val 和 test 进行插入；
    # 按照imageId 查询标注信息；因此，需要生成 以 imageId 为key的哈希存储类型，方便查询；
    # 按照lienses 查询liences信息，info的话，直接插入
    # # 三类标注，以字典形式载入内存
    instance_idAnn_Map = {}
    # 1：N   (one picture vs multiple labels;)
    for item in instances_train2014['annotations']:
        # sefdefault,同get()方法，如不存在，将会添加键，并将至设为默认值；
        #                         如存在，返回该键对应的值，否则返回该键设置的值；
        instance_idAnn_Map.setdefault(item['image_id'], [])
        instance_idAnn_Map[item['image_id']].append(item)
    for item in instances_val2014['annotations']:
        instance_idAnn_Map.setdefault(item['image_id'], []).append(item)

    cap_idAnn_Map = {}
    for item in captions_train2014['annotations']:
        cap_idAnn_Map.setdefault(item['image_id'],[]).append(item)
    for item in captions_val2014['annotations']:
        cap_idAnn_Map.setdefault(item['image_id'],[]).append(item)

    keypoints_idAnn_Map = {}
    for item in person_keypoints_train2014['annotations']:
        keypoints_idAnn_Map.setdefault(item['image_id'], [])
        keypoints_idAnn_Map[item['image_id']].append(item)
    for item in person_keypoints_val2014['annotations']:
        keypoints_idAnn_Map.setdefault(item['image_id'], [])
        keypoints_idAnn_Map[item['image_id']].append(item)
    categories_map = {}
    # install the map for category_id -- item
    for item in instances_train2014['categories']:
        categories_map[item['id']] = item

    liences_map = {}
    for item in instances_train2014['licenses']:
        liences_map[item['id']] = item
    '''
    # 2014 train

    imgfolder = os.path.join(imgroot,'train2014')
    sum_files = 0
    nums_img = len(instances_train2014['images'])
    for idx,image_item in enumerate(instances_train2014['images']):
        filename = image_item['file_name']
        image_id = image_item['id']      # 索引 其他存在的 map（如标注，执照等）
        
        ## 获得 jsonstr 属性;

        # form JSON data and write it to a file
        json_data = dict()

        json_data['image'] = extract_metadata_image_trainval(image_item)

        instance_flag,keypoint_flag,caption_flag,annotations = extract_metadata_ann(image_id)
        # 提取所有的categories 类别，唯一性；
        func = lambda x,y:x if y in x else x + [y]
        if annotations.get('instances') and 'categories' in annotations.get('instances').keys():
            tag=reduce(func,[[],]+annotations.get('instances')['categories'])
        else:
            tag = None
        json_data['tag'] = tag
        # 标识 有哪些标注信息，放在同 images 一级;
        if instance_flag:
            json_data.setdefault('annType',[]).append('instance')
        if keypoint_flag:
            json_data.setdefault('annType',[]).append('keypoint')
        if caption_flag:
            json_data.setdefault('annType',[]).append('caption')
        json_data.setdefault('annType',None)

        if annotations:
            json_data['annotations'] = annotations
        json_data['info'] = instances_train2014['info']

        jsonstr = json.dumps(json_data)
        ##------------------------------------------------------
        filepath = os.path.join(imgfolder,filename)
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
        with open('log_COCO.txt','a+') as f:
            f.write("train2014:{}|{}\n".format(sum_files, nums_img))

    # 2014 val
    pdb.set_trace()
    imgfolder = os.path.join(imgroot,'val2014')
    sum_files = 0
    nums_img = len(instances_val2014['images'])
    for idx,image_item in enumerate(instances_val2014['images']):
        filename = image_item['file_name']
        image_id = image_item['id']      # 索引 其他存在的 map（如标注，执照等）
        
        ## 获得 jsonstr 属性;

        # form JSON data and write it to a file
        json_data = dict()
        json_data['image'] = extract_metadata_imagetest(image_item)

        instance_flag,keypoint_flag,caption_flag,annotations = extract_metadata_ann(image_id)
        # 提取所有的categories 类别，唯一性；
        func = lambda x,y:x if y in x else x + [y]
        if annotations.get('instances') and 'categories' in annotations.get('instances').keys():
            tag=reduce(func,[[],]+annotations.get('instances')['categories'])
        else:
            tag = None
        json_data['tag'] = tag

        # 标识 有哪些标注信息，放在同 images 一级;
        if instance_flag:
            json_data.setdefault('annType',[]).append('instance')
        if keypoint_flag:
            json_data.setdefault('annType',[]).append('keypoint')
        if caption_flag:
            json_data.setdefault('annType',[]).append('caption')
        json_data.setdefault('annType',None)

        if annotations:
            json_data['annotations'] = annotations
        json_data['info'] = instances_train2014['info']

        jsonstr = json.dumps(json_data)
        ##------------------------------------------------------
        filepath = os.path.join(imgfolder,filename)
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
        with open('log_COCO.txt','a+') as f:
            f.write("train2014:{}|{}\n".format(sum_files, nums_img))    

    # 2014 test
    pdb.set_trace()
    imgfolder = os.path.join(imgroot,'test2014')
    sum_files = 0
    nums_img = len(image_info_test2014['images'])
    for idx,image_item in enumerate(image_info_test2014['images']):
        filename = image_item['file_name']
        image_id = image_item['id']      # 索引 其他存在的 map（如标注，执照等）
        
        ## 获得 jsonstr 属性;

        # form JSON data and write it to a file
        json_data = dict()
        json_data['image'] = extract_metadata_imagetest(image_item)

        jsonstr = json.dumps(json_data)
        #jsonstr = None
        ##------------------------------------------------------
        filepath = os.path.join(imgfolder,filename)
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
        with open('log_COCO.txt','a+') as f:
            f.write("train2014:{}|{}\n".format(sum_files, nums_img)) 
    '''  
    # 2015 test
    pdb.set_trace()
    imgfolder = os.path.join(imgroot,'test2015')
    sum_files = 0
    nums_img = len(image_info_test2015['images'])
    for idx,image_item in enumerate(image_info_test2015['images']):
        filename = image_item['file_name']
        image_id = image_item['id']      # 索引 其他存在的 map（如标注，执照等）
        
        ## 获得 jsonstr 属性;

        # form JSON data and write it to a file
        json_data = dict()
        json_data['image'] = extract_metadata_imagetest(image_item)

        jsonstr = json.dumps(json_data)
        ##------------------------------------------------------
        filepath = os.path.join(imgfolder,filename)
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
        with open('log_COCO.txt','a+') as f:
            f.write("train2014:{}|{}\n".format(sum_files, nums_img))   

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
    pdb.set_trace()

    d1 = extract_info(filepath1)                        # 从图像中提取信息，保存到字典d1中;
   
    srcDataset = 'ImageNet'

    info1 = get_info(d1.get('size'))                    # 从字典 d1 中提取图像尺寸信息;
    pdb.set_trace()
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
def testcode():
    #test_xml_jsonstr()                 # 测试代码 xml 转化为 json 字符串;
    #test_insertdata()                  # 测试代码 向数据库插入数据;
    manipulate_from_folders()           # 操作文件夹;

def main():
    instance_idAnn_Map = {}
    
    cap_idAnn_Map = {}

    keypoints_idAnn_Map = {}

    categories_map = {}

    liences_map = {}
    testcode()

if __name__ == '__main__':
    main()