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
    cursor.execute('''select videofilename from download_log where isdelete is null  ORDER BY downloaddate asc LIMIT 0,15''')
    delList=cursor.fetchall()
    for i in delList:
      print 'delete '+str(i[0])
      os.system('rm -rf /www/wwwroot/youtube.club/upload/videosource/'+str(i[0]))
      cursor.execute('update download_log set isDelete="1" where videofilename="'+str(i[0])+'"')
      db.commit()

if isCanDownload()==False:
    randomDelete()

