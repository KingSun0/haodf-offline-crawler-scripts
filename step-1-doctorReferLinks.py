#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import re
import requests
import traceback

# Global Variables

wait = 1
prov = 'shanghai'
defaultHeaders = {'User-Agent': ''}
defaultSeperator = ','

# resultFilePath = 'D:/haodfdata/step-1-result.csv'
resultFilePath = './step-1-result.csv'

# GRAB HOSPITAL DATA
# https://www.haodf.com/sitemap-ys/prov_shanghai_1

print('Starting crawling hospital pages ...')

stop   = False
pageNo = 0
hospitals = dict()

while not stop:

    # next page
    pageNo += 1
    print('Crawling ' + prov + ' hospital page ' + str(pageNo))

    sourceUrl = 'https://www.haodf.com/sitemap-ys/prov_' + prov + '_' + str(pageNo)

    try:

        res = requests.get(sourceUrl, headers=defaultHeaders)

        # stop on empty shares
        if not bool(re.search('/sitemap-ys/hos', res.text)):
            stop = True
            break

        soupH = BeautifulSoup(res.text,'html.parser')
        hospitalList = soupH.select('li')[1].select('a')

        for h in hospitalList:
            hospitals[h.text] = 'https://www.haodf.com'+h['href']

    except Exception as e:
        traceback.print_exc()
        exit(1)

print('Finished crawling hospital pages, totally '+str(len(hospitals.keys()))+' hospitals collected.\n')

# GRAB DEPARTMENT DATA
print('Starting crawling department pages ...')

desiredDepartmentKeywords  = ['骨','儿科']
departments = dict()
counter = 0

for h,l in hospitals.items():

    sleep(float(wait))
    counter+=1
    print('No '+str(counter)+', Crawling departments in '+h)

    try:

        res = requests.get(l, headers=defaultHeaders)
        soupD = BeautifulSoup(res.text,'html.parser')
        dList = soupD.select('li')[0].select('a')

        for d in dList:
            needed = False
            for dkey in desiredDepartmentKeywords:
                if dkey in d.text:
                    needed = True
            if needed:
                print('Crawling link of ' + h + ' ' + d.text)
                departments['-'.join([h,d.text])] = 'https://www.haodf.com'+d['href']

    except Exception as e:
        traceback.print_exc()
        exit(1)

print('Finished crawling department pages, totally '+str(len(departments.keys()))+' departments collected.\n')

# GRAB DOCTOR INFO PAGE DATA
print('Starting crawling doctor info links ...')

doctorInfoPages = dict()
counter = 0

with open(resultFilePath, "w") as f:

    f.write(defaultSeperator.join(['医生姓名','医院科室','信息中心页']))

    for d,l in departments.items():

        sleep(float(wait))
        counter+=1
        print('No '+str(counter)+', Crawling doctors in '+d)

        try:

            res = requests.get(l, headers=defaultHeaders)
            soupDI = BeautifulSoup(res.text,'html.parser')
            lList = soupDI.select('li')
            if len(lList)==0:
                continue
            diList = soupDI.select('li')[0].select('a')

            for di in diList:
                print('Crawling link of ' + d + ' ' + di.text)
                f.write('\n'+defaultSeperator.join([di.text, d, 'https:'+di['href']]))

        except Exception as e:
            traceback.print_exc()
            exit(1)

print('Finished crawling doctor info links.\n')
