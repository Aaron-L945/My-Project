# coding=utf-8
import functools
import hashlib
import random
import time
from multiprocessing import Pool, Manager
from urllib.request import urlopen
import requests
import os
import re
import logging

# 获取logger的实例
logger = logging.getLogger("Meizi_img")
logger.setLevel(logging.DEBUG)
# 指定logger的输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# 文件日志，终端日志
file_handler = logging.FileHandler("Meizi_img.log")
file_handler.setFormatter(formatter)
# 设置默认的级别
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# ============config===================
Type_ = 'riben'
Mumber = '182'
Local = "image\\"
Num = 2
URL = 'http://www.xixirenti.cc/%s/%s_' % (Type_, Mumber)
B_url = "http://www.xixirenti.cc/%s/%s.html" % (Type_, Mumber)
Logpath = Local + 'log\\'
All_url = "http://www.xixirenti.cc"
Re_img = """var totalpage = ([\s\S]*?);"""
Re_obj = """<div class="arcBody">[\s\S]*?href=[\s\S]*?<img src='([\s\S]*?)' id=[\s\S]*?"""
Ua_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
    "Referer": "http: // www.xixirenti.cc / riben / 2418_10.html"}


# ======================================


def despath():
    path = Local + Mumber + '\\'
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception as e:
            logger.error(e)
    return path


def hashStr(strInfo):
    """
     对字符串做HASH
    """
    h = hashlib.sha256()  # md5,sh1,sha256
    h.update(strInfo.encode("utf-8"))
    return h.hexdigest()


def get_one_page(url):
    time.sleep(random.randint(1, 3))
    """
    发起Http请求，获取Response的响应结果
    """
    reponse = requests.get(url, headers=Ua_headers)
    if reponse.status_code == 200:  # ok
        return reponse.text
    return None


def get_img_url(html):
    time.sleep(random.randint(1, 3))
    pattern = re.compile(Re_obj)
    items = re.findall(pattern, html)
    if items is None:
        return None
    try:
        url = All_url + items[0]
        logger.info(url)
        return url
    except IndexError as e:
        print(e)


def save_img(url):
    time.sleep(random.randint(1, 3))
    imgName = hashStr(time.ctime()) + '.jpg'
    path = despath()
    local = path + imgName
    try:
        data = urlopen(url.strip()).read()
        with open(local, "wb") as f:
            f.write(data)
    except:
        logger.error("downloaded error in " + url)


def get_all_page(html):
    pattern = re.compile(Re_img)
    items = re.findall(pattern, html)
    if items is None:
        return None
    else:
        try:
            page = int(items[0])
            return page
        except IndexError as e:
            logger.error(e)


def CrawlPictureInfo(q, page):
    time.sleep(random.randint(1, 3))
    new_url = URL + str(page) + ".html"
    # print(new_url)
    html = get_one_page(new_url)
    if html:
        result = get_img_url(html)
        if result:
            q.put(result)
        else:
            logger.error('not find the image!' % (result))
    else:
        logger.error('not find html')


def main():
    p = Pool()
    q = Manager().Queue()  # 构造出一个在进程池之间共享的队列
    html = get_one_page(B_url)
    result = get_img_url(html)
    q.put(result)
    page = get_all_page(html)
    cont = str(page) + '_page'
    logger.info(cont + '\n\n')
    if page:
        partial_CrawlPictureInfo = functools.partial(CrawlPictureInfo, q)
        p.map(partial_CrawlPictureInfo, [i for i in range(Num, page + 1)])
        p.close()  # 通知进程池任务添加结束
        All_img = []
        while not q.empty():
            img_url = q.get()
            All_img.append(img_url)
        for i in range(len(set(All_img))):
            save_img(list(set(All_img))[i])
            logger.info("%s page download ok!" % (str(i + 1)))
        p.join()
    else:
        logger.error("not find page ")


if __name__ == '__main__':

    try:
        main()
    except Exception as e:
        logger.error(e)