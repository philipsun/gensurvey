#-------------------------------------------------------------------------------
# Name:        sxpParseDUCText
# Purpose:
#
# Author:      sunxp
#
# Created:     23/03/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=UTF-8
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import sxpTestStringEncode
import codecs
import urllib.request, urllib.parse, urllib.error
import socket
import sxpTextEncode
import sxpIsCharacter
import sxpProcessParaText
import sxpFenciMakeTFIDF
import sxpParseDivPara
import sxpParseSection
import sxpExtractText
import sxpJudgeCharacter
import sxpLogger
import os
import re
import win32file
import sxpReadFileMan
import sxpContextMan
import pickle
from bs4 import BeautifulSoup

import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
import warnings
logfilestr = 'log.txt'
class sxpText:
    fname = ''
    title = ''
    abstract = ''
    relatedwork = ''
    conclusion = ''
    reference = ''
    section_id_dict ={}
    section_list = []
    paraset = []
    whole_sectitle = ''
    whole_text = ''
    keycount = None
    para_tfidf = None
    sentence_tfidf = None
    sentenceset = []
    context_set = []
    d_c = None
    c_p = None
    p_s = None
    s_k = None
    t_s = None #context - sentence
    p_t = None #paragraph - context
    def __init__(self):
        self.fname = ''
        self.title = ''
        self.abstract = ''
        self.relatedwork = ''
        self.conclusion = ''
        self.reference = ''
        self.section_id_dict ={}
        self.section_list = []
        self.paraset = []
        self.whole_sectitle = ''
        self.whole_text = ''
        self.keycount = None
        self.para_tfidf = None
        self.sentence_tfidf = None
        self.sentenceset = []
        self.d_c = None
        self.c_p = None
        self.p_s = None
        self.s_k = None
        self.context_set = []
        self.t_s = None
        self.p_t = None


class sxpSectionTitle:
    title = ''
    id_str = ''
    id_set = ''
    level = 0
    id = 0
    t_type = ''
    def __init__(self):
        self.title = ''
        self.id_str = ''
        self.id_set = ''
        self.level = 0
        self.id = 0
        self.t_type = ''

class sxpPara:
    para_id = ''
    para_text = ''
    para_tuple = []
    para_tfidf =[]
    section_title=''
    sentenceset = []
    context_set = []

    id = 0
    id_sec = 0
    def __init__(self):
        self.para_id = ''
        self.para_text = ''
        self.para_tuple = []
        self.para_tfidf =[]
        self.section_title=''
        self.sentenceset = []
        self.context_set = []
        self.id = 0
        self.id_sec = 0
class sxpSent:
    sentence_text = ''
    id = 0
    id_para = 0
    id_sec = 0
    def __init__(self):
        self.sentence_text = ''
        self.id = 0
        self.id_para = 0
class sxpContext:
    context_txt = ''
    id = 0
    id_para = 0
    id_sec = 0
    context_sent = []
    def __init(self):
        self.id = 0
        self.id_para = 0
        self.id_sec = 0
        self.context_sent = 0

class sxpTextPara:
    text = ''
    type = ''
    index = ''

paperpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt'
logfilename  =  r'.\log.txt'

def ParseModelFile(srcfname):
    txt = sxpReadFileMan.ReadTextUTF(srcfname)
#    pt1 = u'<'
#    s = re.compile(pt1)
#    print(s.findall(txt))
    pt = '\<a\s+href\="\#\d+"\s+id\=\d+\>(.*)\</a\>'
    rpt = re.compile(pt)
    g = rpt.findall(txt)
    return g
##    print(g)
##    if g:
##        print(len(g),g)
def CheckTypeParseLines(text):
    g= re.findall('\.\;',text)
    if len(g) >=2:
       return ParseLinesFromTextH(text)
    g= re.findall('\<P\>',text)
    if len(g) >=2:
       return ParseLinesFromTextByP(text)
    else:
        return ParseLinesFromText(text)
def ParseDUC2007SrcFile(fname):
    print('process,',fname)
    soup = BeautifulSoup(open(fname),'lxml')
    headline = soup.find('headline')
    if headline is None:
        headline = ""
    else:
        headline = headline.get_text()
    cat = soup.find('category')
    if cat is None:
        cat = ""
    else:
        cat = cat.get_text()
    paralist = soup.find_all('p')
    if paralist is None:
        print('Find No Para in !!!!!!!',fname)
        return None
    extractpara_txt_list = []
    if len(paralist)>0:
        for para in paralist:
            extractpara_txt_list.append(para.get_text().strip())
    if len(paralist)==0:
        print('Find No Para in !!!!!!!', fname)
        maintext = soup.find('text')
        if maintext:
            extractpara_txt_list = re.split('\t',maintext.get_text().strip())
        else:
            print('even text is not find,',fname)
            extractpara_txt_list = None;
    para_list=[]
    wholetext = ""
    sent_list = []
    para_txt_list = []
    for para in extractpara_txt_list:
        para_sent = []

        txt = para.replace('\n',' ')
        txt = txt.replace('Mr.','Mr')
        txt = txt.replace('Mrs.', 'Mrs')
        txt = txt.replace('Jr.', 'Jr')
        txt = txt.replace('Dr.', 'Dr')
        para_txt_list.append(txt)
        sent = re.split('\.\s',txt)
        for s in sent:
            if s.strip():
                para_sent.append(s)
                wholetext = wholetext + '\n' + s
                sent_list.append(s)
        para_list.append(para_sent)
    raw_dict = {}
    raw_dict['text'] = wholetext
    raw_dict['title']=headline
    raw_dict['cat'] = cat
    raw_dict['para_list']=para_list
    raw_dict['sent_list'] = sent_list
    raw_dict['para_txt_list']=para_txt_list
    raw_dict['fname']=fname
    return raw_dict
def ParseRawfile(fname):
    wholetext = ''
    headline =''
    raw_dict={}
    raw_dict['text']=''
    raw_dict['title']=''

    try:
        f = codecs.open(fname,'r+','utf-8')
        #uc = sxpIsCharacter.toUTF(content)
        #uc = unicode(content,'gbk','ignore').encode('gkb','ignore')
        #uc = content.decode('gbk','ignore').encode('gbk','ignore')
        #uc = unicode(content, 'gbk')
        #uc = sxpIsCharacter.toGBK(content)
        #if using GetUnicode, it will be written
        txt = f.read()
#        print(txt)
        f.close()
       # patstr = u'\<TEXT\>(.*)\</TEXT\>'
        patstr = '\<TEXT\>(.*)\</TEXT\>'
        #note that to match \n, you need to use re.DOTALL to use . in pat, otherwise, \n will be excluded.
        rpt = re.compile(patstr, re.DOTALL)
        g = rpt.findall(txt,re.DOTALL)
        if g:
            wholetext = g[0]

        patstr='\<HEADLINE\>(.*)\</HEADLINE\>'
        rpt = re.compile(patstr, re.DOTALL)
        g = rpt.findall(txt,re.DOTALL)
        if g:
            headline = g[0]
         #   print wholetext
        raw_dict['text']=wholetext
        raw_dict['title']=headline
        raw_dict['paras']=ParseLinesFromText(wholetext)
        return raw_dict
    except Exception as e:
        msg = 'file:{0}:{1}'.format(fname,e)
        print(msg);
        sxpLogger.logThisMessageStr(logfilename,msg)
        return raw_dict
