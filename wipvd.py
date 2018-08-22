#!/usr/bin/python
# #-*-coding:utf-8-*-
from pytube import YouTube
import uuid
yt720p = YouTube('https://www.youtube.com/watch?v=A-lebYNcgBk').streams
yt720p.first().download(filename='Titanic scena finale - Final scene')
print str(uuid.uuid1())