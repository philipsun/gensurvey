# coding=UTF-8
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
import re
import sxpCompute
import numpy as np
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
def is_chinese(uchar):
##        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False

def is_number(uchar):
##        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar<=u'\u0039':
                return True
        else:
                return False

def is_alphabet(uchar):
##         """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
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
def ReplaceNonEnglishCharacter(str):
#    print type(str)
    unc = str
    p = re.compile(r"([^\x00-\xff])")

    def func(m):
        st = repr(m.group(1).title())
        st = ' ' + st + ' '
        return st
    g = p.sub(func, unc)
    return g
def Test():
    #test uniform
    ustring=u'中国 人“名”ａ高频,3..Ａ‣'
    ustring=uniform(ustring)
    ret=string2ListChinese(ustring,True)
    for ch in ret:
        print(ch)

def Test1():
    ustr = "12ab,:a啊中国‣"

    p = re.compile(u"([^\x00-\xff])")

    def func(m):
        st = repr(m.group(1).title())

        st = ' ' + st + ' '
        return st
    print('sub begin:')

    g= p.sub(func, ustr)

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
    for name,pt in segpatnamedict.items():
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
    s = s + ' '
    pt = '(,\s|\.\s|\?\s)'
    subs = re.split(pt,s)

    segs = []
    for each in subs:
        s = each.strip()
        if s == ',' or s =="." or s=='?':
            continue
        segs.append(s)
    return segs
def cut(strcontent,cut_all=False):
    return splitstr(strcontent)
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
            word_list1.append(word)
#    print(word_list1)
    for word in segsenttowords(s):
        if word not in stopwords:
            word_list2.append(word)
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
            word_list1.append(word)
    #    print(word_list1)
    for word in segsenttowords(s2):
        if word not in stopwords:
            word_list2.append(word)
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
def isspace(c):

    return c.isspace()
def is_mark(c):
    patem = u'[\.\:\,\'\"\?\!\~\`\;\\\/\@\#\$\%\^\&\*\(\)\{\}\[\]\-\_\+\='
    patcm = u'。：！，【】《》“”‘’]'
    pat = patem+patcm
    return re.match(pat,c)
def is_chinsemark(c):
    pat = '[。：！，【】《》“”‘’]'

    return re.match(pat,c)
def is_engsymbol(c):
    pat = '[A-Za-z]'
    return re.match(pat,c)
def parimark():
    pm_dict = {
        "''":'f', #f means flat, no embedding
        '""':'f',
          "()":'f',
          "<>":'f',
          "[]":'f',
          "{}":'f',
          "“”":'f',
          "【】":'f',
          "《》":'f',
          "‘’":'f'
          }
    pmleft_dict ={}
    pair_dict={}
    pair_name_dict={}
    global_pmleftdict={}
    global_pmrightdict={}
    for each,etype in pm_dict.items():
        pmleft_dict[each[0]]=each[1]
        pair_dict[each]=[]
        pair_name_dict[each[0]]=each
        if each[1] not in pair_name_dict.keys():
            pair_name_dict[each[1]]=each
        global_pmleftdict[each[0]]=each[1]
        global_pmrightdict[each[1]] = each[0]
    pmright_dict={}
    for each in pm_dict:
        pmright_dict[each[1]]=each[0]
    pair_info_dict={}
    pair_info_dict['pm_dict']=pm_dict
    pair_info_dict['pair_dict'] = pair_dict
    pair_info_dict['pair_name_dict'] = pair_name_dict
    pair_info_dict['global_pmleftdict'] = global_pmleftdict
    pair_info_dict['global_pmrightdict'] = global_pmrightdict
    return pair_info_dict

pair_info_dict = parimark()

