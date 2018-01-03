import re
import os
from zipfile import ZipFile
from rarfile import RarFile
from zimuku.yyzm.config import *


def deco(a):  # 装饰类函数
    class ExtractFile(object):  # 公共类
        def __init__(self, file_name):#初始化对象
            try:
                self.file_name = file_name  # 参数
                self.wrapped = a(file_name)  # 类对象eg. rar_file
            except Exception as e:
                print(e)
                pass

        def extractf(self, file_name):  # 处理方法
            try:
                print(self.wrapped.namelist())
                # 判断rar文件是否含有文件夹，如果有没有文件夹，就新建一个
                sondir = ''
                # print(sondir,'first')
                for name in self.wrapped.namelist():
                    # print(name)
                    isdir = '/' in name
                    if isdir:
                        break
                israrzip = re.search('\.rar|\.zip', self.wrapped.namelist()[0])  # 第一文件是否rar文件
                if israrzip:  # 一层层扒皮速度太慢
                    for names in self.wrapped.namelist():
                        print('还需解压下级文件！', names)
                        self.wrapped.extract(names)
                        sondir = Rars(os.getcwd() + '\\' + names).extractf(os.getcwd() + '\\' + names)
                        if not sondir:
                            sondir = Zips((os.getcwd() + '\\' + names)).extractf(
                                os.getcwd() + '\\' + names)  ################

                if not isdir:  # 没有文件夹
                    os.mkdir(file_name + '_files')  # file_name[:-4]
                    # print(sondir, 'seconf')
                    for names in self.wrapped.namelist():
                        sondir = file_name.split('\\')[-1] + '_files'  # 取文件夹名
                        # utf-8格式怎么办？？？
                        zh_ptn = re.compile(u'[\u4e00-\u9fa5]+')
                        name = re.search(zh_ptn, names)
                        if name != None:  # 没有乱码
                            filename = names
                        else:
                            filename = names.encode('cp437').decode('gbk')
                        self.wrapped.extract(names, file_name + '_files')  # [:-4]
                        os.chdir(file_name + '_files')  # [:-4]
                        os.rename(names, filename)  # 文件名不含有路径
                    os.chdir(os.path.dirname(file_name))
                else:  # 有文件夹的话
                    for names in self.wrapped.namelist():
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
                            self.wrapped.extract(names)
                            os.chdir(os.path.dirname(file_name))  # 切换到被解压文件的路径
                            os.rename(names, filename)  # names含有子目录
                self.wrapped.close()
                if sondir:
                    print("解压压缩文件成功！", file_name)
                    os.remove(file_name)  # 然后删除rar文件!!!!!!!!!!!!!!!!!!!!
                    print('删除rar文件成功！', file_name)
                return sondir
            except Exception as e:
                print(e)
                pass

    return ExtractFile  # 公共类


@deco
class Zips(ZipFile):  # 继承父类
    pass
    # def __init__(self, filename):
    #     ZipFile.__init__(self, filename)
    #     self.filename = filename


@deco
class Rars(RarFile):  # 继承父类
    def __init__(self, filename):
        RarFile.__init__(self, filename)
        self.filename = filename


if __name__ == '__main__':
    filename2 = 'downton.abbey.s05.christmas.special.720p.bluray.x264 shortbrehd.srt 双语 字幕下载 - 字幕库(zimuku.cn)'
    # filename2 = 'D:\\Python36\\zdh3\\zimuku\\yyzm\\The.Good.Fight.S01E05.720p.WEBRip.X264 DEFLATE.rar'
    # Zips(filename1).extractf(filename1)
    son = Rars(filename2).extractf(filename2)
    print(son)
