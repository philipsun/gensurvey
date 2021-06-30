#-------------------------------------------------------------------------------
# Name:        sxpJudgeCharacter
# Purpose:     This is the package for judging a character is a text or something else
#
# Author:      sunxp
#
# Created:     04/02/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding:GBK -*-
## -*- coding=utf-8 -*-
import re

#from typing import List, Any, Union

import sxpTestStringEncode
import urllib.parse
import nltk
import numpy as np

def is_chinese(uchar):
##        """判断一个unicode是否是汉字"""
        if uchar >= '\u4e00' and uchar<='\u9fa5':
                return True
        else:
                return False

def is_number(uchar):
##        """判断一个unicode是否是数字"""
        if uchar >= '\u0030' and uchar<='\u0039':
                return True
        else:
                return False
def is_charspace(c):
    g = re.match('[\w|\W|\s]',c)
    if g:
        return True
    else:
        return False
def is_alphabet(uchar):
##         """判断一个unicode是否是英文字母"""
        if (uchar >= '\u0041' and uchar<='\u005a') or (uchar >= '\u0061' and uchar<='\u007a'):
                return True
        else:
                return False

def is_other(uchar):
##         """判断是否非汉字，数字和英文字符"""
        if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
                return True
        else:
                return False

def B2Q(uchar):
##         """半角转全角"""
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
                return uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code=0x3000
        else:
                inside_code+=0xfee0
        return chr(inside_code)

def Q2B(uchar):
##         """全角转半角"""
        inside_code=ord(uchar)
        if inside_code==0x3000:
                inside_code=0x0020
        else:
                inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
                return uchar
        return chr(inside_code)



def stringQ2B(ustring):
##         """把字符串全角转半角"""
        return "".join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
##         """格式化字符串，完成全角转半角，大写转小写的工作"""
        return stringQ2B(ustring).lower()

def string2List(ustring):
##         """将ustring按照中文，字母，数字分开"""
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
def string2ListChinese(ustring, keepnonchinese=False):
##         """将ustring按照中文，非中文分开,只保留中文字符，不保留其他字符"""
        retList=[]
        utmp=[]
        dtmp=[]
        for uchar in ustring:
                if not is_chinese(uchar):
                        if len(utmp)==0 and len(dtmp)==0:
                                continue
                        else:
                                if len(utmp) !=0:
                                    retList.append("".join(utmp))
                                    utmp=[]
                                dtmp.append(uchar)
                else:
                        if keepnonchinese==True:
                            if len(dtmp) !=0:
                                retList.append("".join(dtmp))
                            dtmp = []
                        utmp.append(uchar)
        if len(utmp)!=0:
                retList.append("".join(utmp))
        if len(dtmp) !=0:
                retList.append("".join(dtmp))
        return retList
def ReplaceNonEnglishCharacter(txt):
#    print type(str)
    p = re.compile(r"([^\x00-\xff])")

    def func(m):
        st = repr(m.group(1).title())
        st = ' ' + st + ' '
        return st
    g = p.sub(func, txt)
    return g
def Test():
    #test uniform
    ustring='中国 人“名”ａ高频,3..Ａ‣'
    ustring=uniform(ustring)
    ret=string2ListChinese(ustring,True)
    for ch in ret:
        print(ch)

def Test1():
    str = "12ab,:a啊中国‣"
    ustr = sxpTestStringEncode.strencode(str,'utf-8')
    unc =sxpTestStringEncode.strdecode(str,'utf-8')
    print(type(ustr))
    print(type(unc))
    #print ustr
    print(ustr.decode('utf-8'))
    print(repr(ustr.decode('utf-8')))

    p = re.compile(r"([^\x00-\xff])")

    def func(m):
        st = repr(m.group(1).title())

        st = ' ' + st + ' '
        return st
    print('sub begin:')

    g= p.sub(func, unc)
    print('sub result:')
    print(g.decode('utf-8'))
    #print unc.encode('utf-8')