def segpairs(s):
    pair_name_dict =pair_info_dict['pair_name_dict']
    pair_dict = pair_info_dict['pair_dict']
    global_pmleftdict = pair_info_dict['global_pmleftdict']
    pm_dict = pair_info_dict['pm_dict']
    for i,c in enumerate(s):
        if c in pair_name_dict.keys():
            pm = pair_name_dict[c]
            pair_dict[pm].append([i,c])
    pm_range_dict={}
    for pmname,pm in pair_dict.items():
        nlen = len(pm)
        if nlen>0:
            plen = int(nlen/2);
            if nlen %2 != 0:
                print('not consistant closed', pmname,pm[-1])
            else:
                if pm_dict[pmname]=='f':
                    if pmname not in pm_range_dict.keys():
                       pm_range_dict[pmname]=[]
                    for i in range(plen ):
                        pm1=pm[2*i]
                        pm2 = pm[2*i+1]
                        rg =[pm1,pm2]
                        pm_range_dict[pmname].append(rg)
                else:
                    print('cannot handle')
    sentrange=[]
    for pmname,rg in pm_range_dict.items():
        print(pmname,rg)

    for pmname,rg in pm_range_dict.items():
        for each in rg:
            a = each[0][1]
            b = each[1][1]
            ia = each[0][0]+1
            ib = each[1][0]
            if a not in global_pmleftdict.keys():
                print('not start with a left op',[ia,ib,pmname,s[ia-1:ib+1]])
                continue
            if global_pmleftdict[a]==b:
                sentrange.append([ia,ib,pmname,s[ia:ib]])
            else:
                print(ia,ib,pmname)
                print('not end with a right close,',[ia,ib,pmname,s[ia-1:ib+1]])
    okrange=checkintersectrange(sentrange)
    return okrange
def checkintersectrange(pmrangelist):
    spm =sorted(pmrangelist, key=lambda rg: rg[0])
    L = len(spm)
    pos_tag=[]
    problemone =[]
    for i in range(L-1):
        for j in range(i+1,L):
            p = spm[i]
            r = spm[j]
            if p[1]<r[0]:
                continue
            if p[0]>r[1]:
                continue
            if p[0]<=r[0] and p[1]>=r[1]:
                pos_tag.append([i,j,'cover'])
                if i not in problemone:
                    problemone.append(i)
                if j not in problemone:
                    problemone.append(j)
            if r[0] <= p[0] and r[1] >= p[1]:
                pos_tag.append([i, j, 'becover'])
                if i not in problemone:
                    problemone.append(i)
                if j not in problemone:
                    problemone.append(j)
            else:
                pos_tag.append([i,j,'intsect'])
                if i not in problemone:
                    problemone.append(i)
                if j not in problemone:
                    problemone.append(j)
    okpair=[]
    for i in range(L):
        if i in problemone:
            print('still not consist pair',spm[i])
        else:
            okpair.append(spm[i])
    return okpair
class sxpPairRange:
    def __init__(self, pmname):
        self.pmname =pmname
        self.leftc = ''
        self.rightc =''
        self.leftidx = 0
        self.rightidx = 0
        self.textlist=[]
        self.child=[]
        self.text = "" #note that when a pair node is built, his txt will be his child node.
        self.prev = None
        self.next = None
    def addchild(self,sxprange):
        self.child.append(sxprange)
    def match(self,c):
        if len(self.leftc)==0:
            return False
        if pair_info_dict['global_pmleftdict'][self.leftc]==c:
            return True
        return False
def BuildNextPrevLink(root):
    if len(root.child) <= 1:
        return
    for i, ch in range (len(root.child)-1):
        root.child[i].Next = root.child[i+1]
        root.child[i + 1].Prev = root.child[i]
    for each in root.child:
        BuildNextPrevLink(each)
def traversetree(root):
    print('----node---:')
    print(root.pmname,root.text,'has following',len(root.child))

    for each in root.child:
        traversetree(each)
def isleftpair(c):
    return c in pair_info_dict['global_pmleftdict'].keys()
def isrightpair(c):
    return c in pair_info_dict['global_pmrightdict'].keys()
def isbothpair(c):
    if c in pair_info_dict['global_pmleftdict'].keys():
        if c == pair_info_dict['global_pmleftdict'][c]:
            return True
    return False
def ifskipc(c,c1,c2=""):
    if c in pair_info_dict['pair_name_dict'].keys():
        if c1 == '\\':
            return True
        if c == "'" and not isspace(c1) and c2=='s':
            return True
        if c == "'" and isspace(c2) and c1 == 's':
            return True
    else:
        return False
