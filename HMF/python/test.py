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
import pyamf

def get_dict(element):
		rst = {}
		children = element.getchildren()
		for i in children:
				rst[i.tag] = i.text
		return rst

if __name__ == "__main__":
		import time
		path = "E://ItemEquipment.xml"
		fd = open(path, 'rb')
		content = fd.read()
		fd.close()
		print time.time()
		x = etree.XML(content)
		print time.time()
		'''equips = x.findall('Equipment')
		print len(equips)
		o = {}
		for i in equips:
				r = get_dict(i)
				o[r['id_i']] = r
		h = Hmf()
		h.write_object(o)
		h.merge_all()
		s = h.stream
		s.seek(0)
		fd = open("E://out.hmf", "wb")
		fd.write(s.read())
		fd.close()
		
		st = pyamf.encode(o)
		fd = open("E://out.amf", "wb")
		fd.write(st.read())
		fd.close()'''