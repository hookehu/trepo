#-*- coding:utf-8 -*-

def check_runes(res_pool):
		runes = res_pool['runes']
		for k, v in runes.items():
				if not res_pool['languages'].get(v['name_i'], None):
						f = open("error.log", "ab")
						f.write("\r\n符文配置.xlsx 中 id_i = ")
						f.write(str(k))
						f.write("  name_i 指向的值为空")
						f.close()
				if not res_pool['languages'].get(v['desc_i'], None):
						f = open("error.log", "ab")
						f.write("\r\n符文配置.xlsx 中 id_i = ")
						f.write(str(k))
						f.write("  desc_i 指向的值为空")
						f.close()
				if not res_pool['icons'].get(v['icon_i'], None):
						f = open("error.log", "ab")
						f.write("\r\n符文配置.xlsx 中 id_i = ")
						f.write(str(k))
						f.write("  icon_i 指向的值为空")
						f.close()
				#还有效果连接
				
def check_randoms(res_pool):
		randoms = res_pool['rune_randoms']
		for k, v in randoms.items():
				pass
		
def check_vocations(res_pool):
		vocations = res_pool['rune_vocations']
		for k, v in vocations.items():
				pass
		
def check(res_pool):
		check_runes(res_pool)
		check_randoms(res_pool)
		check_vocations(res_pool)
		
if __name__ == '__main__':
		f = open("fff.log", "ab")
		f.close()