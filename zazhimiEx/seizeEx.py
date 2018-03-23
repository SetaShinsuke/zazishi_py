# -*- coding: GBK -*-
import os
import subprocess
import urllib
from datetime import datetime

import requests

# ���� GET: https://app160501.zazhimi.net/api/search.php?k=men
# ���� POST: https://app160501.zazhimi.net/api/show.php HTTP/1.1

HOST = "https://app160501.zazhimi.net/"
API_INDEX = "/api/index.php"
API_SEARCH = "/api/search.php"
API_SHOW = "/api/show.php"

# region ����Ҫ���ص���־
search_url = HOST + API_SEARCH
api_url = HOST + API_SHOW
id = raw_input("�����ؼ���: ")
search_args = {'k': id}
print "Start request..."
request_search = requests.get(search_url, search_args)

print "Search Request : %s" % request_search.url
print "Search complete, %s" % request_search
search_result = request_search.json()
result_magazines = search_result['magazine']
for index, magazine in enumerate(result_magazines):
    print "{}. {}-{}".format(index, magazine['magName'].encode('gbk', 'ignore'),
                             magazine['magId'])

index_str = raw_input("Ҫ���ص����: ")
index = int(index_str)
mag_id = result_magazines[index]['magId']
print "Ҫ���ص���־: {}".format(mag_id)

# endregion

# region ��ȡͼƬ��Ϣ
detail_url = HOST + API_SHOW
detail_args = {'a': mag_id}
print "Start request..."
request_show = requests.get(detail_url, detail_args)

print "Search Request : %s" % request_show.url
print "Search complete, %s" % request_show
detail_json = request_show.json()


# endregion


def filter_img(item):
    return item['magPic']


# ��ǰĿ¼������
dir_path = "download\{}_{}".format(id, datetime.now().microsecond)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

img_urls = map(filter_img, detail_json['content'])
total = len(img_urls)
downloaded = 0
max = total
for img_url in img_urls:
    if downloaded >= max:
        break
    file_name = img_url.split('/')[-1].encode('gbk', 'ignore').replace('\\', '_').replace('/', '_')
    print "Downloading {}/{} : {}".format(downloaded + 1, total, file_name)
    urllib.urlretrieve(img_url, "{}\{}".format(dir_path, file_name))
    downloaded += 1
print "�������{}/{}!\n�ѱ�����\{}".format(downloaded, total, dir_path)
to_open_path = "{}\{}".format(os.getcwd(), dir_path)
subprocess.Popen(r'explorer /select, {}'.format(to_open_path))
