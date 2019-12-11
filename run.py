import yaml
import json
import re
import requests
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
from  jinja2 import Template
#禁用ssl验证代码
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# 把收件人昵称和邮件类型添加到邮件正文里
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

#爬取bing每日图片的链接
def getBingPhotoUrl():
    url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    res = urllib.request.urlopen(url)
    json_txt = res.read()
    txt = json.loads(json_txt)
    url = 'https://www.bing.com/' + txt['images'][0]['url']
    return url

#爬取你好污呀的句子
def getNihaowu():
    url = "https://www.nihaowua.com/"
    html = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"})
    html = html.text
    reg = '<section> <div(.*?) </div> </section>'
    tex = re.findall(reg, html)
    reg = r'>(.*?)</'
    tex = re.findall(reg, str(tex))
    reg = r">(.*)']"
    tex = re.findall(reg, str(tex))
    for i in tex:
        return i

#获取天气信息
def getWeather():
    url = 'http://t.weather.sojson.com/api/weather/city/101200101'
    t = urllib.request.urlopen(url)
    weat = t.read().decode('utf-8')
    js = json.loads(weat)
    weather="今天是{},天气情况为{}，最高温度{}，最低温度{}。空气质量指数为{}，{}。".format(js['data']['forecast'][0]['week'],js['data']['forecast'][0]['type'],js['data']['forecast'][0]['high'][3:],js['data']['forecast'][0]['low'][3:],js['data']['forecast'][0]['aqi'],js['data']['forecast'][0]['notice'])
    return weather

#获取一句里的句子
def getTodayHitokoto():
    url = 'https://v1.hitokoto.cn/'
    response = requests.get(url)
    hit = json.loads(response.text)
    return hit["hitokoto"]

#获取词霸api
def getIcibaToday():
    url ='http://open.iciba.com/dsapi'
    html=urllib.request.urlopen(url)
    html=html.read().decode('utf-8')
    js = json.loads(html)
    en_li=js['content']
    cn_li=js['note']
    pic=js['picture2']
    mis=js['tts']
    html = [pic,en_li,cn_li,mis]
    return html


# 发送邮件函数
def sendMail(title,text,sender,recevicer):
    msg = MIMEMultipart()

    name = sender['name']
    address = sender['address']
    password = sender['password']
    smtp_server = sender['smtp_server']

    msg['From'] = _format_addr('%s <%s>' % (name,address))
    msg['To'] = _format_addr('%s <%s>' % (recevicer['name'],recevicer['address']))
    msg['Subject'] = Header(title, 'utf-8').encode()
    msg.attach(MIMEText(text, 'html', 'utf-8'))

    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.login(address, password)
    server.sendmail(address,recevicer['address'],msg.as_string())
    server.quit()
#调用jinja2的Template类，生成html格式邮件
def renderHtml():
    with open('template.html','r',encoding='utf-8') as f :
        t=Template(f.read())
        t=t.render()
        return t

if __name__ == "__main__":
    with open('conf.yaml', 'r', encoding='utf8') as f:
        data = yaml.load(f)
        print(renderHtml())
        sender = data['send']
        for i in data['recevice']:
            sendMail('title',renderHtml(),sender,i['mail'])



