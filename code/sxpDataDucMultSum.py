#-------------------------------------------------------------------------------
# Name:        sxpDataDucMultSum.py
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

import sxpParseDUCText

from graphengine import sxpGraphEngine

import win32file
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

paperpath = './test/duc2002mult/papers'
fdir = './test/duc2002mult'
pkdir = r'./test/duc2002mult/papers_pk'
multipkdir =r'./test/duc2002mult/mult_papers_pk'
graph_dir =   './test/duc2002mult/papers_graph'
data_dir =r'./test/duc2002mult'

model_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEmodels\SEE.edited.abstracts.in.edus"
rawtxt_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocs\docs"
rawsent_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocswithsentences\docs.with.sentence.breaks"
##single_model_src = r'./test/duc2002/single_model_src'
##single_raw_src = r'./test/duc2002/single_raw_src'
##single_raw_sent_src =r'./test/duc2002/single_raw_sent_src'

mult_model_src = r'./test/duc2002/mult_model_src'
mult_raw_src = r'./test/duc2002/mult_raw_src'
mult_raw_sent_src =r'./test/duc2002/mult_raw_sent_src'
sxpReadFileMan.CheckMkDir(mult_model_src)
sxpReadFileMan.CheckMkDir(mult_raw_src)
sxpReadFileMan.CheckMkDir(mult_raw_sent_src)

sxpReadFileMan.CheckMkDir(fdir)
sxpReadFileMan.CheckMkDir(paperpath)
sxpReadFileMan.CheckMkDir(multipkdir)
sxpReadFileMan.CheckMkDir(graph_dir)

def main():
    cmdlist = ['MakeManuSys',
               'PrepareModelRaw',
               'PrepareSrcRaw',
               "LoadRawPkByDocId",
               'LoadMultiModelSentByPat',
               'LoadRawPkByDocId',
               'BuildGraph'
    ]
    if 'MakeManuSys' in cmdlist:
        MakeManuSys()
    if 'PrepareModelRaw' in cmdlist in cmdlist:#ok
        PrepareModelRaw()
    if 'PrepareSrcRaw'in cmdlist in cmdlist:#ok
        PrepareSrcRaw()

    if 'LoadMultiModelSentByPat' in cmdlist:#ok
      #  print(LoadDocModelSentence())
       md= LoadMultiModelSentByPat()
       for each in md:
        print(each)
    if 'LoadRawPkByDocId' in cmdlist:
        docid ='D083A'
        sxplist =LoadRawPkByDocId(docid)
        print(sxplist)

    if 'BuildGraph' in cmdlist:#ok
        BuildGraph()

duc2002format ='''
Document set number (Dnnn)
|    Summary type (M = multi-doc, P= single-doc)
|    | Base TREC document id
|    | |               Summary target size (10,50,100,200)
|    | |               |    Peer size (whitespace-delimited tokens)
|    | |               |    |  Document selector code (A-J)
|    | |               |    |  |
|    | |               |    |  |   Model summarizer code (A-J)
|    | |               |    |  |   | Assessor code (A-C,E-J)
|    | |               |    |  |   | |  Peer summarizer code (baseline[1-3], manual[A-J]submission, or system submission[15-31])
'''
modelfileformat = '''
D061.P.100.J.I.AP880911-0016.html
document set: D061, Summary Type,P for single-doc, 100: target size:, J Document Selector code, Modlel Summarizer code : I,
AP880911-0016 will ref to only one raw txt which is now in our sub:single_raw_src = r'./test/duc2002/single_raw_src'
For one raw txt:
    there are four models: which is in different group of doc with different document selecter and model summarizer
Note that one same raw txt can occur in two different groups for multi-doc summarization. For example,
AP880911-0016 is in d079a and in d061j, two sub directorys, and in each sub directory, two models are given as a single doc evaluation.
Thus, there are four such single document model for AP880911-0016:
    D061.P.100.J.I.AP880911-0016.html
'''

def PrepareModelRaw():
    model_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEmodels\SEE.edited.abstracts.in.edus"
    rawtxt_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents/DUC2002_Summarization_Documents/duc2002testdocs/docs"
    single_model_src = r'./test/duc2002/single_model_src'
    single_raw_src = r'./test/duc2002/single_raw_src'
    flist = sxpReadFileMan.GetDirFileList(model_src)
  #  pat = '(D\d+)\.P\.(\d+)\.(\w)\.(\w)\.([\w\d-]+)\.html'
    pat = '(D\d+)\.M\.(\d+)\.(\w)\.(\w)\.html'
    pt = re.compile(pat)
    cmd = 'makemodel'
    j = 1
    doc_model_dict ={}
    for i, each in enumerate(flist):
        g= pt.match(each)
        if g:
            print(j)
            j = j + 1
            print(g.groups())
            if cmd == 'makemodel':

                modelsrctrg = os.path.join(model_src,each)
                print(modelsrctrg)

                subdir = g.groups()[0]+g.groups()[2]
            #    docid = subdir+'.'+g.groups()[1] #note that here doci id has len of model summary
                docid = subdir
                sent_list = sxpParseDUCText.ParseModelFile(modelsrctrg)
                print(modelsrctrg)
                print((len(sent_list)))
                model_info = {}
                model_info['fid']=docid+'.'+g.groups()[1]
                model_info['subdir']=subdir
                model_info['len']=g.groups()[1]
                model_info['file_name']=each
                model_info['sent_list']=sent_list
                if docid in doc_model_dict:
                    model_list = doc_model_dict[docid]
                else:
                    model_list = []
                model_list.append(model_info)
                doc_model_dict[docid]=model_list
    doc_model_dict_fname= graph_dir +'\\'+'doc_model_dict.dict'
    sxpReadFileMan.SaveObject(doc_model_dict,doc_model_dict_fname)
    print((len(doc_model_dict)))
    return doc_model_dict
