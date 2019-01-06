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

sourceFilePath = './step-2-result.csv'
resultFilePath = './step-3-4-result.csv'

print('Starting crawling more doctor info ...')

counter = 0
personalWebDict = dict()

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(['医生姓名','职称','科室',
                                        '擅长','执业经历']))
        for row in sf:

            [n,i,p,l] = row.strip().split(defaultSeperator)
            counter+=1
            print('No '+str(counter)+', Crawling more info of '+n+', '+l)
            if p=='':
                continue

            try:                
                res1 = requests.get(p, headers=defaultHeaders)
                soup1 = BeautifulSoup(res1.text,'html.parser')
                name_ocp   = defaultSeperator.join(soup1.select('h3.doc_name')[0].text.strip().split('  '))
                department = '-'.join([p.text for p in soup1.select('div.doc_hospital')[0].select('p > a')])

                popLink = p+'api/index/ajaxdoctorintro?uname='+re.search('https://(.*).haodf.com/',p).group(1)
                res2 = requests.get(popLink, headers=defaultHeaders)
                soup2 = BeautifulSoup(res2.text,'html.parser')
                strength_exp = defaultSeperator.join([' '.join(h.text.strip().split()) for h in soup2.select('p.hh')])

                rf.write('\n'+defaultSeperator.join([name_ocp,department,strength_exp]))

            except Exception as e:
                traceback.print_exc()
                exit(1)

            sleep(float(wait))

print('Finished crawling more doctor info.\n')
