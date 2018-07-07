#-*-coding:utf-8-*-
from pytube import Playlist
from pytube import YouTube
import urllib2
import re
from bs4 import BeautifulSoup
#pl = Playlist("https://www.youtube.com/watch?v=pkGU-g3WFR8&list=PLaO-FUd5lsPVQxhdUTGCVYWjJO2lfi_tw")
#pl.download_all()
#YouTube('https://youtu.be/9bZkp7q19f0').streams.first().download()
reponse=urllib2.urlopen("https://www.youtube.com/channel/UCoC47do520os_4DBMEFGg4A/videos")
htmlstr=reponse.read()
soup=BeautifulSoup(htmlstr,'lxml')
#print soup.prettify()
#print soup.children.next()
for i in soup.find_all(href=re.compile("watch"),class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"):
    #print i
    hrefvalue=re.findall(r'href="(.*?)"',str(i),re.I)
    print hrefvalue[0]
    yt=YouTube(hrefvalue[0]).streams.filter(res='1080p')
    yt.first().download()
print 'end1'
print soup.find_all(href=re.compile("watch"),class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").__len__()
#for i in soup.children:
   # print i
#print htmlstr
#<a class="yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2" dir="ltr" title="吃法一抓一大把，浸润夏天的沁凉果味——百香果"  aria-describedby="description-id-25655" data-sessionlink="ei=GbY5W7GZEYKrgQPoqJ2wCw&amp;feature=c4-videos-u&amp;ved=CFIQlx4iEwjxie3W1f_bAhWCVWAKHWhUB7Yomxw" href="/watch?v=xYmyNCzoCFI" rel="nofollow">吃法一抓一大把，浸润夏天的沁凉果味——百香果</a>
#VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', htmlstr,re.I)
#print reponse.read().decode('utf-8')
#yt=YouTube('https://www.youtube.com/watch?v=zXAqw0Vzr4w').streams.filter(res='1080p',su)
#yt.first().download()
#yt = YouTube('https://www.youtube.com/watch?v=zXAqw0Vzr4w')
#yt.streams.all
# or if you want to download in a specific directory
#pl.download_all('/path/to/directory/')