#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import requests
import traceback

# Global Variables

wait = 1
defaultHeaders = {'User-Agent': ''}
defaultSeperator = ','

sourceFilePath = './step-2-result.csv'
resultFilePath = './step-3-5-result.csv'

print('Starting crawling appointment time ...')

counter = 0
personalWebDict = dict()

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(['医生姓名','医生ID','科室','最近可约时间','信息中心页','地区']))
        for row in sf:

            # [n,i,p,l,dp,il,rg] ~= [医生姓名,医生ID,个人网站,评价分享链接,医院科室,信息中心页,地区]
            [n,i,p,l,dp,il,rg] = row.strip().split(defaultSeperator)
            if i=='':
                continue
            counter+=1
            print('No '+str(counter)+', Crawling more info of '+n+', '+i)

            jiahaoLink = 'https://jiahao.haodf.com/info_'+i+'.html'
            try:                
                res = requests.get(jiahaoLink, headers=defaultHeaders)
                soup = BeautifulSoup(res.text,'html.parser')
                department = '-'.join([p.text for p in soup.select('div.doc_hospital')[0].select('p > a')])
                aptTime = ''
                aptBlock = soup.select('p.r-c-i-result > span')
                if len(aptBlock) > 0:
                    aptTime = aptBlock[0].text.strip()

                rf.write('\n'+defaultSeperator.join([n,i,department,aptTime,il,rg]))

            except Exception as e:
                traceback.print_exc()
                exit(1)

            sleep(float(wait))

print('Finished crawling appointment time.\n')
