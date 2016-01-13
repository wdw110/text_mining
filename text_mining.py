#encoding=utf-8
import MySQLdb
import re  #正则表达式包

db = MySQLdb.connect('localhost','root','','source_base') #打开数据库连接

cursor = db.cursor() #使用cursor()方法获取操作游标

cursor.execute('select content from tb_history where businesstype = "投诉"') # 使用execute方法执行SQL语句

data = cursor.fetchall() # 使用fetchall()方法获取所有剩余数据

content1 = []
content2 = []

for line in data:
	line_re = re.sub('\r\n','',line[0])        #去除每行中的换行符
	arr = re.findall(r'\【.+?\】', line_re)     #找到所有带有中括号的关键词
	content = line_re
	if len(arr):
		for s1 in arr:
			l = re.sub('【|】','',s1)
 			content1.append(l)
 		first = arr[0]
 		content = re.sub(first,'',line_re)
 		if len(arr)>1:
 			del arr[0]
 			surplus = '|'.join(arr)
 			content = re.sub(surplus,'；',content) #去除关键词
 	content2.append(content)


'''
for i in data:
	if i[0].find('【')  == 0 and i[0].find('】') > 0:
		l = i[0].find('】')
		length = len(i[0])
		content1.append(i[0][3:l-1])
		if length > l+3:
			content2.append(i[0][l+3:length])
	else:
		content2.append(i[0])
'''

with open('/Users/wdw/Desktop/work/data/content1.txt','w') as f:
	for line in content1:
		f.write(line+'\n')

with open('/Users/wdw/Desktop/work/data/content2.txt','w') as f:
	for line in content2:
		f.write(line+'\n')



################关键字词频统计##################
def arr_union_sort(arr):                #####数组去重统计并排序函数
	arr_union = set(arr)
	obj = {}
	for w in arr_union:
		obj[w] = arr.count(w)
	return sorted(obj.items(), key=lambda x:x[1], reverse=True)

sat_list = arr_union_sort(content1)

with open('/Users/wdw/Desktop/work/data/sat_word_tousu.txt','w') as f: 
	for word in sat_list:
	#	st = re.sub('\s','',word)
		f.write(word[0] + "\t" + str(word[1]) + "\n")




#############使用jieba做中文分词################
# 去除标点符号和数字
import jieba
import sys
import re  #正则表达式包
reload(sys)
sys.setdefaultencoding('utf-8')
import os

os.chdir('/Users/wdw/Desktop/work/code') #更改当前工作路径

#根据已分词的结果，添加自定义字典
jieba.load_userdict("userdict.txt")

f = open('/Users/wdw/Desktop/work/data/data_tousu.txt','w')

sign = "[\s+\.\!\/_,$%^*()\"\';:\[\]{}0-9]+|[+——！，。？、~@#￥%……&*（）【】；：《》—’]+"

sign = sign.decode("utf8")
ss = "".decode("utf8")

for i in content2:
	i = i.decode("utf8")
	line = re.sub(sign, ss, i) 
	seg = jieba.cut(line)
	string = ' '.join(seg) + '\n'
	f.write(string)

f.close()


########################词频统计##########################
import re
import jieba
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

f = open('/Users/wdw/Desktop/work/data/data_word_freq_tousu.txt','w')

sign = "[\s+\.\!\/_,$%^*()\"\';:\[\]{}0-9]+|[+——！，。？、~@#￥%……&*（）【】；：《》—’]+"

sign = sign.decode("utf8")
ss = "".decode("utf8")
result = {}

for i in content2:
	i = i.decode("utf8")
	line = re.sub(sign, ss, i) 
	seg = jieba.cut(line)
	st = ','.join(seg) 
	str_list = st.split(",")
	for w in str_list:
		if not result.has_key(w):
			result[w] = 0
		result[w] +=  str_list.count(w) 

for o in result:
	ss = o + "\t" + str(result[o]) + "\n"
	f.write(ss)

f.close()



#################关键词提取(TF/IDF)###############
import re
import os
import sys
import jieba
import jieba.analyse
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf-8')

os.chdir('/Users/wdw/Desktop/work/code') #更改当前工作路径

f = open('/Users/wdw/Desktop/work/data/data_tags.txt','w')

sign = "[\s+\.\!\/_,$%^*()\"\';:\[\]{}0-9]+|[+——！，。？、~@#￥%……&*（）【】；：《》—’]+"

sign = sign.decode("utf8")
ss = "".decode("utf8")

for i in content2:
	i = i.decode("utf8")
	line = re.sub(sign, ss, i) 
	seg = jieba.analyse.extract_tags(line, topK=6, withWeight=False, allowPOS=())
	string = '	'.join(seg) + '\n'
	f.write(string)

f.close()


#################词性标注###############
import re
import os
import sys
import jieba
import jieba.posseg as pseg
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf-8')

os.chdir('/Users/wdw/Desktop/work/code') #更改当前工作路径

f = open('/Users/wdw/Desktop/work/data/data_flag.txt','w')

sign = "[\s+\.\!\/_,$%^*()\"\';:\[\]{}0-9]+|[+——！，。？、~@#￥%……&*（）【】；：《》—’]+"

sign = sign.decode("utf8")
ss = "".decode("utf8")

for i in content2:
	i = i.decode("utf8")
	line = re.sub(sign, ss, i) 
	seg = pseg.cut(line)
	string = ''
	for w in seg:
		string += (w.word + w.flag)
	string += '\n'
	f.write(string)

f.close()


'''
con_seg =[] # 建立分词结果文本数组

for i in content:
	seg = jieba.cut(i)
	arr = '/'.join(seg)
	con_seg.append(arr.split('/'))  

with open('/Users/wdw/Desktop/work/data/seg.txt','w') as f:
	f.write(str(con_seg))
'''