def ParseLinesFromTextH(text):
    patstr = '[\.\?\!];'
    pt = re.compile(patstr,re.DOTALL)
    s = pt.split(text)
    ss = []
    pt = '\n'
    subpt = re.compile(pt,re.DOTALL)
    spacept = re.compile('\s+')
    for i, eachs in enumerate( s):
    #    print(i, eachs)
        eachs = eachs.strip() +'.'
        if len(eachs)==0:
            continue
        eachs=subpt.sub(' ', eachs)
        eachs=spacept.sub(' ', eachs)
        ss.append(eachs)
     #   print(ss)
    return ss
def ParseLinesFromTextByP(text):
    ptstr = r'\<P\>(.*?)\<\/P\>'
    pt = re.compile(ptstr,re.DOTALL)
    ss = pt.findall(text)
    return ss
def ParseLinesFromText(text):
    patstr = '[\.\?\!]\n'
    pt = re.compile(patstr,re.DOTALL)
    s = pt.split(text)
    ss = []
    pt = '\n'
    subpt = re.compile(pt,re.DOTALL)
    spacept = re.compile('\s+')
    for i, eachs in enumerate( s):
    #    print(i, eachs)
        eachs = eachs.strip() +'.'
        if len(eachs)==0:
            continue
        eachs=subpt.sub(' ', eachs)
        eachs=spacept.sub(' ', eachs)
        ss.append(eachs)
     #   print(ss)
    return ss
def ParseLineHtml(text):
#    print(text)
    lf = '\<s\s+docid\=\"[A-Za-z0-9\-]+\"\s+num\=\"\d+\"\s+wdcount=\"\d+"\>'
    rf = "\<\/s\>"
    mp = "(.*?)"
    patstr = lf + mp + rf
 #   patstr = "LA112790"
    pt = re.compile(patstr,re.DOTALL)
    s = pt.findall(text)
    return s
def GetSentListFromSentRawSrc(fname):
    text_dict=ParseRawfile(fname)
    s=ParseLineHtml(text_dict['text'])
    return s
def MakeSubSentList(sentlist):
    subsentlist=[]
    for each in sentlist:
        ss=re.split('\,',each)
        for s in ss:
            subsentlist.append(s)
    return subsentlist;
def ParseSentSxptxt(fname,usesub=False):
    text_dict=ParseRawfile(fname)
    if usesub:
        slist=MakeSubSentList(ParseLineHtml(text_dict['text']))
    else:
        slist = ParseLineHtml(text_dict['text']);
    sxptxt = sxpText()
    sxptxt.sentence_list = slist
    sxptxt.title = text_dict['title']
    sxptxt.abstract = ''
    sxptxt.conclusion = ''
    whole_txt = ''
    for each in slist:
        whole_txt = whole_txt +'  ' +each
    sxptxt.whole_text = whole_txt
    sxptxt.sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(slist)
    sxptxt.sentence_textset = slist

#***************************************************************
#****************Now we try to build several matrix for graphs can be
#               extracted from sxptxt
#***************************************************************
    print('we begin to build matrix')
    ss = len(sxptxt.sentence_textset)
    ks = len(sxptxt.sentence_tfidf.word)
    print(ss,ks)

#first we build d-c matrix, which is actually a row vector
#then building c-p matrix
    print('start')

#now to build para_context matrix p_t
    print('sxpsent list')
    for i, sent in enumerate(slist):
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = i
            sxpsent.id_para = 0
            sxpsent.id_sec = 0
            sxptxt.sentenceset.append(sxpsent)



#fourth, building s-k matrix
    print('s_k matrix')
    sxptxt.s_k =csr_matrix(sxptxt.sentence_tfidf.tfidf)

    return sxptxt
def ParseFromSentRawSrc(fname):
    text_dict=ParseRawfile(fname)
    slist=ParseLineHtml(text_dict['text'])
    sxptxt = sxpText()
    sxptxt.sentence_list = slist
#    print(mtxt)
    section_list = []
    whole_section_title =''
    section_id_dict = {}

    sec_id = 0
    sxpsec = sxpSectionTitle()
    sxpsec.id = sec_id
    sxpsec.id_str = 'global'
    sxpsec.level = sec_id
    sxpsec.title = 'global'

    sxptxt.title = text_dict['title']
    section_id_dict['global'] = sec_id
    section_list.append(sxpsec)

    sxptxt.section_id_dict = section_id_dict

    para_textset = []
    sentence_textset = []
    id_para = 0
    id_sent = 0

    print('parse para')
   # ltx_paraset = sxpParseDivPara.ExtractParagraph(papersrc)
    #for each paragraph:
    current_sec = None
    context_id = 0
    whole_text = ''
    unknown_sec_id = 0
    for i, para in enumerate( slist):
        sxp_para = sxpPara()
        #here we find the whole text of a paragraph
        sxp_para.para_text = para
        pid = str(i)
        sxp_para.para_id = pid
        #here we find the section id of the paragraph
        sxp_para.para_tuple = ParseSectionIDStr(pid)
        #here we find the section title of the para_graph
        #if we use dict to store section title, we will be more efficient here
        if sxp_para.para_tuple[0] in section_id_dict:
            sxpsec_id = section_id_dict[sxp_para.para_tuple[0]]
          #  print sxpsec_id
            sxpsec = section_list[sxpsec_id]
            current_sec = sxpsec
            sxp_para.section_title = sxpsec.title;
            sxp_para.id_sec = sxpsec.id
        else:
            uppersection = ParseUpperSection(sxp_para.para_tuple[0])
            while(len(uppersection) >0 ):
                if uppersection in section_id_dict:
                    sec_id = section_id_dict[uppersection]
                    sxpsec = section_list[sec_id]
                    sxp_para.section_title = sxpsec.title;
                    sxp_para.id_sec = sxpsec.id
                    current_sec = sxpsec
                    break
                else:
                    uppersection = ParseUpperSection(uppersection)
            if len(uppersection) == 0:
                if current_sec is not None:
                    sxp_para.section_title = current_sec.title;
                    sxp_para.id_sec = current_sec.id
                else:
                    sxp_para.section_title = 'unknown';
                    sxp_para.id_sec = unknown_sec_id

##        for sxpsec in section_id_dict:
##            if sxp_para.para_tuple is None:
##                print sxp_para
##            if sxp_para.para_tuple[0]== sxpsec.id_str:
##                sxp_para.section_title = sxpsec.title;
##                break;
##            else:
##                sxp_para.section_title = '';

        #for each paragraph, we extract its sentence
        sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
        sxpsent_set = []
        for sent in sentenceset:
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = id_para
            sxpsent.id_sec = sxp_para.id_sec
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sent)
            sxpsent_set.append(sxpsent)
