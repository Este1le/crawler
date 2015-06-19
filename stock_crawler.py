# -*- coding: utf-8 -*-  
import urllib2
import re
import time
import os
ISOTIMEFORMAT='%Y-%m-%d %X'


def stock163(num):

	checkup = urllib2.urlopen('http://quotes.money.163.com/stocksearch/json.do?count=10&word=' + num).read()
	pchecktype = re.compile(r'\"type\":\"(\w+)\"')
	pchecksym = re.compile(r'\"symbol\":\"(\d+)\"')
	basetype = pchecktype.search(checkup)
	basesym = pchecksym.search(checkup)
	

	if basesym:
		basecode = basesym.group(1)
		stype = basetype.group(1)
		if(stype == 'SZ'):
			basecode = '1' + basecode
		elif(stype == 'SH'):
			basecode = '0' + basecode
		else:
			print "非股票类型，请重新输入"
			return
	else:
		print "股票不存在请重新输入。"
		return

	url = 'http://quotes.money.163.com/' + basecode + '.html'

	fname = basecode + '.html'
	sname = ''
	f = open(fname,'w+')

	try:
		m = urllib2.urlopen(url)

	except urllib2.URLError, e:
		if(e.code == 404):
			url = 'http://quotes.money.163.com/fund/' + num + '.html'
			m = urllib2.urlopen(url)

	mm = m.read()
	f.write(mm)
	f.close()

	f = open(fname,"r")
	lines = f.readlines()
	for i in lines:
		p = re.compile(r'<title>(.*)\x88')
		m = p.match(i)

		if m:
			sname = m.group(1)
			print "您选择的股票是  "  + sname
			break

	print '正在下载请求的页面......'
	
	j = 0

	f = open(sname[:-2]+".txt","a+")

	f.write(time.strftime(ISOTIMEFORMAT, time.localtime()))
	f.write('\n\n')

	for i in lines:
		pinfo = re.compile(r'window.stock_info = {')
		minfo = pinfo.match(i.strip())

		if minfo:
			pname = re.compile(r"name: \'(.*)\',")
			mname = pname.match(lines[j + 1].strip())
			name = "股票: " + mname.group(1)
			f.write(name)
			f.write('\n')

			pcode = re.compile(r"code: \'(.*)\',")
			mcode = pcode.match(lines[j + 2].strip())
			code = "code: " + mcode.group(1)
			f.write(code)
			f.write('\n')

			pprice = re.compile(r"price: \'(-*.*)\',")
			mprice = pprice.match(lines[j + 3].strip())
			price = "现价: " + mprice.group(1)
			f.write(price)
			f.write('\n')

			pchange = re.compile(r"change: \'(-*.*)\',")
			mchange = pchange.match(lines[j + 4].strip())
			change = "涨跌幅: " + mchange.group(1)
			f.write(change)
			f.write('\n')
            
			pyesteday = re.compile(r"yesteday: \'(-*.*)\',")
			myesteday = pyesteday.match(lines[j + 5].strip())
			yesteday = "昨收: " + myesteday.group(1)
			f.write(yesteday)
			f.write('\n')

			ptoday = re.compile(r"today: \'(-*.*)\',")
			mtoday = ptoday.match(lines[j + 6].strip())
			today = "今开: " + mtoday.group(1)
			f.write(today)
			f.write('\n')

			phigh = re.compile(r"high: \'(-*.*)\',")
			mhigh = phigh.match(lines[j + 7].strip())
			high = "最高: " + mhigh.group(1)
			f.write(high)
			f.write('\n')

			plow = re.compile(r"low: \'(-*.*)\',")
			mlow = plow.match(lines[j + 8].strip())
			low = "最低: " + mlow.group(1)
			f.write(low)
			f.write('\n')
			j = j + 1
			continue

		pinfo1 = re.compile(r'\xe5\x9f\xba\xe6\x9c\xac\xe6\xaf\x8f\xe8\x82\xa1\xe6\x94\xb6\xe7\x9b\x8a')
		minfo1 = pinfo1.search(i.strip())
		if minfo1:
			ptime = re.compile(r"<th >(\d{4}-\d{2}-\d{2})<\/th>")
			mtime = ptime.findall(lines[j - 4].strip())
			f.writelines('                  ')
			for t in range(len(mtime)):
				f.writelines(mtime[t] + '     ')
			f.writelines('\n')

			f.write('基本每股收益(元)')
			pj = re.compile(r'<td[ class=\'cRed\']*>(-*\d+\.\d*)</td>')
			mj = pj.findall(lines[j + 1].strip())
			for t in range(len(mj)):
				if t == 0:
					f.writelines('      ' + mj[t])
				else:
					f.writelines('           ' + mj[t])
			f.writelines('\n')
			j = j + 1
			continue
		
		pinfo2 = re.compile(r'\xe6\xaf\x8f\xe8\x82\xa1\xe5\x87\x80\xe8\xb5\x84\xe4\xba\xa7')
		minfo2 = pinfo2.search(i.strip())
		if minfo2:
			f.write('每股净资产(元)')
			pmg = re.compile(r'<td[ class=\'cRed\']*>(-*\d+\.\d*)</td>')
			mmg = pmg.findall(lines[j + 1].strip())
			for t in range(len(mmg)):
				if t == 0:
					f.writelines('        ' + mmg[t])
				else:
					f.writelines('          ' + mmg[t])
			f.writelines('\n')
			j = j + 1
			continue

		pinfo3 = re.compile(r'\xe6\xaf\x8f\xe8\x82\xa1\xe7\xbb\x8f\xe8\x90\xa5\xe6\xb4\xbb\xe5\x8a\xa8\xe4\xba\xa7\xe7\x94\x9f')
		minfo3 = pinfo3.search(i.strip())
		if minfo3:
			f.write('每股经营活动产生的\n现金流量净额(元)')
			pmgj = re.compile(r'<td[ class=\'cRed\']*>(-*\d+\.\d*)</td>')
			mmgj = pmgj.findall(lines[j + 1].strip())
			for t in range(len(mmgj)):
				if t == 0:
					f.writelines('      ' + mmgj[t])
				else:
					f.writelines('           ' + mmgj[t])
			f.writelines('\n')
			j = j + 1
			continue

		pinfo4 = re.compile(r'\xe5\x87\x80\xe8\xb5\x84\xe4\xba\xa7\xe6\x94\xb6\xe7\x9b\x8a\xe7\x8e\x87\xe5\x8a\xa0\xe6\x9d\x83')
		minfo4 = pinfo4.search(i.strip())
		if minfo4:
			f.write('净资产收益率加权(%)')
			pjz = re.compile(r'<td>(-*\d+\.\d*)</td>')
			mjz = pjz.findall(lines[j + 1].strip())
			for t in range(len(mjz)):
				if t == 0:
					f.writelines('    ' + mjz[t])
				else:
					f.writelines('          ' + mjz[t])
			f.writelines('\n')
			j = j + 1
			continue

		pinfo5 = re.compile(r'\xe4\xb8\xbb\xe8\x90\xa5\xe4\xb8\x9a\xe5\x8a\xa1\xe6\x94\xb6\xe5\x85\xa5')
		minfo5 = pinfo5.search(i.strip())
		if minfo5:
			f.write('主营业务收入(万元)')
			pzy = re.compile(r'<td>(-*[\d,]*)</td>')
			mzy = pzy.findall(lines[j + 1].strip())
			for t in range(len(mzy)):
				if t == 0:
					f.writelines('    ' + mzy[t])
				else:
					f.writelines('     ' + mzy[t])
			f.writelines('\n')
			j = j + 1
			continue

		pinfo6 = re.compile(r'\xe4\xb8\xbb\xe8\x90\xa5\xe4\xb8\x9a\xe5\x8a\xa1\xe5\x88\xa9\xe6\xb6\xa6')
		minfo6 = pinfo6.search(i.strip())
		if minfo6:
			f.write('主营业务利润(万元)')
			pzyl = re.compile(r'<td>(-*[\d,]*)</td>')
			mzyl = pzyl.findall(lines[j + 1].strip())
			for t in range(len(mzyl)):
				if t == 0:
					f.writelines('    ' + mzyl[t])
				else:
					f.writelines('      ' + mzyl[t])
			f.writelines('\n')
			j = j + 1
			continue

		pinfo7 = re.compile(r'\xe8\x90\xa5\xe4\xb8\x9a\xe5\x88\xa9\xe6\xb6\xa6')
		minfo7 = pinfo7.search(i.strip())
		if minfo7:
			f.write('营业利润(万元)')
			pyyl = re.compile(r'<td>(-*[\d,]*)</td>')
			myyl = pyyl.findall(lines[j + 1].strip())
			for t in range(len(myyl)):
				if t == 0:
					f.writelines('        ' + myyl[t])
				else:
					f.writelines('      ' + myyl[t])
			f.writelines('\n')
			j = j + 1
			continue
		
		pinfo8 = re.compile(r'\xe5\x87\x80\xe5\x88\xa9\xe6\xb6\xa6\x28\xe4\xb8\x87\xe5\x85\x83\x29')
		minfo8 = pinfo8.search(i.strip())
		if minfo8:
			f.write('净利润(万元)')
			pjl = re.compile(r'<td>(-*[\d,]*)</td>')
			mjl = pjl.findall(lines[j + 1].strip())
			for t in range(len(mjl)):
				if t == 0:
					f.writelines('          ' + mjl[t])
				else:
					f.writelines('      ' + mjl[t])
			f.writelines('\n')
			j = j + 1
			continue

		j = j+1
		
	f.write('\n\n\n\n\n')
	os.remove('./'+fname)
	print "股票信息已写入文件    " + sname[:-2] + ".txt."


if __name__ == "__main__":

	print "Welcome!\n"

	while True:
		stockurl = raw_input('请输入您的股票代码或股票名（如000001，平安银行；600000，浦发银行）:\n')
		stock163(stockurl)
		choice = raw_input("输入任意键继续，输入q退出:")
		if (choice == 'q' or choice == 'Q'):
			print "谢谢使用！"
			break
		else:
			continue