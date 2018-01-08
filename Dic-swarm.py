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
def searchsynonym(html):
    words=[]
    refindn=re.search(r"n\.\s*[\u4e00-\u9fa5]*?；",html)
    if refindn:
        words.append(refindn.group(0))
    else:
        words.append("none")
    refindvt=re.search(r"vt\.\s*[\u4e00-\u9fa5|，]*?；",html)
    if refindvt:
        words.append(refindvt.group(0))
    else:
        words.append("none")
    refindvi=re.search(r"vi\.\s*[\u4e00-\u9fa5|，]*?；",html)
    if refindvi:
        words.append(refindvi.group(0))
    else:
        words.append("none")
    refindadj=re.search(r"adj\.\s*[\u4e00-\u9fa5|，]*?；",html)
    if refindadj:
        words.append(refindadj.group(0))
    else:
        words.append("none")
    return words
  
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
    tplt = "{0:10}\t{1:15}\t{2:15}\t{3:15}\t{4:15}"
    print("Here are some synonyms !\n")
    for w in words:
        i=i+1
        h1=w.split(">")
        h2=h1[1].split("<")
        htmlforsyn=getResponse(formurlforphrase(h2[0]))
        wordss=searchsynonym(htmlforsyn)
        print(tplt.format(h2[0],wordss[0],wordss[1],wordss[2],wordss[3]))
        if(i>=12):
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