#*******for each paragraph, we parse a context set from it by iterating its sentences
        print('parse context')
        context = []
        context_result = []
        i = 0
        distset =[0]
        for st in sxpsent_set:
            s = st.sentence_text
            if len(context) == 0:
                context.append(st)
            else:
                [isrel,dist] = is_relevant(context, s, 0.08)#the parameter determine the context group
                distset.append(dist)
                if isrel == True:
                    context.append(st)
                else:
                    para_context = sxpContext()
                    para_context.id = context_id
                    context_id = context_id + 1
                    para_context.id_para = id_para
                    para_context.id_sec = sxp_para.id_sec
                    para_context.context_sent = context
                    context_result.append(para_context)
                    context = []
                    context.append(st)
            i = i + 1
        if len(context)>0:
                para_context = sxpContext()
                para_context.id = context_id
                context_id = context_id + 1
                para_context.id_para = id_para
                para_context.id_sec = sxp_para.id_sec
                para_context.context_sent = context
                context_result.append(para_context)
                context = []
        print(np.mean(distset))
#for this para, we add the context result to the global storage
        sxp_para.context_set = context_result
        sxptxt.context_set.extend(context_result)

#********for each paragraph, we add them to global storate variables
        para_textset.append(para[1])
        whole_text = whole_text + '\n' + para[1]
        sxp_para.id = id_para
        id_para = id_para + 1
        sxptxt.paraset.append(sxp_para)
    sxptxt.abstract = ''
    sxptxt.conclusion = ''
    sxptxt.whole_text = whole_text
    sxptxt.section_list = section_list
    print('extract keycount')

#**************************************************************
#****************Now we try to extract the key counter of whole_text
    sxptxt.keycount = sxpProcessParaText.ExtractKeyCount(whole_text)

#**************************************************************
    print('make tfidf')

#**************************************************************
#****************Now we try to extract the sentence from the whole_text
##    sxptxt.sentenceset = sxpExtractText.MySentence(whole_text)
##    return sxptxt
#**************************************************************

    sxptxt.para_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(para_textset)

    sxptxt.sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentence_textset)
    sxptxt.sentence_textset = sentence_textset
#***************************************************************
#****************Now we try to build several matrix for graphs can be
#               extracted from sxptxt
#***************************************************************
    print('we begin to build matrix')
    cs = len(sxptxt.section_id_dict) #because we have 0 as the global doc and 1 as the section from the
    ps = len(sxptxt.paraset)
    ss = len(sxptxt.sentenceset)
    ks = len(sxptxt.sentence_tfidf.word)
    ts = len(sxptxt.context_set)
    print(cs, ps, ss, ks,ts)
#first we build d-c matrix, which is actually a row vector
    print('d_c matrix')
    sxptxt.d_c = csr_matrix(np.ones((1,cs), dtype=np.float))
#then building c-p matrix
    print('building c_p matrix')
    sxptxt.c_p = csr_matrix((cs,ps), dtype=np.float)
    print('start')
    print(sxptxt.c_p.shape)
    for para in sxptxt.paraset:
        c = para.id_sec
        p = para.id
#        print c, p
        sxptxt.c_p[c, p] = 1.0

#now to build para_context matrix p_t
    print('building p_t matrix and t_s matrix')
    sxptxt.p_t = csr_matrix((ps,ts), dtype=np.float)
    sxptxt.t_s = csr_matrix((ts,ss), dtype=np.float)
    print('start')
    print(sxptxt.p_t.shape)
    print(sxptxt.t_s.shape)
    for para in sxptxt.paraset:
        p = para.id
        for cont in para.context_set:
            t = cont.id
            sxptxt.p_t[p, t] = 1.0
            for eachs in cont.context_sent:
                s = eachs.id
                sxptxt.t_s[t,s] = 1.0

#        print c, p

#        sxptxt.c_p[p, c] = 1.0
#third, building p-s matrixx
    print('p_s matrix')
    sxptxt.p_s = csr_matrix((ps,ss), dtype=np.float)
    for sent in sxptxt.sentenceset:
        p = sent.id_para
        s = sent.id
        sxptxt.p_s[p,s] = 1.0
#        sxptxt.p_s[p,s] = 1.0

#fourth, building s-k matrix
    print('s_k matrix')
    sxptxt.s_k =csr_matrix(sxptxt.sentence_tfidf.tfidf)
##
##
###fifth, we will build k-k matrix which is the incident relationship of
##    print 'k_k matrix'
##    sxptxt.k_k =csr_matrix((ks,ks), dtype=np.float)
##    for sent in sxptxt.sentenceset:
##        ws =sxpExtractText.ExtractEnglishWord(sent.sentence_text)
##        kwpos= []
##        if len(ws)>0:
##           for w in ws:
##              if w in sxptxt.sentence_tfidf.word:
##                 kwpos.append(sxptxt.sentence_tfidf.word.index(w))
##           n = len(kwpos)
##           for i in range(n-1):
##              sxptxt.k_k[kwpos[i],kwpos[i+1]] = 1
#return sxptxt
    return sxptxt
def ParseDUC2007(fname):
    text_dict=ParseDUC2007SrcFile(fname)
    return ParseFromSentRawSrcTextDict(text_dict)
def ParseDUC2006(fname):
    text_dict=ParseDUC2007SrcFile(fname)
    return ParseFromSentRawSrcTextDict(text_dict)
def ParseFromSentRawSrcTextDict(text_dict):
    slist=text_dict['para_txt_list']
    sxptxt = sxpText()
    sxptxt.sentence_list = text_dict['sent_list']
#    print(mtxt)
    section_list = []
    whole_section_title =''
    section_id_dict = {}

    sec_id = 0
    sxpsec = sxpSectionTitle()
    sxpsec.id = sec_id
    sxpsec.id_str = 'global'
    sxpsec.level = sec_id
    sxpsec.title = 'global'

    sxptxt.title = text_dict['title']
    section_id_dict['global'] = sec_id
    section_list.append(sxpsec)

    sxptxt.section_id_dict = section_id_dict

    para_textset = []
    sentence_textset = []
    id_para = 0
    id_sent = 0

    print('parse para')
   # ltx_paraset = sxpParseDivPara.ExtractParagraph(papersrc)
    #for each paragraph:
    current_sec = None
    context_id = 0
    whole_text = ''
    unknown_sec_id = 0
    for i, para in enumerate( slist):
        sxp_para = sxpPara()
        #here we find the whole text of a paragraph
        sxp_para.para_text = para
        pid = str(i)
        sxp_para.para_id = pid
        #here we find the section id of the paragraph
        sxp_para.para_tuple = ParseSectionIDStr(pid)
        #here we find the section title of the para_graph
        #if we use dict to store section title, we will be more efficient here
        if sxp_para.para_tuple[0] in section_id_dict:
            sxpsec_id = section_id_dict[sxp_para.para_tuple[0]]
          #  print sxpsec_id
            sxpsec = section_list[sxpsec_id]
            current_sec = sxpsec
            sxp_para.section_title = sxpsec.title;
            sxp_para.id_sec = sxpsec.id
        else:
            uppersection = ParseUpperSection(sxp_para.para_tuple[0])
            while(len(uppersection) >0 ):
                if uppersection in section_id_dict:
                    sec_id = section_id_dict[uppersection]
                    sxpsec = section_list[sec_id]
                    sxp_para.section_title = sxpsec.title;
                    sxp_para.id_sec = sxpsec.id
                    current_sec = sxpsec
                    break
                else:
                    uppersection = ParseUpperSection(uppersection)
            if len(uppersection) == 0:
                if current_sec is not None:
                    sxp_para.section_title = current_sec.title;
                    sxp_para.id_sec = current_sec.id
                else:
                    sxp_para.section_title = 'unknown';
                    sxp_para.id_sec = unknown_sec_id

