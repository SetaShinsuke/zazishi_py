# -*- coding: GBK -*-
import getpass
import os
import subprocess
import urllib
from datetime import datetime

import requests

# http://app130.zazhimi.net/api/index.php?t=1&p=1&s=36&sign=b8d01a3ceb2fa6f7eae492f7967b9225
# http://120.26.56.13/api/show.php?a=12065&sign=c25b53c0874fc756819fd8ebb1aa30b2

HOST = "http://120.26.56.13/"
# HOST = "http://app130.zazhimi.net/"
API_INDEX = "/api/index.php"
API_SHOW = "/api/show.php"
api_url = HOST + API_SHOW
id = raw_input("请输入杂志 id: ")
sign = raw_input("Please input sign: ")
# id = "12065"
# sign = "c25b53c0874fc756819fd8ebb1aa30b2"
kwargs = {'a': id, 'sign': sign}
print "Start request..."
request = requests.get(api_url, kwargs)
print "Request : %s" % request.url
print "Request complete, %s" % request
jsonResult = request.json()


def filter_img(item):
    return item['magPic']


# 创建下载文件夹
user_name = getpass.getuser()
folderName = "C:\Users\{}\Downloads".format(user_name)
# 当前目录中下载
dir_path = "download\{}_{}".format(id, datetime.now().microsecond)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

img_urls = map(filter_img, jsonResult['content'])
total = len(img_urls)
downloaded = 0
max = total
for img_url in img_urls:
    if downloaded >= max:
        break
    file_name = img_url.split('/')[-1]
    print "Downloading {}/{} : {}".format(downloaded + 1, total, file_name)
    urllib.urlretrieve(img_url, dir_path + "\\" + file_name)
    downloaded += 1
print "下载完成!\n已保存在\{}".format(dir_path)
to_open_path = "{}\{}".format(os.getcwd(), dir_path)
subprocess.Popen(r'explorer /select, {}'.format(to_open_path))
