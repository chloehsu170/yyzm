# encoding:utf-8
# import zipfile
# from unrar import rarfile
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


def un_rar11111111111111111111(file_name):
    try:
        """unrar RAR file"""
        rar = rarfile.RarFile(file_name)
        rar.extractall()
        # if os.path.isdir(file_name[:-4] + "_files"):
        #     pass
        # else:
        #     os.mkdir(file_name[:-4] + "_files")
        # os.chdir(file_name[:-4] + "_files")
        # rar.extractall()
        rar.close()
        print("解压成功！", file_name)
        os.remove(file_name)  # 然后删除rar文件
        print('删除rar文件成功！', file_name)
        return True
    except Exception as e:
        print(e)
        return False


def un_rar(file_name):  # rar文件解压后有乱码问题
    try:
        """unrar rar file"""
        rar_file = rarfile.RarFile(file_name)
        print(rar_file.namelist())
        # 判断rar文件是否含有文件夹，如果有没有文件夹，就新建一个
        sondir = ''
        # print(sondir,'first')
        for name in rar_file.namelist():
            # print(name)
            isdir = '/' in name
            if isdir:
                break
        israr = re.search('\.rar|\.zip', rar_file.namelist()[0])  # 第一文件是否rar文件
        if israr:  # 一层层扒皮速度太慢
            for names in rar_file.namelist():
                print('还需解压下级文件！', names)
                rar_file.extract(names)
                sondir = un_rar(os.getcwd() + '\\' + names)
                if not sondir:
                    sondir = un_zip(os.getcwd() + '\\' + names)
        #########################################################################################
        # if names[-4:] == '.rar':
        #     print('还需解压下级rar文件！', names)
        #     rar_file.extract(names)
        #     if not un_rar(os.getcwd() + '\\' + names):
        #         if un_zip(os.getcwd() + '\\' + names):
        #             sondir = KEYWORD1  # 解压成功
        # if names[-4:] == '.zip':
        #     print('还需解压下级zip文件！', names)
        #     rar_file.extract(names)
        #     if not un_zip(os.getcwd() + '\\' + names):
        #         if un_rar(os.getcwd() + '\\' + names):
        #             sondir = KEYWORD1
        ######################################################################################
        elif not isdir:  # 没有文件夹
            os.mkdir(file_name + '_files')  # file_name[:-4]
            # print(sondir, 'seconf')
            for names in rar_file.namelist():
                sondir = file_name.split('\\')[-1] + '_files'  # 取文件夹名
                # utf-8格式怎么办？？？
                zh_ptn = re.compile(u'[\u4e00-\u9fa5]+')
                name = re.search(zh_ptn, names)
                if name != None:  # 没有乱码
                    filename = names
                else:
                    filename = names.encode('cp437').decode('gbk')
                rar_file.extract(names, file_name + '_files')  # [:-4]
                os.chdir(file_name + '_files')  # [:-4]
                os.rename(names, filename)  # 文件名不含有路径
            os.chdir(os.path.dirname(file_name))
        else:  # 有文件夹的话
            for names in rar_file.namelist():
                # utf-8格式怎么办？？？
                zh_ptn = re.compile(u'[\u4e00-\u9fa5]+')
                name = re.search(zh_ptn, names)
                if re.search('/', names):  # 解压带文件夹的文件
                    sondir = names.split('/')[0]  # 取文件夹名
                    # print(sondir,'thh')
                    if name != None:  # 没有乱码
                        filename = names
                    else:
                        filename = names.encode('cp437').decode('gbk')
                    rar_file.extract(names)
                    os.chdir(os.path.dirname(file_name))  # 切换到被解压文件的路径
                    os.rename(names, filename)  # names含有子目录
        rar_file.close()
        if sondir:
            print("解压rar文件成功！", file_name)
            os.remove(file_name)  # 然后删除rar文件!!!!!!!!!!!!!!!!!!!!
            print('删除rar文件成功！', file_name)
        return sondir
    except Exception as e:
        print(e)
        return False


