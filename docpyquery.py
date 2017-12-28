import rarfile
import chardet
import os
from zimuku.yyzm.jieya import *
import rarfile
import requests
import asstosrt
# import langconv
from pyquery import PyQuery as pq
import codecs
import re
import lzma


# file_name='D:\\Python36\\zdh3\\zimuku\\yyzm\\[zmk.tw]Good.Behavior.S01E04.720p.HDTV.x264.rar'
file_name = 'D:\\Python36\\zdh3\\zimuku\\yyzm\\House.of.Cards.2013.S05.720p.WEBRip.x264 MOROSE.7z'
os.system('7z x \"{0}\"'.format(file_name))
#     print(file_content)
# assfile = 'D:\\Python36\\zdh3\\zimuku\\Good.Behavior.S01E02.720P.ass'
# ass_file =codecs.open(assfile,encoding='utf-16')
# # print(ass_file.readlines())
# srt_file = asstosrt.convert(ass_file)
# with codecs.open(assfile[:-4]+'.srt','w') as ss:
#     ss.write(srt_file.replace('\r', ''))
# with codecs.open(assfile[:-4]+'.srt','r') as ff:
#     print(ff.read())
# with codecs.open(assfile[:-4]+'.srt','w') as mm:
#     lines = mm.readlines()
#     i = 0
#     for line in lines:



def un_rar(file_name):  # rar文件解压后有乱码问题

    """unrar rar file"""
    rar_file = rarfile.RarFile(file_name)
    rar_file.extractall()
    # 判断rar文件是否含有文件夹，如果有没有文件夹，就新建一个
    isdir = re.search('/$', rar_file.namelist()[0])  # 第一文件是否是文件夹,不是就创建文件夹file_name[:-4]
    israr = re.search('\.rar', rar_file.namelist()[0])  # 第一文件是否rar文件
    # if israr:#一层层扒皮速度太慢
    #     for names in rar_file.namelist():
    #         if names[-4:] == '.rar':
    #             print('还需解压下级rar文件！', names)
    #             rar_file.extract(names)
    #             un_rar(os.getcwd() + '\\' + names)
    if not isdir:
        os.mkdir(file_name[:-4])
        for names in rar_file.namelist():
            # utf-8格式怎么办？？？
            zh_ptn = re.compile(u'[\u4e00-\u9fa5]+')
            name = re.search(zh_ptn, names)
            if name != None:  # 没有乱码
                filename = names
            else:
                filename = names.encode('cp437').decode('gbk')
            rar_file.extract(names, file_name[:-4])
            os.chdir(file_name[:-4])
            os.rename(names, filename)  # 文件名不含有路径
        os.chdir(os.path.dirname(file_name))
    else:  # 有文件夹的话
        for names in rar_file.namelist():
            # utf-8格式怎么办？？？
            zh_ptn = re.compile(u'[\u4e00-\u9fa5]+')
            name = re.search(zh_ptn, names)
            if not re.search('/$', names):  # 不是文件夹
                if name != None:  # 没有乱码
                    filename = names
                else:
                    filename = names.encode('cp437').decode('gbk')
                rar_file.extract(names)
                os.chdir(os.path.dirname(file_name))  # 切换到被解压文件的路径
                os.rename(names, filename)  # names含有子目录
    rar_file.close()
    print("解压rar文件成功！", file_name)


# def main():
    # un_raar(file_name)

    # cmd = '\"C:\\Program Files\\WinRAR\\unrar.exe\" t \"{0}\"'.format(file_name)
    # os.popen(cmd)



# if __name__ == '__main__':
#     main()
# print(srt_file)
"""unrar rar file"""
# rar_file = rarfile.RarFile(file_name)
# isdir = re.search('/$',rar_file.namelist()[0])#第一文件是否是文件夹,不是就创建文件夹file_name[:-4]
# print(isdir)
#
# for filename in rar_file.namelist():
#     print(filename)

# encoding = chardet.detect(name).get('encoding')
# print(encoding)
# if encoding=='UTF-16':
#     print(filename.encode('cp437').decode('gbk'))
# print(filename)
# print(chardet.detect(filename.filename))
# print(isinstance(filename.filename,str))
# iscp437 = filename.encode('cp437').decode('gbk')
# if iscp437:
#     print(iscp437)
#
#
# # if os.path.isdir(file_name + "_files"):
# #     pass
# # else:
# #     os.mkdir(file_name + "_files")
# # for names in rar_file.namelist():
# #     rar_file.extract(names)
# # rar_file.close()
# # print("解压成功！", file_name)
#
#
#
#
# file ='D:\\Python36\\zdh3\\zimuku\\syzm\\SRT\\Behavior.S01E01.srt'
# with open(file, 'rb') as f:
#     coding = chardet.detect(f.read())
#     cd = coding.get('encoding')
#     print(cd)
#     f.close()
# with codecs.open(file,'r',cd) as cc:
#     content =cc.readlines()
#     print(content)


# url = 'http://www.zimuku.cn/subs/39779.html'
# response =requests.get(url)
# doc = pq(response.text)
# shows=[]
# items1 = doc('#subtb .odd').items()
# items2 = doc('#subtb .even').items()
# for item1 in items1:
#     if item1.find('.label-danger').text() =='YYeTs字幕组' and 'SRT' in item1.find('.label-info').text():
#         show = (item1.find('.first a').attr('title'),item1.find('.first a').attr('href'))
#         shows.append(show)
# for item2 in items2:
#     if item2.find('.label-danger').text() =='YYeTs字幕组' and 'SRT' in item2.find('.label-info').text():
#         show = (item2.find('.first a').attr('title'),item2.find('.first a').attr('href'))
#         shows.append(show)
# j =0
# for sh in shows:
#     print(sh[0])

# print(items2)
