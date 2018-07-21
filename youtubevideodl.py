#!/usr/bin/python
# #-*-coding:utf-8-*-
from pytube import YouTube
import urllib2
import re
import sys
from bs4 import BeautifulSoup
from DBDao import getConnectDB
from DBDao import initScrapyRecord
from DBDao import initDownloadLog
import datetime
import time
import uuid
from getNetworkIp import getNetWorkIp
import traceback
from youtubeDLTools import isCanDownload
from youtubeDLTools import randomDelete
from youtubeDLTools import isNewDirPath
reload(sys)
sys.setdefaultencoding("utf-8")
class initParam:
    'init params class'
    def __init__(self,channelUrl,fornumname):
        self.channelUrl=channelUrl
        self.fornumname=fornumname
def getContent(videotitle,fornumid):
    #缤纷花食，悄悄挖掘玫瑰的不同吃法[mp4]http://45.62.226.188/缤纷花食，悄悄挖掘玫瑰的不同吃法.mp4[/mp4]
    return str(videotitle)+"[mp4]http://"+getNetWorkIp()+'/videosource/'+str(fornumid)+'/'+str(videotitle)+'.mp4[/mp4]'
def getTid(cursor):
    cursor.execute('select tid from pre_forum_post order by tid desc limit 0,1')
    return cursor.fetchone()[0]

def getFid(cursor,fornumname):
    try:
        cursor.execute('select fid from pre_forum_forum where name="'+fornumname+'"')
        fid=cursor.fetchone()[0]
        return fid
    except:
        print 'function getFid() error'
def publishWebsite(fornumname,videotitle):
    db=getConnectDB()
    cursor=db.cursor()
    try:
      cursor.execute('select pid from pre_forum_post order by pid desc limit 0,1')
      lastPid=cursor.fetchone()[0]
      lastPid+=1
      print lastPid
      fid=getFid(cursor,fornumname)
      tid=getTid(cursor)
      tid+=1
      timeminute=time.time()
      cursor.execute("""insert into pre_forum_post(pid, fid, tid,first, author,
                                                  authorid,subject,dateline,message,useip,
                                                  port,invisible,anonymous,usesig,htmlon,
                                                  bbcodeoff,smileyoff,parseurloff,attachment,rate,
                                                  ratetimes,position) 
                                                  values("%s","%s","%s","%s","%s",
                                                         "%s","%s","%s","%s","%s",
                                                         "%s","%s","%s","%s","%s",
                                                         "%s","%s","%s","%s","%s",
                                                         "%s","%s")"""
                                                  %(lastPid,fid,tid,'1','admin',
                                                    '1',videotitle,str(timeminute),getContent(videotitle,fid),'127.0.0.1',
                                                    '740','0','0','1','0',
                                                    '0','-1','0','0','0',
                                                    '0','1'))
      cursor.execute("""insert into  pre_forum_thread(tid,fid,posttableid,typeid,sortid,readperm,price,author,authorid,subject,dateline, lastpost,lastposter,views,replies,displayorder,highlight,digest,rate,special,attachment,moderated,closed,stickreply,recommends,recommend_add,recommend_sub,heats,status,isgroup,favtimes,sharetimes,stamp,icon,pushedaid,cover,replycredit) 
VALUES("%s" ,"%s", 0, 0, 0, 0, 0, 'admin', 1, "%s","%s", "%s", "admin", 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,32, 0, 0, 0, -1, -1, 0, 0, 0)"""%(tid,fid,videotitle,str(timeminute),str(timeminute)))
      cursor.execute("""insert into pre_forum_post_tableid(pid) values("%s")"""%(lastPid))
      #"UPDATE `pre_forum_forum` SET threads=threads+1, posts=posts+1,todayposts=todayposts+1 ,lastpost='" + currentPId + " " + rss.getTitle() + " " + time + " 狂飙蜗牛" + "' WHERE fid=" + fid;
      cursor.execute('UPDATE pre_forum_forum SET threads=threads+1, posts=posts+1,todayposts=todayposts+1 ,lastpost="' + str(lastPid) + ' ' + videotitle + ' ' +str(timeminute) + ' admin' + '" WHERE fid=' + str(fid))
      db.commit()
    except Exception, e:
      print 'str(Exception):\t', str(Exception)
      print 'str(e):\t\t', str(e)
      print 'repr(e):\t', repr(e)
      print 'e.message:\t', e.message
      print 'traceback.print_exc():';
      traceback.print_exc()
      print 'traceback.format_exc():\n%s' % traceback.format_exc()
      print 'function publishWebsite error'
    finally:
        db.close()
    return

def writeDownloadLog(fornumid,fornumname,videotitle):
    db=getConnectDB()
    cursor=db.cursor()
    videoid=str(uuid.uuid1())
    try:
        dldate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print """insert into download_log(videoid,videotitle,videofilename,fornumname,fornumid,downloaddate)
 values("%s","%s","%s","%s","%s","%s")"""%(videoid,videotitle,'/www/wwwroot/youtube.club/upload/videosource/'+str(fornumid)+'/'+videotitle+'.mp4',fornumname,fornumid,str(dldate))
        cursor.execute("""insert into download_log(videoid,videotitle,videofilename,fornumname,fornumid,downloaddate)
 values("%s","%s","%s","%s","%s","%s")"""%(videoid,videotitle,'/www/wwwroot/youtube.club/upload/videosource/'+str(fornumid)+'/'+videotitle+'.mp4',fornumname,fornumid,str(dldate)))

        db.commit()
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        print 'traceback.print_exc():';
        traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        print 'function write download_log error'
    finally:
        db.close()
    return