def segpairtree(s):
    pair_name_dict =pair_info_dict['pair_name_dict']
    pair_dict = pair_info_dict['pair_dict']
    global_pmleftdict = pair_info_dict['global_pmleftdict']
    pm_dict = pair_info_dict['pm_dict']
    root = sxpPairRange('root')
    current_node = root
    pm_stack={}

    for each,pm in pair_dict.items():
        pm_stack[each]=[]
    pm_wrong =[]
    pm_node_list=[current_node]
    all_pm_stack = [root]
    current_text = ""
    for i,c in enumerate(s):
        if i>0:
            c1 = s[i-1]
        else:
            c1 = ''
        if i < len(s)-1:
            c2 = s[i+1]
        else:
            c2 = ""
        #c1 c c2
        if ifskipc(c,c1,c2):
            current_text = current_text + c
            continue
        if c in pair_name_dict.keys():
            pm = pair_name_dict[c]
            if isbothpair(c):
                if current_node.match(c):
                    current_node.rightc = c
                    current_node.rightidx = i
                    current_node.text = s[current_node.leftidx:current_node.rightidx + 1]
                    if len(current_text) > 0:
                        textnode = sxpPairRange('txt')
                        textnode.text = current_text
                        textnode.rightc = i-1 #because i is the index of bracket, so you need to minus -1 to get the text index
                        textnode.leftc = i- 1- len(current_text)
                        pm_node_list.append(textnode)
                        current_node.addchild(textnode)
                        current_text = ""
                    pm_node_list.append(current_node)
                    if len(all_pm_stack) > 0:
                        all_pm_stack.pop()
                        if len(all_pm_stack) > 0:
                            current_node = all_pm_stack[-1]
                        else:
                            current_node = root
                    else:
                        print('to match', current_node.leftc, current_node.leftidx, 'but wrong matched by', i, c)
                        current_node.rightc = c
                        current_node.rightidx = i
                        if len(current_text) > 0:
                            textnode = sxpPairRange('txt')
                            textnode.text = current_text
                            textnode.rightc = i - 1  # because i is the index of bracket, so you need to minus -1 to get the text index
                            textnode.leftc = i - 1- len(current_text)
                            pm_node_list.append(textnode)
                            current_node.addchild(textnode)
                            current_text = ""
                        pm_wrong.append(current_node)
                        current_node.textlist.append(current_text)
                        current_text = ""
                    continue
                else:
                    if len(current_text) > 0:
                        textnode = sxpPairRange('txt')
                        textnode.text = current_text
                        textnode.rightc = i - 1  # because i is the index of bracket, so you need to minus -1 to get the text index
                        textnode.leftc = i - 1 - len(current_text)
                        pm_node_list.append(textnode)
                        current_node.addchild(textnode)
                        current_text = ""
                    newnode = sxpPairRange(pm)
                    newnode.leftc = c
                    newnode.leftidx = i
                    current_node.addchild(newnode)
                    all_pm_stack.append(newnode)
                    current_node = newnode
                    continue
            if isleftpair(c):
                newnode = sxpPairRange(pm)
                newnode.leftc=c
                newnode.leftidx=i
                if len(current_text) > 0:
                    textnode = sxpPairRange('txt')
                    textnode.text = current_text
                    textnode.rightc = i - 1  # because i is the index of bracket, so you need to minus -1 to get the text index
                    textnode.leftc = i - 1 - len(current_text)
                    pm_node_list.append(textnode)
                    current_node.addchild(textnode)
                    current_text = ""
                current_node.addchild(newnode)
                all_pm_stack.append(newnode)
                current_node = newnode
                continue
            if isrightpair(c): #in this case, if the left char is the same as the right c,
                #the right char will be taken as a left char, which will not match
                if current_node.match(c):
                    current_node.rightc = c
                    current_node.rightidx = i
                    current_node.text = s[current_node.leftidx:current_node.rightidx+1]
                    if len(current_text) > 0:
                        textnode = sxpPairRange('txt')
                        textnode.text = current_text
                        textnode.rightc = i - 1  # because i is the index of bracket, so you need to minus -1 to get the text index
                        textnode.leftc = i - 1 - len(current_text)
                        pm_node_list.append(textnode)
                        current_node.addchild(textnode)
                        current_text = ""
                    pm_node_list.append(current_node)
                    if len(all_pm_stack)>0:
                        all_pm_stack.pop()
                        if len(all_pm_stack)>0:
                            current_node = all_pm_stack[-1]
                        else:
                            current_node = root
                    else:
                        print('to match',current_node.leftc,current_node.leftidx, 'but wrong matched by', i, c)
                        current_node.rightc = c
                        current_node.rightidx = i
                        if len(current_text) > 0:
                            textnode = sxpPairRange('txt')
                            textnode.text = current_text
                            textnode.rightc = i - 1  # because i is the index of bracket, so you need to minus -1 to get the text index
                            textnode.leftc = i - 1- len(current_text)
                            pm_node_list.append(textnode)
                            current_node.addchild(textnode)
                            current_text = ""
                        pm_wrong.append(current_node)
                else:
                    print('to match', current_node.leftc, current_node.leftidx, 'but wrong matched by', i, c)
                    current_node.rightc = c
                    current_node.rightidx = i
                    if len(current_text) > 0:
                        textnode = sxpPairRange('txt')
                        textnode.text = current_text
                        textnode.rightc = i - 1  # because i is the index of bracket, so you need to minus -1 to get the text index
                        textnode.leftc = i - 1 - len(current_text)
                        pm_node_list.append(textnode)
                        current_node.addchild(textnode)
                        current_text = ""
                    pm_wrong.append(current_node)
        else:
            current_text = current_text + c

    L = len(all_pm_stack)
    h = int(L/2)
    current_node = root
    for i in range(L):
        l = i
        r = L-i-1
        if l==r:
            if all_pm_stack[i].pmname =='root':
                continue
            print('wrong in matched at',all_pm_stack[i].leftc,all_pm_stack[i].leftidx)
            pm_wrong.append(all_pm_stack[i])
            break
        pmname = all_pm_stack[i].pmname
        pnode= sxpPairRange(pmname)
        pl = all_pm_stack[l]
        pr = all_pm_stack[r]
        pnode.rightc = pl.leftc
        pnode.leftc = pr.leftc
        pnode.leftidx = pl.leftidx
        pnode.rightidx = pr.leftidx
        pnode.text = s[current_node.leftidx:current_node.rightidx+1]
        current_node.addchild(pnode)
        pm_node_list.append(pnode)
        current_node = pnode

        if l == r-1:
            break

    parse_dict={}
    parse_dict['root']=root
    parse_dict['node_list']=pm_node_list
    txt_node_list =[]
    txt_list =[]
    for each in pm_node_list:
        if each.pmname == 'txt':
            txt_list.append(each.text)
            txt_node_list.append(each)
    parse_dict['txt_list']=txt_list
    parse_dict['txt_node_list']=txt_node_list
    return parse_dict


