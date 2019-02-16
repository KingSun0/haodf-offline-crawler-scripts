#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import re
import requests
import traceback

# Global Variables

wait = 1
defaultHeaders = {'User-Agent': ''}
defaultSeperator = ','
secondarySeperator = '|'

sourceFilePath = './step-2-result.csv'
resultFilePath = './step-3-4-result.csv'

def decodeHtml(text):
    return text.replace('\\n','\n')\
               .replace('\\t','\t')\
               .replace('\\"','"')\
               .replace('\\/','/')

print('Starting crawling more doctor info ...')

counter = 0
personalWebDict = dict()

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(['医生姓名','职称','科室','擅长','执业经历',
                                        '医生热度','患者投票详情','患者分享统计',
                                        '信息中心页','地区']))
        for row in sf:

            # [n,i,p,l,dp,il,rg] ~= [医生姓名,医生ID,个人网站,评价分享链接,医院科室,信息中心页,地区]
            [n,i,p,l,dp,il,rg] = row.strip().split(defaultSeperator)
            counter+=1
            print('No '+str(counter)+', Crawling more info of '+n+', '+l)

            ddep = ''
            docp = ''
            dstg = ''
            dexp = ''
            dhot = ''
            dvot = ''
            dsha = ''

            try:

                # 医生信息中心页
                res0 = requests.get(il, headers=defaultHeaders)

                # 医生基本信息板块
                doctorAbout = re.search(r'\<div class=\\\"doctor_about\\\"\>.*\<div class=\\\"middletr\\\"\>.*?(\<table.*?)\<\!\-\-0125',res0.text).group(1)
                doctorAbout = decodeHtml(doctorAbout)
                dATrList = BeautifulSoup(doctorAbout,'html.parser').select('tr')

                for tr in dATrList:
                    cList = tr.select('td')
                    if len(cList) > 1:
                        item = cList[1].text.encode().decode('unicode-escape')
                        if item == '科　　室：':
                            ddep = cList[2].select('a')[0].text.strip().encode().decode('unicode-escape')
                        elif item == '职　　称：':
                            docp = cList[2].text.strip().encode().decode('unicode-escape')
                        elif item == '擅　　长：':
                            fullDS = cList[2].select('#full_DoctorSpecialize')
                            if len(fullDS) > 0:
                                dstg = fullDS[0].text.strip().encode().decode('unicode-escape')
                        elif item == '执业经历：':
                            fullExp = cList[2].select('#full')
                            if len(fullExp) > 0:
                                dexp = fullExp[0].text.strip().encode().decode('unicode-escape').replace('<< 收起','')

                # 医生热度板块
                dhot = re.search(r'\<p class=\\\"r\-p\-l\-score\\\"\>(.*?)\<',res0.text).group(1).strip()

                # 医生患者投票板块
                doctorVote = re.search(r'"id":"bp_doctor_getvote".*?\<div class=\\\"doctor_panel\\\"\>.*(\<div class=\\\"middletr\\\"\>.*?)\<div class=\\\"bottomtr\\\"\>',res0.text).group(1)
                doctorVote = decodeHtml(doctorVote)
                ltDivLinks = BeautifulSoup(doctorVote,'html.parser').select('.ltdiv')[0].select('a')
                dvot = ''.join([a.text.strip().encode().decode('unicode-escape').replace('评价/投票','').replace('票','票'+secondarySeperator).replace('查看两年前患者投票'+secondarySeperator+'(','两年前患者投票').replace('票'+secondarySeperator+')>>','票') for a in ltDivLinks])

                # 医生患者分享板块
                doctorShare = re.search(r'"id":"bp_doctor_share".*?\<div class=\\\"doctor_panel\\\"\>.*(\<div class=\\\"toptr\\\".*?)\<div class=\\\"middletr\\\"\>',res0.text).group(1)
                doctorShare = decodeHtml(doctorShare)
                ltDivs = BeautifulSoup(doctorShare,'html.parser').select('.lt > div')
                dsha = ''.join([div.text.strip().encode().decode('unicode-escape').replace('\n','').replace(')',')'+secondarySeperator) for div in ltDivs])

                rf.write('\n'+defaultSeperator.join([n,docp,ddep,dstg,dexp,dhot,dvot,dsha,il,rg]))

            except Exception as e:
                traceback.print_exc()
                exit(1)

            sleep(float(wait))

print('Finished crawling more doctor info.\n')
