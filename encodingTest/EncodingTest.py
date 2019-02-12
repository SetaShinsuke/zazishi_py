# -*- coding: UTF-8 -*-
import sys
import chardet

# reload(sys)
# sys.setdefaultencoding('utf-8')

s = "测试"
print type("测试")
print "测试"
print chardet.detect(s)
print unicode(s.decode(chardet.detect(s)["encoding"]))
# print u"测试".decode().encode("utf-8")