def segbychar(s):
    seglist = []
    nc = None
    ne = None
    nd = None
    len_s = len(s)
    hanzi = 'hanzi' #chinese chars
    yingwen = 'yingwen'#english char and symboles
    shuzi = 'shuzi' #digit numbers
    biaodian = 'biaodian' #markers
    feishibie ='feishibie'
    cs = None
    current = []
    i = 0
    while i < len_s:
        c = s[i]
        i = i + 1
        if isspace(c):
            if cs is not None:
                if cs == shuzi: # 3 4 2 they are the number  3.4 2.3 3 + 3 -23
                    continue
                else:
                    seglist.append([cs,current]) # 'a ' is met, so a seg is met
                    cs = None
                    current = []
                    continue
            else:
                continue
        if is_mark(c):
            if i <len_s:
                print(i,len_s)
                si = isspace(s[i])#here check if next is a space
            else:
                if cs == biaodian:
                    current.append(cs)
                    continue
                else:
                    seglist.append([cs,current])
                    cs = biaodian
                    current=[c]
                    continue
            if si: #means that next char is a space '. '
                if cs is None:
                    current.append(c)
                    cs = biaodian
                    continue
                else:
                    #means that a space '. ' is met, we end the current seg and
                    #start a new seg.
                    if cs == biaodian: #means that '.. ' is met, so we use '..' as
                        current.append(c)
                        continue
                    else:   #else, 'a. ' is met
                        seglist.append([cs, current]) #put previous seg into list
                        cs = biaodian # build current mark into a new list
                        seglist.append([cs, [c]])
                        current = [] #since next is a space, so start a new process
                        cs = None
                        continue
            else:
                # means that '.a' is located,
                # in this case, we deem it as not a separeting marker, but a
                # continuous symbol.
                if is_chinsemark(c):
                    seglist.append([cs, current])  # put previous seg into list
                    cs = biaodian  # build current mark into a new list
                    current=[c]
                    continue
                else:
                    current.append(c) #do not update previous sate
                    continue

        if is_chinese(c):
            if is_chinsemark(c): #because, chinse mark will be handled by is_mark
                continue
            if cs is None:
                current =[c]
                cs = hanzi
                continue
            else:
                if cs == hanzi: # two continuous hanzi
                    current.append(c)
                    continue
                else:
                    seglist.append([cs,current]) #now it met a hanzi, so store previous one andstart a new
                    cs = hanzi
                    current=[c]
                    continue

        if is_engsymbol(c):
            if cs is None:
                current =[c]
                cs = yingwen
                continue
            else:
                if cs == yingwen: # two continuous hanzi
                    current.append(c)
                    continue
                else:
                    seglist.append([cs,current]) #now it met a hanzi, so store previous one andstart a new
                    cs = yingwen
                    current=[c]
                    continue

        if is_number(c):
            if cs is None:
                current =[c]
                cs = shuzi
                continue
            else:
                if cs == shuzi: # two continuous hanzi
                    current.append(c)
                    continue
                else:
                    seglist.append([cs,current]) #now it met a hanzi, so store previous one andstart a new
                    cs = shuzi
                    current=[c]
                    continue
        print(c,'is not accepted')
        if cs is None:
            current = [c]
            cs = feishibie
        else:
            seglist.append([cs, current])  # now it met a hanzi, so store previous one andstart a new
            cs = feishibie
            current = [c]
            continue
    if cs is not None:
        seglist.append([cs, current])  # now it met a hanzi, so store previous one andstart a new
    return seglist

