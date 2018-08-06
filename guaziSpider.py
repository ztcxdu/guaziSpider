#/usr/bin/python3
#coding:utf-8
import requests
import re
from hashlib import md5
import demjson

from execute_script import excuteScript

"""
reference:https://bbs.csdn.net/topics/392377474?list=lz
author:Mrtddc
"""

def getAntipas():
    """获取cookie中的参数antipas"""
    
    url = 'https://www.guazi.com/bj/'
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    #'Cookie': 'antipas=45r154945f5D0200252W9PV793m',
    'Host': 'www.guazi.com',
    #'Referer': 'https://www.guazi.com/bj/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
    
    r = requests.get(url,headers=headers)
    value = re.findall('value=anti\((?<=[(（])[^（）()]*(?=[)）])\)',r.text)[0]
    anti = re.findall("'(.*?)'",value)
    antipas = excuteScript(anti[0],anti[1])
    return antipas
    
def getToken(antipas):
    """获取发送短信验证码时需要提交的参数token和time"""
    
    url = 'https://www.guazi.com/bj/'
    
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'antipas='+str(antipas),
    'Host': 'www.guazi.com',
    'Referer': 'https://www.guazi.com/bj/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
    
    r = requests.get(url,headers=headers)
    time = re.findall("data-time='[0-9]*'",r.text,re.S)[0][-11:-1]
    data_str = re.findall("data-str='[0-9a-f]*'",r.text,re.S)[0][-33:-1]
    return data_str,time
    
def sendSms(phoneNumber,data_str,time,antipas):
    """以post方式提交"""
    
    url = 'https://www.guazi.com/zq_user/?act=register'
    
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '72',
    'Cookie': 'antipas='+str(antipas),
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.guazi.com',
    'Origin': 'https://www.guazi.com',
    'Referer': 'https://www.guazi.com/bj/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}
    
    data = {
    'phone': phoneNumber,
    'time': time,
    'token': md5((data_str+'guazi&js&token'+str(phoneNumber)).encode('utf-8')).hexdigest() #从JS代码中找到的token的生成方法
    }
    
    r = requests.post(url,headers=headers,data=data)
    result = demjson.decode(r.text)
    print(result)
    
    
if __name__ == '__main__':
    phoneNumber = input('PLease input phone number:')
    antipas = getAntipas()
    data_str,time = getToken(antipas)
    sendSms(phoneNumber,data_str,time,antipas)
