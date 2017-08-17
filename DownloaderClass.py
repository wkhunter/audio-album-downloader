#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
# import json
import urllib
import requests
import socket
import webbrowser
socket.setdefaulttimeout(20.0)

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

    # 获取下载链接
    def getData(self, albumUrl):
        urlSlices = albumUrl.split('/')
        albumId = urlSlices[len(urlSlices) - 1] or urlSlices[len(urlSlices) - 2]
        r = requests.get("http://mobile.ximalaya.com/mobile/v1/album", params={"albumId": albumId, "pageSize": 500})
        # listJson = json.loads(r.text)
        try:
            listJson = r.json()
        except:
            print 'Error: no json data, url may be not right'
            return
        
        # if listJson.has_key('albumTitle'):
        if listJson['data']['album']['title']:
            self._albumTitle = listJson['data']['album']['title']
            print '专辑名称: '.decode('utf-8') + self._albumTitle

        # if listJson.has_key('data'):
        if listJson['data']['tracks']['list']:
            musicList = listJson['data']['tracks']['list']
            if len(musicList) > 0:
                # 所有下载链接
                for music in musicList:
                    self._list.append({
                        'downloadUrl': music['playUrl64'],
                        'name': music['title']
                    })


    # 开始执行所有下载操作
    def __init__(self, albumUrl, dist):
        if albumUrl:
            print '你输入的链接是: %s'.decode('utf-8') % albumUrl
        self.getData(albumUrl)
        if dist:
            self._dist = os.path.expanduser(dist)
        if len(self._list) > 0:
            # 下载并命名归类文件
            self.downloadFiles(self._albumTitle)
        
        if len(self._list) > 0:
            print '专辑下载完毕！'.decode('utf-8')
            webbrowser.open(self._dist)
        else:
            print '输入不正确！'.decode('utf-8')

        raw_input(u'按回车键退出程序'.encode(sys.stdin.encoding))
        sys.exit('Bye!')

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
        for item in self._list:
            self.downloadFile(item, dist)
        
        print '\n' + albumTitle + ' ' + str(len(self._list)) + ' files 下载完毕\n'.decode('utf-8')
        return

    def downloadFile(self, item, dist):
        # 取文件扩展名称
        def getFileExp(file):
            return '.' + file[-3:]

        fileName = dist + '/' + item['name'] + getFileExp(item['downloadUrl'])

        if not os.path.isfile(fileName):
            try:
                urllib.urlretrieve(item['downloadUrl'], fileName)
                print '[下载完成] '.decode('utf-8') + item['name']
            except Exception,e:
                print e
                print '[下载失败] '.decode('utf-8') + item['name'] + item['downloadUrl']
                pass
        else:
            print '[已经存在] '.decode('utf-8') + item['name']
