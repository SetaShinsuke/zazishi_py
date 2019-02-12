# -*- coding: UTF-8 -*-
import sys

import requests

reload(sys)
sys.setdefaultencoding('utf-8')
url = 'https://img130.zazhimi.net/aazzmpic/other/2014.11.14 橋本環奈 ファースト写真集 『 Little Star -KANNA15- 』/006.jpg'
print url.decode('UTF-8').encode(sys.stdout.encoding)

in_str = raw_input(u"请输入:".encode(sys.stdout.encoding)).decode(sys.stdin.encoding).encode('utf8')
print in_str.encode(sys.stdout.encoding)

resp = requests.get(url)
print resp
