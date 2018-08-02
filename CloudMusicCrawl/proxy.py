# -*- coding:utf-8 -*-
import requests
import os
from CloudMusicCrawl.wordanalyse import Read_Txt,Save_Txt

proxypath = os.path.join('doc','proxy.txt')

def Get_Proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


def DeleteProxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

#proxy会用记录的能用的proxy，挂了就会再读取一个继续用,返回response
def GetResponse(url, header={}, cookie={}):
    currentproxy = Read_Txt(proxypath)
    while True:
        retry_count = 1
        while retry_count > 0:
            try:
                html = requests.get(url, headers=header, cookies=cookie,
                                    proxies={"http": "http://{}".format(currentproxy)})
                #print(html.status_code)
                # 使用代理访问
                if(html.status_code == 200 and html.content):
                    #print('proxy {p} visit {u} successfully'.format(p=currentproxy, u=url))
                    return html
            except Exception as e:
                print(e)
                retry_count -= 1
        DeleteProxy(currentproxy)
        print('invalid proxy {} change another proxy'.format(currentproxy))
        Save_Txt(proxypath, str(Get_Proxy(), encoding='utf-8'))
