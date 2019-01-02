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

# sourceFilePath = 'D:/haodfdata/step-1-result.csv'
# resultFilePath = 'D:/haodfdata/step-2-result.csv'
sourceFilePath = './step-1-result.csv'
resultFilePath = './step-2-result.csv'

print('Starting crawling more doctor links ...')

counter = 0
personalWebDict = dict()

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(['医生姓名','医生ID','个人网站','评价分享链接']))

        for row in sf:

            [n,d,l] = row.strip().split(defaultSeperator)
            counter+=1
            print('No '+str(counter)+', Crawling more links of '+n+', '+l)

            try:
                personalWeb = ''
                doctorID = ''
                offlineCommentLink = ''

                # CRAWL PERSONAL WEBSITE LINKS
                res = requests.get(l, headers=defaultHeaders)
                personalWebMatch = re.search('<a class=blue href="(\/\/.+\.haodf\.com\/)', res.text)

                if personalWebMatch:
                    personalWeb = 'https:'+personalWebMatch.group(1)

                    if personalWeb in personalWebDict:
                        print('+++++++++++++++++++++',n,personalWeb)
                        continue
                    else:
                        personalWebDict[personalWeb] = True
                        
                        # CRAWL DOCTOR ID
                        sleep(float(wait))
                        clinicLink = personalWeb+'clinic/selectclinicservice'
                        r = requests.head(clinicLink, headers=defaultHeaders)
                        doctorID = re.search('host_user_id=(\d+)\&', r.headers.get('Location') ).group(1)
                        
                        # CRAWL OFFLINE COMMENT LINKS
                        sleep(float(wait))
                        jingyanLink = l.replace('.htm','/jingyan/1.htm')
                        offlineCommentLink = 'https:'+requests.head(jingyanLink, headers=defaultHeaders).headers.get('Location')

                rf.write('\n'+defaultSeperator.join([n,doctorID,personalWeb,offlineCommentLink]))

            except Exception as e:
                traceback.print_exc()
                exit(1)

print('Finished crawling more doctor links.\n')
