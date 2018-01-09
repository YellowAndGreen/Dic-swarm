# Dic-swarm
###一月六日
写下这篇文章的第一天，由于要期末复习，先说下规划。不盈词典是开源的，放在[github](https://github.com/YellowAndGreen/Dic-swarm)上了。由于是私人使用，所以直接用的爬虫。目前已经完成了同义词和词组的爬取。后期可能会和移动贩卖小组的人一起完成。![思路](http://upload-images.jianshu.io/upload_images/8887974-4e86c7c2d6f8e8cd.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#爬虫的的实现
>首先，走的是用requests库进行网页抓取和用BeautifulSoup和re库进行处理。
+ 组成网址的函数
```
def formurlforsynonym(word):
    url="http://www.thesaurus.com/browse/"+word+"?s=t"
    return url

def formurlforphrase(word):
    url="http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.top"
    return url
```
+ 网页抓取的函数
```
def getResponse(url):
    try:
        r=requests.get(url)
        r.raise_for_status
        r.encoding=r.apparent_encoding
        t=r.text
        return t
    except:
        print("请求失败")
```
+ 查找的函数
```def searchtag(html):
    ilist=re.findall(r"<a class=\"search-js\" href=\".*?#keyfrom=dict.basic.wordgroup\">.*?</span>",html)  
    return ilist

def searchre(html):
    refind=re.findall(r"<span class=\"text\">.*</span>",html)
    return refind
```
+ 主函数
``` 
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

```
+ 最后只需要在一个while中不断循环即可
```
while(1):
    search()

```
>这里有两个问题以待日后改正
1. 函数名称和变量名不符合规范，以后会改正
2. 搜索网页内容时，</p>不知道为何搜索不了，导致无法显示中文

![思路图](http://upload-images.jianshu.io/upload_images/8887974-2056a48d6b978df8.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
#一月八日
今天复习完英语，突然想给同义词加上中文意思，结果...碰到了好多坑...还好，有所收获
首先,仍然是用查找词组时的网址（有道）
```
def formurlforphrase(word):
    url="http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.top"
    return url
```
然后是最最难受的是re的处理！
```
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
```
这里我遇到的第一个坑是中文字符的;和；是不一样的...
第二个坑是千万不要用.这个任意字符...不然会匹配出一堆代码出来，所以要匹配任意数量的中文字符，用：[\u4e00-\u9fa5|
第三个坑是这个网页上面例如“adj.”之后有的有空格，有的还不止一个，所以还要加上零个或零个以上空格字符：\s*
第四个坑...我被这个坑惨了...基础不好...一开始用的匹配函数是match()，匹配出来的结果都是none...调试了半天，回头看了下函数说明才发现这个是从字符串一开始匹配的...
第五个坑是要分清楚find()和findall()是基于HTML的查找方法，不是正则的...
第六个坑是如果一个单词加入没有名词的解释，正则可能会匹配到下面其它单词的解释，甚至找到一些奇怪的代码，一开始是想用排除数字来消除这种情况，但后来发现还是会有其他代码...后来发现加入中文字符限制就可以了

最后要把它显示出来.
```
tplt = "{0:10}\t{1:15}\t{2:15}\t{3:15}\t{4:15}"
for w in words:
        i=i+1
        h1=w.split(">")
        h2=h1[1].split("<")
        htmlforsyn=getResponse(formurlforphrase(h2[0]))
        wordss=searchsynonym(htmlforsyn)
        print(tplt.format(h2[0],wordss[0],wordss[1],wordss[2],wordss[3]))
        if(i>=12):
            break
```
这里也有坑...
首先是格式化tplt里面如果在行距前面加上^就表示居中，但在这里居中会不齐，所以后来去掉了。最坑的是wordss数组，一开始名字的是words，结果显示出来基本上都是none，我看了好久才发现原来这个数组在前面用过...这个事例充分说明了起名字的重要性...
本来只是想加入一个小功能，没想到遇到这么多的坑，真是意外...
正则表达式可真是玄学问题呢呢
