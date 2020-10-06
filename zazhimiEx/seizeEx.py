# -*- coding: utf-8 -*-
import locale
import os
import re
import subprocess
import sys
import urllib.request
import urllib.parse
from datetime import datetime
# import chardet

import requests

# reload(sys)
# sys.setdefaultencoding('utf-8')

# 搜索 GET: https://app160501.zazhimi.net/api/search.php?k=men
# 详情 POST: https://app160501.zazhimi.net/api/show.php HTTP/1.1
# 
# HOST = "https://app130.zazhimi.net/"
HOST = "https://app2020.zazhimi.net/"
# HOST = "http://120.26.56.13/.zazhimi.net/"
API_INDEX = "/api/index.php"
API_SEARCH = "/api/search.php"
API_SHOW = "/api/show.php"


def r_in(hint):
    # return raw_input(hint.encode(sys.stdin.encoding))
    return input(hint)


def r_out(content):
    # return content.encode(sys.stdout.encoding)
    return content


def r_print(content):
    print(r_out(content))


# def slugify(value):
#     import unicodedata
#     value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
#     value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
#     value = unicode(re.sub('[-\s]+', '-', value))

# region 搜索要下载的杂志
search_url = HOST + API_SEARCH
api_url = HOST + API_SHOW
id = r_in("搜索关键词: ")
id_k = urllib.parse.quote(id.encode('gb2312'))
search_args = {'k': id_k}
print("Start request...")
request_search = requests.get(search_url, search_args)

print("Search Request : %s" % request_search.url)
print("Search complete, %s" % request_search)
search_result = request_search.json()
result_magazines = search_result['magazine']
for index, magazine in enumerate(result_magazines):
    r_print("{}. {}-{}".format(index, magazine['magName'], magazine['magId']))

index_str = r_in("要下载的序号: ")
index = int(index_str)
mag_id = result_magazines[index]['magId']
# 从服务器拿到的 utf8 数据, 解码 decode 后使用
mag_name = result_magazines[index]['magName'].replace('\\', '_').replace('/', '_')
r_print("To download mag id: {}".format(mag_id))

# endregion

# region 拉取图片信息
detail_url = HOST + API_SHOW
detail_args = {'a': mag_id}
print("Start request...")
request_show = requests.get(detail_url, detail_args)

print("Search Request : %s" % request_show.url)
detail_json = request_show.json()


# endregion


def filter_img(item):
    return item['magPic']


# 当前目录中下载
dir_path = "download\{}_{}".format(mag_name, datetime.now().microsecond)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

img_urls = list(map(filter_img, detail_json['content']))
total = len(img_urls)
downloaded = 0
max_amount = total
# max_amount = 3
for img_url in img_urls:
    if downloaded >= max_amount:
        break
    file_name = img_url.split('/')[-1].replace('\\', '_').replace('/', '_')
    # file_name = img_url.split('/')[-1].encode('gbk', 'ignore').replace('\\', '_').replace('/', '_')
    r_print("Downloading {}/{} : {}".format(downloaded + 1, total, file_name))
    # final_url = img_url.encode('utf8')
    url_tail = img_url.split('//')[-1]
    final_url = img_url.replace(url_tail, urllib.parse.quote(url_tail.encode('gb2312')))
    print("Pic url: {}".format(final_url))

    # p = urlparse.urlparse(img_url)
    # # final_url = "{}://{}/{}?{}".format(p.scheme, p.hostname,
    # #                                    urllib.quote_plus(p.path.encode('gbk')).replace('%2F', '/'), p.params)
    # print type(p.path)
    # print urllib.urlencode(str(p.path.decode('GBK')))
    # final_url = "{}://{}/{}?{}".format(p.scheme, p.hostname, urllib.urlencode(p.path), p.params)
    # r_print(u"file_url: {}".format(final_url))
    # r_print(u"file_name: {}\{}".format(dir_path, file_name))
    # urllib.urlretrieve(u"{}".format(final_url), u"{}\{}".format(dir_path, file_name))

    # resp = requests.get(final_url)
    # print resp

    urllib.request.urlretrieve(final_url, "{}\{}".format(dir_path, file_name))
    downloaded += 1
r_print("Download finished {}/{}!\nSaved at \{}".format(downloaded, total, dir_path))
# print unicode(dir_path)
# 查看字符串的 encoding
# print(chardet.detect("{}".format(dir_path)))
# print(chardet.detect("测试"))
to_open_path = "{}\{}".format(os.getcwd(), dir_path)
r_print("Open:{}".format(to_open_path))
subprocess.Popen('explorer /select, {}'.format(to_open_path), shell=True)
