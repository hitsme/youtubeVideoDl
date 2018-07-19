import urllib2
from bs4 import BeautifulSoup
def getNetWorkIp():
    url = "http://ip.chinaz.com/siteip"
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content)
    ip = soup.find("dd", {"class": "fz24"})
    return ip.string