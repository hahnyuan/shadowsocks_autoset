# coding=utf-8
import json
import urllib
import re
import os

u=urllib.urlopen('http://www.ishadowsocks.net/')

lines=u.readlines()
def find_pass(lines):
    ok=0
    for line in lines:
        if not re.search(u'us1.iss.tf', line) and ok==0:
            continue
        ok=1
        if re.search('密码',line):
            rst=re.findall(':(\d*)',line)
            print rst[0]
            return rst[0]
    return 0
passwd=find_pass(lines)
assert passwd!=0 ,'cannot get passwd'
f=open('gui-config.json').read()
data=json.loads(f)
for i in data['configs']:
    if i['server']=='US1.ISS.TF':
        i['password']=passwd
s=json.dumps(data)
f=open('gui-config.json','w')
f.write(s)
f.close()
os.system('Shadowsocks.exe')