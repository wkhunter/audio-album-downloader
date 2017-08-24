#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from BaseDownloader import Downloader

'''
QTFM album downloader

@argv
argv[1] albumUrl
argv[2] dist

api:
http://i.qingting.fm/wapi/channels/110670
http://i.qingting.fm/wapi/channels/110670/programs/page/1/pagesize/500
'''

class Qingting(Downloader):
    # 获取蜻蜓FM下载链接
    def getData(self, albumUrl):
        urlSlices = albumUrl.split('/')
        albumId = urlSlices[len(urlSlices) - 1] or urlSlices[len(urlSlices) - 2]
        rAlbum = requests.get("http://i.qingting.fm/wapi/channels/" + albumId)
        r = requests.get("http://i.qingting.fm/wapi/channels/" + albumId + "/programs/page/1/pagesize/500")
        # listJson = json.loads(r.text)
        try:
            albumInfo = rAlbum.json()
            listJson = r.json()

            if albumInfo['data'] and albumInfo['data']['name']:
                self._albumTitle = albumInfo['data']['name'] + '-qtfm-' + albumId
                print '专辑名称: '.decode('utf-8') + self._albumTitle

            # if listJson.has_key('data'):
            if listJson['data']:
                musicList = listJson['data']
                if len(musicList) > 0:
                    # 所有下载链接
                    for music in musicList:
                        self._list.append({
                            'downloadUrl': 'http://od.qingting.fm/' + music['file_path'] if music['file_path'] else None,
                            'name': music['name']
                        })
        except Exception,e:
            print 'Error: no json data, url may be not right', e
            return

    # 开始执行所有下载操作
    def __init__(self, albumUrl, dist):
        Downloader.__init__(self, albumUrl, dist)
