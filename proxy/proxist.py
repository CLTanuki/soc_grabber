#!/usr/bin/env python
#=========================================================#
# [+] Title: Hide My Ass Proxy Grabber - Proxist 1.0      #
# [+] Script: proxist.py                                  #
# [+] Blog: http://pytesting.blogspot.com                 #
#=========================================================#

import re
import socket
import datetime
import requests
from optparse import OptionParser


def requestProxy():

    response = requests.get("http://proxylist.hidemyass.com/?pr[]=0&pr[]=1&s=0&o=0&pp=3&sortBy=date")
    return response.text


def testConnection(proxy):
    socket.setdefaulttimeout(10)
    try:
        # http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # http.connect((ip, int(port)))
        # request = "GET /search?output=search&q=Python+Pentesting HTTP/1.1\r\n"
        # request += "Host: www.google.com:80\r\n"
        # request += "User-Agent: Proxist 1.0\r\n"
        # request += "Referer: http://pytesting.blogspot.com\r\n"
        # request += "\r\n"
        #
        # requestTime = datetime.datetime.now() # get date and time
        # requestTime = requestTime.timetuple() # store date and time in tuple
        # # time.hour*3600+time.minute*60+time.second
        # requestTime = requestTime[3]*3600+requestTime[4]*60+requestTime[5]
        # http.send(request)
        #
        # response = http.recv(65535)
        # responseTime = datetime.datetime.now()
        # responseTime = responseTime.timetuple()
        # responseTime = responseTime[3]*3600+responseTime[4]*60+responseTime[5]
        #
        # speed = responseTime-requestTime

        speed = requests.get('http://www.google.com:80', proxies=proxy).elapsed.total_seconds()
        return speed
    except socket.error:
        return -1


def getNoneStyle(entry):
     # find all .XXX{display:XXXXX} styles
    temp = re.findall("\.(.+){display:(.+)}", entry)
    # will be filled with styles of display:none (MUST be initialized with display:none)
    none=["display:none"]
    for s in temp:
        if "none" in s[1]:
            none.append(s[0])
    return none


def getEntries(dest, table, pattern, special=False):
    """
        dest: where the values will be stored
        table: where to search
        pattern: what to search for
        special: should be set True if a value is located in </smthg>XXXX
    """
    
    end = 0
    temp = table
    while True:
        result = re.search(pattern, temp)
        if result:
            if special:  # if format is </smthg>XXXX
                dest += [("inline", result.group(1),result.start()+end)]
            else:
                dest += [(result.group(1),result.group(2),result.start()+end)]
            end += result.end()
            temp = temp[result.end():]
        else:
            break


def getIP(table, nones):
    table = sorted(table, key=lambda n: n[2])  # sort by position (third element)
    ip = ""
    for element in table:
        if element[0] not in nones:
            ip += element[1]
    return ip


def stripTime(time):
    """
        INPUT:
            time: %d hour(s) and %d minute(s)
        OUTPUT:
            %dh:%dm
    """
    stime = time  # Stripped time

    stime = stime.replace(" hours", "h")
    stime = stime.replace(" hour", "h")
    stime = stime.replace(" and ", "")
    stime = stime.replace(" minutes", "m")
    stime = stime.replace(" minute", "m")
    return stime


def querryInfo(html, info):

    if info == "port":
        result = re.search('([0-9]+)</td>', html).group(1)
    elif info == "country":
        result = re.search('alt="flag "/>(.+)</span>', html).group(1)
    elif info == "protocol":
        result = re.search('<td>(.+)</td>', html).group(1)
    elif info == "anonymity":
        result = re.search('<td nowrap>(.+)</td>', html).group(1)
    else:
        result = None

    return result


def printProxy(proxies, pfile, saveall):

    header = "  IP Address   | Port | Protocol | Resp Time"
    hFile = open(pfile, "a")
    if hFile and saveall:
        hFile.write("-"*77)
        hFile.write("\r\n"+header+"\r\n")
        hFile.write("-"*77+"\r\n")
            
    for proxy in proxies:
        entry = "%-15s|%-5s|%-8s|%-6s" % (proxy[1], proxy[2],
                                          proxy[4], str(proxy[6]) + " sec")
        if hFile:
            if saveall:
                hFile.write(entry+"\r\n")
            else:
                hFile.write(proxy[1]+":"+proxy[2]+"\r\n")

    if hFile:
        print("\r\n[+] Sorted proxy list stored in: %s" % pfile)
        hFile.close()
    

def main():
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="output", type="string",
                      help="Output file", metavar="FILE", default="proxist.log")
    parser.add_option("-a", "--all", dest="saveall",
                      help="Store all information", action="store_true", default=False)

    options, args=parser.parse_args()
    output = options.output
    saveall = options.saveall

    proxy_dict = {"http": "",
                  "https": ""}

    # Request page
    html = requestProxy()

    # will contain the index of start of every proxy table
    index = []
    rip = html
    # pattern object of proxy table
    p = re.compile('<tr class=".*"  rel=".*">')
    while True:
        try:
            start = p.search(rip).start()
            end = p.search(rip).end()
            # store the index of the current proxy table
            index.append(start)
            # get rid of the start of the current proxy table
            rip = rip[end:]
        except AttributeError:
            break

    # browse all proxy entries to extract data
    proxies = []
    print("-"*46)
    print("  IP Address   | Port | Protocol | Resp Time")
    print("-"*46)
    for start in index:
        # get rid of stuff before the current proxy entry
        html = html[start:]
        # find the end of the proxy's entry
        end = re.search('[0-9]+</td>', html).end()
        # store the table in element
        element = html[:end]
        # element = element[result.end():end]  # get rid of updates

        # will be filled with styles of display:none
        none = getNoneStyle(element)
        # git rid of .XXXX{display:XXXXXXX}    
        proxy = re.search("</style>(.+)</span></td>", element).group(1)
        # list of span's & </div>[0-9.]+ values and it's position
        table = []

        #==============================================
        # find <span ...="XXX">XXX</span>
        getEntries(table, proxy, '<span .+?="(.+?)">(.+?)</span>')
        #==============================================
        # find <span...>...</span>XXX<span...>
        #==============================================
        getEntries(table, proxy, '</span>([0-9.]+)', True)
        #==============================================
        # find <div...>...</div>XXX<span...>
        #==============================================
        getEntries(table, proxy, '</div>([0-9.]+)', True)
        #==============================================
        # special:XXX<span... at the beginning
        #==============================================
        result=re.match('([0-9.]+)', proxy)
        if result:
            table += [("inline", result.group(1), result.start())]

        ip = getIP(table, none)
        port = querryInfo(html, "port")
        country = querryInfo(html, "country")
        protocol = querryInfo(html, "protocol")
        anonymity = querryInfo(html, "anonymity")
        proxy_dict[protocol] = ip + ':' + port
        speed = testConnection(proxy_dict)
        if speed != -1:
            print("%-15s|%-6s|%-10s|%-6s" % (ip, port,
                                             protocol, str(speed) + " sec"))
            proxies += [(ip, port, country, protocol, anonymity, speed)]

        end = re.search('<tr class=".*"  rel=".*">', html).end()
        html = html[end:]

    # Sort proxies by connection speed
    proxies = sorted(proxies, key=lambda n: n[6])
    printProxy(proxies, output, saveall)


if __name__ == '__main__':
    main()