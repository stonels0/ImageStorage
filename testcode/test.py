# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-25 10:49:10
# @Last Modified by:   anchen
# @Last Modified time: 2017-07-25 16:47:14
import os,os.path
import io
import sys
import _init_paths
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import pdb

#from tools import *
#gbkTypeStr = unicodeTypeStr.encode('GBK', 'ignore')
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码

def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    # has error!!encode!!
    try:
        pdb.set_trace()
        img = Image.open(fname)
        if hasattr(img,'_getexif'):
            if img._getexif():
                exif = { PIL.ExifTags.TAGS[k]:v for k,v in img._getexif().items() if k in PIL.ExifTags.TAGS}
                return exif
    except IOError:
        print ("IOError "+ fname)  
    return None              


def storage2database():
    filename = 'E:/FeiGe/results/pascal_car/111.jpg'
    exif = get_exif_data(filename)
    for k,v in exif.iteritems():
        #print u"exif[%s]="%k,str(v).decode('GBK','ignore').encode('utf-8')
        print u"exif[%d]="%k,v

    print type(exif)
    print exif.keys()
def main():
    storage2database()

if __name__ == '__main__':
    main()