# Haodf Offline Crawler Scripts

## 项目简介

从 `www.haodf.com` 上获取信息的离线爬虫程序集
运行环境: `python3`

### 文件描述

#### `step-1-doctorReferLinks.py`
```
文件用途: 获取好大夫网站注册医生的信息中心页
输入文件: 无
输出文件: step-1-result.csv
输出内容: 医生姓名,医院科室,信息中心页
```

#### `step-2-doctorMoreLinks.py`
```
文件用途: 由医生的信息中心页获取其个人网站和评价分享链接
输入文件: step-1-result.csv
输出文件: step-2-result.csv
输出内容: 医生姓名,医生ID,个人网站,评价分享链接
```

#### `step-3-1-offlineComments.py`
```
文件用途: 获取患者看病的经验分享
输入文件: step-2-result.csv
输出文件: step-3-1-result.csv
输出内容: 医生姓名,医生ID,患者,时间,所患疾病,看病目的,治疗方式,疗效,态度,选择该医生就诊的理由,本次挂号途径,目前病情状态,本次看病费用总计,分享,该患者的其他分享
```

#### `step-3-2-onlineConsults.py`
```
文件用途: 获取医生在线咨询服务的详细信息
输入文件: step-2-result.csv
输出文件: step-3-2-result.csv
输出内容: 医生姓名,医生ID,医院科室,医生职称,上次在线时间,患者投票数,在线服务患者数,疗效满意度,态度满意度,图文线上门诊价格,图文一问一答价格,电话咨询价格,24小时回复率,24小时接听率,电话咨询评价数,电话咨询综合评分
```

#### `step-3-3-phoneConsultComments.py`
```
文件用途: 获取用户对医生电话咨询服务的评价
输入文件: step-3-2-result.csv
输出文件: step-3-3-result.csv
输出内容: 医生姓名,医生ID,用户名,第几次使用电话咨询,评价标签,评价文字内容,通话时间
```

#### `step-3-4-doctorInfo.py`
```
文件用途: 获取医生个人详细信息
输入文件: step-2-result.csv
输出文件: step-3-4-result.csv
输出内容: 医生姓名,职称,科室,擅长,执业经历
```

#### `step-3-5-appointmentTime.py`
```
文件用途: 获取医生可预约时间信息
输入文件: step-2-result.csv
输出文件: step-3-5-result.csv
输出内容: 医生姓名,科室,最近可约时间
```

## 如何运行

#### 安装 python 工具包
```
pip3 install -r requirements.txt
```

#### 修改输入输出文件路径
```
sourceFilePath=<输入文件路径(默认为程序文件夹)>
resultFilePath=<输出文件路径(默认为程序文件夹)>
```

#### 运行程序
```
python3 <程序名>.py
```

## 常用技巧

#### 程序由于网络原因中断了怎么办?
首先备份已获取的数据, 然后通过命令行打印出的日志找到中断点, 将输入文件中已处理的部分删除(删除之前请备份), 重新运行文件

#### 每次都要运行所有文件吗?
由于`step-1`, `step-2`的数据变化不大, 一般情况下不必全部重新运行, 结果已上传.

建议使用如下方法运行前两步:

1. 首先运行 `step-1`
2. 通过如下命令查看 `step-1` 数据变化
```
git diff step-1-result.csv
```
3. 然后只对不同的结果运行 `step-2`
