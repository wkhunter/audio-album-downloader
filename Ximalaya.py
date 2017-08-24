#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from BaseDownloader import Downloader

'''
XMLY album downloader

@argv
argv[1] albumUrl
argv[2] dist

api:
# http://mobile.ximalaya.com/mobile/playlist/album?albumId=5289107   # 没有分页信息，无法设置 pageSize
http://mobile.ximalaya.com/mobile/v1/album/track/ts-153737273737?albumId=277579&pageSize=500
'''

class Ximalaya(Downloader):
    # 获取下载链接
    def getData(self, albumUrl):
        urlSlices = albumUrl.split('/')
        albumId = urlSlices[len(urlSlices) - 1] or urlSlices[len(urlSlices) - 2]
        r = requests.get("http://mobile.ximalaya.com/mobile/v1/album", params={"albumId": albumId, "pageSize": 500})
        # listJson = json.loads(r.text)
        try:
            listJson = r.json()
        
            # if listJson.has_key('albumTitle'):
            if listJson['data']['album']['title']:
                self._albumTitle = listJson['data']['album']['title'] + '-xmly-' + albumId
                print '专辑名称: '.decode('utf-8') + self._albumTitle

            # if listJson.has_key('data'):
            if listJson['data']['tracks']['list']:
                musicList = listJson['data']['tracks']['list']
                if len(musicList) > 0:
                    # 所有下载链接
                    for music in musicList:
                        self._list.append({
                            'downloadUrl': music['playUrl64'] if music['playUrl64'] else None,
                            'name': music['title']
                        })
        except Exception,e:
            print 'Error: no json data, url may be not right', e
            return

    # 开始执行所有下载操作
    def __init__(self, albumUrl, dist):
        Downloader.__init__(self, albumUrl, dist)

