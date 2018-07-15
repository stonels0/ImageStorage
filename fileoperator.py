# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-04 19:25:23
# @Last Modified by:   anchen
# @Last Modified time: 2017-07-04 23:36:28
import os,os.path
import sys
import hashlib
import shutil
from PIL import Image

def deal_file(filepath,desDir,hashID=None, num = 2):
    # filepath: E:\Lishi\n00005787_10793.JPEG
    # desDir: E:\Lishi\test
    if hashID is None:
        hashID = sha256(filepath)
    strSplit = split_str(hashID,num)
    dstpath = os.path.join(desDir,strSplit[0],strSplit[1]) # destination folder;
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    checkformat(filepath,dstpath)

def deal_files(filelist,desDir,hashlistID = None,num = 2):
    '''
    target: move list file to the destination folders;
    filelist: ['E:\Lishi\n00005787_10793.JPEG','E:\Lishi\n00005787_10793.JPEG'...]
    desDir: 'E:\Lishi\test'
    hashlistID:['FADC...','FEACB...'...]
    '''

def checkformat(filepath,despath):
    '''
    filepath: E:\Lishi\n00005787_10793.JPEG;the name of file,that has not the suffix but contain the path;
    ext : '.jpg','.png'
    '''
    filename,ext = os.path.splitext(filepath)  # E:\Lishi\n00005787_10793
    name = os.path.basename(filepath) # n00005787_10793.JPEG
    folder = os.path.dirname(filepath)
    ext = ext[1:]
    movForm = ['jpg','png']
    JPEG = [m+n+z+y for m in 'Jj' for n in 'Pp' for z in 'Ee' for y in 'Gg']
    JPG = [m+n+z for m in 'Jj' for n in 'Pp' for z in 'Gg']
    PNG = [m+n+z for m in 'Pp' for n in 'Nn' for z in 'Gg']
    JPG.extend(JPEG)
    JPG.extend(PNG)
    if ext in movForm:
        movefile(filepath,despath)
    elif ext in JPG:
        if ext in JPEG:
            filename = filename + '.jpg'
        else:
            ext = '.'+ ext.lower()
            filename = filename + ext
        os.rename(filepath,filename)
        movefile(filename,despath)
    else:
        img = Image.open(filepath);
        baseName = name.split('.')[0] + '.jpg'
        dstfile = os.path.join(despath,baseName)
        img.save(dstfile)
        os.remove(filepath) # remove the original file;
    try:
        os.rmdir(folder) # can only remove the null folder;
    except:
        return
    else:
        pass

    
    #!!!!shutil.rmtree(folder) # !!! remove all the folder,that contains the null and has files' folder;
    return

def movefile(filepath,despath):
    '''
    filepath:E:\Lishi\n00005787_10793.JPEG;
    despath:E:\Lishi\testimage
    shutil.move([1],[2]):[2]must be folder
    '''
    # path ignore the case letter;
    # make sure the legal input;
    if not os.path.isdir(despath) or not os.path.isfile(filepath):
        return False
    #if not os.path.exists(despath): # make sure the dest folder exist,outside the function;
        #os.makedirs(despath)
    dectfile = os.path.join(despath,os.path.basename(filepath))
    if not os.path.exists(dectfile):
        shutil.move(filepath,despath)
    '''
    dectfile = os.path.join(despath,os.path.basename(filename))
    if not os.path.exists(dectfile):# detect the files and folders
        shutil.move(filename,despath)
    '''
    return
    #return flag

def split_str(s, n):
    ''' Genarator the file path , default two level;
    '''
    length = len(s)
    return [ s[i:i+n] for i in range(0, length, n) ]

def sha256(filename):
    '''Computes the SHA-256 checksum of a file. Returns the hex digest.
    '''
    m = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if data:
                m.update(data)
            else:
                break
    return m.hexdigest()


def getFilelist_recursion(filepath,filelist=None):
    if filelist is None:
        filelist = []

    for root, dirs, files in os.walk(filepath):
        print 'the root dir is : ',root
        if len(files):
            filelist.extend(files)

    return filelist

def getFolderlist_current(filepath):
    return os.listdir(filepath)


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
        checkformat(filepaths[i],desDir)

    #os.system('pause')
    #filelist = getFilelist_recursion(sourceDir)
    #print len(filelist)
    #print getFilelist_current(sourceDir)
    #desDir = ''


if __name__ == '__main__':
    main()

