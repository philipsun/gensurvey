#-------------------------------------------------------------------------------
# Name:        sxpACLSum.py
# Purpose:
#
# Author:      sunxp
#
# Created:     23/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=UTF-8
import re
import os
import json
import collections
import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
import pickle

#import sxpPackage
import sxpReadFileMan
import sxpTextEncode

import sxpProcessParaText
import sxpFenciMakeTFIDF
import sxpParseDivPara
import sxpParseSection
import sxpExtractText
import sxpJudgeCharacter
from sxpPackage import *
import sxpParseSectionNetwork
import sxpContextMan


import sxpFenciMakeTFIDF
import sxpJudgeCharacter
import sxpTestStringEncode

from graphengine import sxpGraphEngine

#from graphengine.sxpGraphEngine import *

class sxpNode:
    node_type=''
    node_text = ''
    node_child = []
    node_id =0
    node_idx=0
    def __init__(self,ndtype):
        self.notde_type=ndtype
        self.node_child=[]
        self.node_text = []
        self.node_title=''
        self.node_id =0
        self.node_idx=0
    def AddSubNode(self,sxpnode):
        self.node_child.append(sxpnode)
    def AddSubText(self,txtnd):
        self.node_text.append(txtnd)

paperpath = './test/acl2014/papers'
fdir = './test/acl2014'
pkdir = r'./test/acl2014/papers_pk'
graph_dir =   './test/acl2014/papers_graph'
data_dir =r'./test/acl2014'
def main():
    cmd = 'Work'
    if cmd == "MakeFileList":
        MakeFileList()
    if cmd == 'TestWork':
        TestWork()
    if cmd == 'Work':
        Work()
    if cmd =='LoadDocModelSentence':
      #  print(LoadDocModelSentence())

        LoadDocModelSentence()
def TestWork():
    TestProcessOne()
def Work():
 #   LoadExtractJsonFiles()
 #   pkdir = r'./test/multipaper/papers_pk'
 #   ShowTitle(pkdir)
  #  TestProcessOne()
    BuildGraph(include_absconc=True)
 #   graph_dir =   './test/multipaper/papers_graph'
 #   LoadGraphFileName(pkdir,graph_dir)
def GetFileName(fdir,keystr):
    fname_dict={}
    fname_dict['grah_dict']=os.path.join(fdir, keystr)
    fname_dict['sentence_dict']=os.path.join(fdir,  keystr)
    return fname_dict
def ShowTitle(pkdir):
    fnamelist = sxpReadFileMan.GetDirFileListType(pkdir,'pk')
    graph_fname_list =[]
    for fname in fnamelist:
        graph_dict = sxpReadFileMan.LoadSxptext(fname)
        fid =graph_dict['id']
        title= graph_dict[u'title']
        print(fid,title)
def LoadGraphFileName(pkdir,graph_dir):
    fnamelist = sxpReadFileMan.GetDirFileListType(pkdir,'pk')
    graph_fname_list =[]
    for fname in fnamelist:
        graph_dict = sxpReadFileMan.LoadSxptext(fname)
    #    jsdict =  data_dict['jsdict']
    #    print(jsdict)
    #    graph_dir =   './test/multipaper/papers_graph'
        #print('build graph for',fname)
        #ParsePaperJson(jsdict,data_dict['id'],graph_dir)
        fid =graph_dict['id']
        title= graph_dict[u'title']
        graphname =fid +'.graph'
     #   graph_dict = MakeGraph(graph_root,graphname,graph_dir)
     #   sxpgraph = sxpGraphEngine.sxpNetwork(graph_dir,graphname,dbinit=False)
        graph_dictname = os.path.join(graph_dir,graphname+'.grah_dict')
        matrix_dictname = os.path.join(graph_dir,graphname+'.matrix_vec_dict')
        sentence_data_dictname =os.path.join(graph_dir,graphname+'.sentence_data_dict')
#        print('graphdict',graph_dictname)
        fname_dict={}
        fname_dict['fname']=fname
        fname_dict['graph_dictname']=graph_dictname
        fname_dict['matrix_dictname']=matrix_dictname
        fname_dict['sentence_data_dictname']=sentence_data_dictname
        fname_dict['graphname']=graphname
        fname_dict['title']=title
        fname_dict['fid']=fid
        graph_fname_list.append(fname_dict)

        #graph_dict=sxpReadFileMan.LoadSxptext(fdictname)

    return graph_fname_list
def BuildGraph(include_absconc=True):
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir =   r'./test/multipaper/papers_graph'
#    data_dir =r'./test/multipaper'

    flist =sxpReadFileMan.GetDirFileList(paperpath)
    for i, fn in enumerate(flist):
        fset = fn.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'xhtml':
                fid =  '{0:0>4}'.format(i)

                SentenceParseOnePaper(fid,fn,include_absconc = include_absconc)