##        for sxpsec in section_id_dict:
##            if sxp_para.para_tuple is None:
##                print sxp_para
##            if sxp_para.para_tuple[0]== sxpsec.id_str:
##                sxp_para.section_title = sxpsec.title;
##                break;
##            else:
##                sxp_para.section_title = '';

        #for each paragraph, we extract its sentence
        sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
        sxpsent_set = []
        for sent in sentenceset:
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = id_para
            sxpsent.id_sec = sxp_para.id_sec
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sent)
            sxpsent_set.append(sxpsent)
#*******for each paragraph, we parse a context set from it by iterating its sentences
        print('parse context')
        context = []
        context_result = []
        i = 0
        distset =[0]
        for st in sxpsent_set:
            s = st.sentence_text
            if len(context) == 0:
                context.append(st)
            else:
                [isrel,dist] = is_relevant(context, s, 0.08)#the parameter determine the context group
                distset.append(dist)
                if isrel == True:
                    context.append(st)
                else:
                    para_context = sxpContext()
                    para_context.id = context_id
                    context_id = context_id + 1
                    para_context.id_para = id_para
                    para_context.id_sec = sxp_para.id_sec
                    para_context.context_sent = context
                    context_result.append(para_context)
                    context = []
                    context.append(st)
            i = i + 1
        if len(context)>0:
                para_context = sxpContext()
                para_context.id = context_id
                context_id = context_id + 1
                para_context.id_para = id_para
                para_context.id_sec = sxp_para.id_sec
                para_context.context_sent = context
                context_result.append(para_context)
                context = []
        print(np.mean(distset))
#for this para, we add the context result to the global storage
        sxp_para.context_set = context_result
        sxptxt.context_set.extend(context_result)

#********for each paragraph, we add them to global storate variables
        para_textset.append(para)
        whole_text = whole_text + '\n' + para
        sxp_para.id = id_para
        id_para = id_para + 1
        sxptxt.paraset.append(sxp_para)
    sxptxt.abstract = ''
    sxptxt.conclusion = ''
    sxptxt.whole_text = whole_text
    sxptxt.section_list = section_list
    print('extract keycount')

#**************************************************************
#****************Now we try to extract the key counter of whole_text
    sxptxt.keycount = sxpProcessParaText.ExtractKeyCount(whole_text)

#**************************************************************
    print('make tfidf')

#**************************************************************
#****************Now we try to extract the sentence from the whole_text
##    sxptxt.sentenceset = sxpExtractText.MySentence(whole_text)
##    return sxptxt
#**************************************************************

    sxptxt.para_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(para_textset)

    sxptxt.sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentence_textset)
    sxptxt.sentence_textset = sentence_textset
#***************************************************************
#****************Now we try to build several matrix for graphs can be
#               extracted from sxptxt
#***************************************************************
    print('we begin to build matrix')
    cs = len(sxptxt.section_id_dict) #because we have 0 as the global doc and 1 as the section from the
    ps = len(sxptxt.paraset)
    ss = len(sxptxt.sentenceset)
    ks = len(sxptxt.sentence_tfidf.word)
    ts = len(sxptxt.context_set)
    print(cs, ps, ss, ks,ts)
#first we build d-c matrix, which is actually a row vector
    print('d_c matrix')
    sxptxt.d_c = csr_matrix(np.ones((1,cs), dtype=np.float))
#then building c-p matrix
    print('building c_p matrix')
    sxptxt.c_p = csr_matrix((cs,ps), dtype=np.float)
    print('start')
    print(sxptxt.c_p.shape)
    for para in sxptxt.paraset:
        c = para.id_sec
        p = para.id
#        print c, p
        sxptxt.c_p[c, p] = 1.0

#now to build para_context matrix p_t
    print('building p_t matrix and t_s matrix')
    sxptxt.p_t = csr_matrix((ps,ts), dtype=np.float)
    sxptxt.t_s = csr_matrix((ts,ss), dtype=np.float)
    print('start')
    print(sxptxt.p_t.shape)
    print(sxptxt.t_s.shape)
    for para in sxptxt.paraset:
        p = para.id
        for cont in para.context_set:
            t = cont.id
            sxptxt.p_t[p, t] = 1.0
            for eachs in cont.context_sent:
                s = eachs.id
                sxptxt.t_s[t,s] = 1.0

#        print c, p

#        sxptxt.c_p[p, c] = 1.0
#third, building p-s matrixx
    print('p_s matrix')
    sxptxt.p_s = csr_matrix((ps,ss), dtype=np.float)
    for sent in sxptxt.sentenceset:
        p = sent.id_para
        s = sent.id
        sxptxt.p_s[p,s] = 1.0
#        sxptxt.p_s[p,s] = 1.0

#fourth, building s-k matrix
    print('s_k matrix')
    sxptxt.s_k =csr_matrix(sxptxt.sentence_tfidf.tfidf)
##
##
###fifth, we will build k-k matrix which is the incident relationship of
##    print 'k_k matrix'
##    sxptxt.k_k =csr_matrix((ks,ks), dtype=np.float)
##    for sent in sxptxt.sentenceset:
##        ws =sxpExtractText.ExtractEnglishWord(sent.sentence_text)
##        kwpos= []
##        if len(ws)>0:
##           for w in ws:
##              if w in sxptxt.sentence_tfidf.word:
##                 kwpos.append(sxptxt.sentence_tfidf.word.index(w))
##           n = len(kwpos)
##           for i in range(n-1):
##              sxptxt.k_k[kwpos[i],kwpos[i+1]] = 1
#return sxptxt
    return sxptxt
def ParseUpperSection(sectionid):
    para_seg = sectionid.split('.')
    n = len(para_seg)
    upper = para_seg[0:n-1]
    if len(upper) == 0:
        return ''
    i = 0
    s = ''
    for u in upper:
        if i == 0:
            s = s+ u
        else:
            s = s + '.' + u
        i = i + 1
    return s
class sxpDUCText(HTMLParser):
    include_it = False
    unit_index = 0;
    text_type = 'p'
    text_set = []
    text_para = False;
    text_content = ''
    rootpath =  r'D:\pythonwork\data\duc'
    reference_id = 0;
    reference_set = []
    isendtag = False
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []
        self.__headtext = []
        self.unit_index = 0;
        self.starttag = ''
        self.startendtag = ''
        self.text_set = []
        self.text_para = False
        self.isendtag = False
    def initText(self,rpath):
        if not os.path.exists(rpath):
            print('create the path first')
            os.path.os.mkdir(rpath);
        self.rootpath =  rpath
        self.logfilename  = rpath+'\\'+'latexpaper.log'

    def handle_data(self, data):
        text = data.strip()
        HTMLParser.handle_data(self, data)
        if len(text) > 0 :
            if self.skiptag(self.starttag):
                return;
            g= self.gettagtext(self.starttag)
            if g[0] == True and g[1] == 'text':
                text = sub('[ \s\t\r\n]+', ' ', sxpTestStringEncode.strdecode(text))
                self.__text.append(text)
            else:
                if g[0] == True and g[1] == 'head':
                    headtext = sub('[ \s\t\r\n]+', ' ', sxpTestStringEncode.strdecode(text))
                    self.__headtext.append(headtext)
                elif self.include_it == True:
                    text = sub('[ \s\t\r\n]+', ' ', sxpTestStringEncode.strdecode(text))
                    self.__text.append(text)


