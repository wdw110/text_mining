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


#################客户意见库样例#################
import re

format_base = ['咨询-电费-过高','咨询-电量','咨询-电价','咨询-电费','报修-停电','营业厅-地址-咨询','装置-线路-故障','客户-重复-报修','设置-密码','咨询-发票-打印','咨询-抄表-日期','工作人员-态度-差','银行-代收-咨询','抄表-误差','短信-提醒','咨询-峰谷-电价']

dict1 = {
'咨询':['咨询','查询','询问','质询','查'],
'电费':['电费'],
'过高':['过高','偏高','高','增高','突增','增多','过多','升高','突高','高于','变高','明显增加','多倍'],
'电量':['电量'],
'电价':['电价','单价','价格','资费'],
'报修':['报修'],
'营业厅':['营业厅','营业网点','营业点'],
'地址':['地址','具体地址'],
'装置':['装置','电表','点表','采集器','互感器','终端','接收器','表计'],
'线路':['线路','电线','进户线','接户线','电路','线头','电缆线','母线','接线柱','表线','户线','高压线','输电线','排线','连接处','铜丝','熔丝'],
'重复':['重复','同工单','合并','已派','前次','催办','同单'],
'设置':['设置','初始化','初始'],
'发票':['发票','普通发票','专用发票'],
'打印':['打印','打印发票','清单','传真','开具'],
'日期':['日期','周期','截止日','周期时间','起止日期'],
'工作人员':['人员','师傅','公司员工','施工人员'],
'态度':['态度','语气','认真负责','热情','认真','服务态度','细致','友好','蛮横','生硬','熟练','积极'],
'差':['差','不好','很差','冷漠','不耐烦','不佳','语气','辱骂','较差','冷淡','生硬','强硬','争吵','蛮横','嘈杂','极差','听不清','不太好','脏话','恶劣','不号','谩骂','较弱','听不见','答非所问','断断续续','推诿'],
'银行':['银行','建设银行','工商银行','银行卡','招商银行','邮储','招行','邮政储蓄','建行','交通银行','邮政','网上支付','分行','农业银行','存折','工商','华夏银行','中国农业银行','交行','民生银行','中国银行','中信银行','农行','中国工商银行','工行','中国民生银行','中国建设银行','浦发银行'],
'密码':['密码','初始化','初始密码'],
'代收':['代收','代缴','代售点','代收','代售','代购','代交','代扣','代收费','缴纳'],
'抄表':['抄表','超表','月表','示数','实数'],
'误差':['误差','相减','差额','微小','等于','远大于','准确度','差距','相差','少抄','相差太大','差别','多现','铁损','多度','远远','多多','少于'],
'提醒':['提醒','短信','终止','取消','发错','错发','发件','错收','接收','催费','订阅','催缴','催缴单','订购','退订','收到','催交','催费单'],
'峰谷':['峰谷','峰时','分谷','时段','谷时','为峰','分时','峰','谷','谷峰','平谷','峰值','亮谷','为谷','峰灯','谷灯']
}

f = open('/Users/wdw/Desktop/work/data/data.txt','r')
res = open('/Users/wdw/Desktop/work/data/data_format.txt','w')

for line in	f.readlines():
	for word1 in format_base:
		word1_string = re.sub(r'-','|',word1)
		word2_list = re.findall(word1_string,line)
		if len(word2_list) == len(word1.split('-')):
			string += word1 + '\t'
	res.write(string + '\n')

res.close()
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








