#-*- coding:utf-8 -*-
import xlrd

base_path = "../product/配置表/Excel模版最终版/"
icon = "Icon表.xlsx"
language = "中文字符配置表.xlsx"

jewel = "宝石配置表.xlsx"
rune_vocation = "符文解锁配置.xlsx"
rune = "符文配置.xlsx"
rune_price = "符文刷新金钱配置.xlsx"
rune_random = "符文随机生成配置.xlsx"
rune_unlock = "符文位解锁配置.xlsx"

has_error = False

def readExcel(path):
		book = xlrd.open_workbook(path)
		sheet = book.sheet_by_index(0)
		return sheet
		
def get_id_idx(sheet):
		row_len = sheet.nrows
		col_len = sheet.ncols
		for i in range(row_len):
				for j in range(col_len):
						if sheet.cell(i, j).value == "id_i":
								return (i, j)

def read_cfg(path):
		sheet = readExcel(path)
		id_idx = get_id_idx(sheet)
		if not id_idx:
				print path + ' 没有id_i项'
				return
		row_len = sheet.nrows
		col_len = sheet.ncols
		#print path
		i, j = id_idx
		links = sheet.row_values(i-1)
		props = sheet.row_values(i)
		link = []
		#查找关联表名
		for ii in range(len(props)):
				if props[ii] == '':
						continue
				if links[ii] == '':
						continue
				if not isinstance(links[ii], str) and not isinstance(links[ii], unicode):
						continue
				lk = links[ii].split(",")
				if len(lk) != 2:
						continue
				link.append({'prop':props[ii], 'file':lk[0].encode('gb2312'), 'link_to':lk[1]})
		i = i + 1
		rst = {}
		rst['link'] = link
		while i < row_len:
				r = {}
				while j < col_len:
						#r[props[j]] = sheet.cell(i, j).value
						if sheet.cell(i, j).value != "":
							try:
								 r[props[j]] = convert_value(props[j], sheet.cell(i, j).value)
							except:
									f = open("error.log", "ab")
									f.write('\r\n')
									f.write(path)
									f.write("\r\n第 %d 行 " % (i + 1))
									f.write(props[j])
									f.write(" 的值有错（可能是类型不对，或用了中文符号)")
									f.write("\r\n值为: ")
									s = sheet.cell(i, j).value
									if isinstance(s, str) or isinstance(s, unicode):
											s = s.encode('gb2312')
									else:
											s = str(s)
									f.write(s)
									f.close()
									global has_error
									has_error = True
									#return
						j = j + 1
				rst[r["id_i"]] = r
				i = i + 1
				j = id_idx[1]
		return rst

def convert_value(key, value):
		subfix = key[-2:]
		if subfix == "_i":
				if value == "":
						return 0
				return int(value)
		elif subfix == "_f":
				if value == "":
						return 0.0
				return float(value)
		elif subfix == "_l":
				if not isinstance(value, str) and not isinstance(value, unicode):
						return [float(value)]
				l = value.split(",")
				for i in range(len(l)):
						l[i] = float(l[i])
				return l
		elif subfix == "_k":
				if not isinstance(value, str) and not isinstance(value, unicode):
						return [int(value)]
				k = value.split(",")
				for i in range(len(k)):
						k[i] = int(k[i])
				return k
		elif subfix == "_m":
				if value == '':
						return {}
				m = value.split(",")
				rv = {}
				for i in range(len(m)):
						kv = m[i].split(":")
						if kv[0].isdigit():
								k1 = float(kv[0])
						else:
								k1 = kv[0]
						if kv[1].isdigit():
								v1 = float(kv[1])
						else:
								v1 = kv[1]
						rv[k1] = v1
				return rv
		elif subfix == "_s":
				return value
		else:
				return value
				
def check(res_pool, res, filename):
		lns = res['link']
		for l in lns:
				prop = l['prop'] #本文件的列名
				f = l['file'] #对应的文件名
				link_to = l['link_to'] #链接到的列名
				if not res_pool.has_key(f):
						fd = open("error.log", "ab")
						fd.write("\r\n")
						fd.write(filename)
						fd.write(" 文件 %s 列的链接文件 %s 不存在" % (prop.encode('gb2312'), f))
						fd.close()
						return
				vs = res_pool[f].keys()
				if len(vs) == 1:
						fd = open("error.log", "ab")
						fd.write("\r\n")
						fd.write(filename)
						fd.write(" 文件 %s 列的在链接文件 %s 内容为空" % (prop.encode('gb2312'), f))
						fd.close()
						continue
				k = None
				for k1 in vs:
						if k1 == 'link':
								continue
						k = k1
						break
				if not res_pool[f][k].has_key(link_to):
						fd = open("error.log", "ab")
						fd.write("\r\n")
						fd.write(filename)
						fd.write(" 文件 %s 列的链接属性在链接文件 %s 上找不到" % (prop.encode('gb2312'), link_to.encode('gb2312')))
						fd.close()
						continue
				subfix = prop[-2:]
				if subfix == '_i':
						_check_i(res_pool, res, filename, prop, f, link_to)
				elif subfix == '_l':
						_check_l(res_pool, res, filename, prop, f, link_to)
						
def _check_i(res_pool, res, filename, prop, f, link_to):
		link_file = res_pool[f]
		for k, v in res.items():
				if k == 'link':
						continue
				if v[prop] <= 0:
						#小于0的值无效,或是等于-1
						continue
				exist = False
				for k1, v1 in link_file.items():
						if k1 == 'link':
								continue
						if v[prop] == v1[link_to]:
								exist = True
								break
				if not exist:
						fd = open("error.log", "ab")
						fd.write("\r\n")
						fd.write(filename)
						fd.write(" 文件 id_i = %d 的 %s 列的值在链接文件找不到" % (k, prop.encode('gb2312')))
						fd.close()
		
def _check_l(res_pool, res, filename, prop, f, link_to):
		link_file = res_pool[f]
		for k, v in res.items():
				if k == 'link':
						continue
				vs = v[prop]
				if len(vs) == 0:
						continue
				for vs1 in vs:
						if vs1 <= 0:
								#小于0的值无效,或是等于-1
								continue
						exist = False
						for k1, v1 in link_file.items():
								if k1 == 'link':
										continue
								if vs1 == v1[link_to]:
										exist = True
										break
						if not exist:
								fd = open("error.log", "ab")
								fd.write("\r\n")
								fd.write(filename)
								fd.write(" 文件 id_i = %d 的 %s 列的值在链接文件找不到" % (k, prop.encode('gb2312')))
								fd.close()

if __name__ == "__main__":
	import sys, traceback, os, dircache
	import checklink
	if os.path.exists("error.log"):
			os.remove("error.log")
	files = dircache.listdir(base_path)
	res_pool = {}
	for f in files:
			if f == '.svn':
					continue
			res_pool[f] = read_cfg(base_path + f)
	#res_pool['icons'] = read_cfg(base_path + icon)
	#res_pool['languages'] = read_cfg(base_path + language)
	#res_pool['runes'] = read_cfg(base_path + rune)
	#res_pool['rune_prices'] = read_cfg(base_path + rune_price)
	#res_pool['rune_randoms'] = read_cfg(base_path + rune_random)
	#res_pool['rune_unlocks'] = read_cfg(base_path + rune_unlock)
	#res_pool['rune_vocations'] = read_cfg(base_path + rune_vocation)
	if has_error:
			raise
	#checklink.check(res_pool)
	for f in files:
			if f == '.svn':
					continue
			if len(res_pool[f]['link']) == 0:
					continue
			res = res_pool[f]
			check(res_pool, res, f)
	print 'check complete'
	