#    g = re.match(ur"([\u4e00-\u9fa5]+)",ustr.decode('utf-8'))
#    g = re.search(ur"([^\w]+)",ustr.decode('utf-8'))
#    g = re.search(ur"([\u4e00-\u9fa5]+)",ustr.decode('utf-8'))
    g = re.search(r"([^\x00-\xff]+)",ustr.decode('utf-8'))
    if g is not None:
        for g in g.groups():
            print(g)
    else:
        print(g)
def SearchProcess(patstr, s, pat_name='',pi=0):
    pattern = re.compile(patstr)
    match =pattern.search(s)
    pattern_pos = []
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(s,posd[1])
        pattern_pos.append([tgtxt,posd,tg,pat_name,pi])
    return pattern_pos
#this will pasre string text like this:
# The most-nominated film was ``All About Eve'' in 1950.
#into three parts, by extracting "All About Eve" as the tagged structure
def segbymarksamepair(segpat_list,txt,segpatnamedict=None):
    if len(txt)==0:
        return []
    if txt[-1] !='.':
        txt =txt+'.'
    stxt = txt +'#'
    segpat = '|'.join(segpat_list) + r'|\.#'
    pt_pos = SearchProcess(segpat,stxt,pat_name='segpair')
    if segpatnamedict is None:
        sdict = {}
        for pt in segpat_list:
            sdict[pt]='g'
    elif isinstance(segpatnamedict,str):
        sdict = {}
        for pt in segpat_list:
            sdict[pt]='g'
    else:
        sdict = segpatnamedict
    i = 1
    s = 0
    sent = []
    for pt in pt_pos:
        l = pt[1][0]
        if pt[0] in segpat_list:
            if divmod(i,2)[1] == 0: #if two are paired, we will seg them , note that this will not handle recursive quatation marks.
                seg = stxt[s:l]
                s = pt[1][1]
                sent.append([sdict[pt[0]],seg])
            else:
                mainpart = stxt[s:l]
                sent.append(['m',mainpart])
                s =  pt[1][1]
        if pt[0] in [".#"]: #this means that it reach the end
            l = pt[1][0]
            mainpart = stxt[s:l]
            sent.append(['m',mainpart])
        i = i + 1
    return sent
#this will pasre string text like this:
# The most-nominated film was <All About Eve> in 1950.
#into three parts, by extracting "All About Eve" as the tagged structure
#but this version does not handle recursively emembded brackets.

def segbysympair(stxt,segpatnamedict):
    ptlist= []
    pt_name_dict ={}
    #here pt is defined as 'bracket':['<','>']
    for name,pt in list(segpatnamedict.items()):
        ptlist.append(pt[0])
def segbymark(segpat_list,txt,segpatname):
    if txt[-1] !='.':
        txt =txt+'.'
    stxt = txt +'#'
    segpat = '|'.join(segpat_list) + '|\.#'
    pt_pos = SearchProcess(segpat,stxt,pat_name=segpatname)
    i = 1
    s = 0
    sent = []
    for pt in pt_pos:
        l = pt[1][0]
        if pt[0] in["''","``",'"']:
            if divmod(i,2) == 0: #if two are paired, we will seg them , note that this will not handle recursive quatation marks.
                seg = stxt[s:l]
                s = pt[1][1]
                sent.append([segpatname,seg])
            else:
                mainpart = stxt[s:l]
                sent.append(['m',mainpart])
                s =  pt[1][1]
        if pt[0] in [".#"]: #this means that it reach the end
            l = pt[1][0]
            mainpart = stxt[s:l]
            sent.append(['m',mainpart])
    return sent
def segsenttowords(txt):
#    pt = '\s+'
#    wd = re.split(pt,txt)
#    return wd
    return splitword(txt)

def seg_comma(txt):
    pt = '[,\s+]'
    subsent = re.split(pt,txt)
    return subsent
def seg_colon(txt):
    pt = '[:\s+]'
    subsent = re.split(pt,txt)
    return subsent
def seg_quest(txt):
    pt = '[:\s+]'
    subsent = re.split(pt,txt)
    return subsent

