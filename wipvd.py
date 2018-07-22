#!/usr/bin/python
# #-*-coding:utf-8-*-
from pytube import YouTube
import uuid
yt720p = YouTube('https://www.youtube.com/watch?v=4RUGmBxe65U').streams
yt720p.first().download(output_path='G:\pycharmWorkspace\youtubeVideoDl',filename='test')
print str(uuid.uuid1())