def MakeFileList():
    fdir
    flist =sxpReadFileMan.GetDirFileList(paperpath)
    exc_pk_file =[]
    inc_pk_file =[]
    fdict_list = []
    for i, fn in enumerate(flist):
        fid_name = {}
        fid =  '{0:0>4}'.format(i)
        fid_name['id']= fid
        fid_name['raw']=fn
        fid_name['exc_pk']= pkdir + '\\exc\\' + fid +  '.pk'
        fid_name['inc_pk']= pkdir + '\\inc\\' + fid +  '.pk'
        fdict_list.append(fid_name)
    fname = fdir +'/fdict_list.dict'
    sxpReadFileMan.SaveObject(fdict_list,fname)
    return fdict_list
def LoadDocModelSentence(incabs='inc'):
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir = r'./test/multipaper/papers_graph'
#    data_dir = r'./test/multipaper'
    fdict_list = GetFileNameDictList()
    doc_model_sent_list =[]
    for fdict in fdict_list:
        doc_dict ={}
        if incabs == 'inc':
            sxptxt = sxpReadFileMan.LoadSxptext(fdict['inc_pk'])
            abstract =sxptxt.abstract
            conclusion = sxptxt.conclusion
            sxpsent = sxptxt.sentenceset[0]
        print(fdict['id'], sxptxt.section_list[0].title)
##        print(abstract)
##        print(conclusion)
        abs_sent = abstract.split('.**.\n')
        abs_sent_f =[]
        for s in abs_sent:
            s = s.strip()
            if len(s)==0:
                continue
            else:
                abs_sent_f.append([s])

        con_sent = conclusion.split('.**.\n')

        con_sent_f =[]
        for s in con_sent:
            s = s.strip()
            if len(s)==0:
                continue
            else:
                con_sent_f.append([s])
        doc_dict['model']=[abs_sent_f,con_sent_f]
        doc_dict['title']=sxptxt.section_list[0].title
        doc_dict['fid']=fdict['id']
        doc_dict['sentence_textset'] = sxptxt.sentence_textset
        doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list

def GetFileNameDictList():
    fname = fdir +'/fdict_list.dict'
    fdict_list=sxpReadFileMan.LoadObject(fname)
    return fdict_list

def SentenceParseOnePaper(fid,fn,include_absconc = True):
    #fn = 'P14-1008.xhtml'
    fname = paperpath + '/' + fn
    print('process', fname,fid)
    #include_absconc = False
    #3_.pickle is for inclusiong of abstract and conclusion
    #2_.pickle is for exclusion of abstract and conclusion
    if include_absconc == False:
        sxptxt = ParseOnePaper(fname,include_absconc)
        fpname = pkdir + '/exc/' + fid +  '.pk'
        StoreSxptext(sxptxt, fpname)
    include_absconc = True;
    if include_absconc == True:
        sxptxt = ParseOnePaper(fname,include_absconc)
        fpname = pkdir + '/inc/' + fid +  '.pk'
        StoreSxptext(sxptxt, fpname)
def LoadACLData(graph_dict_fid,test_case):
    sxptxt=None
    if test_case =='inc':
        fpname = pkdir + '/inc/' + graph_dict_fid
        print('load ACL file',fpname)
        sxptxt = sxpReadFileMan.LoadSxptext(fpname)
    if test_case =='exc':
        fpname = pkdir + '/exc/' + graph_dict_fid
        sxptxt = sxpReadFileMan.LoadSxptext(fpname)
    return sxptxt
def LoadFile(fname):
    if not os.path.exists(fname):
        print('file does not exists',fname)
        return ''
    # f = open(fname,'r')
    # txtc = f.read()
    # f.close();
    # tstr = sxpTestStringEncode.strencode(txtc,'utf-8')
    tstr = sxpReadFileMan.ReadTextUTF(fname)
    return tstr
def ParseOnePaper(fname,include_absconc = True):
    print('load file:', fname)
    papersrc = LoadFile(fname)
    papersrc = sxpJudgeCharacter.ReplaceNonEnglishCharacter(papersrc)
#    papersrc = repr(papersrc.decode('utf-8','ignore').encode('utf-8'))
#    papersrc = papersrc.replace(r'\n',' ')
   # print papersrc
##    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
##   # titleitem = soup.findAll(attr={"class":"ltx_title ltx_title_document"})
##    titleitem = soup.find_all("ltx_title ltx_title_section")
    shortfname = fname.split('\\')[-1]
    sxptxt = sxpText()
    sxptxt.fname = fname;
    abstract_str = ''
    conclusion_str = ''
    whole_text = ''
    print('load section title')