def segquotation(txt):
    #first we need to add end mark to the txt to help seg them

    #then, we begine to search quotation marks
    pat_list = [r"''",r"``",r'"',r"'"]#note that, those are just single side symbole, not two symbol.
    sent=segbymarksamepair(pat_list,txt)
    return sent
def isCapitalWords(txt):
    return txt.istitle()
mystopword=['a', 'an','the','this','that','which','in','for','it','with','by','and','to','from','at','on','of','are','was','how','what'
          ,'can','will','would','when','after','before','under','is','some','them','they','but','many','other','these','now','where',
          'we','has','have','been','being','its','their','each','then','our','as','or','not','no','if',
          ]
stopwordline = open('stopwords.txt', 'r').readlines()
stopword=[]

for each in stopwordline:
    stopword.append(each.strip())

def isstopword(w):
    for s in stopword:
        if w.lower()==s:
            return True

    return False
def removestops(tops):
    newtops = []
    for eachsent in tops:
        segs=splitword(eachsent)
        s = " "
        for w in segs:
            if isstopword(w):
                continue
            s = s + w +' '
        newtops.append(s)
    return newtops
def splitword(txt):
    if len(txt)==0:
        return [""]
    s =segquotation(txt)
    wdlist=[]
    for each  in s:
        if each[0]=='m':
            gotog =2
        if each[0]=='g':
            gotog=1
        if gotog==1:
            if isCapitalWords( each[1]):
                wdlist.append(each[1])
                continue
            else:
                gotog=2
        if gotog==2:
            txt = each[1] + ' '
            spt = "[\.\,\?\!\:\'\"\']\s+"
            wds = re.split(spt, txt)
            for w in wds:
                if w.isspace():
                    continue
                if len(w)==0:
                    continue
                wpt = '\s'
                sd = re.split(wpt,w)
                for ew in sd:
                    if ew.isspace():
                        continue
                    if len(ew)==0:
                        continue
                    wdlist.append(ew)
    if len(wdlist)==0:
        return [txt]
    else:
        return wdlist
def allsymdig(sent):
    pt = '[\d\(\)\,\.\+\-]'
    g = re.findall(pt,sent)
    np = len(g)
    n = len(sent)
    if np*1.0/n >0.5:
        return True
    return False
def haspattern(pt,sent):
    g = re.findall(pt,sent)
    if g is None:
        return False
    if len(g)>0:
        return True
    return False
def remsymdig(sent):
    pt = '[\d\(\)\,\.\+\-]'
    g = re.findall(pt,sent)
    np = len(g)
    n = len(sent)
    if n==0:
        return ""
    if np*1.0/n >0.5:
        return ""
    else:
        ns=re.sub(pt,"",sent).strip()
        return ns
def sentdist(s1,s2):
    return Similarity(s1,s2,'jaccard')
def splitstr(s):
    pt = '(,\s|\.\s|\?\s)'
    subs = re.split(pt,s)
    g = re.findall(pt,s)
    segs = []
    for each in subs:
        s = each.strip()
        if s == ',' or s =="." or s=='?':
            continue
        segs.append(s)
    return segs

def SplitSubSent(txt):
    subs=segquotation(txt)  # type: Union[List[Any], List[List[Union[str, Any]]]]
    s = '(\,\s+) |(\:\s+)|(\.\s+)'
    allsubs=[]
    #print(subs)
    for (tag,seg) in subs:
        if len(seg)==0:
            continue
        subs=splitstr(seg)
        for each in subs:
            if len(each)==0:
                continue
            txt = ClearEndAnd(each)
            txt = ClearEndMark(txt)
            if len(txt)==0:
                continue
            allsubs.append(txt)
    return allsubs
def ClearEndAnd(txt):
    pt = '(.+)and(\s*|\,|\.|\!|\:)$'
    g=re.match(pt,txt)
  #  print(g)
    if g:
        return g.groups()[0]
    else:
        return txt
    return g
def ClearEndMark(txt):
    pt = "(.+)(\,|\.|\!|\:)\s*$"
    g=re.match(pt,txt)
  #  print(g)
    if g:
        return g.groups()[0]
    else:
        return txt
    return g

