#-*- coding:utf-8 -*-
import sys, os, shutil, struct, zlib

path = "E:/pngs"

class PNGDecoder(object):
		def __init__(self):
				self.cnt = 0
				
		def analyse(self, p):
				self.idat = None
				fd = open(p, 'rb')
				self.readSig(fd)
				while True:
						l = self.readLen(fd)
						t = self.readType(fd)
						if not self.readChunk(fd, t, l):
								break
						self.readCRC(fd)
				
				fd.close()
				
		def readChunk(self, fd, t, l):
				print "chunk type %s chunk len %d " % (t, l)
				if hasattr(self, "read" + t):
						handler = getattr(self, "read" + t)
						handler(fd, l)
				elif t == "IEND":
						self.idat = zlib.decompress(self.idat)
						return False
				else:
						print "unknown chunk %s " % t
						#jump the chunk
						for i in range(l):
								fd.read(1)
						
				return True
				
		def readSig(self, fd):
				struct.unpack('B', fd.read(1))
				struct.unpack('B', fd.read(1))
				struct.unpack('B', fd.read(1))
				struct.unpack('B', fd.read(1))
				struct.unpack('B', fd.read(1))
				struct.unpack('B', fd.read(1))
				struct.unpack('B', fd.read(1))
				struct.unpack('B', fd.read(1))
				
		def readLen(self, fd):
				i3 = struct.unpack('B', fd.read(1))
				i2 = struct.unpack('B', fd.read(1))
				i1 = struct.unpack('B', fd.read(1))
				i0 = struct.unpack('B', fd.read(1))
				l = i3[0] << 24 | i2[0] << 16 | i1[0] << 8 | i0[0]
				return l
				
		def readType(self, fd):
				i3 = fd.read(1)
				i2 = fd.read(1)
				i1 = fd.read(1)
				i0 = fd.read(1)
				#print struct.unpack('B', i3)
				#print struct.unpack('B', i2)
				#print struct.unpack('B', i1)
				#print struct.unpack('B', i0)
				return i3 + i2 + i1 + i0
				
		def readIHDR(self, fd, length):
				i3 = struct.unpack('B', fd.read(1))
				i2 = struct.unpack('B', fd.read(1))
				i1 = struct.unpack('B', fd.read(1))
				i0 = struct.unpack('B', fd.read(1))
				w = i3[0] << 24 | i2[0] << 16 | i1[0] << 8 | i0[0]
				self.width = w
				i3 = struct.unpack('B', fd.read(1))
				i2 = struct.unpack('B', fd.read(1))
				i1 = struct.unpack('B', fd.read(1))
				i0 = struct.unpack('B', fd.read(1))
				h = i3[0] << 24 | i2[0] << 16 | i1[0] << 8 | i0[0]
				self.height = h
				bitdepth = struct.unpack('B', fd.read(1))[0]
				self.bit_depth = bitdepth
				colortype = struct.unpack('B', fd.read(1))[0]
				self.color_type = colortype
				compression = struct.unpack('B', fd.read(1))[0]
				self.compression = compression
				filtermethod = struct.unpack('B', fd.read(1))[0]
				self.filter_method = filtermethod
				interlace = struct.unpack('B', fd.read(1))[0]
				self.interlace = interlace
				if interlace == 1:
						print p
				print "width = %d, height = %d, bitdepth = %d, colortype = %d, compression = %d, filtermethod = %d, interlace = %d" %\
							(w, h, bitdepth, colortype, compression, filtermethod, interlace)
				return w, h, bitdepth, colortype, compression, filtermethod, interlace
				
		def readCRC(self, fd):
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				return (i3 << 24 | i2 << 16 | i1 << 8 | i0)
				
		def readPLTE(self, fd, length):
				rst = []
				if (length % 3) != 0:
						print "PLTE ERROR"
						return None
				l = length / 3
				for i in range(l):
						r = struct.unpack('B', fd.read(1))[0]
						g = struct.unpack('B', fd.read(1))[0]
						b = struct.unpack('B', fd.read(1))[0]
						rst.append((r, g, b))
				self.plte = rst
				return rst
		
		def readIDAT(self, fd, length):
				rst = []
				#for i in range(length):
				#		fd.read(1)
				if self.idat is None:
						self.idat = fd.read(length)
						return rst
				self.idat = self.idat + fd.read(length)
				#self.idat = zlib.decompress(self.idat)
				#print 1024 * 512
				#print struct.unpack('B', self.idat[0])
				#print struct.unpack('B', self.idat[1025])
				#print struct.unpack('B', self.idat[2050])
				#print len(self.idat)
				return rst
				
		def readcHRM(self, fd, length):
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				whitex = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				whitey = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				redx = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				redy = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				greenx = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				greeny = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				bluex = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				bluey = i3 << 24 | i2 << 16 | i1 << 8 | i0
				return ((whitex, whitey), (redx, redy), (greenx, greeny), (bluex, bluey))
				
		def readgAMA(self, fd, length):
				i3 = struct.unpack('B', fd.read(1))[0]
				i2 = struct.unpack('B', fd.read(1))[0]
				i1 = struct.unpack('B', fd.read(1))[0]
				i0 = struct.unpack('B', fd.read(1))[0]
				gamma = i3 << 24 | i2 << 16 | i1 << 8 | i0
				
		def readiCCP(self, fd, length):
				#jump iCCP chunk
				self.profile_name = ""
				l = 0
				while True:
						c = fd.read(1)
						l += 1
						if c == "\0":
								break
						self.profile_name += c
				self.iccp_compression_method = struct.unpack('B', fd.read(1))[0]
				self.iccp_compression_profile = ""
				length = length -l - 1
				for i in range(length):
						self.iccp_compression_profile += fd.read(1)
						
		def readsBIT(self, fd, length):
				if self.color_type == 0:
						self.grey_scale = struct.unpack('B', fd.read(1))[0]
				elif self.color_type == 2 or self.color_type == 3:
						self.red = struct.unpack('B', fd.read(1))[0]
						self.green = struct.unpack('B', fd.read(1))[0]
						self.blue = struct.unpack('B', fd.read(1))[0]
						print "sBit R = %d, G = %d, B = %d" % (self.red, self.green, self.blue)
				elif self.color_type == 4:
						self.grey_scale = struct.unpack('B', fd.read(1))[0]
						self.alpha = struct.unpack('B', fd.read(1))[0]
				elif self.color_type == 6:
						self.red = struct.unpack('B', fd.read(1))[0]
						self.green = struct.unpack('B', fd.read(1))[0]
						self.blue = struct.unpack('B', fd.read(1))[0]
						self.alpha = struct.unpack('B', fd.read(1))[0]
						print "sBit R = %d, G = %d, B = %d, A = %d" % (self.red, self.green, self.blue, self.alpha)
				else:
						#if err color type, jump the chunk
						for i in range(length):
								fd.read(1)
				
		def readsRGB(self, fd, length):
				for i in range(length):
						fd.read(1)
				return
				self.intent = struct.unpack('B', fd.read(1))[0]
				
		def readbKGD(self, fd, length):
				if self.color_type == 0 or self.color_type == 4:
						self.bg_grey_scale = struct.unpack('H', fd.read(2))[0]
				elif self.color_type == 2 or self.color_type == 6:
						self.bg_red = struct.unpack('H', fd.read(2))[0]
						self.bg_green = struct.unpack('H', fd.read(2))[0]
						self.bg_blue = struct.unpack('H', fd.read(2))[0]
				elif self.color_type == 3:
						self.bg_plte_index = struct.unpack('B', fd.read(1))[0]
				else:
						#if err color type, jump the chunk
						for i in range(length):
								fd.read(1)
		
		def readhIST(self, fd, length):
				for i in range(length):
						fd.read(1)
						
		def readtRNS(self, fd, length):
				if self.color_type == 0:
						self.grey_sample = struct.unpack('H', fd.read(2))[0]
				elif self.color_type == 2:
						self.red_sample = struct.unpack('H', fd.read(2))[0]
						self.blue_sample = struct.unpack('H', fd.read(2))[0]
						self.green_sample = struct.unpack('H', fd.read(2))[0]
				elif self.color_type == 3:
						self.alpha_table = []
						for i in range(len(self.plte)):
								self.alpha_table.append(struct.unpack('B', fd.read(1))[0])
				else:
						#if err color type, jump the chunk
						for i in range(length):
								fd.read(1)
		
		def readpHYs(self, fd, length):
				for i in range(length):
						fd.read(1)
						
		def readsPLT(self, fd, length):
				for i in range(length):
						fd.read(1)
						
		def readtIME(self, fd, length):
				for i in range(length):
						fd.read(1)
						
		def readiTXt(self, fd, length):
				for i in range(length):
						fd.read(1)
						
		def readtEXt(self, fd, length):
				self.ext_keyword = ""
				l = 0
				while True:
						c = fd.read(1)
						l += 1
						if c == "\0":
								break
						self.ext_keyword += c
				self.ext_text = ""
				length = length - l
				for i in range(length):
						self.ext_text += fd.read(1)
				#for i in range(length):
				#		fd.read(1)
						
		def readzTXt(self, fd, length):
				self.ztxt_keyword = ""
				l = 0
				while True:
						c = fd.read(1)
						l += 1
						if c == "\0":
								break
						self.ztxt_keyword += c
				self.ztxt_compression_method = struct.unpack('B', fd.read(1))[0]
				self.ztxt_compression_text = ""
				length = length -l - 1
				for i in range(length):
						self.iccp_compression_profile += fd.read(1)
				#for i in range(length):
				#		fd.read(1)
				

if __name__ == '__main__':
	files = os.listdir(path)
	f = files[0]
	print f
	p = PNGDecoder()
	#p.analyse(os.path.join(path, f))
	for f in files:
			print f
			#if f == "10504_ground_1.png":
			p.analyse(os.path.join(path, f))
	print "total TXt EXt %d " % p.cnt
	print("hhh")