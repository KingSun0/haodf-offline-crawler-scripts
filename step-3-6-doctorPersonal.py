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
resultFilePath = './step-3-6-result.csv'

print('Starting crawling more doctor info ...')

counter = 0
personalWebDict = dict()

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(['医生姓名','医生ID','科室',
                                        '个人网站统计','门诊时间','预约挂号统计'
                                        '信息中心页','地区']))
        for row in sf:

            # [n,i,p,l,dp,il,rg] ~= [医生姓名,医生ID,个人网站,评价分享链接,医院科室,信息中心页,地区]
            [n,i,p,l,dp,il,rg] = row.strip().split(defaultSeperator)
            counter+=1
            if p=='':
                continue

            print('No '+str(counter)+', Crawling recent calls of '+n+', '+p)

            try:
                res = requests.get(p, headers=defaultHeaders)
                soup = BeautifulSoup(res.text,'html.parser')
                stats = secondarySeperator.join([li.text for li in soup.select('.space_statistics > li')])
                menzhenTime = soup.select('.menzhen_time')[0].select('tr#scrolltd')[0].text.strip().replace('\n',secondarySeperator)
                pNum = soup.select('font.blue4')[0].text

                rf.write('\n'+defaultSeperator.join([n,i,dp,stats,menzhenTime,pNum,il,rg]))

            except Exception as e:
                traceback.print_exc()
                exit(1)

            sleep(float(wait))

print('Finished crawling more doctor info.\n')