def Similarity(sentence, s,d='jaccard'):
    #if sentence is a tf-idf vector, then use cosine similarity
    #if sentence is a string, use jaccard similarity
    if d=='jaccard':
        return jaccard_similarity(sentence, s)
    else:
        return cosine_similarity(sentence, s)


def jaccard_similarity(sentence, s):
    stopwords = open('stopwords.txt','r').readlines()
    stopwords=[]
    word_list1 = []
    word_list2 = []
    for word in segsenttowords(sentence):
        if word not in stopwords:
            word_list1.append(word.lower().strip())
#    print(word_list1)
    for word in segsenttowords(s):
        if word not in stopwords:
            word_list2.append(word.lower().strip())
#    print(word_list2)
    a = len(set(word_list2).intersection(set(word_list1)))*1.0
    b = len(set(word_list2).union(set(word_list1)))*1.0
 #   print(a,b)
    return a/b
def jaccard_sim_norm(s1,s2):
    stopwords = open('stopwords.txt', 'r').readlines()
    stopwords = []
    word_list1 = []
    word_list2 = []
    for word in segsenttowords(s1):
        if word not in stopwords:
            word_list1.append(word.lower().strip())
    #    print(word_list1)
    for word in segsenttowords(s2):
        if word not in stopwords:
            word_list2.append(word.lower().strip())
    a = len(set(word_list2).intersection(set(word_list1)))*1.0
    l1 = len(word_list1)
    if l1==0:
        l1 =1
    l2 = len(word_list2)
    if l2==0:
        l2 =1
    b = np.log(len(word_list1))+np.log(len(word_list2))
    if b == 0:
        return 0
    return a/b
def cosine_similarity(sentence, s):
    x = np.array(sentence)
    y = np.array(s)
    Lx = np.sqrt(x.dot(x))
    Ly = np.sqrt(y.dot(y))
    cos_angle = x.dot(y)/(Lx * Ly)
    return cos_angle
def GetWordSent(sent_set):
    pass
def Test2():
    s =r"The most-nominated film was ``All About Eve'' in 1950. It has three 3.5's pages in its list."
    s =r"The motion picture industry's most coveted award, Oscar, was created 60 years ago and 1,816 of the statuettes have been produced so far."
    s =r"The Academy holds all the rights on the statue and ``reserves the right to buy back an Oscar before someone takes it to a pawn shop,'' said Academy spokesman Bob Werden."
    s = r"He certainly will not say 'well done, keep it up'"
    print(s)
    print((segquotation(s)))
    print((splitword(s)))
    s1 = 'hello word'
    s2 = 'good word'
    print((segsenttowords(s1)))
    print((jaccard_similarity(s1,s2)))
    print((jaccard_sim_norm(s1,s2)))
    print((SplitSubSent(s)))
def Test3():
    s = " In [2], Lucille Ball, the leggy showgirl, model and B-grade movie queen whose pumpkin hair and genius for comedy made her an icon of television? died early Wednesday. a week after undergoing emergency heart surgery ."
    print((splitstr(s)))
    print((SplitSubSent(s)))
    print((splitword(s)))
    print((haspattern(r'\[\d+\]', s)))
    s = "hello"
    print((haspattern(r'\[\d+\]', s)))
    s = "12, 2132, (12) hello this is a new one that we have"
    print((allsymdig(s)))
    print((remsymdig(s)))
    s =remsymdig("")
    if s is None:
        print((s, 'is none'))
    else:
        print((s,'not none'))
    print(('remove stop',removestops(['hello, this is a word','and this is a top'])))
def TestDist():
    s1 = 'hello world'
    s2 = 'ok world'
    print((jaccard_sim_norm(s1,s2)))
if __name__=="__main__":
 #Q   Test1()
   # Test2()
   #Test3()
    TestDist()
        #test Q2B and B2Q
##        for i in range(0x0020,0x007F):
##                print Q2B(B2Q(unichr(i))),B2Q(unichr(i))
