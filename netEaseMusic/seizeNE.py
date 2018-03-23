# -*- coding: GBK -*-
import os
import subprocess
import urllib
from datetime import datetime

import requests

# http://music.163.com/api/v3/playlist/detail?id=512808550

HOST_NET_EASE = "https://api.imjad.cn/cloudmusic"
API_PLAYLIST_DETAIL = ""
# HOST_NET_EASE = "http://music.163.com/"
# API_PLAYLIST_DETAIL = "/api/v3/playlist/detail"
api_url = HOST_NET_EASE + API_PLAYLIST_DETAIL
id = raw_input("请输入歌单 id: ")
kwargs = {'id': id, 'type': 'playlist'}
headers = {
    'method': "GET",
    'authority': 'api.imjad.cn',
    'upgrade-insecure-requests': '1',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'api.imjad.cn',
    'Upgrade-Insecure-Requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
print "Start request..."
request = requests.get(api_url, kwargs, headers=headers)
# request = requests.get(api_url, kwargs)
print "Request : %s" % request.url
print "Request complete, %s" % request
jsonResult = request.json()
list_name = jsonResult['playlist']['name'].encode('gbk', 'ignore')
print "歌单名称:{}".format(list_name)


# .encode('unicode_escape')


def filter_img(item):
    img_name = "{}_{}.{}".format(item['al']['name'].encode('gbk', 'ignore').replace('\\', '_').replace('/', '_'),
                                 datetime.now().microsecond, item['al']['picUrl'].split('.')[-1])
    return {'name': img_name, 'url': item['al']['picUrl']}


# 创建下载文件夹
# user_name = getpass.getuser()
# folderName = "C:\Users\{}\Downloads".format(user_name)
# 当前目录中下载
dir_path = "download\{}_{}".format(list_name, datetime.now().microsecond)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

img_beans = map(filter_img, jsonResult['playlist']['tracks'])
total = len(img_beans)
print 'total: {}'.format(total)
downloaded = 0
# max = 0
for img_bean in img_beans:
    if downloaded >= total:
        break
    file_name = img_bean['name']
    file_url = img_bean['url']
    print "Downloading {}/{} : {}".format(downloaded + 1, total, file_name)
    print "Url: {}".format(file_url)
    urllib.urlretrieve(file_url, "{}\{}".format(dir_path, file_name))
    downloaded += 1
print "下载完成{}/{}!\n已保存在\{}".format(total, downloaded, dir_path)
to_open_path = "{}\{}".format(os.getcwd(), dir_path)
subprocess.Popen(r'explorer /select, {}'.format(to_open_path))
