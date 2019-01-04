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

# sourceFilePath = 'D:/haodfdata/step-2-result.csv'
# resultFilePath = 'D:/haodfdata/step-3-1-result.csv'
sourceFilePath = './step-2-result.csv'
resultFilePath = './step-3-1-result.csv'

# CRAWL OFFLINE COMMENT DATA

print('Starting crawling offline comments data ...')

counter = 0
personalWebDict = dict()

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        resultHeaders = [ '医生姓名','医生ID','患者','时间','所患疾病',
                          '看病目的','治疗方式','疗效','态度',
                          '选择该医生就诊的理由','本次挂号途径','目前病情状态',
                          '本次看病费用总计','分享','该患者的其他分享' ]

        rf.write(defaultSeperator.join(resultHeaders))

        for row in sf:

            # REMOVE ME
            # if counter%100 != 0:
            #     counter += 1
            #     continue
            # END

            [n,i,p,l] = row.strip().split(defaultSeperator)
            counter+=1
            print('No '+str(counter)+', Crawling offline comments of '+n+', '+l)
            if l=='':
                continue

            stop   = False
            pageNo = 0

            while not stop:

                # next page
                pageNo += 1

                # REMOVE ME
                # if (pageNo > 1):
                #     stop = True
                #     break
                # END

                pageUrl = l+'?p='+str(pageNo)
                try:
                    res = requests.get(pageUrl, headers=defaultHeaders)
                    soup = BeautifulSoup(res.text,'html.parser')
                    commentTables = soup.select('[class=doctorjy]')

                    # stop on empty comments
                    if (len(commentTables) == 0):
                        stop = True
                        break

                    # sleep(float(wait))                

                    for st in commentTables:

                        patientDetails = st.select('[class=dlemd]')[0].select('td')
                        patientComment = st.select('[class=spacejy]')[0]
                        clinicDetails  = st.select('table')[1].select('tr')[2].select('div')

                        infoMap = {
                            '患者': '',
                            '时间': '',
                            '所患疾病': '',
                            '看病目的': '',
                            '治疗方式': '',
                            '疗效': '',
                            '态度': '',
                            '该患者的其他分享': '',
                            '选择该医生就诊的理由': '',
                            '本次挂号途径': '',
                            '目前病情状态': '',
                            '本次看病费用总计': ''
                        }

                        for pd in patientDetails:
                            pattr = pd.text.strip().split('：')
                            if len(pattr)>1 :
                                infoMap[pattr[0]] = pattr[1]

                        for cd in clinicDetails:
                            cattr = cd.text.strip().split('：')
                            if len(cattr)>1 :
                                infoMap[cattr[0]] = cattr[1]

                        comment = patientComment.text.strip().replace('\n',' ')

                        rf.write('\n'+defaultSeperator.join([n,i,infoMap['患者'],infoMap['时间'],infoMap['所患疾病'],
                                                             infoMap['看病目的'],infoMap['治疗方式'],infoMap['疗效'],
                                                             infoMap['态度'],infoMap['选择该医生就诊的理由'],
                                                             infoMap['本次挂号途径'],infoMap['目前病情状态'],
                                                             infoMap['本次看病费用总计'],comment,infoMap['该患者的其他分享']]))

                except Exception as e:
                    traceback.print_exc()
                    exit(1)

print('Finished crawling offline comments data.\n')