##    for s in sectionset:
##        print s.parent_id, s.text
## Now first we extract section ti  ltes
    section_list = []
    whole_section_title =''
    section_id_dict = {}
    sec_set = sxpParseSection.ExtractSection(papersrc)
    sec_id = 0
    for sec in sec_set:
        sxpsec = sxpSectionTitle()
        sxpsec.id = sec_id
        sxpsec.id_set = ParseParaID(sec.id_str)
        sxpsec.id_str = sec.id_str.lower()
        sxpsec.t_type = sec.title_type
        sxpsec.title = sec.title
        whole_section_title = whole_section_title + '\n' + sec.title
        if sxpsec.id_str in section_id_dict.keys():
            print(sxpsec.id_str, sxpsec.title)
           # section_list[os] = sxpsec
        else:
            section_id_dict[sxpsec.id_str]=sec_id
            sec_id = sec_id + 1
            section_list.append(sxpsec)
    unknown_sec_id = 0
    if 'unknown' in section_id_dict.keys() == False:
        sxpdoc = sxpSectionTitle()
        sxpdoc.id = sec_id
        sxpdoc.title = 'unknown'
        sxpdoc.id_str = 'unknown'
        sxpdoc.level = 0
        sxpdoc.t_type = 'unknown'
        section_id_dict['unknown']=sec_id
        unknown_sec_id = sec_id
        section_list.append(sxpdoc)
        sec_id = sec_id + 1

    sxptxt.section_id_dict = section_id_dict
    sxptxt.whole_sectitle = whole_section_title
##    for sec in section_list:
##        print sec.id

#**************************************************************
#*********First we add section title to paragraphs*************
    para_textset = []
    sentence_textset = []
    id_para = 0
    id_sent = 0
    add_sec_title_to_para  = 0
    if add_sec_title_to_para == 1:
        for sec in section_list:
            sxp_para = sxpPara()
            sxp_para.para_text = sec.title
            sxp_para.id = id_para
            sxp_para.id_sec = sec.id
            sxp_para.para_id = sec.id_str
            para_textset.append(sxp_para.para_text)
            #add sentence
            sxpsent = sxpSent()
            sxpsent.sentence_text = sec.title
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = id_para
            sxpsent.id_sec = sec.id
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sec.title)
            whole_text = whole_text + '\n' + sec.title
            sxp_para.section_title = sxpsec.title;
            id_para = id_para + 1
            sxptxt.paraset.append(sxp_para)

#*********Following is to extract the paragraph and its section title
##    print 'begin to find all ltx_para'
##    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
##    paraset = []
##    ltx_paraset = soup.find_all(class_=re.compile("ltx_para"))
    print('parse para')
    ltx_paraset = sxpParseDivPara.ExtractParagraph(papersrc)
    #for each paragraph:
    current_sec = None
    context_id = 0
    abstract_str = ''
    conclusion_str = ''
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
        if sxp_para.para_tuple[0] in section_id_dict.keys():
            sxpsec_id = section_id_dict[sxp_para.para_tuple[0]]
          #  print sxpsec_id
            sxpsec = section_list[sxpsec_id]
            current_sec = sxpsec
            sxp_para.section_title = sxpsec.title;
            sxp_para.id_sec = sxpsec.id
        else:
            uppersection = ParseUpperSection(sxp_para.para_tuple[0])
            while(len(uppersection) >0 ):
                if uppersection in section_id_dict.keys():
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

        if IsAbstract(sxp_para.section_title) == 1:
            sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
            for sent in sentenceset:
                rsent = RemoveUStrSpace(sent) + '.'
                abstract_str = abstract_str +rsent + '**.\n'
            if include_absconc == False:
                continue

        if IsConclusion(sxp_para.section_title) == 1:
            sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
            for sent in sentenceset:
                rsent = RemoveUStrSpace(sent) + '.'
                conclusion_str = conclusion_str +rsent + '**.\n'
            if include_absconc == False:
                continue

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

        context = []
        context_result = []
        i = 0
        for st in sxpsent_set:
            s = st.sentence_text
            if len(context) == 0:
                context.append(st)
            elif is_relevant(context, s, 0.06):
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

#for this para, we add the context result to the global storage
        sxp_para.context_set = context_result
        sxptxt.context_set.extend(context_result)

#********for each paragraph, we add them to global storate variables
        para_textset.append(para[1])
        whole_text = whole_text + '\n' + para[1]
        sxp_para.id = id_para
        id_para = id_para + 1
        sxptxt.paraset.append(sxp_para)
    sxptxt.abstract = abstract_str
    sxptxt.conclusion = conclusion_str
    sxptxt.whole_text = whole_text
    sxptxt.section_list = section_list
    print (' parse section network')
    sxptxt.c_c = sxpParseSectionNetwork.ParseSectionNetwork(sxptxt)

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
    sxptxt.c_p = csr_matrix((cs,ps), dtype=float)
    print('start')
    print(sxptxt.c_p.shape)
    for para in sxptxt.paraset:
        c = para.id_sec
        p = para.id
