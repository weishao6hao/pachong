# encoding=utf8
import urllib2
from bs4 import BeautifulSoup
# import urllib.requests
import socket
import requests
session = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

'''
获取所有代理IP地址   http://ip.zdaye.com/
'''


def getProxyIp():
    proxy = []
    for i in range(1, 10):
        try:
            url = 'http://www.kuaidaili.com/free/inha/' + str(i)
            # req = urllib2.Request(url, headers=header)
            res = session.get(url).content
            soup = BeautifulSoup(res, "html.parser")
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[0].text + "\t" + tds[1].text
                proxy.append(ip_temp)
        except:
            continue
    return proxy


'''
验证获得的代理IP地址是否可用
'''

def validateIp(proxy):
    url = "http://www.bjtu.edu.cn"
    f = open("C:/Users/DELL/Desktop/ip.txt", "w")
    socket.setdefaulttimeout(3)
    for i in range(0, len(proxy)):
        try:
            ip = proxy[i].strip().split("\t")
            proxy_host = "http://" + ip[0] + ":" + ip[1]
            proxy_temp = {"http": proxy_host}
            session.get(url, proxies=proxy_temp)
            f.write(proxy[i] + '\n')
            print(proxy[i])
        except Exception:
            continue
    f.close()
'''
更换ip 
# proxie = { 
#         'http' : 'http://122.193.14.102:80'
#     }   
# url = 'xxx'
# 
# response = s.get(url, verify=False, proxies = proxie, timeout = 20)
'''

if __name__ == '__main__':
    proxy = getProxyIp()
    validateIp(proxy)