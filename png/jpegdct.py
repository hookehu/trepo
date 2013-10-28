#-*- coding:utf-8 -*-
import math

orgi = [[-76, -73, -67, -62, -58, -67, -64, -55],
				[-65, -69, -73, -38, -19, -43, -59, -56],
				[-66, -69, -60, -15, 16, -24, -62, -55],
				[-65, -70, -57, -6, 26, -22, -58, -59],
				[-61, -67, -60, -24, -2, -40, -60, -58],
				[-49, -64, -68, -58, -51, -60, -70, -53],
				[-43, -57, -64, -69, -73, -67, -63, -45],
				[-41, -49, -59, -60, -63, -52, -50, -34]]

new = [[-76, -73, -67, -62, -58, -67, -64, -55],
				[-65, -69, -73, -38, -19, -43, -59, -56],
				[-66, -69, -60, -15, 16, -24, -62, -55],
				[-65, -70, -57, -6, 26, -22, -58, -59],
				[-61, -67, -60, -24, -2, -40, -60, -58],
				[-49, -64, -68, -58, -51, -60, -70, -53],
				[-43, -57, -64, -69, -73, -67, -63, -45],
				[-41, -49, -59, -60, -63, -52, -50, -34]]
				
def dct(u, v, o):
		cu = 1
		if u == 0:
				cu = math.sqrt(2) / 2
		cv = 1
		if v == 0:
				cv = math.sqrt(2) / 2
		t = 0
		for i in range(8):
				for j in range(8):
						pixel = o[i][j]
						ccu = math.cos(((2 * i + 1) * u * 3.14) / 16)
						ccv = math.cos(((2 * j + 1) * v * 3.14) / 16)
						t = t + (ccu * ccv * pixel)
		return cu * cv * t / 4
		
def idct(x, y, n):
		t = 0
		for u in range(8):
				for v in range(8):
						cu = 1
						if u == 0:
								cu = math.sqrt(2) / 2
						cv = 1
						if v == 0:
								cv = math.sqrt(2) / 2
						pixel = n[u][v]
						ccx = math.cos(((2 * x + 1) * u * 3.14) / 16)
						ccy = math.cos(((2 * y + 1) * v * 3.14) / 16)
						t = t + (cu * cv * pixel * ccx * ccy)
		return t / 4.0
		
if __name__ == "__main__":
	print dir(math)
	for i in orgi:
			print i
	for u in range(8):
			for v in range(8):
					new[u][v] = int(round(dct(u, v, orgi)))
	print '---------'
	for i in new:
			print i
	print 'nnnnnnnnn'
	for x in range(8):
			for y in range(8):
					orgi[x][y] = int(round(idct(x, y, new)))
	for i in orgi:
			print i