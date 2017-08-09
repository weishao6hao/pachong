#coding=utf-8
import time
from http import cookiejar
from lxml import html
import os

import requests
from bs4 import BeautifulSoup

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    print(session.cookies)
    session.cookies.load(ignore_discard=True)

except:
    print("还没有cookie信息")


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get('value')
    return xsrf


def get_captcha():
    """
    把验证码图片保存到当前目录，手动识别验证码
    :return:
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码：")
    return captcha


def login(email, password):
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'remember_me': 'true'}
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code['msg'])
    for i in session.cookies:
        print(i)
    session.cookies.save()
def get_link_ist(collection_num):
    page = input('你想要多少页？:')
    page=int(page)
    result = []
    collection_title = None
    for i in range(1, page+1):
        link = 'https://www.zhihu.com/collection/{}?page={}'.format(collection_num, str(i))
        response = requests.get(link, headers=headers).content
        sel = html.fromstring(response)
        # 创建文件夹
        if collection_title is None:
            # 收藏夹名字
            collection_title = sel.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()')[0].strip()
            if not os.path.exists(collection_title):
                os.mkdir(collection_title)
        each = sel.xpath('//div[@class="zm-item"]//h2[@class="zm-item-title"]/a')
        for e in each:
            link = 'https://www.zhihu.com' + e.xpath('@href')[0]
            result.append(link)
    return [collection_title, result]
def get_pic(collection, answer_link):
    response = requests.get(answer_link, headers=headers).content
    sel = html.fromstring(response)
    title = sel.xpath('//h1[@class="QuestionHeader-title"]/text()')[0].strip()
    try:
        # 匿名用户
        author = sel.xpath('//a[@class="UserLink-link"]/text()')[0].strip()
    except:
        author = u'匿名用户'
    # 新建路径
    path = collection + '/' + title + ' - ' + author
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        n = 1
        for i in sel.xpath('//div[@class="RichContent-inner"]//img/@src'):
            # 去除whitedot链接
            if 'whitedot' not in i:
                # print i
                pic = requests.get(i).content
                fname = path + '/' + str(n) + '.jpg'
                with open(fname, 'wb') as p:
                    p.write(pic)
                n += 1
        print (u'{} 已完成'.format(title))
    except :
        pass


if __name__ == '__main__':
    email = "798364373@qq.com"
    password = "*********"
    login(email, password)
    collection_num = input('输入收藏夹号码：')
    r = get_link_ist(collection_num)
    collection = r[0]
    collection_list = r[1]
    for k in collection_list:
        get_pic(collection, k)
