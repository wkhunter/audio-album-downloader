#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
# import json
import requests
import socket
import webbrowser
import gevent
from gevent import socket
from gevent import monkey; monkey.patch_all()
socket.setdefaulttimeout(60.0)

'''
XMLY album downloader

@argv
argv[1] albumUrl
argv[2] dist

api:
# http://mobile.ximalaya.com/mobile/playlist/album?albumId=5289107   # 没有分页信息，无法设置 pageSize
http://mobile.ximalaya.com/mobile/v1/album/track/ts-153737273737?albumId=277579&pageSize=500
'''

class Downloader():
    _dist = os.path.expanduser(os.path.join('~', 'Downloads'))
    _list = []
    _albumTitle = ''

    def getData (self, albumUrl):
        print '@TODO: get data...'

    # 开始执行所有下载操作
    def __init__(self, albumUrl, dist):
        if albumUrl:
            print '你输入的链接是: %s'.decode('utf-8') % albumUrl

        # TODO: 通过 interface 重构，在 main 中进行 url 判断
        
        self.getData(albumUrl)

        if dist:
            self._dist = os.path.expanduser(dist)
        if len(self._list) > 0:
            # 下载并命名归类文件
            self.downloadFiles(self._albumTitle)
        
        if len(self._list) > 0:
            print '专辑下载完毕！'.decode('utf-8')
            webbrowser.open(self._dist.encode('utf-8'))
        else:
            print '输入不正确！'.decode('utf-8')
            # raw_input(u'按回车键退出程序'.encode(sys.stdin.encoding))
            # sys.exit('Bye!')

    # 下载文件
    def downloadFiles(self, albumTitle):
        # 替换非法字符, 解决 windows 环境创建目录失败的问题
        # albumTitle = re.sub(ur'[^\w\u4e00-\u9fff]+', '-', albumTitle)
        albumTitle = re.sub(ur'[\/:*?"<>|]+', '-', albumTitle)

        # 创建文件夹
        dist = os.path.join(self._dist, albumTitle)

        if False == os.path.isdir(dist):
            os.makedirs(dist)

        # webbrowser.open(dist)
        self._dist = dist

        print '文件保存路径: '.decode('utf-8') + os.path.abspath(dist)

        print '\n开始下载, 请勿关闭程序...\n'.decode('utf-8')
        # for item in self._list:
            # self.downloadFile(item, dist)
        
        jobs = [gevent.spawn(self.downloadFile, item, dist) for item in self._list]
        gevent.joinall(jobs, timeout=600)
        
        print '\n' + albumTitle + ' ' + str(len(self._list)) + ' files 下载完毕\n'.decode('utf-8')
        return

    def downloadFile(self, item, dist):
        if item['downloadUrl'] is None:
            return

        # 取文件扩展名称
        def getFileExp(file):
            return '.' + file[-3:]

        fileName = dist + '/' + item['name'] + getFileExp(item['downloadUrl'])

        if not os.path.isfile(fileName):
            r = requests.get(item['downloadUrl'])
            try:
                with open(fileName, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                print '[下载完成] '.decode('utf-8') + item['name']
            except Exception,e:
                print e
                print '[下载失败] '.decode('utf-8') + item['name'] + item['downloadUrl']
                pass
        else:
            print '[已经存在] '.decode('utf-8') + item['name']