def Test2():
    s =r"The most-nominated film was ``All About Eve'' in 1950. It has three 3.5's pages in its list."
    s =r"The motion picture industry's most coveted award, Oscar, was created 60 years ago and 1,816 of the statuettes have been produced so far."
    s =r"The Academy holds all the rights on the statue and ``reserves the right to buy back an Oscar before someone takes it to a pawn shop,'' said Academy spokesman Bob Werden."
    s = r"He certainly will not say 'well done, keep it up'"
    print(s)
    print(segquotation(s))
    print(splitword(s))
    s1 = 'hello word'
    s2 = 'good word'
    print(segsenttowords(s1))
    print(jaccard_similarity(s1,s2))
    print(jaccard_sim_norm(s1,s2))
    print(SplitSubSent(s))
def Test3():
    s = u" In [2], Lucille Ball, the leggy showgirl, model and B-grade movie queen whose pumpkin hair and genius for comedy made her an icon of television? died early Wednesday. a week after undergoing emergency heart surgery ."
    print(splitstr(s))
    print(SplitSubSent(s))
    print(splitword(s))
    print(haspattern(r'\[\d+\]', s))
    s = "hello"
    print(haspattern(r'\[\d+\]', s))
    s = "12, 2132, (12) hello this is a new one that we have"
    print(allsymdig(s))
    print(remsymdig(s))
    s =remsymdig("")
    if s is None:
        print(s, 'is none')
    else:
        print(s,'not none')
    print('remove stop',removestops(['hello, this is a word','and this is a top']))
    nc = ['hello']
    nglist=[]
    nglist.append(nc)
    nc = None
    print(nglist,nc)
def extractfrompairs(s):
    pair_info_dict = segpairtree(s)
    sentlist =[]
    current_sent = ""
    for each in pair_info_dict['node_list']:
        if each.pmname == 'txt':
            sentlist.append(each.text)
    sentseglist=[]
    for eachtxt in sentlist:
        ss=split2sent(eachtxt)
        for each in ss['txt_list']:
            sentseglist.append(each)
    return sentseglist

