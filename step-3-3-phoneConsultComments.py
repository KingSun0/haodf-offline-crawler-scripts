#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import re
import requests
import traceback

# Global Variables

wait = 1
defaultHeaders = {'User-Agent':'', 'Cookie':'newaskindex=1'}
defaultSeperator = ','

# sourceFilePath = 'D:/haodfdata/step-3-2-result.csv'
# resultFilePath = 'D:/haodfdata/step-3-3-result.csv'
sourceFilePath = './step-3-2-result.csv'
resultFilePath = './step-3-3-result.csv'

# CRAWL ONLINE CONSULTS DATA

print('Starting crawling phone consult comments data ...')

counter = 0

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        resultHeaders = [ '医生姓名','医生ID',
                          '用户名','第几次使用电话咨询',
                          '评价标签','评价文字内容','通话时间' ]

        rf.write(defaultSeperator.join(resultHeaders))

        for row in sf:

            # REMOVE ME
            # if counter%100 != 0:
            #     counter += 1
            #     continue
            # END

            rList = row.strip().split(defaultSeperator)
            docName   = rList[0]
            docID     = rList[1]
            totalEval = rList[14]
            counter+=1
            print('No '+str(counter)+', Crawling phone consult comments of '+docName+', '+docID)
            if totalEval=='':
                continue

            stop   = False
            pageNo = 0

            while not stop:

                # next page
                pageNo += 1

                # REMOVE ME
                # if (pageNo > 2):
                #     stop = True
                #     break
                # END

                pageUrl = 'https://zixun.haodf.com/payment/ajaxjudgelist?userid=' + str(docID) + '&nowPage=' + str(pageNo)

                try:
                    res = requests.get(pageUrl, headers=defaultHeaders)
                    soup = BeautifulSoup(res.text,'html.parser')
                    evals = soup.select('[class=evaluate_information]')

                    # stop on empty shares
                    if (len(evals) == 0):
                        stop = True
                        break

                    sleep(float(wait))

                    for ev in evals:
                        # [ '用户名','第几次使用电话咨询','评价标签','评价文字内容','通话时间' ]
                        userName    = ev.select('[class=username]')[0].text
                        numUsage    = ev.select('[class=use_product_information]')[0].text.replace('第','').replace('次使用电话咨询','')
                        evalTags    = '|'.join([et.text for et in ev.select('[class=evaluate_content]')])
                        evalContent = ev.select('[class=user_evaluate_content]')[0].select('span')[0].select('span')[0].text
                        phoneTime   = ev.select('[class=phone_time]')[0].select('span')[0].text

                        rf.write('\n'+defaultSeperator.join([docName,docID,
                                                             userName,numUsage,
                                                             evalTags,evalContent,phoneTime]))
                except Exception as e:
                    traceback.print_exc()
                    exit(1)

print('Finished crawling phone consult comments data.\n')