#           print self.startendtag,':st-end:',self.starttag,':st:',text,'\n\n'
    def gettagtext(self, tagstr):
        if tagstr.lower() in ['text']:
            return [True,'text']
        if tagstr.lower() in ['head']:
            return [True, 'head']
        return [False,'no']
    def skiptag(self, tagstr):
        if tagstr == 'script':
            return True
        elif tagstr == 'style':
            return True
        elif tagstr == 'code':
            return True
##        elif tagstr == 'sup':
##            return True
##        elif tagstr == 'span':
##            return True
        return False;
    def handle_starttag(self, tag, attrs):
        self.starttag = tag
        if tag  in ['text']:
            self.include_it = True
        HTMLParser.handle_starttag(self, tag, attrs)

    def handle_endtag(self, tag):
        if tag  in ['text']:
            self.include_it = False
        pass


    def text(self):
        self.text_content = ' '.join(self.__text).strip()
        #self.text_content = sub('[\n]+', '\n', ttext)
        self.htext = ' '.join(self.__headtext).strip()
        return [self.htext, self.text_content]
    def savefiletext(self,fname,text):
        try:
            uc = sxpTestStringEncode.strdecode(text)
            f = codecs.open(fname,'w+','utf-8')
            #uc = sxpIsCharacter.toUTF(content)
            #uc = unicode(content,'gbk','ignore').encode('gkb','ignore')
            #uc = content.decode('gbk','ignore').encode('gbk','ignore')
            #uc = unicode(content, 'gbk')
            #uc = sxpIsCharacter.toGBK(content)
            #if using GetUnicode, it will be written
            f.write(uc)
            f.close()
        except Exception as e:
            msg = 'file:{0}:{1}'.format(fname,e)
            sxpLogger.logThisMessageStr(self.logfilename,msg)
            print(msg);
    def savefile(self,fname):
        try:
            uc = sxpTestStringEncode.strdecode(self.text_content)
            f = codecs.open(fname,'w+','utf-8')
            #uc = sxpIsCharacter.toUTF(content)
            #uc = unicode(content,'gbk','ignore').encode('gkb','ignore')
            #uc = content.decode('gbk','ignore').encode('gbk','ignore')
            #uc = unicode(content, 'gbk')
            #uc = sxpIsCharacter.toGBK(content)
            #if using GetUnicode, it will be written
            f.write(uc)
            f.close()
        except Exception as e:
            msg = 'file:{0}:{1}'.format(fname,e)
            sxpLogger.logThisMessageStr(self.logfilename,msg)
            print(msg);

    def RetrieveWeb(self, urlstr):
        timeout = 6
        try:
            socket.setdefaulttimeout(timeout)
            sock = urllib.request.urlopen(urlstr)
            #sock = urllib2.urlopen()
            urlcontent = sock.read()
            sock.close()
        except Exception as e:
            print('failed to access the web page')
            strmsg = '{0}:{1}:{2}'.format('RetrieveWeb',urlstr,e)
            print(strmsg)
            return 0
        return urlcontent;
def GetParafromDUCTxt(txt):
    patstr = '\*\*\*\*'
    pattern = re.compile(patstr)
    para = pattern.split(txt)
    para_set = []
    pid = 0
    i = 0
    for eachp in para:
        if len(eachp)<=0:
            continue
        if i == 0:
            htxt = eachp
            i = i + 1
            continue
        para_set.append([str(pid),eachp.lower().strip()])
        pid = pid + 1
        i = i + 1
    return [htxt,para_set]
def TestPara():
    fname = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\AP880217-0100'
    txt = sxpReadFileMan.ReadTextContent(fname)
    print(GetParafromDUCTxt(txt))
def TestParseOnePaperFile():
    fname = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\FBIS4-62505'
    ParseStructure(fname)
def ParseSectionIDStr(pid):
    return ['global',0]
def ParseStructure(mtxt):
  #  mtxt = sxpReadFileMan.ReadTextContent(fname)
    print(mtxt)
    section_list = []
    whole_section_title =''
    section_id_dict = {}

    sec_id = 0
    sxptxt = sxpText()
    sxpsec = sxpSectionTitle()
    sxpsec.id = sec_id
    sxpsec.id_str = 'global'
    sxpsec.level = sec_id
    sxpsec.title = 'global'
    [htxt, ltx_paraset] = GetParafromDUCTxt(mtxt)
    sxptxt.title = htxt
    section_id_dict['global'] = sec_id
    section_list.append(sxpsec)

    sxptxt.section_id_dict = section_id_dict

    para_textset = []
    sentence_textset = []
    id_para = 0
    id_sent = 0

    print('parse para')
   # ltx_paraset = sxpParseDivPara.ExtractParagraph(papersrc)
    #for each paragraph:
    current_sec = None
    context_id = 0
    whole_text = ''


    unknown_sec_id =0
    for para in ltx_paraset:
        sxp_para = sxpPara()
        #here we find the whole text of a paragraph
        sxp_para.para_text = para[1]
        pid = para[0].lower()
        sxp_para.para_id = pid
        #here we find the section id of the paragraph
        sxp_para.para_tuple = ParseSectionIDStr(pid)
        #here we find the section title of the para_graph
        #if we use dict to store section title, we will be more efficient here
        if sxp_para.para_tuple[0] in section_id_dict:
            sxpsec_id = section_id_dict[sxp_para.para_tuple[0]]
          #  print sxpsec_id
            sxpsec = section_list[sxpsec_id]
            current_sec = sxpsec
            sxp_para.section_title = sxpsec.title;
            sxp_para.id_sec = sxpsec.id
        else:
            uppersection = ParseUpperSection(sxp_para.para_tuple[0])
            while(len(uppersection) >0 ):
                if uppersection in section_id_dict:
                    sec_id = section_id_dict[uppersection]
                    sxpsec = section_list[sec_id]
                    sxp_para.section_title = sxpsec.title;
                    sxp_para.id_sec = sxpsec.id
                    current_sec = sxpsec
                    break
                else:
                    uppersection = ParseUpperSection(uppersection)
            if len(uppersection) == 0:
                if current_sec is not None:
                    sxp_para.section_title = current_sec.title;
                    sxp_para.id_sec = current_sec.id
                else:
                    sxp_para.section_title = 'unknown';
                    sxp_para.id_sec = unknown_sec_id

##        for sxpsec in section_id_dict:
##            if sxp_para.para_tuple is None:
##                print sxp_para
##            if sxp_para.para_tuple[0]== sxpsec.id_str:
##                sxp_para.section_title = sxpsec.title;
##                break;
##            else:
##                sxp_para.section_title = '';

        #for each paragraph, we extract its sentence
        sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
        sxpsent_set = []
        for sent in sentenceset:
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = id_para
            sxpsent.id_sec = sxp_para.id_sec
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sent)
            sxpsent_set.append(sxpsent)
