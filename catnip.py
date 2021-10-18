import sys
import requests
import optparse
import multiprocessing
import re
from bs4 import BeautifulSoup
from requests.packages import urllib3
from requests.exceptions import MissingSchema, InvalidURL

urllib3.disable_warnings()

requestEngine = multiprocessing.Manager()

session = requests.Session()
global paramResults
paramResults = requestEngine.list()

#def params():
globals().update(locals())

def spiderPage(url):
    globals().update(locals())
    if not url.startswith('http'):
        url='http://'+url
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
               "Connection": "close",
               "Accept-Encoding": "gzip, deflate"}

    try:
        rawResp = session.get(url,headers=headers,allow_redirects=False, verify=False,timeout=5)

        soupmebitch = BeautifulSoup(rawResp.text, 'html.parser')
        inputBuffer = soupmebitch.find_all('input')

        if inputBuffer:
            paramResults.append(url + ':' + str(inputBuffer))

        print(url)
        print(inputBuffer)

    except requests.exceptions.ConnectionError:
        print('[x] Failed to Connect: '+url)
        pass
    except KeyboardInterrupt:
        print('[!] Stoping spidering...')
        exit(0)
    except (MissingSchema, InvalidURL):
        pass


def main():
    globals().update(locals())
    #params()
    
    sys.setrecursionlimit(100000)

    if not sys.stdin.isatty():
        urls = sys.stdin.read()
    else:
        f = open(optionsOpt.file)
        urls = map(str.strip, f.readlines())

    multiReq = multiprocessing.Pool(optionsOpt.threads)

    try:
        multiReq.map(spiderPage, urls)
        multiReq.close()
        multiReq.join()
    except UnboundLocalError:
        pass
    except KeyboardInterrupt:
        exit(0)

    if optionsOpt.output:
        print("\n[!] Saving the output result in: %s" % optionsOpt.output)

        with open(optionsOpt.output, "w") as f:
            for result in paramResults:
                f.write("%s\n" % result)
        f.close()

if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option('-u', '--url', action="store", dest="url", help='Base target uri (ex. http://target-uri/)')
    parser.add_option('-f', '--file', dest="file", help='example.txt')
    parser.add_option('-t', '--threads', dest="threads", type=int,default=10)
    parser.add_option('-m', '--maxtimeout', dest="timeout", type=int,default=8)
    parser.add_option('-o', '--output', dest="output", type=str,default='cookies.txt')
    optionsOpt, args = parser.parse_args()

    main()
