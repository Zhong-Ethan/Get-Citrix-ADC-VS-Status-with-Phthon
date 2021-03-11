import requests
import json
import re
import schedule
import time
from prettytable import PrettyTable


def getauth_token():
    url = "http://172.16.32.50/nitro/v1/config/login"
    payload = {"login": {"username": "nsroot", "password": "citrix@123"}}
    header = {"Content-Type": "application/vnd.com.citrix.netscaler.login+json"}
    response = requests.post(url, data=json.dumps(payload), headers=header)
    cookie = response.headers.get("Set-Cookie")
    token = re.findall('NITRO_AUTH_TOKEN=.*?;', cookie)[0]
    return token


def get_vs(token):
    url = "http://172.16.32.50/nitro/v1/config/lbvserver"
    header = {"Content-Type" : "application/json", 'Cookie': token}
    res = requests.get(url, headers=header).json()
    vs_list = res['lbvserver']
    vs_info = []
    for vs in vs_list:
        vs_name = vs['name']
        vs_status = vs['curstate']
        vs_info.append([vs_name, vs_status])
    return vs_info


def show_vs(vs):
    for i in vs:
        table = PrettyTable(["vs名称", "vs状态"])
        table.add_row([i[0], i[1]])
        table.left_padding_width = 3
        table.right_padding_width = 3
        print(table)


def master():
    auth_token = getauth_token()
    result = get_vs(auth_token)
    show_vs(result)


schedule.every(5).seconds.do(master)

while True:
    schedule.run_pending()
    time.sleep(1)