def un_zip(file_name):  # zip文件解压后有乱码问题
    try:
        """unzip zip file"""
        zip_file = zipfile.ZipFile(file_name)
        # 判断zip文件是否含有文件夹，如果有没有文件夹，就新建一个
        sondir = ''
        print(zip_file.namelist())
        for name in zip_file.namelist():
            # print(name)
            # isdir = re.search('/', name)  # 文件是否带有文件夹,不是就创建文件夹file_name[:-4]
            isdir = '/' in name
            if isdir:
                break

        israr = re.search('\.rar|\.zip', zip_file.namelist()[0])  # 第一文件是否rar文件
        if israr:  # 一层层扒皮速度太慢
            for names in zip_file.namelist():
                print('还需解压下级文件！', names)
                zip_file.extract(names)
                sondir = un_zip(os.getcwd() + '\\' + names)
                if not sondir:
                    sondir = un_rar(os.getcwd() + '\\' + names)

        #############################################################################################
        elif not isdir:#没有文件夹的话
            os.mkdir(file_name + '_files')  # file_name[:-4]
            sondir = file_name.split('\\')[-1] + '_files'  # 取文件夹名
            for names in zip_file.namelist():
                # utf-8格式怎么办？？？
                zh_ptn = re.compile(u'[\u4e00-\u9fa5]+')
                name = re.search(zh_ptn, names)
                if name != None:  # 没有乱码
                    filename = names
                else:
                    filename = names.encode('cp437').decode('gbk')
                zip_file.extract(names, file_name + '_files')  # [:-4]
                os.chdir(file_name + '_files')  # [:-4]
                os.rename(names, filename)
                os.chdir(FILEPATH)
        else:  # 有文件夹的话
            for names in zip_file.namelist():
                # utf-8格式怎么办？？？
                zh_ptn = re.compile(u'[\u4e00-\u9fa5]+')
                name = re.search(zh_ptn, names)
                if re.search('/', names):  # 解压带文件夹的文件
                    sondir = names.split('/')[0]  # 取文件夹名
                    if name != None:  # 没有乱码
                        filename = names
                    else:
                        filename = names.encode('cp437').decode('gbk')
                    zip_file.extract(names)
                    os.chdir(FILEPATH)
                    os.rename(names, filename)
                    # os.chdir(FILEPATH)

        zip_file.close()
        if sondir:
            print("解压成功！", file_name)
            os.remove(file_name)  # 然后删除zip文件!!!!!!!!!!!!!!
            print('删除zip文件成功！', file_name)
        return sondir
    except Exception as e:
        print(e)
        return False


def select_file1111111111111111111111(filedir):
    try:
        filelists = os.listdir(filedir)
        ptn = re.compile('简体&英文.srt')  # 匹配srt文件
        for file in filelists:
            ll = re.search(ptn, file)
            if ll:
                print('已找到', file)
                if save_srt_file(filedir + '\\' + file):  # 找到srt文件后複製到srt文件夾
                    read_file(filedir + '\\' + file)  # 讀取srt文件內容
    except:
        pass


def select_file(filedir):
    try:
        filelists = os.listdir(filedir)
        srtPtn = re.compile('简体&英文.srt|简英.srt|chs&eng.srt|精校版.*?\.srt|双语.*?\.srt|初校版.*?\.srt', re.IGNORECASE)
        # 匹配srt文件 |.srt
        assPtn = re.compile('简体&英文.ass|简英.ass|chs&eng.ass|精校版.*?\.ass|双语.*?\.ass|初校版.*?\.ass|繁体&英文.ass',
                            re.IGNORECASE)  # 匹配ass文件 |.ass
        srtfPtn = re.compile('繁体&英文.srt|繁英.srt')  # 匹配繁体srt文件
        srtResult = 0  # 找到srt文件
        srtfResult = 0  # 找到繁体srt文件
        assResult = 0  # 找到ass文件
        for file in filelists:
            srtll = re.search(srtPtn, file)
            if srtll:
                srtResult = 1
                print('已找到srt文件', file)
                if save_srt_file(filedir + '\\' + file):  # 找到srt文件后複製到srt文件夾
                    read_file(filedir + '\\' + file)  # 讀取srt文件內容
                # break不能break 需要查找全部符合条件的文件

        if srtResult == 0:
            print('没有找到简英srt文件找繁英srt文件')  #
            for file in filelists:
                srtfll = re.search(srtfPtn, file)
                if srtfll:
                    srtfResult = 1
                    print('已找到繁英srt文件', file)
                    if save_srt_file(filedir + '\\' + file):  # 找到srt文件后複製到srt文件夾
                        read_file(filedir + '\\' + file)  # 讀取srt文件內容
                    # break不能break 需要查找全部符合条件的文件

        if srtfResult == 0:
            print('没有找到繁英srt文件找ass文件')  #
            for file in filelists:
                assll = re.search(assPtn, file)
                if assll:
                    assResult = 1
                    print('已找到ass文件', file)
                    srtfile = ass_to_srt(filedir + '\\' + file)
                    # print(srtfile)
                    if save_srt_file(srtfile):  # ass转srt文件后複製到srt文件夾
                        read_file(srtfile)  # 讀取srt文件內容
                    # break不能break 需要查找全部符合条件的文件
        return srtfResult or srtfResult or assResult
    except Exception as e:
        print(e)


