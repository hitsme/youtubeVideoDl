#!/usr/bin/python
# #-*-coding:utf-8-*-
from pytube import YouTube
import uuid
#yt720p = YouTube('https://www.youtube.com/watch?v=A-lebYNcgBk').streams
#yt720p.first().download(filename='Titanic scena finale - Final scene')
print str(uuid.uuid1())
import urllib2
import re
from  bs4 import BeautifulSoup
reponse = urllib2.urlopen("https://www.youtube.com/channel/UCoC47do520os_4DBMEFGg4A/videos")
htmlstr = reponse.read()
print(htmlstr)
soup = BeautifulSoup(htmlstr, 'lxml')
    # print soup.prettify()
    # print soup.children.next()
for i in soup.find_all(href=re.compile("watch"),
                           class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"):
        #print i
        hrefvalue = re.findall(r'href="(.*?)" rel="nofollow" title="(.*?)"', str(i), re.I)
        print(hrefvalue[0][1])