#*******for each paragraph, we parse a context set from it by iterating its sentences
        print('parse context')
        context = []
        context_result = []
        i = 0
        distset =[0]
        for st in sxpsent_set:
            s = st.sentence_text
            if len(context) == 0:
                context.append(st)
            else:
                [isrel,dist] = is_relevant(context, s, 0.08)#the parameter determine the context group
                distset.append(dist)
                if isrel == True:
                    context.append(st)
                else:
                    para_context = sxpContext()
                    para_context.id = context_id
                    context_id = context_id + 1
                    para_context.id_para = id_para
                    para_context.id_sec = sxp_para.id_sec
                    para_context.context_sent = context
                    context_result.append(para_context)
                    context = []
                    context.append(st)
            i = i + 1
        if len(context)>0:
                para_context = sxpContext()
                para_context.id = context_id
                context_id = context_id + 1
                para_context.id_para = id_para
                para_context.id_sec = sxp_para.id_sec
                para_context.context_sent = context
                context_result.append(para_context)
                context = []
        print(np.mean(distset))
#for this para, we add the context result to the global storage
        sxp_para.context_set = context_result
        sxptxt.context_set.extend(context_result)

#********for each paragraph, we add them to global storate variables
        para_textset.append(para[1])
        whole_text = whole_text + '\n' + para[1]
        sxp_para.id = id_para
        id_para = id_para + 1
        sxptxt.paraset.append(sxp_para)
    sxptxt.abstract = ''
    sxptxt.conclusion = ''
    sxptxt.whole_text = whole_text
    sxptxt.section_list = section_list
    print('extract keycount')

#**************************************************************
#****************Now we try to extract the key counter of whole_text
    sxptxt.keycount = sxpProcessParaText.ExtractKeyCount(whole_text)

#**************************************************************
    print('make tfidf')

#**************************************************************
#****************Now we try to extract the sentence from the whole_text
##    sxptxt.sentenceset = sxpExtractText.MySentence(whole_text)
##    return sxptxt
#**************************************************************

    sxptxt.para_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(para_textset)

    sxptxt.sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentence_textset)

#***************************************************************
#****************Now we try to build several matrix for graphs can be
#               extracted from sxptxt
#***************************************************************
    print('we begin to build matrix')
    cs = len(sxptxt.section_id_dict) #because we have 0 as the global doc and 1 as the section from the
    ps = len(sxptxt.paraset)
    ss = len(sxptxt.sentenceset)
    ks = len(sxptxt.sentence_tfidf.word)
    ts = len(sxptxt.context_set)
    print(cs, ps, ss, ks,ts)
#first we build d-c matrix, which is actually a row vector
    print('d_c matrix')
    sxptxt.d_c = csr_matrix(np.ones((1,cs), dtype=np.float))
#then building c-p matrix
    print('building c_p matrix')
    sxptxt.c_p = csr_matrix((cs,ps), dtype=np.float)
    print('start')
    print(sxptxt.c_p.shape)
    for para in sxptxt.paraset:
        c = para.id_sec
        p = para.id
#        print c, p
        sxptxt.c_p[c, p] = 1.0

#now to build para_context matrix p_t
    print('building p_t matrix and t_s matrix')
    sxptxt.p_t = csr_matrix((ps,ts), dtype=np.float)
    sxptxt.t_s = csr_matrix((ts,ss), dtype=np.float)
    print('start')
    print(sxptxt.p_t.shape)
    print(sxptxt.t_s.shape)
    for para in sxptxt.paraset:
        p = para.id
        for cont in para.context_set:
            t = cont.id
            sxptxt.p_t[p, t] = 1.0
            for eachs in cont.context_sent:
                s = eachs.id
                sxptxt.t_s[t,s] = 1.0

#        print c, p

#        sxptxt.c_p[p, c] = 1.0
#third, building p-s matrixx
    print('p_s matrix')
    sxptxt.p_s = csr_matrix((ps,ss), dtype=np.float)
    for sent in sxptxt.sentenceset:
        p = sent.id_para
        s = sent.id
        sxptxt.p_s[p,s] = 1.0
#        sxptxt.p_s[p,s] = 1.0

#fourth, building s-k matrix
    print('s_k matrix')
    sxptxt.s_k =csr_matrix(sxptxt.sentence_tfidf.tfidf)
##
##
###fifth, we will build k-k matrix which is the incident relationship of
##    print 'k_k matrix'
##    sxptxt.k_k =csr_matrix((ks,ks), dtype=np.float)
##    for sent in sxptxt.sentenceset:
##        ws =sxpExtractText.ExtractEnglishWord(sent.sentence_text)
##        kwpos= []
##        if len(ws)>0:
##           for w in ws:
##              if w in sxptxt.sentence_tfidf.word:
##                 kwpos.append(sxptxt.sentence_tfidf.word.index(w))
##           n = len(kwpos)
##           for i in range(n-1):
##              sxptxt.k_k[kwpos[i],kwpos[i+1]] = 1
#return sxptxt
    return sxptxt
def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def SentenceParseOneDUCTxt(fn):

    #fn = 'P14-1008.xhtml'
    fname = paperpath + '\\' + fn
    sxptxt = ParseStructure(fname)
##    fpname = paperpath + '\\pickle\\' + fn +  '_2.pickle'
##    StoreSxptext(sxptxt, fpname)
##    sxptxt = LoadSxptext(fpname)
##    sxpPPT.MakePPTFromTextA(sxptxt)


##    intro_id = FindIntroductionSection(sxptxt)
##    PrintAllPara(sxptxt)
##    PrintAllSentence(sxptxt)
##    PrintIntroductionSent(sxptxt,intro_id)
##    tfid = sxptxt.sentence_tfidf
##    print sxptxt.d_c.shape
##    print sxptxt.c_p.shape
##    print sxptxt.p_s.shape
##    print sxptxt.s_k.shape
##    print sxptxt.p_t.shape
##    print sxptxt.t_s.shape
    return sxptxt

##    print sxptxt.abstract
##    print sxptxt.conclusion
##def SentenceParseOnePaperFile(fn):
##    #fn = 'P14-1007.xhtml'
##    print 'process', fn
##    fname = paperpath + '\\' + fn
##    sxptxt = ParseOnePaper(fname)
##    fpname = paperpath + '\\pickle\\' + fn +  '_2.pickle'
##    StoreSxptext(sxptxt, fpname)
##    sxptxt = LoadSxptext(fpname)
##    print sxptxt.d_c.shape
##    print sxptxt.c_p.shape
##    print sxptxt.p_s.shape
##    print sxptxt.s_k.shape

def parsefile(fname):
    try:
        f = codecs.open(fname,'r+','utf-8')
        #uc = sxpIsCharacter.toUTF(content)
        #uc = unicode(content,'gbk','ignore').encode('gkb','ignore')
        #uc = content.decode('gbk','ignore').encode('gbk','ignore')
        #uc = unicode(content, 'gbk')
        #uc = sxpIsCharacter.toGBK(content)
        #if using GetUnicode, it will be written
        urltext = f.read()

        f.close()
        patstr = '\s\s\s'
        p = re.compile(patstr)
        textu =p.sub(' **** ',urltext)
        print(textu)
        parser = sxpDUCText()
        parser.feed(textu)
        parser.close()
        return parser.text()
    except Exception as e:
        msg = 'file:{0}:{1}'.format(fname,e)
        sxpLogger.logThisMessageStr(logfilename,msg)
        print(msg);
        return ['']
