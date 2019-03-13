#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import re
import requests
import traceback

# Function for hospital data
# https://www.haodf.com/sitemap-ys/prov_shanghai_1

def grabHospitalData(prov):

    hospitals = []
    stop   = False
    pageNo = 0

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
                hospitals.append([prov,h.text,'https://www.haodf.com'+h['href']])

        except Exception as e:
            traceback.print_exc()
            exit(1)

    print('Finished crawling hospital in '+prov+', totally '+str(len(hospitals))+' hospitals collected.\n')

    return hospitals

# Function for department data
# hList ~= [['地区'，'医院名', '医院链接']]

def grabDepartmentData(hList,inDepKeys,exDepKeys,inHosKeys,exHosKeys):

    departments = []
    counter = 0

    for h in hList:

        sleep(float(wait))
        counter+=1
        print('No '+str(counter)+', Crawling departments in '+h[1])

        try:

            res = requests.get(h[2], headers=defaultHeaders)
            soupD = BeautifulSoup(res.text,'html.parser')
            dList = soupD.select('li')[0].select('a')

            for d in dList:

                # 默认不抓取
                needed = False

                # 抓取含有关键字的科室(在144行添加 includedDepartmentKeywords)
                for indkey in inDepKeys:
                    if indkey in d.text:
                        needed = True

                # 剔除含有关键字的科室(在145行添加 excludedDepartmentKeywords)
                for exdkey in exDepKeys:
                    if exdkey in d.text:
                        needed = False

                # 抓取指定医院所有科室(在146行添加 includedHospitalKeywords)
                for inhkey in inHosKeys:
                    if inhkey in h:
                        needed = True

                # 剔除指定医院所有科室(在147行添加 excludedHospitalKeywords)
                for exhkey in exHosKeys:
                    if exhkey in h:
                        needed = False

                # 依据以上逻辑判断运行
                if needed:
                    print('Crawling link of ' + h[1] + ' ' + d.text)
                    departments.append([h[0],'-'.join([h[1],d.text]),'https://www.haodf.com'+d['href']])

        except Exception as e:
            traceback.print_exc()
            exit(1)

    return departments

# Global Variables

wait = 1
defaultHeaders = {'User-Agent': ''}
defaultSeperator = ','

resultFilePath = './step-1-result.csv'

# GRAB HOSPITAL DATA

print('Starting crawling hospital pages ...')

hospitalList = []

# 地区列表
provs = [
    'beijing','shanghai','guangdong',
    'guangxi','jiangsu','zhejiang',
    'anhui','jiangxi','fujian',
    'shandong','sx','hebei',
    'henan','tianjin','liaoning',
    'heilongjiang','jilin','hubei',
    'hunan','sichuan','chongqing',
    'shanxi','gansu','yunnan',
    'xinjiang','neimenggu','hainan',
    'guizhou','qinghai',
    'ningxia','xizang'
]
for prov in provs:
    hospitalList = hospitalList + grabHospitalData(prov)

print('Finished crawling hospital pages, totally '+str(len(hospitalList))+' hospitals collected.\n')

# GRAB DEPARTMENT DATA

print('Starting crawling department pages ...')

includedDepartmentKeywords = ['骨','足','脊柱','手足','手外','关节','伤','运动']
excludedDepartmentKeywords = ['儿','烧','口']
includedHospitalKeywords   = []
excludedHospitalKeywords   = ['儿','妇幼']

departmentList = grabDepartmentData(hospitalList,
                                    includedDepartmentKeywords,
                                    excludedDepartmentKeywords,
                                    includedHospitalKeywords,
                                    excludedHospitalKeywords)

print('Finished crawling department pages, totally '+str(len(departmentList))+' departments collected.\n')

# GRAB DOCTOR INFO PAGE DATA

print('Starting crawling doctor info links ...')

doctorInfoPages = dict()
counter = 0

with open(resultFilePath, "a") as f:

    f.write(defaultSeperator.join(['医生姓名','医院科室','信息中心页','地区']))

    for d in departmentList:

        sleep(float(wait))
        counter+=1
        print('No '+str(counter)+', Crawling doctors in '+d[0]+' '+d[1])

        try:

            res = requests.get(d[2], headers=defaultHeaders)
            soupDI = BeautifulSoup(res.text,'html.parser')
            lList = soupDI.select('li')
            if len(lList)==0:
                continue
            diList = soupDI.select('li')[0].select('a')

            for di in diList:
                print('Crawling link of ' + d[0] + ' ' + d[1] + ' ' + di.text)
                f.write('\n'+defaultSeperator.join([di.text,d[1],'https:'+di['href'],d[0]]))

        except Exception as e:
            traceback.print_exc()
            exit(1)

print('Finished crawling doctor info links.\n')
