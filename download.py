from urllib.parse import urlencode
import requests
from zimuku.yyzm.jieya import *
from pyquery import PyQuery as pq


def search():
    data = {
        'q': KEYWORD1
    }
    url = 'http://www.zimuku.cn/search?' + urlencode(data)
    response = requests.get(url)
    if response.status_code == 200:
        # print(response.text)
        return response.text
    else:
        return None


def parse_dramaShows_url(html):
    ptn = re.compile('<p class="tt clearfix"><a href="(/subs/.*?html)" target="_blank"><b>(.*?)</b></a></p>', re.S)
    results = re.findall(ptn, html)
    if results:
        return results
    raise Exception('字幕庫不存在：', KEYWORD1)


def get_shows_html(url):
    url = "http://www.zimuku.cn" + url
    responseS = requests.get(url)
    if responseS.status_code == 200:
        # print(responseS.text)
        return responseS.text
    else:
        return None


def parse_shows_url(html):
    doc = pq(html)
    resultS = []
    items1 = doc('#subtb .odd').items()
    items2 = doc('#subtb .even').items()
    for item1 in items1:
        if ZIMUZU in item1.find('.label-danger').text() :
            it1s = doc(item1.find('.lang img')).items()
            for it1 in it1s:
                if it1.attr('alt') == SUBTITLE:
                    show = (item1.find('.first a').attr('title'), item1.find('.first a').attr('href'))
                    resultS.append(show)

    for item2 in items2:
        if ZIMUZU in item2.find('.label-danger').text():
            it2s = doc(item2.find('.lang img')).items()
            for it2 in it2s:
                if it2.attr('alt') == SUBTITLE:
                    show = (item2.find('.first a').attr('title'), item2.find('.first a').attr('href'))
                    resultS.append(show)

    if resultS:
        print(resultS)
        result = []
        for res in resultS:
            # print(res)
            # name_ptn = re.compile('([a-zA-Z0-9.]*?[sS]02)', re.IGNORECASE)  # [Ee]\d\d) [简中].*?英.*?
            name_ptn = re.compile('({0})'.format(SHOWSPTN), re.IGNORECASE)
            name = re.search(name_ptn, res[0])
            if name:
                # print(name)
                result.append(res[1])
        print(result)
        return result
    else:
        return None


def get_show_html(url):
    url = 'http://www.zimuku.cn' + url
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        # print(response.text)
        return response.text
    else:
        return None


def parse_show_url(html):
    # title_ptn = re.compile('<title>.*?({0}.*?\.(zip|rar|7z)).*?</title>'.format(SHOWSPTN), re.IGNORECASE)
    title_ptn = re.compile('<title>.*?({0}.*?)</title>'.format(SHOWSPTN), re.IGNORECASE)
    url_ptn = re.compile('href="(/download/.*?)"', re.S)
    showTitleResult = re.search(title_ptn, html)
    showURLresult = re.search(url_ptn, html)
    if showURLresult and showTitleResult:
        print('http://www.zimuku.cn' + showURLresult.group(1), showTitleResult.group(1))
        return showURLresult.group(1), showTitleResult.group(1) #, showTitleResult.group(2)
    else:
        print('没有匹配的字幕供下载！')
        # return None
        pass


def download(showURLresult, showTitleResult):
    url = 'http://www.zimuku.cn' + showURLresult
    print("downloading with requests")
    r = requests.get(url)
    if r.status_code == 200:
        with open(showTitleResult, "wb") as code:  # +'.rar'
            code.write(r.content)  # 读进来content内容
            code.close()
        print('下载字幕文件成功!', showTitleResult)  # +'.rar'
        return True
    else:
        print('下载字幕文件失败!', showTitleResult)
        return None