def PrepareSrcRaw():
    model_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEmodels\SEE.edited.abstracts.in.edus"
    rawtxt_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents/DUC2002_Summarization_Documents/duc2002testdocs/docs"
  #  rawtxt_sent_src = r'E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocswithsentences\docs.with.sentence.breaks'
    rawtxt_sent_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocswithsentences\docs.with.sentence.breaks"
    doc_model_dict_fname= graph_dir +'/'+'doc_model_dict.dict'
    doc_model_dict=sxpReadFileMan.LoadObject(doc_model_dict_fname)
    model_raw_src_dict ={}
    for docid,model_info in list(doc_model_dict.items()):
        rawsub = rawtxt_sent_src + '\\' + docid
        rawfnamelist = sxpReadFileMan.GetDirFileList(rawsub)
        rawlists =[]
        for eachf in rawfnamelist:
            fname = rawsub + '\\' + eachf
            print(fname)
##            sxpReadFileMan.ReadTextUTF(fname)
            sxptxt = sxpParseDUCText.ParseFromSentRawSrc(fname)
            rawdict = {}
            rawdict['file_name']=eachf
            rawdict['sxptxt']=sxptxt
            rawlists.append(rawdict)
        model_raw_src_dict[docid]=rawlists
        pkfname = multipkdir + r'/' + docid +'.pk'
        sxpReadFileMan.SaveObject(model_raw_src_dict,pkfname)
    model_raw_src_dict_fname= graph_dir +'/'+'model_raw_src_dict.dict'
    sxpReadFileMan.SaveObject(model_raw_src_dict,model_raw_src_dict_fname)
#'(D\d+)\.M\.(\d+)\.(\w)\.(\w)\.html'

def LoadDocAllSent():
    doc_all_doc_sent_list_name= graph_dir +'\\'+'doc_all_doc_sent_list.dict'
    return sxpReadFileMan.LoadObject(doc_all_doc_sent_list_name)
def LoadMultiModelSentByPat(model_file_pat='(D\d+)\.M\.(\d+)\.(\w)\.(\w)\.html'):
    doc_model_dict_fname= graph_dir +'\\'+'doc_model_dict.dict'
    doc_model_dict=sxpReadFileMan.LoadObject(doc_model_dict_fname)
    doc_model_sent_list = []
    i = 0
    for docid, model_list in list(doc_model_dict.items()):
        md_list =[]
        model_len =[]
        for model_info in model_list:
##            model_len.append(model_info['len'])
##            md_list.append((model_info,model_info['sent_list']))
            file_name = model_info['file_name']
            print(file_name)
            if re.findall(model_file_pat,file_name):
                model_len.append(model_info['len'])
                md_list.append((model_info,model_info['sent_list']))
        doc_dict = {}
        doc_dict['model']=md_list
        doc_dict['title']=docid
        doc_dict['fid']=docid
        doc_dict['model_len']=model_len
        doc_dict['model_idx']=docid#'{0:0>4}'.format(i)
        i = i + 1
        doc_model_sent_list.append(doc_dict)
    doc_model_sent_list_name =  graph_dir +'\\'+'doc_model_sent_list.list'
    sxpReadFileMan.SaveObject(doc_model_sent_list,doc_model_sent_list_name)
    return doc_model_sent_list


def LoadMultiModelSentByLen(model_len='all'):
    if model_len =='all':
        return LoadMultiModelSentByPat()
    model_file_pat='(D\d+)\.M\.({0})\.(\w)\.(\w)\.html' %(model_len)
    return LoadMultiModelSentByPat(model_file_pat)

