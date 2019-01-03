#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import requests
import traceback

# Global Variables

wait = 1
defaultHeaders = {'User-Agent':'', 'Cookie':'newaskindex=1'}
defaultSeperator = ','

# sourceFilePath = 'D:/haodfdata/step-2-result.csv'
# resultFilePath = 'D:/haodfdata/step-3-2-result.csv'
sourceFilePath = './step-2-result.csv'
resultFilePath = './step-3-2-result.csv'

# CRAWL ONLINE CONSULTS DATA

print('Starting crawling online consults data ...')

counter = 0

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        resultHeaders = [ '医生姓名','医生ID','医院科室','医生职称',
                          '上次在线时间','患者投票数','在线服务患者数',
                          '疗效满意度','态度满意度',
                          '图文线上门诊价格','图文一问一答价格','电话咨询价格',
                          '24小时回复率','24小时接听率',
                          '电话咨询评价数','电话咨询综合评分' ]

        rf.write(defaultSeperator.join(resultHeaders))

        for row in sf:

            # REMOVE ME
            # if counter%100 != 0:
            #     counter += 1
            #     continue
            # END

            [docName,docID,p,l] = row.strip().split(defaultSeperator)
            counter+=1
            print('No '+str(counter)+', Crawling online consults of '+docName+', '+docID)
            if docID=='':
                continue

            pageUrl1 = 'https://zixun.haodf.com/newcase/askguidepage?host_user_id='+str(docID)
            pageUrl2 = 'https://zixun.haodf.com/newcase/teldoctorcomments?spaceId='+str(docID)

            try:
                res = requests.get(pageUrl1, headers=defaultHeaders)
                soup1 = BeautifulSoup(res.text,'html.parser')
                doctorDetailBlock = soup1.select('[class=w-doctor-details]')[0]
                doctorDetails = doctorDetailBlock.select('p')

                doctorGrade      = doctorDetails[0].select('[class=doc-grade]')[0].text
                doctorLoc        = doctorDetails[1].text
                lastOnline       = ''
                votePatients     = ''
                onlinePatients   = ''
                performanceScore = ''
                attibuteScore    = ''
                n24hourReply     = ''
                n24hourAnswer    = ''
                totalEval        = ''
                netCasePrice     = ''
                oneCasePrice     = ''
                telCasePrice     = ''
                doctorTelRating  = ''

                if '医生上次在线时间' in doctorDetails[2].text:
                    lastOnline = doctorDetails[2].select('span')[0].text

                doctorScores   = doctorDetailBlock.select('[class=score_fen]')
                votePatients   = doctorScores[0].text
                onlinePatients = doctorScores[1].text
                if len(doctorScores) > 2:
                    performanceScore = doctorScores[2].text
                    attibuteScore    = doctorScores[3].text

                serviceBlock  = soup1.select('[class=service-box]')[0]
                serviceTypes  = serviceBlock.select('[class*=f18]')
                serviceItems  = serviceBlock.select('[class*=js-service-item]')
                serviceToSee  = serviceBlock.select('[class=fr]')
                
                if len(serviceTypes) > 0:

                    for t in serviceTypes:
                        title = t.select('[class=title-flag]')[0].text
                        scoreList = t.select('[class=score_fen]')
                        if len(scoreList) > 0:
                            s = scoreList[0].text
                            if title == '图文':
                                n24hourReply = s
                            elif title == '电话':
                                n24hourAnswer = s

                if len(serviceItems) > 0:

                    for i in serviceItems:
                        itemTitle = i.select('[class=service-name-title]')[0].text
                        itemPrice = i.select('[class=service-name-price]')[0].text
                        if itemTitle == '线上门诊':
                            netCasePrice = itemPrice
                        elif itemTitle == '一问一答':
                            oneCasePrice = itemPrice
                        elif itemTitle == '电话咨询':
                            telCasePrice = itemPrice

                if len(serviceToSee) > 0:

                    totalEval = serviceToSee[0].select('[class=score_fen]')[0].text

                    # doctor tel rating from another page
                    sleep(float(wait))
                    res = requests.get(pageUrl2, headers=defaultHeaders)
                    soup2 = BeautifulSoup(res.text,'html.parser')
                    rateScore = soup2.select('[class=score]')
                    if len(rateScore) > 0:
                        doctorTelRating = rateScore[0].text

                rf.write('\n'+defaultSeperator.join([docName,docID,doctorLoc,doctorGrade,
                                                     lastOnline,votePatients,onlinePatients,
                                                     performanceScore,attibuteScore,
                                                     netCasePrice,oneCasePrice,telCasePrice,
                                                     n24hourReply,n24hourAnswer,
                                                     totalEval,doctorTelRating]))

            except Exception as e:
                traceback.print_exc()
                exit(1)

            sleep(float(wait))

print('Finished crawling online consults data.\n')
