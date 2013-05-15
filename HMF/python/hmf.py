#-*- coding:utf-8 -*-
'''The MIT License (MIT)

Copyright(C) 2013 <Hooke HU>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ��Software��), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ��AS IS��, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from StringIO import StringIO
from util import *
from tag import *

class Hmf(object):
		""""""
		def __init__(self):
				self.reset()
				
		def reset(self):
				self.ints = [] #Int pool
				self.strs = [] #str pool
				self.doubles = [] #double pool
				self.bools = [False, True] #bool pool
				self.stream =  StringIO() #byte stream
				
		def set_stream(self, stream):
				self.stream = stream
				
		def write_object(self, obj):
				t = type(obj)
				if isinstance(obj, list):
						self.write_array(obj)
				elif isinstance(obj, dict):
						self.write_dict(obj)
				elif isinstance(obj, int):
						self.write_int(obj)
				elif isinstance(obj, float):
						self.write_number(obj)
				elif isinstance(obj, str):
						self.write_string(obj)
				else:
						pass
						
		def write_int(self, v):
				write_varint32(INT_TAG, self.stream)
				if v in self.ints:
						idx = self.ints.index(v)
						write_varint32(idx, self.stream)
						return
				self.ints.append(v)
				idx = len(self.ints) - 1
				write_varint32(idx, self.stream)
				
		def write_number(self, v):
				write_varint32(DOUBLE_TAG, self.stream)
				if v in self.doubles:
						idx = self.doubles.index(v)
						write_varint32(idx, self.stream)
						return
				self.doubles.append(v)
				idx = len(self.doubles) - 1
				write_varint32(idx, self.stream)
				
		def write_string(self, v):
				write_varint32(STRING_TAG, self.stream)
				if v in self.strs:
						idx = self.strs.index(v)
						write_varint32(idx, self.stream)
						return
				self.strs.append(v)
				idx = len(self.strs) - 1
				write_varint32(idx, self.stream)
				
		def write_array(self, v):
				#write array tag to stream
				write_varint32(ARRAY_TAG, self.stream)
				l = len(v)
				write_varint32(l, self.stream)
				for i in v:
						self.write_object(i)
				
		def write_dict(self, v):
				#write object tag to stream
				write_varint32(OBJECT_TAG, self.stream)
				l = len(v)
				write_varint32(l, self.stream)
				for k1, v1 in v.items():
						self.write_object(k1)
						self.write_object(v1)
						
		def merge_all(self):
				rst = StringIO()
				write_varint32(len(self.ints), rst)
				for i in self.ints:
						write_varint32(i, rst)
				write_varint32(len(self.doubles), rst)
				for i in self.doubles:
						write_double(i, rst)
				write_varint32(len(self.strs), rst)
				for i in self.strs:
						write_varint32(len(i), rst)
						write_str(i, rst)
				self.stream.seek(0)
				rst.write(self.stream.read())
				self.stream = rst
				
		def parse(self, stream):
				self.stream = stream
				self.init_pool()
				
		def read_object(self):
				tag = read_varint32(self.stream)
				print tag
				if tag == ARRAY_TAG:
						return self.read_array()
				elif tag == OBJECT_TAG:
						return self.read_dict()
				else:
						return None
						
		def read_dict(self):
				d = {}
				l = read_varint32(self.stream)
				for i in range(l):
						tag = read_varint32(self.stream)
						if tag == ARRAY_TAG:
								k = self.read_array()
						elif tag == OBJECT_TAG:
								k = self.read_dict()
						elif tag == INT_TAG:
								k = self.ints[read_varint32(self.stream)]
						elif tag == STRING_TAG:
								k = self.strs[read_varint32(self.stream)]
						elif tag == DOUBLE_TAG:
								k = self.doubles[read_varint32(self.stream)]
								
						tag = read_varint32(self.stream)
						if tag == ARRAY_TAG:
								v = self.read_array()
						elif tag == OBJECT_TAG:
								v = self.read_dict()
						elif tag == INT_TAG:
								v = self.ints[read_varint32(self.stream)]
						elif tag == STRING_TAG:
								v = self.strs[read_varint32(self.stream)]
						elif tag == DOUBLE_TAG:
								v = self.doubles[read_varint32(self.stream)]
						d[k] = v
				return d
				
		def read_array(self):
				rst = []
				l = read_varint32(self.stream)
				for i in range(l):
						tag = read_varint32(self.stream)
						if tag == ARRAY_TAG:
								rst.append(self.read_array())
						elif tag == OBJECT_TAG:
								rst.append(self.read_dict())
						elif tag == INT_TAG:
								rst.append(self.ints[read_varint32(self.stream)])
						elif tag == STRING_TAG:
								rst.append(self.strs[read_varint32(self.stream)])
						elif tag == DOUBLE_TAG:
								rst.append(self.strs[read_varint32(self.stream)])
				return rst
				
		def init_pool(self):
				len_ints = read_varint32(self.stream)
				for i in range(len_ints):
						self.ints.append(read_varint32(self.stream))
				len_doubles = read_varint32(self.stream)
				for i in range(len_doubles):
						self.doubles.append(read_double(self.stream))
				len_strs = read_varint32(self.stream)
				for i in range(len_strs):
						l = read_varint32(self.stream)
						self.strs.append(read_str(self.stream, l))
				
if __name__ == "__main__":
		import time, pyamf
		h = Hmf()
		'''o = {'a':[1,2,3], 'b':{'c':1}, 1:2, 3:0.3312344}
		print o
		h.write_object(o)
		h.merge_all()
		s = h.stream
		print s.len
		h.reset()
		s.seek(0)
		print s.len
		h.parse(s)
		e = h.read_object()
		print e
		print "success"'''
		
		fd = open("E://out.hmf", "rb")
		st = StringIO()
		st.write(fd.read())
		fd.close()
		st.seek(0)
		print time.time()
		h.parse(st)
		e = h.read_object()
		print len(e)
		fd.close()
		print time.time()
		print '-----------------'
		fd = open("E://out.amf", "rb")
		#s = fd.read()
		#fd.close()
		print time.time()
		o = pyamf.decode(fd).readElement()
		
		print time.time()
		print len(o)
		