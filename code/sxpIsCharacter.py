#-------------------------------------------------------------------------------
# Name:        sxpIsCharacter
# Purpose:     This package is to judge if one
#
# Author:      sunxp
#
# Created:     04/02/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
import urllib.parse
def parseURL(hosturlstr,urlstr):
    hu = urllib.parse.urlparse(hosturlstr)#this is the main url str of a web page
    if hu.netloc == '':
        return [-1, ''];
    hstr = hosturlstr
    #means that there is no http: head so we need to tell if it is //
    if hu.scheme == '':
        hstr = 'http://'+hstr;

    up = urllib.parse.urlparse(urlstr)
    #if there is no net location string, just return -1
    if up.scheme == 'http':
        return [1, urlstr];
    if up.scheme == '':
        if up.netloc == '':
            if up.path == '': #this url is really a not url
                if up.fragment != '':
                    #here url is like this '#home'
                    #means that this is an anchor point in the main hosturl page
                    return [0, up.fragment]
                else:
                    return [-1, ''];
            else:
                #here url is like this: '/wiki/db'
                #this url is a relative path, we need to add the host to it
                print(up)
                return [2, urllib.parse.urljoin(hstr,urlstr)]
        else:
            #here urlstr is like this: '//wiki.com'
            return [1,'http:' + urlstr]
    else:
        return [-1, up.scheme];

def parseURLOld(hosturlstr,urlstr):
    hu = urllib.parse.urlparse(hosturlstr)#this is the main url str of a web page
    if hu.netloc == '':
        return [-1, ''];
    hstr = hosturlstr
    #means that there is no http: head so we need to tell if it is //
    if hu.scheme == '':
        hstr = 'http://'+hstr;

    up = urllib.parse.urlparse(urlstr)
    #if there is no net location string, just return -1
    if up.scheme == 'http':
        return [1, urlstr];
    if up.scheme == '':
        if up.netloc == '':
            if up.path == '': #this url is really a not url
                if up.fragment != '':
                    #here url is like this '#home'
                    #means that this is an anchor point in the main hosturl page
                    return [0, up.fragment]
                else:
                    return [-1, ''];
            else:
                #here url is like this: '/wiki/db'
                #this url is a relative path, we need to add the host to it
                print(up)
                if urlstr[0] != '/':
                    return [2, hstr + '/'+ urlstr]
                else:
                    return [2, hstr + urlstr];
        else:
            #here urlstr is like this: '//wiki.com'
            return [1,'http:' + urlstr]
    else:
        return [-1, up.scheme];

def toGBK(str):
    if isinstance(str,str):
        ugs = str.encode('gbk') #using gb2312 is also ok for baidu news
    else:
        gs = str.decode('utf-8','ignore').encode('gbk','ignore')
        ugs = gs.decode('gbk')
    return ugs
def toPringGBK(str):
    restr = ''
    try:
        restr = str.decode('utf-8').encode('gbk')
    except Exception as e:
        restr = str;
    return restr;
def toUTF(str):
##    try:
## #       print str
##        gs = str.encode('utf-8')
##    except Exception as e:
##        print e;
##        print str;
##        print type(str)
##        print isinstance(str,unicode)
##        exit()
    if isinstance(str,str):
        gs = str.encode('gbk') #using gb2312 is also ok for baidu news
    else:
        gs = str.decode('utf-8').encode('gbk')
    return gs
def is_chinese(uchar):
#"""判断一个unicode是否是汉字"""
    if uchar >= '\u4e00' and uchar<='\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
#"""判断一个unicode是否是数字"""
    if uchar >= '\u0030' and uchar<='\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
#"判断一个unicode是否是英文字母"""
    if (uchar >= '\u0041' and uchar<='\u005a') or (uchar >= '\u0061' and uchar<='\u007a'):
        return True
    else:
        return False

def is_other(uchar):
#"""判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False

def B2Q(uchar):
#"""半角转全角"""
    inside_code=ord(uchar)
    if inside_code<0x0020 or inside_code>0x7e: #不是半角字符就返回原来的字符
        return uchar
    if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code=0x3000
    else:
        inside_code+=0xfee0
    return chr(inside_code)

def Q2B(uchar):
#"""全角转半角"""
    inside_code=ord(uchar)
    if inside_code==0x3000:
        inside_code=0x0020
    else:
        inside_code-=0xfee0
    if inside_code<0x0020 or inside_code>0x7e: #转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)

def stringQ2B(ustring):
#"""把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
#"""格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()

def string2List(ustring):
#"""将ustring按照中文，字母，<strong>数字</strong>分开"""
    retList=[]
    utmp=[]
    for uchar in ustring:
        if is_other(uchar):
            if len(utmp)==0:
                continue
            else:
                retList.append("".join(utmp))
            utmp=[]
        else:
            utmp.append(uchar)
            if len(utmp)!=0:
                retList.append("".join(utmp))
    return retList

def testURLParse():
    hs = r'http://www.sina.com.cn'

    s = r'javascript:void(0)'
    up = parseURL(hs,s)
    print(s, up)

    s = r'www.sina.com.cn'
    up = parseURL(hs,s)
    print(s, up)

    s = r'//www.sina.com.cn'
    up = parseURL(hs,s)
    print(s, up)

    s = r'/www.sina.com.cn'
    up = parseURL(hs,s)
    print(s, up)

    s = r'#home'
    up = parseURL(hs,s)
    print(s, up)

    s = r'index.html'
    up = parseURL(hs,s)
    print(s, up)

    s = r"../../findallsupplier.action?sign=0"
    up = parseURL(hs,s)
    print(s, up)

    hs = r'http://www.sohu.com/time/host/hello.htm';
    s = r"../../findallsupplier.action?sign=0"
    ts = urllib.parse.urljoin(hs,s)
    print(ts);

    bs = r'http://www.knowledgegrid.net/skg2015/'
    s = r'./index_files/right_news.html'
    ts = urllib.parse.urljoin(bs,s)
    print(ts);

def main():
    testURLParse()

if __name__ == '__main__':
    main()