# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-07-28 14:07:30
# @Last Modified by:   anchen
# @Last Modified time: 2017-07-28 17:23:56

import os, ConfigParser, time
import hashlib
import shutil
from glob import glob
import pp
import pdb

def file_list_pp(job_server,task_zip):
    
    #task_zip = tuple(task_zip)
    number = len(task_zip)

    jobs = [(task,job_server.submit(move_file, (task,), (get_destfolder, ), ("os","os.path","shutil")) ) for task in task_zip]
    pdb.set_trace()
    #for item,job in jobs:
        #print 'the item is :{}'.format(item)
        #print ('the job is :{}'.format(job()))
    result = [items() for i,items in jobs]
    try:
        idx=result.index(False)
        with open('log_movefile.txt','a') as f:
            for i in xrange(len(idx)):
                f.write(jobs[i][0])
    except Exception as e:
        pass
    print ('the number of image move is :{}'.format(number))

def fetchFiles(dirpath,extension):
    return glob(os.path.join(dirpath,('*'+extension)));

def getAllImgs(dirpath):
    endings = ['.png','.jpg','.bmp','.jpeg']
    images = []
    for ext in endings:
        images.extend(fetchFiles(dirpath,ext))
    return images

def split_str(s, n=2):
    ''' Genarator the file path , default two level;'''
    length = len(s)
    return [ s[i:i+n] for i in range(0, length, n) ]

def get_destfolder(hashid,dst_dir='E:/Lishi/test/validation/test111'):
    split_hash = split_str(hashid, 2)
    destfolder = os.path.join(dst_dir, '{}/{}'.format(split_hash[0], split_hash[1]))
    #return destfolder
    return os.path.normpath(destfolder)

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

def move_file(item):
    oldfile_path = item[0]
    newfile_folder = item[1]
    flag = False
    filename = os.path.basename(oldfile_path)
    newfile_path = os.path.join(newfile_folder,filename)
    if not os.path.exists(newfile_folder):
        os.makedirs(newfile_folder)
    try:
        #os.rename(oldfile_path, newfile_path)
        shutil.move(oldfile_path,newfile_path)
        flag = True
    except Exception, e:
        pass
    finally:
        folder = os.path.dirname(oldfile_path)
        if not os.listdir(folder):
            os.rmdir(folder)
        return flag

def deal_file(filepath, folder_root):
    filename = os.path.basename(filepath)
    hashid = sha256(filepath)
    print hashid
    split_hash = split_str(hashid,2)
    dest_folder = os.path.join(folder_root,'{}/{}'.format(split_hash[0],split_hash[1]))
    move_file1(filepath, destfolder)

def move_file1(oldfile_path,newfile_folder):
    flag = False
    filename = os.path.basename(oldfile_path)
    newfile_path = os.path.join(newfile_folder,filename)
    if not os.path.exists(newfile_folder):
        os.makedirs(newfile_folder)
    try:
        os.rename(oldfile_path, newfile_path)
        flag = True
        os.rmdir(folder)
        #shutil.move(oldfile_path, newfile_path)
    except Exception, e:
        print e
    finally:
        return flag


def testcode():
    #file_name = file_openate()
    src_dir = 'E:/Lishi/test/validation/n00475403'
    dst_dir = 'E:/Lishi/test/validation/test111'

    pdb.set_trace()
    filelist = getAllImgs(src_dir) # must be filepath
    hashlist = map(sha256, filelist)
    dstfolder = map(get_destfolder, hashlist)
    task_zip = zip(filelist, dstfolder)           # task list;
    #task_zip = map(list,task_zip)

    start = time.time()
    ppservers = ()
    job_server = pp.Server(ppservers = ppservers)
    # ncpus = 4
    # job_server = pp.Server(ncpus,ppservers = ppservers)
    print "Starting pp with ", job_server.get_ncpus(), "workers"

    file_list_pp(job_server,task_zip) # test perfect!!

    # 测试未成功;
    #jobs = [(task, job_server.submit(deal_file, (task,dst_dir), (move_file1,sha256,split_str), ("os","os.path","shutil"))) for task in filelist]
    #print ('the number of image move is :{}'.format(number))    

    print ('the file hash id have over. the cost of time is:{}'.format(time.time() - start))




def main():
    testcode()

if __name__ == '__main__':
    main()



