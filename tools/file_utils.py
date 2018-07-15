# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-07-24 16:28:07
# @Last Modified by:   Lishi
# @Last Modified time: 2018-02-23 14:12:06

import os,os.path
import sys
import hashlib
import shutil
from glob import glob
from PIL import Image
#from delivery import *
'''文件的相关操作'''


def getAllFiles(dirpath,endings):
    '''
        Get all specifical format files into a list.

        Inputs:
        - dirpath: the file path;
        - extension: the format of file lists ;
    '''
    def fetchFiles(dirpath,extension):
        """
        Get all extension files into a list.
        Inputs:
        - dirpath: the file path;
        - extension: the format of file ;
        """
    return glob(os.path.join(dirpath,('*'+extension)))
    

    if endings is None: endings=['.jpg','.png','.bmp','.jpeg']
    files = []
    for ext in endings:
        files.extend(fetchFiles(dirpath,ext))
    return files


def deal_file(filepath,desDir,hashID=None, num = 2):
    # filepath: E:\Lishi\n00005787_10793.JPEG
    # desDir: E:\Lishi\test
    if hashID is None:
        hashID = sha256(filepath)
    strSplit = split_str(hashID, num)
    dstfolder = os.path.join(desDir, strSplit[0], strSplit[1]) # destination folder,按照sha256两级目录存放;
    if not os.path.exists(dstfolder):
        os.makedirs(dstfolder)                                 # 不同于os.mkdir()
    checkformat(filepath,dstfolder)

def deal_files(filelist,desDir,hashlistID = None,num = 2):
    '''
    target: move list file to the destination folders;
    filelist: ['E:\Lishi\n00005787_10793.JPEG','E:\Lishi\n00005787_10793.JPEG'...]
    desDir: 'E:\Lishi\test'
    hashlistID:['FADC...','FEACB...'...]
    '''

def normalize(filepath):
    '''function: image normalization'''
    # return source filesuffix and destination filesuffix;
    filename,ext = os.path.splitext(filepath)  # [E:\Lishi\n00005787_10793,jpg]

    srcext = ext[1:]
    tarext = ['jpg','png']
    suffix = ['JPEG','JPG']
    if srcext.upper() in suffix:
        tarext = 'jpg'
        filename = filename + '.' + tarext
        #os.rename(filepath,filename)
    elif srcext.upper() == 'PNG':
        tarext = 'png'
        filename = filename + '.' +tarext
        #os.rename(filepath,filename)
    else:
        tarext = 'jpg'
        #dstfile = filename + '.' + tarext
        #Image.open(filepath).save(dstfile)

    return srcext,tarext    

def normalize_move(filepath,despath):
    ''' make the uniform format'''
    # rule1: upper case ===> lower case
    # rule2: JPEG ===> usually format,jpg
    # rule3:  common patterns: jpg, png
    '''
    example:
    filepath: E:\Lishi\n00005787_10793.JPEG;the name of file,that has not the suffix but contain the path;
    ext : '.jpg','.png'
    '''
    filename,ext = os.path.splitext(filepath)  # E:\Lishi\n00005787_10793
    folder,name = os.path.split(filename)     # n00005787_10793.JPEG

    srcext = ext[1:]
    movForm = ['jpg','png']
    JPEG = [m+n+z+y for m in 'Jj' for n in 'Pp' for z in 'Ee' for y in 'Gg']
    JPG = [m+n+z for m in 'Jj' for n in 'Pp' for z in 'Gg']
    PNG = [m+n+z for m in 'Pp' for n in 'Nn' for z in 'Gg']
    JPG.extend(JPEG)
    JPG.extend(PNG)
    if srcext in movForm:
        movefile(filepath,despath)
        dstext = srcext
    elif srcext in JPG:        # ["JPEg",'Jpg','PnG'], rename format;
        if srcext in JPEG:     # ["JPEg",]
            filename = filename + '.jpg'
            dstext = 'jpg'
        else:       # ['Jpg','PnG',]
            dstext = srcext.lower()
            filename = filename + '.' + dstext
        
        os.rename(filepath,filename)
        movefile(filename,despath)
    else:       # modify the image format;
        baseName = name.split('.')[0] + '.jpg'
        dstext = 'jpg'
        dstfile = os.path.join(despath,baseName)
        try:
            Image.open(filepath).save(dstfile)
        except IOError:
            print ("canot convert infile!")
        os.remove(filepath) # remove/delete the original file;
    try:
        os.rmdir(folder) # can only remove the null folder or throw exception,that contains the null and has files' folder;
    except:
        pass
    finally:
        return srcext,dstext

def movefile(filepath,despath):
    '''filepath:E:/Lishi/n00005787_10793.JPEG;despath:E:/Lishi/testimage
    shutil.move([1],[2]):[2]must be folder
    '''
    # path ignore the case letter;make sure the legal input;
    flag = False
    assert os.path.isdir(despath) and os.path.isfile(filepath)
    dectfile = os.path.join(despath,os.path.basename(filepath))
    if not os.path.exists(dectfile):
        try:
            shutil.move(filepath,despath)
            flag = True
        except:
            flag = False
        
        # shutil.copy(filepath,despath)
        # 备注：copy：第二个参数目的文件夹或者文件都可以
        #       copyfile：第二个只能是文件；
        #shutil.move(filepath,despath)
    return flag

def split_str(s, n):
    ''' Genarator the file path , default two level;2个字符为一级目录'''
    length = len(s)
    return [ s[i:i+n] for i in range(0, length, n) ]

def cmp_ignore_case(s1,s2):
    u1 = s1.upper()
    u2 = s2.upper()
    if u1 == u2:
        return True
    else:
        return False

def sha256(filename):
    '''Computes the SHA-256 checksum of a file. Returns the hex digest.'''
    m = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if data:
                m.update(data)
            else:
                break
    return m.hexdigest()


def getfilepathlist_recursion(filepath,filelist=None):
    if filelist is None:
        filelist = []
    for root, dirs, files in os.walk(filepath):     # don't contain the full path;
        print 'the root dir is : ',root
        if len(files):
            files = [os.path.join(root,_) for _ in files]
            filelist.extend(files)
    return filelist

def getfolderlist_current(filepath):
    return [_ for _ in os.listdir(filepath) if os.path.isdir(os.path.join(filepath,_))]

def fetchFiles(dirpath,extension):
    return glob(os.path.join(dirpath,('*'+extension)));

def getAllImgs(dirpath):
    endings = ['.png','.jpg','.bmp','.jpeg']
    images = []
    for ext in endings:
        images.extend(fetchFiles(dirpath,ext))
    return images

def main():
    '''
    the test for folder's images
    sourceDir = 'E:\\Lishi\\Datasets\\DataSets_release\\MS_COCO'
    desDir = 'E:\\Lishi\\Datasets\\1-Image'

    deal_fileFolder(sourceDir,desDir)
    '''
    sourceDir = 'E:\\Lishi\\testimage\\test'
    desDir = 'E:\\Lishi\\sss'
    if not os.path.exists(desDir):
        os.makedirs(desDir)

    filelist=os.listdir(sourceDir)
    filepaths = [os.path.join(sourceDir,filename) for filename in filelist]
    for i in xrange(len(filepaths)):
        normalize_move(filepaths[i],desDir)

    #os.system('pause')
    #filelist = getFilelist_recursion(sourceDir)
    #print len(filelist)
    #print getFilelist_current(sourceDir)
    #desDir = ''


if __name__ == '__main__':
    main()

