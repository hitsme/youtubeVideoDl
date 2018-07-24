#!/usr/bin/python
#-*- coding: utf-8 -*-
from CheckFreeSpace import disk_usage
from DBDao import getConnectDB
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def isCanDownload():
    if disk_usage('./')[3]<=92:
        return True
    else:
        return False

def randomDelete():
    print 'starting random delete videosource'
    db=getConnectDB()
    cursor=db.cursor()
    cursor.execute('''select DISTINCT fornumid from download_log''')
    fidList=cursor.fetchall();
    for j in fidList:
     cursor.execute('''select videofilename from download_log where fornumid="%s" and isdelete is null  ORDER BY downloaddate asc LIMIT 0,2'''%j[0])
     delList=cursor.fetchall()
     for i in delList:
      print 'delete '+str(i[0])
      try:
        os.remove(str(i[0]))
      except:
          print '文件不存在！'
      cursor.execute('update download_log set isDelete="1" where videofilename="'+str(i[0])+'"')
      db.commit()

def isNewDirPath(fornumid):
    if os.path.exists('/www/wwwroot/youtube.club/upload/videosource/'+fornumid):
        return
    else:
        os.mkdir('/www/wwwroot/youtube.club/upload/videosource/'+fornumid)
        return


