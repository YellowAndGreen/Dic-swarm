import requests
from bs4 import BeautifulSoup
import re
def getResponse(url):
    try:
        r=requests.get(url)
        r.raise_for_status
        r.encoding=r.apparent_encoding
        t=r.text
        return t
    except:
        print("请求失败")

def searchtag(html,tag):
    soup=BeautifulSoup(html,"html.parser")
    tlist=[]
    for item in soup.find(tag):
        if isinstance(tag,bs4.element.tag):
            tlist.append([tag.string])

def searchre(html):
        refind=re.findall(r"<span class=\"text\">.*</span>",html)
        return refind

def formurl(word):
    url="http://www.thesaurus.com/browse/"+word+"?s=t"
    return url

def search():
    word=input("please enter a word：")
    url=formurl(word)
    html=getResponse(url)
    words=searchre(html)
    i=0
    for w in words:
        i=i+1
        h1=w.split(">")
        h2=h1[1].split("<")
        print(h2[0])
        if(i>=7):
            break
search()
m=input("nothing")
