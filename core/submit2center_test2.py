# -*- coding: utf-8 -*-
# @Author: Lishi
# @Date:   2017-07-24 16:24:50
# @Last Modified by:   Lishi
# @Last Modified time: 2018-06-13 21:52:30
''''PostgreSQL至少有三个python接口程序可以实现访问，包括PsyCopg|PyPgSQL|PyGreSQL(PoPy已经整合在PyGreSQL中)，'''
import psycopg2
from psycopg2 import sql
import pdb
import json
import os,os.path


def options(x):
    return{'a':1,'b':2,}[x]

def connection(db='osdba', usr='postgres', pwd='vrlabh1109', target ='127.0.0.1' ):
    #return conn=psycopg2.connect(database = db, user=usr,password=pwd, host=target, port = '5432')
    return psycopg2.connect(database = 'osdba', user='postgres', password='vrlabh1109', host='127.0.0.1', port = '5432')
def insertdata(sqlquery,values):
    conn = connection()
    cur = conn.cursor()
    flag = False
    try:
        #pdb.set_trace()
        cur.execute(sqlquery,values)
        #cur.execute(sqlquery)
        #cur.execute('INSERT INTO image_info VALUES (%s) ', ("bar",)) # must always be a %s
        #cur.execute('INSERT INTO image_info VALUES (%s) ', ["bar"])
        conn.commit()
        flag = True
        #print ('Congratulation!!! insert the data to the dataset sucessed!!')
    except Exception,e:
        conn.rollback()
        print e
    finally:
        cur.close()
        conn.close()
        return flag

def insertbatch(sqlblock):
    '''sqlblock:list'''
    # cursor.execute("insert into people values (%s, %s)", (who, age))
    # curosr.executemany(sql, seq_of_parameters)
    conn = connection()
    cur = conn.cursor()
    flag = False
    try:
        for sqlquery in sqlblock:
            cur.execute(sqlquery)
        conn.commit()
        print ('insert the data to the dataset sucessed!!')
        flag = True
    except Exception, e:
        conn.rollback() # 回滚任何更改数据库
        print e
    finally:
        cur.close()
        conn.close()    # don't auto-commit
        return flag

#def formsql(srcDataset, srcImgTitle, srcImgExt,srcAnn,dstImgTitle,dstImgExt,width,height,channel,id = None):
def formsql():
    '''generate the sqlquery template,that's the first half part of the cursor.execute(sql,(,)), that is the sql '''
    #my_table = 'image_info'
    my_table = 'test2'#入库的表名
    t0 = sql.Identifier(my_table)
    names = ['srcDataset', 'srcImageTitle', 'srcImageExt','srcAnn','dstImageTitle', 'dstImageExt', 'width', 'height', 'channel','mode']
    #values = [srcDataset, srcImgTitle, srcImgExt,srcAnn,dstImgTitle, dstImgExt, width, height, channel]

    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(t0, sql.SQL(',').join(map(sql.Identifier, names)), sql.SQL(',').join(sql.Placeholder() * len(names) ) )
    #query = sql.SQL("INSERT INTO {0} ({1}) VALUES ({2})").format(t0, sql.SQL(',').join(map(sql.Identifier, names)), sql.SQL(',').join(sql.Placeholder() * len(names) ) )
    return query
    #print (query.as_string(conn))
    #>>> insert into table ("foo", "bar", "baz") values (%s, %s, %s)
    #query = sql.SQL("INSERT INTO {} ({}) VALUES ({})".format(t0, sql.SQL(',').join(map(sql.Identifier, names) ), sql.SQL(',').join(map(sql.Placeholder, names)) )
    #print (query.as_string(conn))
    #>>>insert into table ("foo", "bar", "baz") values (%(foo)s, %(bar)s, %(baz)s)

def createTable():
    conn = connection()
    cur = conn.cursor()
    sqlquery = 'create table imageinfo (id serial primary key not null, "srcDataset" varchar, "srcImgTitle" varchar, "srcImgExt" varchar, "srcAnn" json, "dstImgTitle" varchar, "dstImgExt" varchar,width smallint, height smallint, channel smallint,mode varchar);'
    anns=cur.execute(sqlquery)
    print anns
    conn.commit()
    cur.close()
    conn.close()

def main():
    '''test the module'''
    #createTable()
    srcDataset='imagenet'
    srcImgTitle='ssss'
    srcImgExt='jpg'
    srcAnn1={"annotation": {"segmented": "0", "object": {"bndbox": {"xmin": "614", "ymin": "388", "ymax": "1374", "xmax": "1871"}}},"label":"puppy"}
    srcAnn = '{"annotation": {"segmented": "1", "object": [{"bndbox": {"xmin": "123", "ymin": "115", "ymax": "275", "xmax": "379"}, "difficult": "0", "pose": "Unspecified", "name": "dog", "truncated": "0"}, {"bndbox": {"xmin": "75", "ymin": "1", "ymax": "375", "xmax": "428"}, "difficult": "0", "pose": "Frontal", "name": "chair", "truncated": "1"}], "filename": "2007_000063.jpg", "source": {"image": "flickr", "annotation": "PASCAL VOC2007", "database": "The VOC2007 Database"}, "folder": "VOC2012", "size": {"width": "500", "depth": "3", "height": "375"}}, "label": "puppy"}'
    dstImgTitle='sssswe'
    dstImgExt='png'
    width=1
    height=2
    channel=3
    mode = 'RGB'
    #pdb.set_trace()
    query = formsql()
    values = [srcDataset, srcImgTitle, srcImgExt,srcAnn,dstImgTitle, dstImgExt, width, height, channel, mode]
    insertdata(query,values)


if __name__ == '__main__':
    main()