def split2sent(txt):
    patem ="([\.\:\,\'\\\"\?\!\;]+\s+)|([。：！，【】《》“”‘’])+"
    sentlist=re.split(patem,txt)

    sentlist_dict={}
    n = len(sentlist)
    if n == 1:
        sentlist_dict['seg_list']=[[txt,'.']]
        sentlist_dict['txt_list']=[txt]
        return sentlist_dict
    k = int(n /3)
    sentmark_list=[]
    subtxt_list =[]
    i = 0
    while(i<n):
        p = sentlist[i].strip()
        i = i + 1
        if i > n-1:
            p1 = None
        else:
            p1 = sentlist[i]
        i = i + 1
        if i > n -1:
            p2 = None
        else:
            p2 = sentlist[i]
        i = i + 1
        if p1 is None and p2 is not None:
            sentmark_list.append([p, p2.strip()])
        if p1 is not None and p2 is None:
            sentmark_list.append([p, p1.strip()])
        if p1 is None and p2 is None:
            sentmark_list.append([p,'.'])

    csent_list = correctsent(sentmark_list)

    for each in csent_list:
        subtxt_list.append(each[0])
    fullsent_list = findfullsent(csent_list)
    sentlist_dict['seg_list'] = csent_list
    sentlist_dict['txt_list'] = subtxt_list
    sentlist_dict['fullsent_list'] = fullsent_list

    senttxt_list = []
    for ss in fullsent_list:
        sent_txt = ""
        for s in ss:
            a = s[0].strip()
            if isspace(a):
                continue
            sent_txt = sent_txt + ' ' +a
        senttxt_list.append(sent_txt)
    sentlist_dict['fulltxt_list']=senttxt_list
    return sentlist_dict

def correctsent(sentlist):
    n = len(sentlist)
    new_sent = []
    for i in range(n):
        p = sentlist[i]
        ss = re.split("[\.\?\!]([^0-9])",p[0])
        e = p[1]
        if len(ss)==1:
            new_sent.append(p)
        if len(ss)>1:
            k = len(ss)
            j = 1
            new_sent.append([ss[0],'.'])
            while(j<k):
                h =  ss[j]
                j = j + 1
                if j >k-1:
                   s = ""
                else:
                   s = ss[j]
                fs = h + s

                if j == k -1:
                    new_sent.append([fs,e])
                else:
                    new_sent.append([fs,'.'])
                j = j + 1

    subnew=[]
    for i, st in enumerate(new_sent):
        s = st[0]
        ss  = re.split("([\,])",s)
        if len(ss)==1:
            subnew.append(st)
        if len(ss)>1:
            for i,s in enumerate(ss):
                if i < len(ss)-1:
                    subnew.append([s,','])
                else:
                    subnew.append([s,st[1]])
    return subnew
def findfullsent(sentmark_list):
    current_sent = []
    subsent_list = []
    for each in sentmark_list:
        mark = each[1].strip()
        txt = each[0]
        if mark[-1] in '.!?。':
            current_sent.append( each)
            subsent_list.append(current_sent)
            current_sent = []
        else:
            current_sent.append(each)
    return subsent_list
def cutword(strcontent,cut_all=False):
    strcontent = strcontent +' '
    ws = re.split('[\.\,\:\!\?\(\)\<\>]*\s+', strcontent)
    swd = []
    for each in ws:
        if len(each.strip()) > 0:
            swd.append(each)
    return swd
def seg2subsentlist(txt):
    sentlist_dict=split2sent(txt)
    return sentlist_dict['txt_list']
def seg2fullsentlist(txt):
    sentlist_dict=split2sent(txt)
    return sentlist_dict['fullsent_list']
def seg2wordseqlist(txt):
    sentlist_dict=split2sent(txt)
    return SegEngWord(sentlist_dict['txt_list'])
def seg2lammwordseqlist(txt):
    sentlist_dict=split2sent(txt)
    sent_word_list=SegEngWord(sentlist_dict['txt_list'])
    sentwd =[]
    for sent in sent_word_list:
        wdlist=[]
        for wd in sent:
            lwd = lemmatizer.lemmatize(wd.lower())
            wdlist.append(lwd)
        sentwd.append(wdlist)
    sentlist_dict['send_lmwd']=sentwd
    return sentlist_dict
def makewdvect(txt):
    sentlist_dict=seg2lammwordseqlist(txt)
    sentwd = sentlist_dict['send_lmwd']
    wd_dict={}
    j = 0
    sentwd_id_list=[]
    for i, eachsent in enumerate(sentwd):
        sent_wdid=[]
        for eachwd in eachsent:
            if eachwd not in wd_dict.keys():
                wd_dict[eachwd] = j
                sent_wdid.append(j)
                j = j + 1
            else:
                sent_wdid.append(wd_dict[eachwd])
        sentwd_id_list.append(sent_wdid)
    sentlist_dict['wd_dict']=wd_dict
    sentlist_dict['sentwd_id_list']=sentwd_id_list
    return sentlist_dict