def selectVideoResToDL(videoUrl,videotitle,fornumname):
    #init table Download_log
    print 'Download starting'
    if isCanDownload()==False:
        randomDelete()
        print 'hello---------------------------'
    #initDownloadLog()
    db=getConnectDB()
    cursor=db.cursor()
    cursor.execute('select count(*) from download_log where videotitle="'+videotitle+'"')
    count=cursor.fetchone()[0]
    if count==0:
        isNewDirPath(str(getFid(cursor,fornumname)))
        yt720p = YouTube(videoUrl).streams.filter(res='720p')
        if yt720p.first() != None:
            print videotitle+".mp4(720p) download starting"

            yt720p.first().download(output_path='/www/wwwroot/youtube.club/upload/videosource/'+str(getFid(cursor,fornumname)))
            writeDownloadLog(getFid(cursor,fornumname),fornumname,videotitle)
            #push website
            publishWebsite(fornumname,videotitle)
            # push website end
        else:
            yt360p = YouTube(videoUrl).streams.filter(res='360p')
            if yt360p.first() != None:
                print videotitle + ".mp4(360p) download starting"
                yt360p.first().download(output_path='/www/wwwroot/youtube.club/upload/videosource/'+str(getFid(cursor,fornumname)))
                writeDownloadLog(getFid(cursor, fornumname), fornumname, videotitle)
                # push website
                publishWebsite(fornumname, videotitle)
                # push website end
            else:
                yt240p = YouTube(videoUrl).streams.filter(res='240p')
                if (yt240p != None):
                    print videotitle + ".mp4(360p) download starting"
                    yt240p.first().download(output_path='/www/wwwroot/youtube.club/upload/videosource/'+str(getFid(cursor,fornumname)))
                    writeDownloadLog(getFid(cursor, fornumname), fornumname, videotitle)
                    # push website
                    publishWebsite(fornumname, videotitle)
                    # push website end
                else:
                    yt144p = YouTube(videoUrl).streams.filter(res='144p')
                    if yt144p != None:
                        print videotitle + ".mp4(144p) download starting"
                        yt144p.first().download(output_path='/www/wwwroot/youtube.club/upload/videosource/'+str(getFid(cursor,fornumname)))
                        writeDownloadLog(getFid(cursor, fornumname), fornumname, videotitle)
                        # push website
                        publishWebsite(fornumname, videotitle)
                        # push website end
    db.close()
    return
#pl = Playlist("https://www.youtube.com/watch?v=pkGU-g3WFR8&list=PLaO-FUd5lsPVQxhdUTGCVYWjJO2lfi_tw")
#pl.download_all()
#YouTube('https://youtu.be/9bZkp7q19f0').streams.first().download(output_path='/www/wwwroot/youtube.club/upload/videosource/'+getFid(cursor,fornumname))
#initDownloadLog()
#initScrapyRecord()
db=getConnectDB()
cursor=db.cursor()
cursor.execute("""select scrapyUrl,fornumname from Scrapy_Record where isEnable='1'""")
scrapyRcdlst=cursor.fetchall()
for scrapyRcd in scrapyRcdlst:
    #"https://www.youtube.com/channel/UCoC47do520os_4DBMEFGg4A/videos"
    print str(scrapyRcd[0])
    reponse = urllib2.urlopen(str(scrapyRcd[0]))
    htmlstr = reponse.read()
    soup = BeautifulSoup(htmlstr, 'lxml')
    # print soup.prettify()
    # print soup.children.next()
    for i in soup.find_all(href=re.compile("watch"),
                           class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"):
        #print i
        hrefvalue = re.findall(r'href="(.*?)" rel="nofollow" title="(.*?)"', str(i), re.I)
        #print hrefvalue[0][1]
        # yt=YouTube(hrefvalue[0]).streams.filter(res='1080p',audio_codec='mp4a.40.2')
        # yt = YouTube(hrefvalue[0]).streams.filter(res='720p')
        # begin download
        #fornumname='李子柒'
        selectVideoResToDL(str(hrefvalue[0][0]), str(hrefvalue[0][1]), scrapyRcd[1])
    print 'download end'

#print soup.find_all(href=re.compile("watch"),class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").__len__()
#for i in soup.children:
   # print i
#print htmlstr
#<a class="yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2" dir="ltr" title="吃法一抓一大把，浸润夏天的沁凉果味——百香果"  aria-describedby="description-id-25655" data-sessionlink="ei=GbY5W7GZEYKrgQPoqJ2wCw&amp;feature=c4-videos-u&amp;ved=CFIQlx4iEwjxie3W1f_bAhWCVWAKHWhUB7Yomxw" href="/watch?v=xYmyNCzoCFI" rel="nofollow">吃法一抓一大把，浸润夏天的沁凉果味——百香果</a>
#VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', htmlstr,re.I)
#print reponse.read().decode('utf-8')
#yt=YouTube('https://www.youtube.com/watch?v=zXAqw0Vzr4w').streams.filter(res='1080p',su)
#yt.first().download(output_path='/www/wwwroot/youtube.club/upload/videosource/'+getFid(cursor,fornumname))
#yt = YouTube('https://www.youtube.com/watch?v=zXAqw0Vzr4w')
#yt.streams.all
# or if you want to download in a specific directory
#pl.download_all('/path/to/directory/')
