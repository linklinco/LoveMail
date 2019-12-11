import yaml
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