#        print c, p
        sxptxt.c_p[c, p] = 1.0

#now to build para_context matrix p_t
    print('building p_t matrix and t_s matrix')
    sxptxt.p_t = csr_matrix((ps,ts), dtype=float)
    sxptxt.t_s = csr_matrix((ts,ss), dtype=float)
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
    sxptxt.p_s = csr_matrix((ps,ss), dtype=float)
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
##    sxptxt.k_k =csr_matrix((ks,ks), dtype=float64)
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
        return True
    return False
def is_relevantA(sentences, s, t):
    max_dis = 0
    maintxt = ''
    for eachs in sentences:
        maintxt = maintxt + ' ' + eachs.sentence_text
    max_dis = sxpContextMan.Similarity(maintxt, s)
    if max_dis > t:
        return True
    return False
def RemoveUStr(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
##    patstr = "\s"
##    pattern = re.compile(patstr)
##    nstr = pattern.sub(' ',nstr)
    return nstr
def RemoveUStrSpace(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
    patstr = "\s+"
    pattern = re.compile(patstr)
    nstr = pattern.sub(' ',nstr)
    return nstr

def SegSent(s):
    patstr = u',|\.\s|\:|\?|，|。|：|？|！|；'
    pattern = re.compile(patstr)
    ss = pattern.split(s)
    return ss
def SearchSentProcess(patstr, s, pat_name,pi):
    sent_list = SegSent(s)
    sent_pos_list = []
    i = 0;
    for eachs in sent_list:
        sent_pos = SearchProcess(patstr, eachs,'n', pat_name,pi)
        for eachsubpos in sent_pos:
            eachsubpos.extend([i])
            sent_pos_list.append(eachsubpos)
        i  = i + 1
    return sent_pos_list
def SearchProcess(patstr, s, sent='y', pat_name='',pi=0):
    if sent == 'y':
        return SearchSentProcess(patstr,s, pat_name,pi)
    pattern = re.compile(patstr)
    match =pattern.search(s)
    pattern_pos = []
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(s,posd[1])
        pattern_pos.append([tgtxt,posd,tg,pat_name,pi,0])
    return pattern_pos
def IsAbstractConclusion(strtitle):
    patstr = u'abstract|conclusion'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def IsConclusion(strtitle):
    patstr = u'conclusion'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def IsAbstract(strtitle):
    patstr = u'abstract'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def TestIsAbstractConclusion():
    s = 'Abbstract'
    print(IsAbstractConclusion(s))
    s = 'Conclusions'
    print(IsAbstractConclusion(s))
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
def ParseSectionIDStr(para_id):
    if isinstance(para_id,list):
        paraid_str = para_id[0]
    else:
        paraid_str = para_id
    para_seg = paraid_str.split('.')
    p = '^(s+)x*\d+'
    pp = '^(p+)x*\d+'
    sectstr= ''
    parastr = ''
    for seg in para_seg:
        g = re.match(p,seg,0)
        if g is not None:
            if len(sectstr)==0:
                sectstr = sectstr+seg
            else:
                sectstr = sectstr+'.'+seg
        g = re.match(pp,seg,0)
        if g is not None:
            if len(parastr)==0:
                parastr = parastr+seg
            else:
                parastr = parastr+'.'+seg
    if len(sectstr)==0:
        sectstr = paraid_str
    if len(parastr)==0:
        parastr = paraid_str
    return [sectstr, parastr]
def ParseParaIDSetStr(para_id):
    if isinstance(para_id,list):
        paraid_str = para_id[0]
    else:
        paraid_str = para_id
    if  paraid_str is not None:
        p = '(.+)\\.p(\d+)$'
        g = re.match(p,paraid_str,0)
        if g is not None:
            return g.groups()
        else:
            return [paraid_str,'0'];
    else:
        return['noid','0']
def ParseParaID(paraid_str):
    if isinstance(paraid_str,list):
        paraid_str = paraid_str[0]
    sec = paraid_str.split('.')
    pa = r'(\D+)(\d+)'
    seclevel = len(sec)
    if  sec is not None:
        secpara = []
        i = 0
        for secstr in sec:
            g = re.match(pa,secstr,0)
            if g is not None:
                secpara.append(g.groups())
            else:
                t = [secstr,'{0}'.format(i)]
                secpara.append(t)
            i = i + 1
        return secpara;
    else:
        return[]

def LoadDocData():
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    for fname_dict in graph_fname_list:
        fname_dict = graph_fname_list[0]
        graph_dict, matrix_dict,sentence_data_dict=LoadFileData(fname_dict['fid'])
        doc_dict ={}
        abstract =sentence_data_dict['abstract']
        conclusion=sentence_data_dict['conclusion']
        doc_dict['model']=[abstract,conclusion]
        doc_dict['title']=fname_dict['title']
        doc_dict['fid']=fname_dict['fid']
        doc_dict['graph_dict']=graph_dict
        doc_dict['matrix_dict']=matrix_dict
        doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list
def LoadGraphMatrixSentence(fid=[]):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    for fname_dict in graph_fname_list:
        fname_dict = graph_fname_list[0]
        if len(fid)>0:
            if fname_dict['fid'] in fid:
                graph_dict, matrix_dict,sentence_data_dict=LoadFileData(fname_dict['fid'])
                doc_dict ={}
##                abstract =sentence_data_dict['abstract']
##                conclusion=sentence_data_dict['conclusion']
                doc_dict['sentence_data_dict']=sentence_data_dict
                doc_dict['title']=fname_dict['title']
                doc_dict['fid']=fname_dict['fid']
                doc_dict['graph_dict']=graph_dict
                doc_dict['matrix_dict']=matrix_dict
                doc_model_sent_list.append(doc_dict)
        else:
            graph_dict, matrix_dict,sentence_data_dict=LoadFileData(fname_dict['fid'])
            doc_dict ={}
##                abstract =sentence_data_dict['abstract']
##                conclusion=sentence_data_dict['conclusion']
            doc_dict['sentence_data_dict']=sentence_data_dict
            doc_dict['title']=fname_dict['title']
            doc_dict['fid']=fname_dict['fid']
            doc_dict['graph_dict']=graph_dict
            doc_dict['matrix_dict']=matrix_dict
            doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list
def TestProcessOne():
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir =   r'./test/multipaper/papers_graph'
#    data_dir =r'./test/multipaper'
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)

    fname_dict=graph_fname_list[10]

    print(fname_dict['fname'],fname_dict['graphname'],fname_dict['graph_dictname'],fname_dict['matrix_dictname'])
    #the following commented code is for parsing json file of paper to build one graph for the
    json_dict = sxpReadFileMan.LoadSxptext(fname_dict['fname'])
    jsdict =  json_dict['jsdict']
##   # print(jsdict)
    graph_dict,matrix_dict,sentence_data_dict=ParsePaperJson(jsdict,json_dict['id'],graph_dir)
#    graph_dict = sxpReadFileMan.LoadSxptext(fname_dict['graph_dictname'])
#    matrix_dict = sxpReadFileMan.LoadSxptext(fname_dict['matrix_dictname'])
    print('abstract,*************')
    for sent in sentence_data_dict['abstract']:
        print(sent)
    print('conclusion,*************')
    for sent in sentence_data_dict['conclusion']:
        print(sent)

    print('sentence,*************')
    sentence_dict =sentence_data_dict['sentence_dict']
    for kid in sorted(sentence_dict.keys()):
        print(kid, sentence_dict[kid])
    print(matrix_dict['d_c'].shape)
    print(matrix_dict['c_c'].shape)
    print(matrix_dict['c_p'].shape)
    print(matrix_dict['p_s'].shape)
    print(matrix_dict['s_k'].shape)

# the following codes are for showing how the matrix_dict is defined:
##    matrix_dict['section_vec']= section_vec
##    matrix_dict['paragraph_father']= paragraph_father
##    matrix_dict['paragraph_vec']= paragraph_vec
##    matrix_dict['sentence_vec']= sentence_vec
##    matrix_dict['sentence_vec_father']= sentence_vec_father
##    matrix_dict['d_c']= d_c
##    matrix_dict['c_c']= c_c
##    matrix_dict['c_p']= c_p
##    matrix_dict['p_s']= p_s
##    matrix_dict['s_k']= s_k
##    matrix_dict['sentence_dict']=sentence_dict
##    matrix_dict['word']=sentence_tfidf.word
##    matrix_dict['id']=graphname

def LoadExtractJsonFiles():
#    fdir = './test/multipaper/papers_json'
    fnamelist = sxpReadFileMan.GetDirFileListType(fdir,'json')
#    pkdir = './test/multipaper/papers_pk'
    for i, each in enumerate( fnamelist):
        print('******', i)
        print(each)
        jstr = sxpReadFileMan.ReadTextUTF(each)
        if jstr is None:
            print('wrong in open')
            break
        us = sxpTextEncode.GetUnicode(jstr)
        jsdict = json.loads(us,encoding='utf-8')
#        print(jsdict)
        pkname = os.path.join(pkdir, 'p_{0:0>4}.pk'.format(i))
        json_dict ={}
        json_dict['fname']=each
        json_dict['id'] =  '{0:0>4}'.format(i)
        json_dict['title']=jsdict['title']
        json_dict['jsdict'] = jsdict
        sxpReadFileMan.StoreSxptext(json_dict,pkname)
def ParsePaperJson(jsdict,fid,graph_dir):
    title = jsdict['title']
    refid = jsdict['number']
    content_body = jsdict['content']
    node_dict = []
    root = sxpNode('root')
    root.node_title = "root"

    jsdict['kind']='Chapter'
    graph_root = ParseTree(jsdict,root)
    graphname =fid +'.graph'
 #   graph_dict = MakeGraph(graph_root,graphname,graph_dir)\
    graph_dict,matrix_dict,sentence_data_dict = MakeSubGraph(graph_root,graphname,graph_dir)
    graph_dict['title']=title
    matrix_dict['title']=title
    fdictname =  os.path.join(graph_dir, graphname+'.grah_dict')
    StoreSxptext(graph_dict,fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.matrix_vec_dict')
    StoreSxptext(matrix_dict,fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.sentence_data_dict')
    StoreSxptext(sentence_data_dict,fdictname)
    return graph_dict, matrix_dict,sentence_data_dict
def LoadFileData(fid):
    graphname =fid +'.graph'
    fdictname =  os.path.join(graph_dir, graphname+'.grah_dict')
    graph_dict = LoadSxptext(fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.matrix_vec_dict')
    matrix_dict = LoadSxptext(fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.sentence_data_dict')
    sentence_data_dict=LoadSxptext(fdictname)
    return graph_dict, matrix_dict,sentence_data_dict
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def makelabel(fullstr, labellen=10):
    nlen=len(fullstr)

    if nlen < labellen:
        return fullstr
    else:
        return fullstr[0:labellen]


def MakeGraph(graph_root, graphname, graph_dir):
    node_dict = {}
    node_stack = collections.deque([])
    node_stack.appendleft(graph_root)
    sxpgraph = sxpGraphEngine.sxpNetwork(graph_dir, graphname)
    node_name = 'root'
    node_label = makelabel(graph_root.node_title)
    rid = sxpgraph.AddNode(node_name, node_label, nodetype='root')
    node_dict = {}
    node_dict[rid] = graph_root
    sentence_dict = {}
    sentence_doc =[]
    while(len(node_stack)>0):
        cnd = node_stack.pop()
        for eachpara in cnd.node_text:
            node_name = 'para'
            node_label = makelabel(eachpara.node_title,30)
            nid = sxpgraph.AddNode(node_name, node_label, nodetype='para')
            node_dict[nid]=eachpara
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            print(eachpara.node_title)
            for eachsent in sentenceset:
                node_name = 'sentence'
                node_label = makelabel(eachsent, 30)
                sid = sxpgraph.AddNode(node_name, node_label,
                                       nodetype='sentence')
                sentnode = sxpNode('sentence')
                sentnode.node_title = eachsent
                node_dict[sid] = sentnode
                sentence_dict[sid] = eachsent
                sxpgraph.AddEdgeByID(nid, sid, edgename='contain')
                sentence_doc.append(eachsent)

        for eachsub in cnd.node_child:
            node_name = 'sub'
            node_label = makelabel(eachsub.node_title)
            nid = sxpgraph.AddNode(node_name, node_label, nodetype='section')
            node_dict[nid]=eachsub
            sxpgraph.AddEdgeByID(rid, nid, edgename='contain')

            node_stack.appendleft(eachsub)
    #one paper document has one word vector
    sxptfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentenceset)
    sxpgraph.Save()
    graph_dict = {}
    graph_dict['node_dict']=node_dict
    graph_dict['sentence_tfidf']=sxptfidf
    graph_dict['sxpgraph']=sxpgraph
    graph_dict['id']=graphname
    graph_dict['sentence_dict']= sentence_dict
    fdictname =  os.path.join(graph_dir, graphname+'.grah_dict')

    sxpReadFileMan.StoreSxptext(graph_dict,fdictname)

    return graph_dict

def GetSentence(graph_root,gid,graphname, graph_dir):
    node_dict = {}
    node_stack =collections.deque([])
    node_stack.appendleft((graph_root,0))
    sxpgraph = sxpGraphEngine.sxpNetwork(graph_dir, graphname)
    node_name = 'root'
    node_label = makelabel(graph_root.node_title)
    graph_root.node_id=0
    rid = sxpgraph.AddNode(node_name,node_label,nodetype='root')
    node_dict = {}
    node_dict[rid]=graph_root
    sentence_dict = {}
    sentence_doc =[]
    section_vec=[]
    section_father_vec=[]
    paragraph_vec=[]
    paragraph_father=[]
    sentence_vec =[]
    sentence_vec_father=[]
    word_vec=[]
    secid = 0
    paraid =0
    sentenceid=0
    current_secid=0
    abstract =[]
    conclusion =[]
    acknolwedge = []
    reference = []
    while(len(node_stack)>0):
        (cnd,current_secid) = node_stack.pop()
        rid = cnd.node_id

        for eachpara in cnd.node_text:
            node_name = 'para'
            node_label = makelabel(eachpara.node_title,30)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='para')
            eachpara.node_id = nid
            sentence_para_id =str(paraid)
            paragraph_vec.append(nid)
            paraid = paraid + 1
            paragraph_father.append(current_secid)
            node_dict[nid]=eachpara
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            for i, eachsent in enumerate( sentenceset):
                sentence_idstr = str(gid) + '.'+sentence_para_id + '.' + str(i)
                node_name = 'sentence'
                node_label = makelabel(eachsent,30)
                sid = sxpgraph.AddNode(node_name,node_label,nodetype='sentence')
                sentnode=sxpNode('sentence')
                sentnode.node_id=sid
                sentnode.node_title=eachsent
                node_dict[sid]=sentnode
                sentence_dict[sentence_idstr]=(sid,eachsent)
                sxpgraph.AddEdgeByID(nid,sid,edgename='contain')
                sentence_doc.append(eachsent)
                sentence_vec.append(sid)
                sentenceid = sentenceid +1
                sentence_vec_father.append(paraid-1)
        for eachsub in cnd.node_child:
            node_name = 'sub'
            node_label = makelabel(eachsub.node_title)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
            eachsub.node_id=nid
            node_dict[nid]=eachsub
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            section_vec.append(rid)
            section_father_vec.append(current_secid)
            node_stack.appendleft((eachsub,secid))
            secid=secid+1
    return sentence_dict
def GetSentenceFromNodeList(graph_root_list,graphname, graph_dir):
    all_sent = {}
    for i, graph_root in enumerate( graph_root_list):
        sent_dict = GetSentence(graph_root,i,graph_dir,graphname)
        for sid,sent in sent_dict.items():
            all_sent[sid]=sent
    allsentlist=[]
    for sid in sorted(all_sent.keys()):
     allsentlist.append(all_sent[sid])
    return allsentlist

def MakeSubGraph(graph_root, graphname, graph_dir):
    node_dict = {}
    node_stack =collections.deque([])
    node_stack.appendleft((graph_root,0))
    sxpgraph = sxpGraphEngine.sxpNetwork(graph_dir, graphname)
    node_name = 'root'
    node_label = makelabel(graph_root.node_title)
    graph_root.node_id=0
    rid = sxpgraph.AddNode(node_name,node_label,nodetype='root')
    node_dict = {}
    node_dict[rid]=graph_root
    sentence_dict = {}
    sentence_doc =[]
    section_vec=[]
    section_father_vec=[]
    paragraph_vec=[]
    paragraph_father=[]
    sentence_vec =[]
    sentence_vec_father=[]
    word_vec=[]
    secid = 0
    paraid =0
    sentenceid=0
    current_secid=0
    abstract =[]
    conclusion =[]
    acknowledge = []
    reference = []
    while(len(node_stack)>0):
        (cnd,current_secid) = node_stack.pop()
        rid = cnd.node_id

        for eachpara in cnd.node_text:
            node_name = 'para'
            node_label = makelabel(eachpara.node_title,30)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='para')
            eachpara.node_id = nid
            sentence_para_id =str(paraid)
            paragraph_vec.append(nid)
            paraid = paraid + 1
            paragraph_father.append(current_secid)
            node_dict[nid]=eachpara
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            for i, eachsent in enumerate( sentenceset):
                sentence_idstr = sentence_para_id + '.' + str(i)
                node_name = 'sentence'
                node_label = makelabel(eachsent,30)
                sid = sxpgraph.AddNode(node_name,node_label,nodetype='sentence')
                sentnode=sxpNode('sentence')
                sentnode.node_id=sid
                sentnode.node_title=eachsent
                node_dict[sid]=sentnode
                sentence_dict[sentence_idstr]=(sid,eachsent)
                sxpgraph.AddEdgeByID(nid,sid,edgename='contain')
                sentence_doc.append(eachsent)
                sentence_vec.append(sid)
                sentenceid = sentenceid +1
                sentence_vec_father.append(paraid-1)
        for eachsub in cnd.node_child:
            node_name = 'sub'
            node_label = makelabel(eachsub.node_title)
            print('section title:**********', node_label)
            if sxpExtractText.isabstract( eachsub.node_title):
                abstract.append(eachsub)
                nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
                eachsub.node_id=nid
                node_dict[nid]=eachsub
                sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
                section_vec.append(rid)
                section_father_vec.append(current_secid)
                node_stack.appendleft((eachsub,secid))
                secid=secid+1
            elif sxpExtractText.isreference( eachsub.node_title):
                reference.append(eachsub)
            elif sxpExtractText.isconclusion( eachsub.node_title):
                conclusion.append(eachsub)
                nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
                eachsub.node_id=nid
                node_dict[nid]=eachsub
                sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
                section_vec.append(rid)
                section_father_vec.append(current_secid)
                node_stack.appendleft((eachsub,secid))
                secid=secid+1
            elif sxpExtractText.isacknolwedge( eachsub.node_title):
                acknowledge.append(eachsub)
            else:
                nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
                eachsub.node_id=nid
                node_dict[nid]=eachsub
                sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
                section_vec.append(rid)
                section_father_vec.append(current_secid)
                node_stack.appendleft((eachsub,secid))
                secid=secid+1

    sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentence_doc)

    if len(abstract)==0:
        print("abstract is zeror*******",graphname)
    if len(abstract)==0:
        print("conclusion is zeror*******",graphname)
    sentence_data_dict = {}
    sentence_data_dict['abstract']=GetSentenceFromNodeList(abstract,graphname, graph_dir)
    sentence_data_dict['reference']=GetSentenceFromNodeList(reference,graphname, graph_dir)
    sentence_data_dict['conclusion']=GetSentenceFromNodeList(conclusion,graphname, graph_dir)
    sentence_data_dict['acknowledge']=GetSentenceFromNodeList(acknowledge,graphname, graph_dir)
    sentence_data_dict['sentence_dict']=sentence_dict
##    print abstract
##    test = True
##    if test == True:
##        return
#***************************************************************
    print('we begin to build matrix')

    cs = len(section_vec)
    ps = len(paragraph_vec)
    ss = len(sentence_vec)
    ks = len(sentence_tfidf.word)
    print('cs,ps,ss,ks:',cs,ps,ss,ks)
#first we build d-c matrix, which is actually a row vector
    print('d_c matrix')
    d_c = csr_matrix(np.ones((1,cs), dtype=np.float))

    print('building c_c matrix')
    c_c = csr_matrix((cs,cs), dtype=float)
    for i, secid in enumerate( section_vec):
        f=section_father_vec[i]
        c_c[f,i]=1.0
    print('building c_p matrix')
    c_p = csr_matrix((cs,ps), dtype=float)
    for i, paraid in enumerate( paragraph_vec):
        f=paragraph_father[i]
        c_p[f,i]=1.0
    print('building p_s matrix')
    p_s = csr_matrix((ps,ss), dtype=float)
    for i, sentid in enumerate( sentence_vec):
        f=sentence_vec_father[i]
        p_s[f,i]=1.0

    print('building s_w matrix')
    s_k = csr_matrix((ss,ks), dtype=float)

    for i, sentid in enumerate( sentence_vec):
        sxpnode = node_dict[sentid]
        if sxpnode.notde_type == 'sentence':
          vec = sentence_tfidf.vectorizer.transform([sxpnode.node_title])
          r,c = vec.shape
          for j in range(c):
             if vec[0,j]>0:
              s_k[i,j]=1


    print('save graph dict')
  #  sxpgraph.Save()
    graph_dict = {}
    graph_dict['node_dict']=node_dict
    graph_dict['sentence_tfidf']=sentence_tfidf
    graph_dict['sxpgraph']=sxpgraph
    graph_dict['id']=graphname
    graph_dict['sentence_dict']= sentence_dict
    matrix_dict={}
    print('save matrix dict')
    matrix_dict['section_vec']= section_vec
    matrix_dict['paragraph_father']= paragraph_father
    matrix_dict['paragraph_vec']= paragraph_vec
    matrix_dict['sentence_vec']= sentence_vec
    matrix_dict['sentence_vec_father']= sentence_vec_father
    matrix_dict['d_c']= d_c
    matrix_dict['c_c']= c_c
    matrix_dict['c_p']= c_p
    matrix_dict['p_s']= p_s
    matrix_dict['s_k']= s_k

    matrix_dict['word']=sentence_tfidf.word
    matrix_dict['id']=graphname

    return graph_dict,matrix_dict,sentence_data_dict

def ParseTree(jsdict,root):
    subnodes = []
    subnd = None
    txt_id =0
    if jsdict['kind'] == 'Chapter':
        if 'title' in jsdict.keys():
            title = jsdict['title']
            subnd = sxpNode('Chapter')
            subnd.node_title=title
            root.AddSubNode(subnd)
        #    print('find sub node',title)
        if 'content' in jsdict.keys():
            subnodes.append(jsdict['content'])
    if jsdict['kind']=='Paragraph':
        if 'content' in jsdict.keys():
            txt = jsdict['content']
            txtnd = sxpNode('Paragraph')
            txtnd.node_title=txt
            txtnd.node_idx = txt_id
            txt_id = txt_id +1
            root.AddSubText(txtnd)
       #     print('find paragraph',txt)
    if len(subnodes)==1:
       content_body= subnodes[0]
       for eachdict in content_body:
        ParseTree(eachdict,subnd)
    return root

if __name__ == '__main__':
    main()
