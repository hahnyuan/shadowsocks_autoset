# coding=utf-8
# Please put this file in your shadowsocks root direction

import json
import urllib
import re
import os,sys

os.chdir(sys.path[0])

server_name='usa.iss.tf'
url='http://www.ishadowsocks.net/'
code='utf-8'

u=urllib.urlopen(url)

lines=u.readlines()
def find_pass(lines):
    ok=0
    passwd=0
    port=0
    for line in lines:
        if not re.search(server_name, line) and ok==0:
            continue
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
            return passwd,port
    return 0,0
passwd,port=find_pass(lines)
assert passwd!=0 ,'cannot get passwd'

if not os.path.isfile('gui-config.json'):
    f=open('gui-config.json','w')
    f.write('{"configs" : []}')
    f.close()
conf=open('gui-config.json').read()
data=json.loads(conf)

is_init=0
for i in data['configs']:
    if i['server']==server_name:
        is_init=1
        i['password']=passwd
        i['server_port']=port

if not is_init:
    new_conf={'server':server_name,
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
