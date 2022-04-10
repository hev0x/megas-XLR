#!/usr/bin/python3

import requests
import json
import optparse
import re

from requests.packages import urllib3
from requests.exceptions import MissingSchema, InvalidURL

urllib3.disable_warnings()

session = requests.Session()

#route_getVulns = '/api/v1/vulnerabilities'
route_vulnTypes = '/api/v1/vulnerability_types' # -> this endpoint could be used to filter this vulns by severity and get id to search detaileds results
#route_vulnGroups = '/api/v1/vulnerability_groups' 

awvs_url ='https://xxxxxxxx'
apikey = '1986ad8c0a5b3df4d7:D-not-so-fast-bitch!!'
headers = {'Accept': 'application/json','Content-Type': 'application/json',"X-Auth": apikey}

#response = session.get(awvs_url + route_getVulns,headers=headers,verify=False)
#response = session.get(awvs_url + route_vulnTypes,headers=headers,verify=False)
response = session.get(awvs_url + route_vulnGroups,headers=headers,verify=False)


print(response.text)
