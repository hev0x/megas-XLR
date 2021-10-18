#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
version = sys.version_info
if version < (3, 0):
    print('The current version is not supported, you need to use python3')
    sys.exit()
import requests
import json,ast
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import configparser
cf = configparser.ConfigParser()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
secs=cf.sections()
awvs_url ='https://127.0.0.1:13443/'
apikey = ''
headers = {'Content-Type': 'application/json',"X-Auth": apikey}
add_count_suss=0
error_count=0
target_scan=False
target_list=[]
pages = 10

def get_target_list():#获取扫描器内所有目标
    global pages,target_list
    while 1:
        target_dict={}
        get_target_url=awvs_url+'/api/v1/targets?c={}&l=10'.format(str(pages))
        r = requests.get(get_target_url, headers=headers, timeout=30, verify=False)
        result = json.loads(r.content.decode())
        try:
            for targetsid in range(len(result['targets'])):
                target_dict={'target_id':result['targets'][targetsid]['target_id'],'address':result['targets'][targetsid]['address']}
                target_list.append(target_dict)
            pages=pages+10

            if len(result['targets'])==0:
                break
        except Exception as e:
            return r.text


def addTask(url,target):
    try:
        url = ''.join((url, '/api/v1/targets/add'))
        data = {"targets":[{"address": target,"description":"Adicionado via script xD"}],"groups":[]}
        r = requests.post(url, headers=headers, data=json.dumps(data), timeout=30, verify=False)
        result = json.loads(r.content.decode())
        return result['targets'][0]['target_id']
    except Exception as e:
        return e
