#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
# import json
import urllib
import requests

'''
XMLY album downloader
'''
class Downloader():
    _list = []
    _albumTitle = ''

    # 获取下载链接
    def getData(self, albumUrl):
        urlSlices = albumUrl.split('/')
        albumId = urlSlices[len(urlSlices) - 1] or urlSlices[len(urlSlices) - 2]
        r = requests.get("http://mobile.ximalaya.com/mobile/playlist/album", params={"albumId": albumId})
        # listJson = json.loads(r.text)
        try:
            listJson = r.json()
        except:
            print 'Error: no json data, url may be not right'
            return
        
        # if listJson.has_key('albumTitle'):
        if listJson['albumTitle']:
            self._albumTitle = listJson['albumTitle']
            print 'Album name: ' + listJson['albumTitle']

        # if listJson.has_key('data'):
        if listJson['data']:
            musicList = listJson['data']
            if len(musicList) > 0:
                # 所有下载链接
                for music in musicList:
                    self._list.append({
                        'downloadUrl': music['playUrl32'],
                        'name': music['title']
                    })
        return


    # 开始执行所有下载操作
    def __init__(self, albumUrl):
        if __name__ == '__main__':
            if albumUrl:
                print 'You input album link: %s' % albumUrl
            self.getData(albumUrl)
            if len(self._list) > 0:
                # 下载并命名归类文件
                self.downloadFiles(self._albumTitle)
            
            print str(len(self._list)) + ' files download completed, Mission complete.'
    

    # 下载文件
    def downloadFiles(self, albumTitle):
        # 创建文件夹
        if False == os.path.isdir(albumTitle):
            os.mkdir(albumTitle)

        for item in self._list:
            self.downloadFile(item)
        
        print albumTitle + str(len(self._list)) + ' files download completed.'
        return

    def downloadFile(self, item):
        # 取文件扩展名称
        def getFileExp(file):
            return '.' + file[-3:]

        fileName = self._albumTitle + '/' + item['name'] + getFileExp(item['downloadUrl'])

        if not os.path.isfile(fileName):
            try:
                urllib.urlretrieve(item['downloadUrl'], fileName)
            except:
                print 'error'
            print item['name'] + ' file ' + item['downloadUrl'] + ' is downloaded.'
        else:
            print item['name'] + ' file ' + item['downloadUrl'] + ' already exists.'

def waitAlbumUrl():
    msg = '请输入专辑链接(例子：http://www.ximalaya.com/6749726/album/5289107/): \n'
    albumUrl = raw_input(msg).decode(sys.stdin.encoding)
    return albumUrl

albumUrl = waitAlbumUrl()
Downloader(albumUrl)
