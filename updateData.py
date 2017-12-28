# encoding:utf-8
import re
import codecs
import shutil
import zipfile

import asstosrt
import chardet
import rarfile
import os
from zimuku.yyzm.config import *
import pymongo
# from zimuku.download import *
client = pymongo.MongoClient(MONGODB_URL)
db = client[MONGODB_DB]

def read_file(file):
    try:
        with open(file, 'rb') as f:  # 读取文件编码
            coding = chardet.detect(f.read())
            cd = coding.get('encoding')
            print(cd)
            f.close()
        if re.match('GB2312', cd, re.IGNORECASE):  # 编码为GB23112时
            cd = None
        with codecs.open(file, 'r', cd) as cc:
            lines = cc.readlines()
            # print(lines)
            i = 0
            subtitles = []
            time_pattern = re.compile(u'(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})', re.S)
            # 匹配时间模式
            # title_pattern = re.compile('([a-zA-Z0-9.]*?S\d\dE\d\d)')
            title_pattern = re.compile('({0})'.format(SHOWPTN))  # 匹配title模式
            titles = re.findall(title_pattern, file)
            eng_pattern = re.compile('(^[a-zA-Z0-9."\'(-]+)')  # 匹配英语字幕模式,起始位置模式

            while i < len(lines) - 1:  # 要减一
                # 字幕字典需同时包含时间、英文字幕
                if re.search(time_pattern, lines[i + 1]) and re.search(eng_pattern, lines[i + 3]):
                    # match起始位置匹配成功
                    subtitle = {
                        'index': KEYWORD1 + '.' + titles[-1] + '--' + lines[i].replace('\n', '').replace('\r', ''),
                        'time': lines[i + 1].replace('\n', '').replace('\r', ''),
                        'content1': lines[i + 2].replace('\n', '').replace('\r', ''),
                        'content2': lines[i + 3].replace('\n', '').replace('\r', '')
                    }
                    i = i + 5
                    subtitles.append(subtitle)
                else:  # 没有符合的情况下list索引往下加一
                    i = i + 1
            newlist = sorted(subtitles, key=lambda d: d['time'])  # 对list按时间排序
            # print(newlist)
            save_to_mongodb(newlist)
    except Exception as e:
        print('讀取文件失敗',e)
        return None


def save_to_mongodb(list):  # 保存至mongodb
    # if db[MONGODB_COLLECTION].insert_many(list):
    try:
        for ll in list:
            db[MONGODB_COLLECTION].update({}, {'$set':ll},upsert=True)
        print('保存到MONGODB成功！')
    except Exception as e:
        print('保存到MONGODB失败！',e)


def main():
    filename = 'SRT\\good.fight.S01E01.srt'
    read_file(filename)

if __name__ == '__main__':
    main()