def check2sameword(w1,w2):
    ping = '(\w+)ing'
    ped = '(\w+)ed'
    pd = '(\w+)d'
    pied = '(\w+)ied'
    pes = '(\w+)(s|ch|sh|x)es'
    pes = '(\w+)ies'
    pves = '(\w+)ves'
    ps =  '(\w+)s'
    pn = '(\w+)n'

    print(lemmatizer.lemmatize('characters'))


def SegEngWord(txt_list):
    sent_word_list=[]
    for each in txt_list:
        ws = re.split('\s+',each)
        swd =[]
        for each in ws:
            if len(each.strip())>0:
                swd.append(each)
        sent_word_list.append(swd)
    return sent_word_list

def worposdist(keywordseq,txt,skipzero=False):
    wd_dist_dict={}

    for eachkey in keywordseq:
        if len(eachkey.strip())==0:
            continue
        wd_dist = computetxtpos(eachkey,txt)
        wd_dist_dict[eachkey]=wd_dist
    return wd_dist_dict
def wordsentposdist(keywordseq,sent_list):
    wd_dist_dict={}

    for eachkey in keywordseq:
        if len(eachkey.strip())==0:
            wd_dist[eachkey]=[]
            continue
        wd_dist = computewordsentpos(eachkey,sent_list)
        wd_dist_dict[eachkey]=wd_dist
    return wd_dist_dict
def dualwordsentposdist(keywordseq,sent_list):
    wd_dist_dict={}
    senlen = len(sent_list)
    sent_dist_dict={}
    for eachkey in keywordseq:
        if len(eachkey.strip())==0:
            wd_dist[eachkey]=[]
            continue
        wd_dist = computewordsentpos(eachkey,sent_list)
        sentpos = np.zeros((senlen,1))
        sentpos[wd_dist,0]=1
        wd_dist_dict[eachkey]=wd_dist
        sent_dist_dict[eachkey]=sentpos
    return wd_dist_dict,sent_dist_dict
def dualwordsetposrealdist(keywordseq,sent_list):
    pass
def computewordsentpos(eachkey,sent_list):
    x = []
    for i, each in enumerate(sent_list):
        # pos=re.search(eachkey.lower(),each.lower())
        pos = searchall(each.lower(), eachkey.lower())
        if len(pos) == 0:
            continue
        else:
            x.append(i)
    return x

def worddist(keywordseq,sent_list,skipzero=False):
    wd_dist_dict={}
    for eachkey in keywordseq:
        if len(eachkey.strip())==0:
            continue
        wd_dist = computeworddist(eachkey,sent_list,skipzero)
        wd_dist_dict[eachkey]=wd_dist
    return wd_dist_dict

def computetxtpos(eachkey,txt):
    pos = searchall(txt.lower(), eachkey.lower())
    return pos;
def computeworddist(eachkey,sent_list,skipzero=False):
    x =[]
    if skipzero:
        for i, each in enumerate(sent_list):
            #pos=re.search(eachkey.lower(),each.lower())
            pos = searchall(each.lower(),eachkey.lower())
            if len(pos)==0:
                 continue
            else:
                x.append(i)
            #    x.append(len(pos))
    else:
        for i, each in enumerate(sent_list):
            #pos=re.search(eachkey.lower(),each.lower())
            pos = searchall(each.lower(),eachkey.lower())
            x.append(len(pos))
    return x

def testsegword():
    cs = 'abc.123。\\a '
    for c in cs:
        print(c)
        print('space',isspace(c),'mark',
              is_mark(c),'number',is_number(c),'chinese',is_chinese(c),'en', is_engsymbol(c))
    s = u'你好，我们没有考虑你的问题。但10年的时候，这个产量还是12.5公斤。We have worked on it so that we can make a little bit different sinces.'
    sg = segbychar(s)
    for each in sg:
        print(each[0],each[1])
def testpairseg():
    s = u'hello, this is (a (new) p)a<adf>ir,("we) just \"have \"to make", (10), [120i,120]'
    ps = segpairs(s)
    for each in ps:
        print(each)
    print('----------segpairtree:', s)
    pstree_dict = segpairtree(s)
    for each in pstree_dict["node_list"]:
        print(each.leftc,each.rightc,each.leftidx,each.rightidx,each.text)

    s = u'hello, this is (a (new) p)a<adf>ir,("we just have to make",but we know), (10), [120i,120]'
    print('----------segpairtree:',s)
    pstree_dict = segpairtree(s)
    for each in pstree_dict["node_list"]:
        print(each.leftc,each.rightc,each.leftidx,each.rightidx,each.text)
