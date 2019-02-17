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
resultFilePath = './step-3-7-result.csv'

print('Starting crawling more doctor info ...')

counter = 0
personalWebDict = dict()

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(['医生姓名','医生ID','科室',
                                        '近期通话',
                                        '信息中心页','地区']))
        for row in sf:

            # [n,i,p,l,dp,il,rg] ~= [医生姓名,医生ID,个人网站,评价分享链接,医院科室,信息中心页,地区]
            [n,i,p,l,dp,il,rg] = row.strip().split(defaultSeperator)
            counter+=1
            if p=='':
                continue

            print('No '+str(counter)+', Crawling recent calls of '+n+', '+p)

            try:
                res = requests.post(p+'/api/flow/ajaxgettelvisitinfos', 
                                     json={'uname': re.search('https://(.*).haodf.com/',p).group(1)},
                                     headers=defaultHeaders)
                soup = BeautifulSoup(res.text,'html.parser')
                recentCalls = secondarySeperator.join([li.text for li in soup.select('#vertical-ticker > li')])
                rf.write('\n'+defaultSeperator.join([n,i,dp,recentCalls,il,rg]))

            except Exception as e:
                traceback.print_exc()
                exit(1)

            sleep(float(wait))

print('Finished crawling more doctor info.\n')
