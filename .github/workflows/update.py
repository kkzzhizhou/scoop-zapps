#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import logging

import requests

def get_redirect_url(url):
    r = requests.head(url, stream=True)
    logging.debug(r.headers)
    if 'Location' in r.headers:
        return r.headers['Location']
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        response = requests.get(url, headers=headers)
        logging.debug(response.url)
        return response.url

def get_update_v3(app_name,url,pattern):
    content = requests.get(url).text
    current_version =re.findall(pattern,content)[0]
    update_app(app_name,current_version)

def get_update_multimarkdown():
    name = 'multimarkdown'
    _response = json.loads(requests.get('https://api.github.com/repos/fletcher/MultiMarkdown-6/releases').text)
    for each in _response:
        for asset in each['assets']:
            if '.zip' in asset['name']:
                current_version = asset['name'].split('-')[-1].rsplit('.zip')[0]
                break
        if current_version:
            break
    update_app(name,current_version)

def get_redirect_url(url):
    r = requests.head(url, stream=True)
    if 'Location' in r.headers:
        return r.headers['Location']
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        response = requests.get(url, headers=headers)
        return response.url

def get_update_v1(url,appname):
    try:
        content = get_redirect_url(url)
    except Exception as e:
        print(e)
    else:
        update_app(appname,content)

def get_update_v2(url,appname):
    try:
        download_url = get_redirect_url(url)
    except Exception as e:
        print(e)
    else:
        filename = download_url.split('=')[-1]
        content = "%s %s" % (filename,download_url)
        update_app(appname,content)

def update_app(name,content):
    if os.path.exists('versions/%s.latest' % name):
        bucket_content = os.popen('cat versions/{}.latest'.format(name)).read().replace("\n","")
    else:
        bucket_content = ""
    if content != bucket_content:
        print("%s:%s-->%s" %(name,bucket_content,content))
        os.system("echo {} > versions/{}.latest".format(content,name))
    else:
        print("%s:无需更新" % name)

def fix_noting_update():
    os.system("date > versions/latest")

if __name__ == '__main__':
    get_update_multimarkdown()
    get_update_v1('https://clipber.com/getzip','Copies')
    get_update_v1('https://www.foxmail.com/win/download','Foxmail')
    get_update_v1('https://work.weixin.qq.com/wework_admin/commdownload?platform=win&from=wwindex','WechatWork')
    get_update_v2('http://www.easynlight.com/el-library/eldownload.php?product=Twomon_Windows','TwomonUSB')
    get_update_v2('https://www.bignox.com/en/download/fullPackage','Noxplayer')
    get_update_v3('Charles','https://www.charlesproxy.com/','Charles ([\d.]+) released')
    fix_noting_update()