def scan(url,target,Crawl,user_agent,profile_id,proxy_address,proxy_port,scan_speed,limit_crawler_scope,excluded_paths,scan_cookie,is_to_scan):
    scanUrl = ''.join((url, '/api/v1/scans'))
    target_id = addTask(url,target)
    if target_id:
        try:
            configuration(url,target_id,proxy_address,proxy_port,Crawl,user_agent,scan_speed,limit_crawler_scope,excluded_paths,scan_cookie,target)#配置目标参数信息
            if is_to_scan:
                data = {"target_id": target_id, "profile_id": profile_id, "incremental": False,
                        "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
                response = requests.post(scanUrl, data=json.dumps(data), headers=headers, timeout=30, verify=False)
                result = json.loads(response.content)
                return result['target_id']
            else:
                print(target, '目标仅添加成功')
                return 2

        except Exception as e:
            print(e)


def configuration(url,target_id,proxy_address,proxy_port,Crawl,user_agent,scan_speed,limit_crawler_scope,excluded_paths,scan_cookie,target):#配置目标
    configuration_url = ''.join((url,'/api/v1/targets/{0}/configuration'.format(target_id)))
    if scan_cookie != '':
        data = {"scan_speed":scan_speed,"login":{"kind":"none"},"ssh_credentials":{"kind":"none"},"sensor": False,"user_agent": user_agent,"case_sensitive":"auto","limit_crawler_scope": limit_crawler_scope,"excluded_paths":excluded_paths,"authentication":{"enabled": False},"proxy":{"enabled": Crawl,"protocol":"http","address":proxy_address,"port":proxy_port},"technologies":[],"custom_headers":[],"custom_cookies":[{"url":target,"cookie":scan_cookie}],"debug":False,"client_certificate_password":"","issue_tracker_id":"","excluded_hours_id":""}
    else:
        data = {"scan_speed": scan_speed, "login": {"kind": "none"}, "ssh_credentials": {"kind": "none"},
                "sensor": False, "user_agent": user_agent, "case_sensitive": "auto",
                "limit_crawler_scope": limit_crawler_scope, "excluded_paths": excluded_paths,
                "authentication": {"enabled": False},
                "proxy": {"enabled": Crawl, "protocol": "http", "address": proxy_address, "port": proxy_port},
                "technologies": [], "custom_headers": [], "custom_cookies": [],
                "debug": False, "client_certificate_password": "", "issue_tracker_id": "", "excluded_hours_id": ""}

    r = requests.patch(url=configuration_url,data=json.dumps(data), headers=headers, timeout=30, verify=False)
    #print(configuration_url,r.text)

def delete_targets():#删除全部扫描目标
    global awvs_url,apikey,headers
    while 1:
        quer='/api/v1/targets'
        try:
            r = requests.get(awvs_url+quer, headers=headers, timeout=30, verify=False)
            result = json.loads(r.content.decode())
            if int(result['pagination']['count'])==0:
                print('已全部删除扫描目标，目前为空')
                return 0
            for targetsid in range(len(result['targets'])):
                targets_id=result['targets'][targetsid]['target_id']
                targets_address = result['targets'][targetsid]['address']
                #print(targets_id,targets_address)
                try:
                    del_log=requests.delete(awvs_url+'/api/v1/targets/'+targets_id,headers=headers, timeout=30, verify=False)
                    if del_log.status_code == 204:
                        print(targets_address,' 删除目标成功')
                except Exception as e:
                    print(targets_address,e)
        except Exception as e:
            print(awvs_url+quer,e)


def CustomScan():
    get_target_url = awvs_url + '/api/v1/scanning_profiles'
    post_data={"checks":["wvs/location/cors_origin_validation.js","wvs/CSRF","wvs/SlowHTTPDOS","wvs/Scripts/PerFile/Javascript_Libraries_Audit.script","ovas/"], "custom": True, "name": "CustomScan"}
    r = requests.post(get_target_url, data=json.dumps(post_data),headers=headers, timeout=30, verify=False)
    result = json.loads(r.content.decode())
    get_target_url = awvs_url + 'api/v1/scanning_profiles'
    r = requests.get(get_target_url,headers=headers, timeout=30, verify=False)
    result = json.loads(r.content.decode())
    return result['scanning_profiles'][7]['profile_id']


def main():
    global add_count_suss,error_count,target_scan
    Crawl = False
    proxy_address = '127.0.0.1'
    proxy_port = '777'
    input_urls=sys.argv[1]
    excluded_paths=""
    limit_crawler_scope=""
    scan_speed = "sequential"
    scan_cookie=''
    profile_id="11111111-1111-1111-1111-111111111111"
    is_to_scan=True


    targets = open(input_urls, 'r', encoding='utf-8').read().split('\n')
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.21" #扫描默认UA头
    if Crawl:#仅调用xray进行代理扫描
        profile_id = "11111111-1111-1111-1111-111111111117"
    if target_scan==False:
        for target in targets:
            target = target.strip()
            #if '://' not in target and 'http' not in target:
            if 'http' not in target[0:7]:
                target='http://'+target

            target_state=scan(awvs_url,target,Crawl,user_agent,profile_id,proxy_address,int(proxy_port),scan_speed,limit_crawler_scope,excluded_paths,scan_cookie,is_to_scan)
            if target_state!=2:
                add_count_suss=add_count_suss+1
                #print("{0} adicionado com sucesso:".format(target),str(add_count_suss))
            elif target_state==2:
                pass
            else:
                open('./add_log/error_url.txt', 'a', encoding='utf-8').write(target + '\n')
                error_count=error_count+1
                #print("{0} 添加失败".format(target),str(error_count))
    elif target_scan==True:
        get_target_list()
        scanUrl2= ''.join((awvs_url, '/api/v1/scans'))
        for target_for in target_list:
            data = {"target_id": target_for['target_id'], "profile_id": profile_id, "incremental": False,
                    "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
            configuration(awvs_url, target_for['target_id'], proxy_address, proxy_port, Crawl, user_agent, scan_speed,
                          limit_crawler_scope,
                          excluded_paths, scan_cookie, target_for['address'])  #已有目标扫描时配置
            try:
                response = requests.post(scanUrl2, data=json.dumps(data), headers=headers, timeout=30, verify=False)
                result = json.loads(response.content)
                if 'profile_id' in str(result) and 'target_id' in str(result):
                    print(target_for['address'],'添加到扫描器队列，开始扫描')
            except Exception as e:
                print(str(target_for['address'])+' 扫描失败 ',e)


if __name__ == '__main__':
 main()