def dehtml(text):
    parser = sxpDUCText()
    parser.feed(text)
    parser.close()
    return parser.text()


def testtext():
    text = r'''''
        <html>
            <body>
                <b>Project:</b> DeHTML<br>
                <b>Description</b>:<br>
                This small script is intended to allow conversion from HTML markup to
                plain text.
            </body>
            <script>function {}</script>
            <style> cccs </style>
        </html>
    '''
    print((dehtml(text)))
def testtext1():
    text = r'''
        <html>
            <body>
               <b>Project:</b> DeHTML<br>
                <b>Description</b>:<br>
                This small script is intended to allow conversion from HTML markup to
                plain text.
                <li><a href="http://pinyin.sogou.com/">输入法</a></li>
            </body>
            <script>function {}</script>
            <div class="c-abstract">本文实例讲述了<em>Python单链表</em>的简单实现方法,分享给大家供大家参考。具体方法如下:通常来说,要定义一个单链表,首先定义<em>链表元素</em>:Element.它包含3个字段:...</div>
            <style> cccs </style>
        </html>
    '''
    print((dehtml(text)))
def testlatex():
    text = r'''
    <HEAD>Hurricane Gilbert Heads Toward Dominican Coast</HEAD>
        <text>An <math xmlns="http://www.w3.org/1998/Math/MathML" id="S3.SS3.p1.m1" class="ltx_Math" alttext="n" display="inline"><mi>n</mi></math>-best list reflects a tiny portion of a decoder’s search space, typically fixed at 1000 hypotheses.
    Lattices<span class="ltx_note ltx_role_footnote"><sup class="ltx_note_mark">2</sup><span class="ltx_note_outer"><span class="ltx_note_content"><sup class="ltx_note_mark">2</sup>Or forests for hierarchical and syntactic decoders.</span></span></span> can represent an exponential number of hypotheses
    in a compact structure.
    In this section, we discuss how a lattice from a multi-stack phrase-based decoder such as Moses <cite class="ltx_cite">[<a href="#bib.bib16" title="Moses: open source toolkit for statistical machine translation" class="ltx_ref">17</a>]</cite> can be desegmented
    to enable word-level features.</text>
    '''
    print((dehtml(text)))

def testurl():
    url = r'http://www.sohu.com/'
    parser = sxpDUCText()
    rpath = r'D:\pythonwork\data\baidunews\taskset\1\text'
    parser.initText(rpath)
    text = parser.RetrieveWeb(url)

    utext = sxpTestStringEncode.strdecode(text)
    parser.feed(utext)
    parser.close()
    print(parser.text())
    fname = r'D:\pythonwork\data\baidunews\taskset\1\text' + '\\' + '1.txt'
    parser.savefiletext(fname,parser.text_content)
def testducfile():
    fname = r'D:\pythonwork\code\tjrank_sentences\data\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocs\docs\d061j\AP880911-0016'
    print(parsefile(fname))
    dirname = r'D:\pythonwork\code\tjrank_sentences\data\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocs\docs'
    modeldir = r'D:\pythonwork\code\tjrank_sentences\data\evaluation_results\evaluation_results\abstracts\phase1\SEEmodels\SEE.edited.abstracts.in.edus'
    txtdir = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt'
    storemodeldir = r'D:\pythonwork\code\paperparse\paper\papers\duc\model'
    mf = ProcessDUCFileDir(dirname, modeldir,txtdir,storemodeldir)
    for eachm in mf:
        print(eachm)