def download11111111111111111(showURLresult, showTitleResult, showTitleMode):
    url = 'http://www.zimuku.cn' + showURLresult
    print("downloading with requests")
    r = requests.get(url)
    if r.status_code == 200:
        if showTitleMode == 'rar':
            with open(showTitleResult, "wb") as code:  # +'.rar'
                code.write(r.content)  # 读进来content内容
                code.close()
            print('下载字幕文件成功!', showTitleResult)  # +'.rar'
            return True
        elif showTitleMode == 'zip':
            with open(showTitleResult, "wb") as code:  # +'.zip'
                code.write(r.content)  # 读进来content内容
                code.close()
            print('下载字幕文件成功!', showTitleResult)  # +'.zip'
            return True
    else:
        print('下载字幕文件失败!', showTitleResult)
        return None


def main():
    try:
        html = search()
        urls = parse_dramaShows_url(html)
        for url in urls:
            print('正在查找：', url)
            showsHtml = get_shows_html(url[0])
            showURLlist = parse_shows_url(showsHtml)
            if showURLlist:  # 该字幕组有该季
                for showURL in showURLlist:
                    showHtml = get_show_html(showURL)
                    showResult = parse_show_url(showHtml)
                    # 返回none怎麼辦 showURLresult, showTitleResult, showTitleMode
                    # print('!!!!!!', showResult)
                    if showResult: #该字幕组有该集
                        os.chdir(FILEPATH)  # 重新回到filepath下载路径
                        if download(showResult[0], showResult[1]):
                            sondir = un_rar(FILEPATH + showResult[1])
                            if not sondir:
                                sondir = un_zip(FILEPATH + showResult[1])
                                if not sondir:
                                    if os.system('7z x \"{0}\"'.format(FILEPATH + showResult[1])):
                                        sondir = showResult[1]
                            #####################################################
                            # if showResult[2] == 'rar':
                            #     if not un_rar(FILEPATH + showResult[1]):  # 解压rar文件到当前目录+'.rar'
                            #         un_zip(FILEPATH + showResult[1]) #File is not a rar file
                            # elif showResult[2] == 'zip':
                            #     if not un_zip(FILEPATH + showResult[1]):  # 解压zip文件到当前目录 + '.zip'
                            #         un_rar(FILEPATH + showResult[1]) #File is not a zip file
                            # elif showResult[2] == '7z':
                            #     os.system('7z x \"{0}\"'.format(FILEPATH + showResult[1]))
                    #####################################################################################
                            if sondir:#解压成功
                                ptn = re.compile(KEYWORD1, re.IGNORECASE)  # 匹配showname文件夹名
                                for filename in os.listdir(FILEPATH):
                                    extractName = re.search(ptn, filename)
                                    if (extractName or filename==sondir) and os.path.isdir(filename):#
                                        if select_file(FILEPATH + filename):
                                            shutil.rmtree(FILEPATH + filename)
                                        else:
                                            # print('文件夹中找不到符合模式的srt文件！', filename)
                                            continue
                                    else:
                                        # print('找不到符合模式的文件夹！', extractName,sondir)
                                        continue
                                    # print('刪除文件夾成功！',os.getcwd() +'\\'+ filename)
                            # if os.getcwd() != FILEPATH:
                            #     shutil.rmtree(os.getcwd())
                            # else:
                            #     print("找不到文件夾",extractName)#
                            else:
                                print('解压失败！',showResult[1])
                                continue

                        else:
                            print('下载失败!',showResult)
                            continue
                    else:
                        print('下载页面标题不符合模式!')
                        continue
            else:  # 没有shows可下载
                print('该字幕组没有该季任何字幕可供下载！', url[1])
                continue
    except Exception as e:
        print('出錯啦！', e)
    # finally:
    #     remove_ptn = re.compile(KEYWORD1, re.IGNORECASE)
    #     for file in os.listdir(FILEPATH):
    #         removefile = re.search(remove_ptn, file)
    #         if removefile and os.path.isfile(file):  # 删除所有同模式的文件及文件夹
    #             print(file)
    #             os.remove(file)
    #         elif removefile and os.path.isdir(file):
    #             print(file)
    #             shutil.rmtree(file)


if __name__ == '__main__':
    main()
