# coding:utf-8
# 字幕下载结果输出到log文档
from zimuku.yyzm.config import *
import os
import datetime

time1 = datetime.datetime.now()
time = str(time1)[11:16].replace(':', '-')
print(time)
print('正在执行：' + KEYWORD1 + FILEPATH + 'download.py')
os.system('python \"{0}\" 1>>log{1}.txt 2>&1'.format(FILEPATH + 'download.py', KEYWORD1 + time))
time2 = datetime.datetime.now()
print('执行完成！', (time2 - time1).seconds)
