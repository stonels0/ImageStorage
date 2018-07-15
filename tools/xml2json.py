# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-07-25 19:10:40
# @Last Modified by:   anchen
# @Last Modified time: 2017-07-25 21:43:56
# xml 转 json
# xml2json.py
# Version 1.0

from xml.parsers.expat import ParserCreate
import json
import pdb
import sys

# configure the default encoding;
#reload(sys)
#sys.setdefaultencoding('utf-8')

class Xml2Json:
    ''' multiple labels will form array'''
    LIST_TAGS = ['COMMANDS']

    def __init__(self, data = None):
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.result = None
        if data:
            self.feed(data)
            self.close()

    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        assert attrs == {}
        assert self._data.strip() == ''
        self._stack.append([tag])
        self._data = ''

    def end(self, tag):
        last_tag = self._stack.pop()
        assert last_tag[0] == tag
        if len(last_tag) == 1: #leaf
            data = self._data
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_tag[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if type(el) is not list:
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else: #force into a list
                data = [{k:v} for k, v in last_tag[1:]]
        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self.result = {tag:data}
        self._data = ''

    def data(self, data):
        self._data = data

if __name__ == '__main__':
    xml = open('E:/DataSet_Download/ImageNet/Annotation/Annotation/n01322604/n01322604_3.xml', 'r').read()
    result = Xml2Json(xml).result;
    print type(result) # dict
    jsonstr = json.dumps(result)
    print jsonstr,'\n',type(jsonstr)
    outputfile = open("E:/DataSet_Download/ImageNet/Annotation/Annotation/n01322604/n01322604_3.json", 'w')
    outputfile.write(str(result))
    outputfile.close()

#作者：华天清
#链接：http://www.jianshu.com/p/f21fb92a2b66
#來源：简书
# 当对str 进行编码（encoding）时，会先用默认编码将自己解码为 unicode，然后将unicode编码为你指定编码；
#  s.encode("utf-8") 等价于 s.decode(defaultencoding).encode("utf-8")
# 引出了python2.x中在处理中文时，大多数出现错误的原因所在：python的默认编码，defaultencoding是ascii