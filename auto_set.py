# coding=utf-8
import json
import urllib
import re
import os

server_name='A服务器'
url='http://www.ishadowsocks.net/'
code='utf-8'

u=urllib.urlopen(url)

lines=u.readlines()
def find_pass(lines):
    ok=0
    passwd=0
    port=0
    host_name=''
    for line in lines:
        if not re.search(server_name, line) and ok==0:
            continue
        if host_name=='':
            host_name=re.findall(':([\w\.]*)<',line)[0]
        ok=1
        if '端口' in line:
            rst=re.findall(':(\d*)',line)
            print('port:%s'%rst[0])
            port=rst[0]
        if '密码' in line:
            rst=re.findall(':(\d*)',line)
            print('passwd:%s'%rst[0])
            passwd=rst[0]
        if passwd and port:
            return host_name,passwd,port
    return 0,0
host_name,passwd,port=find_pass(lines)
assert passwd!=0 ,'cannot get passwd'
f=open('gui-config.json').read()
data=json.loads(f)

is_init=0
for i in data['configs']:
    if i['server']==host_name:
        is_init=1
        i['password']=passwd
        i['server_port']=port

if not is_init:
    new_conf={'server':host_name,
            'server_port':int(port),
            'password':passwd,
            'method':"aes-256-cfb",
            }
    data['configs'].append(new_conf)
s=json.dumps(data)
f=open('gui-config.json','w')
f.write(s)
f.close()
os.system('Shadowsocks.exe')
