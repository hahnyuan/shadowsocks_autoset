# coding=utf-8
import json
import urllib
import re
import os

server_name = 'IP地址:'
url = 'http://ss.ishadow.online/index_cn.html'
code = 'utf-8'

u = urllib.urlopen(url)
lines = u.readlines()

json_file_name='gui-config.json'
if not os.path.exists(json_file_name):
    with open(json_file_name,'w') as f:
        new_config=json.dumps({"configs":[]})
        f.write(new_config)

def find_pass(lines):
    result_list = []
    ok = 0
    passwd = 0
    port = 0
    host_name = ''
    for line in lines:
        if not re.search(server_name, line) and ok == 0:
            continue
        if host_name == '':
            host_name = re.findall(':.*?>([\w\.]*)<', line)[0]

        ok = 1
        if '端口' in line:
            rst = re.findall('：(\d*)', line)

            port = rst[0]
        if '密码' in line:
            rst = re.findall(':.*?>([\d]*)<', line)
            if len(rst)==0:
                print("WARNING:the passwd \"%s\" is not set, please don't use it!"%host_name)
                ok = 0
                passwd = 0
                port = 0
                host_name = ''
                continue
            passwd = rst[0]
        if passwd and port:
            print("\nhost name:%s" % host_name)
            print('port:%s' % rst[0])
            print('passwd:%s' % rst[0])
            result_list.append((host_name, passwd, port))
            ok = 0
            passwd=0
            port=0
            host_name = ''
    return result_list

result_list = find_pass(lines)
assert len(result_list) != 0, 'cannot get config'

f = open(json_file_name).read()
data = json.loads(f)
for host_name, passwd, port in result_list:
    is_init = 0
    for i in data['configs']:
        if i['server'] == host_name:
            is_init = 1
            i['password'] = passwd
            i['server_port'] = port

    if not is_init:
        new_conf = {'server': host_name,
                    'server_port': int(port),
                    'password': passwd,
                    'method': "aes-256-cfb",
                    }
        data['configs'].append(new_conf)
s = json.dumps(data,indent=3)
f = open(json_file_name, 'w')
f.write(s)
f.close()
os.system('start Shadowsocks.exe')
