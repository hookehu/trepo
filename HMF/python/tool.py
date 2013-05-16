#-*- coding:utf-8 -*-
'''
The MIT License (MIT)

Copyright(C) 2013 <Hooke HU>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from xml.etree import ElementTree as etree
from hmf import Hmf

subfixs = ['_i', '_f', '_s', '_l', '_k', '_m']

def read_cfg(filename):
		fd = open(filename, "rb")
		content = fd.read()
		fd.close()
		x = etree.XML(content)
		rst = {}
		roots = x.getchildren()
		for r in roots:
				children = r.getchildren()
				if len(children) == 0:
						continue
				r = {}
				for i in children:
						if i.tag[-2:] in subfixs:
								r[i.tag[:-2]] = convert_value(i.tag, i.text)
						else:
								r[i.tag] = convert_value(i.tag, i.text)
				if not r.has_key('id_i') and not r.has_key('id'):
						continue
				if r.has_key('id_i'):
						rst[r['id_i']] = r
				else:
						rst[r['id']] = r
		return rst
		
def convert_value(key, value):
		subfix = key[-2:]
		if value is None:
				return ""
		if isinstance(value, unicode):
				return value.encode('utf-8')
		return value
		if subfix == "_i":
				if value == "" or value is None:
						return 0
				try:
						return int(value)
				except:
						return float(value)
		elif subfix == "_f":
				if value == "" or value is None:
						return 0.0
				return float(value)
		elif subfix == "_l":
				if value is None:
						return []
				if not isinstance(value, str) and not isinstance(value, unicode):
						return [int(value)]
				l = value.split(",")
				for i in range(len(l)):
						l[i] = int(l[i])
				return l
		elif subfix == "_k":
				if value is None:
						return []
				if not isinstance(value, str) and not isinstance(value, unicode):
						return [int(value)]
				k = value.split(",")
				for i in range(len(k)):
						k[i] = int(k[i])
				return k
		elif subfix == "_m":
				if value == "" or value is None:
						return {}
				m = value.split(",")
				rv = {}
				for i in range(len(m)):
						kv = m[i].split(":")
						if kv[0].isdigit():
								k1 = int(kv[0])
						else:
								k1 = kv[0]
						if kv[1].isdigit():
								v1 = int(kv[1])
						else:
								v1 = kv[1]
						rv[k1] = v1
				return rv
		elif subfix == "_s":
				if value is None:
						return ''
				return value
		else:
				if value is None:
						return ''
				return value
		
if __name__ == "__main__":
		import sys, os, dircache
		base_path = '''E:/mogo/doc/product/配置表/xml文件最终版/'''
		out_path = '''E:/hmfoutput/'''
		files = dircache.listdir(unicode(base_path, "utf-8"))
		for name in files:
				if name == '.svn':
						continue
				print name
				r = read_cfg(unicode(base_path, "utf-8") + name)
				#print r
				h = Hmf()
				h.write_object(r)
				h.merge_all()
				s = h.stream
				s.seek(0)
				fd = open(out_path + name[:-4] + '.bytes', "wb")
				fd.write(s.read())
				fd.close()