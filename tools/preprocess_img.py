# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-26 18:51:18
# @Last Modified by:   anchen
# @Last Modified time: 2017-07-26 19:30:54

from PIL import Image
import urllib2
from StringIO import StringIO
import os

# covert the colorspace to RGB
def convert2RGB(impath):
    try:
        img = Image.open(impath)
        #if img.mode == 'CMYK':
        img = img.convert('RGB')
        filepath,filename = os.path.split(impath)
        filename = '1_'+filename
        impath = os.path.join(filepath,filename)
        img.save(impath)
    except Exception, e:
        raise e

# change the size of image:
def resize_img(img_path):
    try:
        img = Image.open(img_path)
        (width, height) = img.size
        new_width = 200
        new_height = height * new_width / width
        out = img.resize((new_width,new_height), Image.ANTIALIAS)
        ext = os.path.splitext(img_path)[1]
        new_file_name = '%s%s' %('small',ext)
        out.save(new_file_name,quality = 95)
    except Exception, e:
        raise e

# change the format of Image
def change_img_type(img_path):
    try:
        img = Image.open(img_path)
        img.save('new_type.png')
    except Exception, e:
        raise e

# deal with the remote image;
def handle_remote_img(img_url):
    try:
        request = urllib2.Request(img_url)
        img_data = urllib2.urlopen(request).read()
        img_buffer = StringIO(img_data)
        img = Image.open(img_buffer)
        img.save('remot.jpg')
        (width, height) = img.size
        out = img.resize((200, height * 200/width), Image.ANTIALIAS)
        out.save('remote_small.jpg')
    except Exception, e:
        raise e

if __name__ == '__main__':
    #img_path = 'test.jpg'
    #resize_img(img_path)
    #change_img_type(img_path)
    img_url = 'http://img.hb.aicdn.com/042f8a4a70239f724ff7b9fa0fc8edf18658f41022ada-WcItWE_fw554'
    handle_remote_img(img_url)

'''
獲得驗證碼的步驟：（2,3步驟中，實數多餘）
step1.獲得網絡圖片
step2.寫入文件到硬盤
step3.使用PIL讀取硬盤中的文件
step4.PIL對文件進行處理
step5.進行文本識別
limit：
PIL的Image.open() 只接受函數名；
Image.fromstring()  只接受像素格式的字符串，不接受圖片文件

example1：
from PIL import Image
import urllib
url = 'http://202.119.81.113:8080/verifycode.servlet'  # 验证码URL
r = urllib.urlopen(url)
f = open('VCode.jpg', 'wb')    #这里是将验证码图片写入到本地文件
f.write(r.read())
f.close()
img = Image.open('VCode.jpg')  # PIL库加载图片

example2：
利用StringIO库(Python:StringIO模块)，将网络图片写入到内存（实际网络图片这是也已经在内存），然后“伪装”成普通文件传给Image.open()：
from PIL import Image
import urllib
import StringIO
url = 'http://202.119.81.113:8080/verifycode.servlet'  # 验证码URL
r = urllib.urlopen(url)
imgBuf = StringIO.StringIO(r.read())
img = Image.open(imgBuf)
'''