def MakeManuSys():
    manualpeers_dir = r'E:\pythonworknew\code\textsum\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEpeers\manualpeers\SEE.abstracts.in.sentences'
    manualpeers_list = sxpReadFileMan.GetDirFileList(manualpeers_dir)
    manualpeer={}
    for each in manualpeers_list:
        pat = r'(D\d\d\d).M.(\d\d\d).([A-Z]).([A-Z]).html' #D061.M.010.J.I.html
        g = re.match(pat,each)
        fullname= manualpeers_dir + '\\'+each
        if g:
            fid = g.groups()[0]
            lenstr = g.groups()[1]
            gid = g.groups()[2]
            sid = g.groups()[3]
            docid = fid +gid
            manualsys = {}
            manualsys['fid']=fid
            manualsys['lenstr']=lenstr
            manualsys['gid']=gid
            manualsys['sid']=sid #different
            manualsys['docid']=docid
           # manualsys['txt']=sxpReadFileMan.ReadTextUTF(fullname)
            manualsys['sent']=sxpParseDUCText.ParseModelFile(fullname)
            if docid in manualpeer:
                peers = manualpeer[docid]
                peers.append(manualsys)
                manualpeer[docid]=peers
            else:
                peers = []
                peers.append(manualsys)
                manualpeer[docid]=peers

    fname = graph_dir +'//' + 'manualpeer.dict'
    sxpReadFileMan.SaveObject(manualpeer,fname)
fname = graph_dir +'//' + 'manualpeer.dict'
manualpeer =sxpReadFileMan.LoadObject(fname)
def LoadManualSys(docid,lenstr='100',peeridx=0):
    peers= manualpeer[docid]
    mat =[]
    for each in peers:
        if lenstr == each['lenstr']:
            mat.append(each)
    cand = mat[peeridx]
    return cand['sent']

def LoadRawPkByDocId(docid):
    pkfname=multipkdir + r'/' + docid +'.pk'
    return sxpReadFileMan.LoadObject(pkfname)

def BuildGraph():
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir =   r'./test/multipaper/papers_graph'
#    data_dir =r'./test/multipaper'
    rawtxt_sent_src = r"E:\pythonworknew\code\textsum\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocswithsentences\docs.with.sentence.breaks"
    doc_model_sent_list_name =  graph_dir +'\\'+'doc_model_sent_list.list'
    doc_model_sent_list= sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    pkname_list_name = graph_dir +'\\'+'pkname_list.list'
    pkname_list = []
    for eachmodel in doc_model_sent_list:
        fid = eachmodel['fid']
        model_idx = eachmodel['model_idx']
        rawsub = rawtxt_sent_src + '\\' + fid
        rawfnamelist = sxpReadFileMan.GetDirFileList(rawsub)
        sxptxtlist =[]
        for eachf in rawfnamelist:
            fname = rawsub + r'/' + eachf
            print(fname)
##            sxpReadFileMan.ReadTextUTF(fname)
            sxptxt = sxpParseDUCText.ParseFromSentRawSrc(fname)
            sxptxtlist.append(sxptxt)

##        txt = sxpReadFileMan.ReadTextUTF(rawsrcfname)
        pkname = multipkdir + '\\' + model_idx + '.pk'
##        sxpReadFileMan.SaveObject(sxptxt,pkname)
        print((sxptxt.sentence_textset))
        pk_dict = {}
        pk_dict['fid']=fid
        pk_dict['model_idx']=model_idx
        pk_dict['pkname']=pkname
        pk_dict['sxptxt']=sxptxtlist
        pk_dict['rawname']=rawsub
        pkname_list.append(pk_dict)
        sxpReadFileMan.SaveObject(sxptxtlist,pkname)
    sxpReadFileMan.SaveObject(pkname_list,pkname_list_name)

def LoadMultDucData(graph_dict_fid,test_case):
    fpname = multipkdir + '\\' + graph_dict_fid
    sxptxt = sxpReadFileMan.LoadObject(fpname)
    return sxptxt
#win32file.CopyFile(sf,mfname, 0)

def Work():
 #   LoadExtractJsonFiles()
 #   pkdir = r'./test/multipaper/papers_pk'
 #   ShowTitle(pkdir)
  #  TestProcessOne()
    BuildGraph()
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
        title= graph_dict['title']
        print((fid,title))
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
        title= graph_dict['title']
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


def LoadDocModelSentence(model_len='all'):
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir = r'./test/multipaper/papers_graph'
#    data_dir = r'./test/multipaper'
    return LoadMultiModelSentByLen(model_len)

def GetFileNameDictList():
    fname = fdir +'/fdict_list.dict'
    fdict_list=sxpReadFileMan.LoadObject(fname)
    return fdict_list

def LoadFile(fname):
    if not os.path.exists(fname):
        print('file does not exists',fname)
        return ''
    f = open(fname,'r')
    txtc = f.read()
    f.close();
    tstr = sxpTestStringEncode.strencode(txtc,'utf-8')
    return tstr


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
    patstr = ',|\.\s|\:|\?|，|。|：|？|！|；'
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
    patstr = 'abstract|conclusion'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def IsConclusion(strtitle):
    patstr = 'conclusion'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def IsAbstract(strtitle):
    patstr = 'abstract'
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


if __name__ == '__main__':
    main()