def test2():
    s = u'Tom\'s Trees\' (a (new) p)a<a"d"f>ir,("we just  \"have \"tmake",but we know), (10), [120i,120]'
    print('----------segpairtree: ',s)
    pstree_dict = segpairtree(s)
    for each in pstree_dict["node_list"]:
        if each.pmname =='txt':
            print('----node:----')
            print(each.leftc,each.rightc,each.leftidx,each.rightidx,each.text)
    print('-----orgin------segged')
    print(s)
    print(pstree_dict['txt_list'])

    print('===============traverse tree from root')
    traversetree(pstree_dict['root'])
def testseg():
    s = "hello, we have been working on this project for years. BUt, we haven't make any progress yet."

    sentlist = split2sent(s)
    print('txt_list-----------')
    for each in sentlist['txt_list']:
         print(each)
def testsplit():
  #  s = 'hello.world,,, we have been working on this for many years. 但是，我们不能把这样的一个问题留给别人。'
#    s = 'hello.world,,, we have been working on.This world is  this for.Many years.但是，我们不能把这样的一个问题留给别人'
    s = "hello, we have been working on this project for years. BUt, we haven't make any progress yet."




    patem = "([\.\:\,\'\\\"\?\!\;]+\s+)|([。：！，【】《》“”‘’])+"
    sentlist = re.split(patem, s)
    print(sentlist)
    print('----------------------')
    ss = re.split("[\.\?\!]([^0-9])",s)
    print(ss)
    #
    sentlist = split2sent(s)
    # for each in sentlist['fullsenttxt_list']:
    #     print(each)


    print('txt_list-----------')
    for each in sentlist['txt_list']:
         print(each)
    print('seg_list-----------')
    for each in sentlist['seg_list']:
         print(each)
    print('fullsent_list-----------')
    for each in sentlist['fullsent_list']:
         print(each)


    print('fulltxt_list-----------')
    for each in sentlist['fulltxt_list']:
        print(each)

def testsegvec():
    s = "hello, we have been working on this project for years. BUt, we haven't make any progress yet."
    sentlist_dict=makewdvect(s)
    print(sentlist_dict['wd_dict'])
    print(sentlist_dict['sentwd_id_list'])
    print(sentlist_dict['txt_list'])
    print('cut word-----')
    print(cut(s,cut_all=False))
    print(cutword(s, cut_all=False))
def searchall(s,pt):
    pos=[]
    p = re.search(pt,s)
    currentpos = 0
    while(p):
        ps = p.span()
        st = currentpos + ps[0]
        pos.append(st)
        et = currentpos + ps[1]
        subs = s[et:]
        currentpos = et
        p = re.search(pt,subs)
        s = subs
    return pos
def searchallpos(s,pt):
    pos=[]
    p = re.search(pt,s)
    currentpos = 0
    while(p):
        ps = p.span()
        st = currentpos + ps[0]
        pos.append(st)
        et = currentpos + ps[1]
        subs = s[et:]
        currentpos = et
        p = re.search(pt,subs)
        s = subs
    return pos

def testre():
    s = 'hello, this is to test how check can be searched by re.search. this is another. we have. our work'
    # g = re.search("hello",s)
    # print(g)
    # print(g.groups())
    # print(g.span())
    # g = re.search("time",s)
    # print(g)
    # g = re.findall("hello",s)
    # print(g)
    # g = re.findall('time',s)
    # print(g)
    # print(s[2:])
    # print(searchall(s,'time'))
    # print(searchall(s,'this\s+is'))
  #  p=searchall(s, 'this[\s-]is|check')
    p = searchall(s, 'in this|we|our|this')
    print(p)
    for i in p:
        print(s[i])

if __name__=="__main__":
 #Q   Test1()
   # Test2()
   #Test3()
    #testsegword() #ok
   # testpairseg()
   # test2()
    #testsplit()
    #testsegvec()
    testre()
        #test Q2B and B2Q
##        for i in range(0x0020,0x007F):
##                print Q2B(B2Q(unichr(i))),B2Q(unichr(i))