def sxpGetDirFileSubList(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
    filelist = []
    subdirlist = []
    try:
        files = os.listdir(filedir)
        #now we first read each file in the txtPath
        for f in files:
          df = os.path.join(filedir, f)
          if os.path.isdir(df):
             subdirlist.append(f)
          else:
             filelist.append(f)
    except Exception as e:
        msg = filedir + ':' + str(e)
        print(msg)
        sxpLogger.logThisMessageStr(logfilestr,msg)
    return filelist, subdirlist
def ProcessDUCFileDir(dirname, modeldir,txtdir,storemodeldir):
    filelist, subdirlist = sxpGetDirFileSubList(dirname)
    total_file_set = []
    for eachsub in subdirlist:
        fullpath = dirname+ '\\' + eachsub
        filelist1, subdirlists = sxpGetDirFileSubList(fullpath)
        for eachf in filelist1:
            f = [eachf, fullpath + '\\' + eachf]
            total_file_set.append(f)
        print(filelist1)

    modelfile_list, subdirlists = sxpGetDirFileSubList(modeldir)
    system_model_file = []
    for eachf in total_file_set:
        fn = eachf[0]
        fnpath = eachf[1]
        modelf = []
        for eachmodelf in modelfile_list:
            if eachmodelf.find(fn)>= 0:
                modelf.append(modeldir + '\\' + eachmodelf)
                sf = modeldir + '\\' + eachmodelf
                tf = storemodeldir + '\\' + eachmodelf
                win32file.CopyFile(sf,tf, 0)
        system_model_file.append([fn,fnpath,modelf])

        [htxt, mtxt] = parsefile(fnpath)
        sf = txtdir + '\\' +  fn
        mtxt =  htxt + mtxt
        sxpReadFileMan.WriteStrFile(sf,mtxt,'utf-8')



    return system_model_file

def is_relevant(sentences, s, t):
    max_dis = 0
    maintxt = ''
    for eachs in sentences:
        maintxt = maintxt + ' ' + eachs.sentence_text
    for eachs in sentences :
        sim = sxpContextMan.Similarity(eachs.sentence_text, s)
        if sim > max_dis:
            max_dis = sim
    if max_dis > t:
        return True,max_dis
    return False,max_dis
def is_relevantA(sentences, s, t):
    max_dis = 0
    maintxt = ''
    for eachs in sentences:
        maintxt = maintxt + ' ' + eachs.sentence_text
    max_dis = sxpContextMan.Similarity(maintxt, s)
    if max_dis > t:
        return True
    return False
def ParseHTMLContentStr(text):
    parser = sxpDUCText()
    parser.feed(text)
    parser.close()
    return parser.text()

def GetDirFileList(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
    filelist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      if os.path.isdir(os.path.join(filedir, f)):
         pass
      else:
         filelist.append(f)
    return filelist
def ProcessFilesInDir():
    paperpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt'
    txtpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\txt'
    flist = GetDirFileList(paperpath)
    modeldir = r'D:\pythonwork\code\paperparse\paper\papers\allmodel'
    mflist = GetDirFileList(modeldir)
    pyrouge = 0
    for fn in flist:
        sxptxt = SentenceParseOneDUCTxt( fn)

        txtpathfn = txtpath + '\\' + fn
        sxpReadFileMan.WriteStrFile(txtpathfn,sxptxt.whole_text,'utf-8')
        i = 1
        for eachm in mflist:
            sf = modeldir + r'\\' + eachm
            tf = paperpath + r'\\model\\' + eachm
            if eachm.lower().find(fn.lower())>= 0:
                print(sf)
                print(tf)
                if pyrouge == 1:
                    win32file.CopyFile(sf,tf, 0)
                if pyrouge == 0:
                    mfname = paperpath + r'\\model\\' + fn + '_reference' + str(i) + '.txt'
                    i = i + 1
                    win32file.CopyFile(sf,mfname, 0)

def ProcessFilesInDirForPyrouge():
    paperpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt'
    txtpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\txt'
    flist = GetDirFileList(paperpath)
    modeldir = r'D:\pythonwork\code\tjextractinfo\data\evaluation_results\evaluation_results\abstracts\phase1\SEEmodels\SEE.edited.abstracts.in.edus'
    print(modeldir)
    mflist = GetDirFileList(modeldir)
    pyrouge = 2
    rougetag = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V']
    for fn in flist:
        sxptxt = SentenceParseOneDUCTxt( fn)

        txtpathfn = txtpath + '\\' + fn
        sxpReadFileMan.WriteStrFile(txtpathfn,sxptxt.whole_text,'utf-8')
        i = 0
        for eachm in mflist:
            sf = modeldir + r'\\' + eachm
            tf = paperpath + r'\\model_html\\' + eachm
            if eachm.lower().find(fn.lower())>= 0:
                print(sf)
                print(tf)
                if pyrouge == 1:
                    win32file.CopyFile(sf,tf, 0)
                if pyrouge == 2:
                    mfname = paperpath + r'\\model\\' + fn + '.' + rougetag[i] + '.html'
                    i = i + 1
                    win32file.CopyFile(sf,mfname, 0)
def ProcessFilesInDirForOnlyModelFile():
    srcpaperpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\txt'
    paperpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt'
    txtpath = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\txt'
    print(paperpath)
    flist = GetDirFileList(srcpaperpath)
    modeldir = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\allmodel'
    mflist = GetDirFileList(modeldir)
    pyrouge = 2
    rougetag = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V']
    for fn in flist:
        sxptxt = SentenceParseOneDUCTxt( fn)

 #       txtpathfn = txtpath + '\\' + fn
 #       sxpReadFileMan.WriteStrFile(txtpathfn,sxptxt.whole_text,'utf-8')
        i = 0
        docname = fn
        for eachm in mflist:
            sf = modeldir + '\\' + eachm
            tf = paperpath + '\\model_html\\' + eachm
            if eachm.lower().find(fn.lower())>= 0:
                if pyrouge == 2:
                   # mfname = paperpath + '\\model_html\\' + 'DUC.' + fn + '.' + rougetag[i] + '.html'
                    docname = eachm
                    mfname = paperpath + '\\model_html\\' + eachm
                    print(mfname)
                    print(sf)
                    i = i + 1
                    win32file.CopyFile(sf,mfname, 0)
        fpname = paperpath + '\\pickle\\' + docname
        StoreSxptext(sxptxt, fpname)

def ProcessFilesInDirForOnlyGraph():
    srcpaperpath = r'D:\pythonwork\code\paperparse\paper\duc\txt'
    paperpath = r'D:\pythonwork\code\paperparse\paper\duc'
    txtpath = r'D:\pythonwork\code\paperparse\paper\duc\txt'
    print(paperpath)
    flist = GetDirFileList(srcpaperpath)
    modeldir = r'D:\pythonwork\code\paperparse\paper\duc\allmodel'
    mflist = GetDirFileList(modeldir)
    pyrouge = 2
    rougetag = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V']
    copymodelfile = False
    for fn in flist:
        sxptxt = SentenceParseOneDUCTxt( fn)

 #       txtpathfn = txtpath + '\\' + fn
 #       sxpReadFileMan.WriteStrFile(txtpathfn,sxptxt.whole_text,'utf-8')
        i = 0
        docname = fn
        if copymodelfile == True:
            for eachm in mflist:
                sf = modeldir + '\\' + eachm
                tf = paperpath + '\\model_html\\' + eachm
                if eachm.lower().find(fn.lower())>= 0:
                    if pyrouge == 2:
                       # mfname = paperpath + '\\model_html\\' + 'DUC.' + fn + '.' + rougetag[i] + '.html'
                        docname = eachm
                        mfname = paperpath + '\\model_html\\' + eachm
                        print(mfname)
                        print(sf)
                        i = i + 1
                        win32file.CopyFile(sf,mfname, 0)
        fpname = paperpath + '\\pickle\\' + docname+'.pickle'
        StoreSxptext(sxptxt, fpname)


def main():
    #testlatex()
    #testurl()
 #   testducfile() #parse duc txt file, make graph pickle, and then copy model file to the specified dir
    #TestPara()
    #TestParseOnePaperFile()
    #ProcessFilesInDir()
 #   ProcessFilesInDirForOnlyModelFile() # only copy model files from duc collection to our specified dir after parsing txt into graph pickles.
 #   ProcessFilesInDirForOnlyGraph() #this is only produce the pickle graph file for the DUC document.
 #   ParseModelFile(r"E:\pythonworknew\code\sentencerank\test\duc2002\single_model_src\D061.P.100.J.I.AP880911-0016.html")
    text_dict=ParseRawfile(r"E:\pythonworknew\code\textsum\test\duc2002\single_raw_src\FT932-15960")
    print("*******************************")
    s=CheckTypeParseLines(text_dict['text'])
    for i, each in enumerate(s):
        print((i,each))
    print("*******************************")
    text_dict=ParseRawfile(r"E:\pythonworknew\code\textsum\test\duc2002\single_raw_src\LA042590-0135")
    s=CheckTypeParseLines(text_dict['text'])
    for i, each in enumerate(s):
        print((i,each))

    print("*******************************")
    text_dict=ParseRawfile(r"E:\pythonworknew\code\textsum\test\duc2002\single_raw_src\SJMN91-06162032")
    s=CheckTypeParseLines(text_dict['text'])
    for i, each in enumerate(s):
        print((i,each))
    print("********************************")
    text_dict=ParseRawfile(r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocswithsentences\docs.with.sentence.breaks\d120i\LA112790-0154.S")
    s=ParseLineHtml(text_dict['text'])
    for i, each in enumerate(s):
        print((i,each))
    print("*********************************")
    text = ''' <s docid="LA112790-0154" num="11" wdcount="22"> Major fell two votes short of the needed majority, but his opponents conceded defeat and Conservative Party officials declared him elected .</s>

<s docid="LA112790-0154" num="11" wdcount="22"> Major fell two votes short of the needed majority, but his opponents conceded defeat and Conservative Party officials declared him elected .</s>

    '''
    s=ParseLineHtml(text)
    for i, each in enumerate(s):
        print((i,each))
def TestParseStruct():
    print('*******************************')
    fname =r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocswithsentences\docs.with.sentence.breaks\d120i\LA112790-0154.S"
    sxptxt =ParseSentSxptxt(fname)
    for i, each in  enumerate(sxptxt.sentenceset):
        print((i,'======='))
        print((each.sentence_text))

    for i, each in enumerate(sxptxt.sentence_textset):
        print((i,'*******'))
        print(each)
if __name__ == '__main__':
    TestParseStruct()
