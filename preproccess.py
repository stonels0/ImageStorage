#coding=utf-8

from PIL import Image
import os,os.path
import pdb

def convert2RGB(impath):
    img = Image.open(impath)
    if img.mode == 'CMYK':
        img = img.convert('RGB')
        filepath,filename = os.path.split(impath)
        filename = '1_'+filename
        impath = os.path.join(filepath,filename)
        img.save(impath)
    return impath

def main():
    impath = 'E:/Lishi/EditProgram/caffe-master/matlab/extractor_dataset/n00005787_10793.jpeg'
    impath1 = convert2RGB(impath)
    

if __name__ == '__main__':
    main()