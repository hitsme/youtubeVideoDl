#!usr/bin/python
#-*- coding:UTF-8 -*-
import MySQLdb
def getConnectDB():
    db=MySQLdb.connect('127.0.0.1','root','a3a7bb21f6b34339','youtubeclub',charset='utf8')
    return db
def initDownloadLog():
    db=getConnectDB()
    cursor=db.cursor()
    createSql="""create table if not exists download_log(videotitle TEXT,videofilename Text,downloaddate datetime,isDelete char(5))
    """
    cursor.execute(createSql)
    db.commit()
    db.close()
    return

def initScrapyRecord():
    db=getConnectDB()
    cursor=db.cursor()
    initSql="""create table if not exists Scrapy_Record(scrapyUrl TEXT,fornumname varchar(500)
,isEnable char(5))"""
    cursor.execute(initSql)
    db.commit()
    db.close()
    return