def ass_to_srt(file):
    with open(file, 'rb') as f:  # 读取文件编码
        coding = chardet.detect(f.read())
        cd = coding.get('encoding')
        print(cd)
        f.close()
    if re.match('GB2312', cd, re.IGNORECASE):  # 编码为GB23112时
        cd = None
    ass_file = codecs.open(file, 'r', cd)  # 读取ass文件内容
    srt_file = asstosrt.convert(ass_file)  # 将ass文件内容转为srt内容
    srtname = file[:-4] + '.srt'
    with codecs.open(srtname, 'w', cd) as ss:  # 保存srt内容至srt文件
        ss.write(srt_file.replace('\r', ''))
        ss.close()
    print('ass文件转srt文件成功！')
    return srtname


def save_srt_file(file):
    # name_pattern = re.compile('([Ss]\d\d[Ee]\d\d)')  # 匹配title模式
    name_pattern = re.compile('({0})'.format(SHOWPTN))
    names = re.findall(name_pattern, file)
    srtpath = SRTPATH + KEYWORD1 + '.' + names[-1] + '.srt'  # 找到文件名匹配而不是文件夹匹配
    if not os.path.exists(srtpath):
        # 判斷目標文件夾是否有這個文件，沒有就複製，basename()取源文件名，dirname()取源路徑名
        # title_pattern = re.compile('([a-zA-Z0-9.]*?S\d\dE\d\d)')
        shutil.copy(file, srtpath)
        print(names[-1], '已成功複製到srt文件夾')
        return True
    else:
        print(names[-1], 'srt文件已存在！')
        return False


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
    except Exception:
        print('讀取文件失敗')
        return None


def save_to_mongodb1111111111111111111111(list):  # 保存至mongodb
    # if db[MONGODB_COLLECTION].insert_many(list):
    if db[MONGODB_COLLECTION].update({}, {'$set':{list}},upsert=True,multi=True):
        print('保存到MONGODB成功！')
    else:
        print('保存到MONGODB失败！')

def save_to_mongodb(list):  # 保存至mongodb
    # if db[MONGODB_COLLECTION].insert_many(list):
    try:
        for ll in list:
            db[MONGODB_COLLECTION].update({}, {'$set':ll},upsert=True)
        print('保存到MONGODB成功！')
    except Exception as e:
        print('保存到MONGODB失败！',e)

def main():
    filename = 's01e02.rar'
    # un_rar(FILEPATH + 'House.of.Cards.S02.rar')

    sondir = un_rar(FILEPATH + filename)
    if not sondir:
        sondir = un_zip(FILEPATH + filename)
        if not sondir:
            if os.system('7z x \"{0}\"'.format(FILEPATH + filename)):
                sondir = filename
   #####################################################################################
    if sondir:  # 解压成功
        ptn = re.compile(KEYWORD1, re.IGNORECASE)  # 匹配showname文件夹名
        for filename in os.listdir(FILEPATH):
            extractName = re.search(ptn, filename)
            print(extractName,sondir)
            if (extractName or filename == sondir) and os.path.isdir(filename):  #
                if select_file(FILEPATH + filename):
                    shutil.rmtree(FILEPATH + filename)
    #
    # ptn = re.compile('Suits', re.IGNORECASE)  # 匹配showname文件夹名
    # for filename in os.listdir(FILEPATH):
    #     extractName = re.search(ptn, filename)
    #     print(extractName)
    #     if extractName and os.path.isdir(filename):
    #         select_file(FILEPATH + filename)
    #         shutil.rmtree(FILEPATH + filename)
    remove_ptn = re.compile(KEYWORD1, re.IGNORECASE)
    # for file in os.listdir(FILEPATH):
    #     removefile = re.search(remove_ptn, file)
    #     if removefile and os.path.isfile(file):  # 删除所有同模式的文件及文件夹
    #         print(file)
    #         os.remove(file)
    #     elif removefile and os.path.isdir(file):
    #         print(file)
    #         shutil.rmtree(file)


if __name__ == "__main__":
    main()
