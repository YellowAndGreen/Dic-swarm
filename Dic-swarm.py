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

def searchtag(html):
    ilist=re.findall(r"<a class=\"search-js\" href=\".*?#keyfrom=dict.basic.wordgroup\">.*?</span>",html)  
    return ilist

def searchre(html):
    refind=re.findall(r"<span class=\"text\">.*</span>",html)
    return refind

def formurlforsynonym(word):
    url="http://www.thesaurus.com/browse/"+word+"?s=t"
    return url

def formurlforphrase(word):
    url="http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.top"
    return url

def search():
    word=input("please enter a word：")
    url1=formurlforsynonym(word)
    url2=formurlforphrase(word)
    html1=getResponse(url1)
    html2=getResponse(url2)
    words=searchre(html1)
    phrases=searchtag(html2)
    i=0
    print("Here are some synonyms !\n")
    for w in words:
        i=i+1
        h1=w.split(">")
        h2=h1[1].split("<")
        print(h2[0])
        if(i>=7):
            break
    j=0
    print("\nHere are phrases !\n")
    for n in phrases:
        j=j+1
        h1=n.split("wordgroup\">")
        h2=h1[1].split("</a>")
        print(h2[0])
        if(j>=10):
            break
    print("\n")

    
while(1):
    search()
