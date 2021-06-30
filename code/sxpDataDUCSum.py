#-------------------------------------------------------------------------------
# Name:        sxpDataDUCSum.py
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

paperpath = './test/duc2002single/papers'
fdir = './test/duc2002single'
pkdir = r'./test/duc2002single/papers_pk'
singlepkdir =r'./test/duc2002single/single_papers_pk'
singlepkdir_sub = r'./test/duc2002single/singlesub_papers_pk'
graph_dir =   './test/duc2002single/single_papers_graph'
data_dir =r'./test/duc2002single'
sxpReadFileMan.CheckMkDir(pkdir)
sxpReadFileMan.CheckMkDir(singlepkdir)
sxpReadFileMan.CheckMkDir(singlepkdir_sub)
sxpReadFileMan.CheckMkDir(graph_dir)
sxpReadFileMan.CheckMkDir(data_dir)

model_src = r"E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEmodels\SEE.edited.abstracts.in.edus"
rawtxt_src = r"E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocs\docs"
rawsent_src = r"E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\DUC2002_Summarization_Documents\DUC2002_Summarization_Documents\duc2002testdocswithsentences\docs.with.sentence.breaks"
single_model_src = r'./test/duc2002/single_model_src'
single_raw_src = r'./test/duc2002/single_raw_src'
single_raw_sent_src =r'./test/duc2002/single_raw_sent_src'
sxpReadFileMan.CheckMkDir(fdir)
sxpReadFileMan.CheckMkDir(paperpath)

sxpReadFileMan.CheckMkDir(graph_dir)

def main():
    cmd = 'BuildGraph'
    if cmd == 'MakeSubmitSys':
        MakeSubmitSingleSys('27')
     #   LoadAllSubmitSys('29')
        LoadOneSubmitSys('27','AP880217-0100')
    if cmd == 'MakeManuSys':
        MakeManuSys()
        s =LoadManualSys('AP880512-0157')
        for each in s:
            print(each)
    if cmd == "MakeFileList":
        MakeFileList(usesub=True)
    if cmd =='PrepareSingleSrcSent':
        PrepareSingleSrc()
        PrepareSingleSrcSent()
    if cmd == 'MakeSingleSrcModelPair':
        #PrepareSingleSrc()
        MakeSingleSrcModelPair()

    if cmd =='LoadDocModelSentence':
      #  print(LoadDocModelSentence())
       md= LoadDocModelSentence()
       for each in md:
        print(each)

    if cmd == 'BuildGraph':
        BuildGraph(usesub=True)
    if cmd == 'GetSentenceListFromFID':
        fid = 'LA112790-0154'
        s = GetSentenceListFromFID(fid)
        for eachs in s:
            print(eachs)
        sxptxt = ParseOneDucFID(fid)
        print(sxptxt.sentenceset)
    if cmd =='TestParseOne':
        TestParseOne()
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
def PrepareSingleSrc():
    flist = sxpReadFileMan.GetDirFileList(model_src)
    pat = '(D\d+)\.P\.(\d+)\.(\w)\.(\w)\.([\w\d-]+)\.html'
    pt = re.compile(pat)
    cmd = 'makeraw'
    j = 1
    for i, each in enumerate(flist):
        g= pt.match(each)
        if g:
            print(j)
            j = j + 1
            print(g.groups())
            if cmd == 'makemodel':
                modelsrcfname = os.path.join(model_src,each)
                print(modelsrcfname)
                modelsrctrg = os.path.join(single_model_src,each)
                print(modelsrctrg)
                win32file.CopyFile(modelsrcfname,modelsrctrg, 0)
            if cmd == 'makeraw':
                subdir = g.groups()[0]+g.groups()[2]
                txtname =g.groups()[4]
                fulltxtname = rawtxt_src+'/'+subdir +'/' + txtname
                txtfullnametrg =single_raw_src+'/'+txtname
                print(fulltxtname)
                print(txtfullnametrg)
                win32file.CopyFile(fulltxtname,txtfullnametrg, 0)
                print(fulltxtname)
def PrepareSingleSrcSent():
    flist = sxpReadFileMan.GetDirFileList(model_src)
    pat = '(D\d+)\.P\.(\d+)\.(\w)\.(\w)\.([\w\d-]+)\.html'
    pt = re.compile(pat)
    cmd = 'makeraw'
    j = 1
    for i, each in enumerate(flist):
        g= pt.match(each)
        if g:
            print(j)
            j = j + 1
            print(g.groups())

            if cmd == 'makeraw':
                subdir = g.groups()[0]+g.groups()[2]
                txtname =g.groups()[4]
                fulltxtname = rawsent_src+'/'+subdir +'/' + txtname +'.S'
                txtfullnametrg =single_raw_sent_src+'/'+txtname
                print(fulltxtname)
                print(txtfullnametrg)
                win32file.CopyFile(fulltxtname,txtfullnametrg, 0)
                print(fulltxtname)
def GetSentenceListFromFID(fid):
    fname = single_raw_sent_src+'/'+fid
    return sxpParseDUCText.GetSentListFromSentRawSrc(fname)
def ParseOneDucFID(fid,usesub=False):
    fname = single_raw_sent_src+'/'+fid
    return sxpParseDUCText.ParseSentSxptxt(fname,usesub)
 #   return sxpParseDUCText.ParseFromSentRawSrc(fname)
def MakeSingleSrcModelPair():
    model_src = r"E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEmodels\SEE.edited.abstracts.in.edus"
    rawtxt_src = r"E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\DUC2002_Summarization_Documents/DUC2002_Summarization_Documents/duc2002testdocs/docs"
    single_model_src = r'./test/duc2002/single_model_src'
    single_raw_src = r'./test/duc2002/single_raw_src'
    flist = sxpReadFileMan.GetDirFileList(model_src)
    pat = '(D\d+)\.P\.(\d+)\.(\w)\.(\w)\.([\w\d-]+)\.html'
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
                docid = g.groups()[4]
                subdir = g.groups()[0]+g.groups()[2]
                sent_list = sxpParseDUCText.ParseModelFile(modelsrctrg)
                print(modelsrctrg)
                print((len(sent_list)))
                model_info = {}
                model_info['fid']=docid
                model_info['subdir']=subdir
                model_info['file_name']=modelsrctrg
                model_info['sent_list']=sent_list
                model_info['docidx']='{0:0>4}'.format(i)
                model_info['modelidx']='{0:0>4}'.format(j)
                if docid in doc_model_dict:
                    model_list = doc_model_dict[docid]
                else:
                    model_list = []
                model_list.append(model_info)
                doc_model_dict[docid]=model_list
    doc_model_dict_fname= graph_dir +'/'+'doc_model_dict.dict'
    sxpReadFileMan.SaveObject(doc_model_dict,doc_model_dict_fname)
    print((len(doc_model_dict)))
    return doc_model_dict

def LoadSingleModelSent():
    doc_model_dict_fname= graph_dir +'/'+'doc_model_dict.dict'
    doc_model_dict=sxpReadFileMan.LoadObject(doc_model_dict_fname)
    doc_model_sent_list = []
    i = 0
    for docid, model_list in list(doc_model_dict.items()):
        md_list =[]
        for model_info in model_list:
            md_list.append(model_info['sent_list'])
        doc_dict = {}
        doc_dict['model']=md_list
        doc_dict['title']=docid
        doc_dict['fid']=docid
        doc_dict['model_idx']='{0:0>4}'.format(i)
        i = i + 1
        doc_model_sent_list.append(doc_dict)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    sxpReadFileMan.SaveObject(doc_model_sent_list,doc_model_sent_list_name)
    return doc_model_sent_list
def GetModelText(fid):
    doc_model_dict_fname= graph_dir +'/'+'doc_model_dict.dict'
    doc_model_dict=sxpReadFileMan.LoadObject(doc_model_dict_fname)
    doc_model_sent_list = []
    i = 0
    for docid, model_list in list(doc_model_dict.items()):
        if docid == fid:
            return model_list
    return []
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
def BuildGraph(usesub=False):
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir =   r'./test/multipaper/papers_graph'
#    data_dir =r'./test/multipaper'
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list= sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    pkname_list_name = graph_dir +'/'+'pkname_list.list'
    pkname_list = []
    for eachmodel in doc_model_sent_list:
        fid = eachmodel['fid']
        model_idx = eachmodel['model_idx']
        rawsrcfname = single_raw_src + '//' + fid

        print((rawsrcfname,fid,model_idx))
##        txt = sxpReadFileMan.ReadTextUTF(rawsrcfname)
    #    pkname = singlepkdir + '//' + model_idx + '.pk'
        if usesub==False:
            pkname = singlepkdir + '//' + fid + '.pk'
        else:
            pkname = singlepkdir_sub+ '//' + fid + '.pk'
##        sxpReadFileMan.SaveObject(sxptxt,pkname)
        sxptxt = ParseOneDucFID(fid,usesub)
        print((sxptxt.sentence_textset))
        pk_dict = {}
        pk_dict['fid']=fid
        pk_dict['model_idx']=model_idx
        pk_dict['pkname']=pkname
        pk_dict['sxptxt']=sxptxt
        pk_dict['rawname']=rawsrcfname
        pkname_list.append(pk_dict)
        sxpReadFileMan.SaveObject(sxptxt,pkname)
    sxpReadFileMan.SaveObject(pkname_list,pkname_list_name)

def MakeManuSys():
    manualpeers_dir = r'E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEpeers\manualpeers\SEE.abstracts.in.sentences'
    manualpeers_list = sxpReadFileMan.GetDirFileList(manualpeers_dir)
    manualpeer={}
    for each in manualpeers_list:
        pat = r'(D\d\d\d).M.(\d\d\d).([A-Z]).([A-Z]).html' #D061.M.010.J.I.html
        pat = r'(D\d\d\d).P.(\d\d\d).([A-Z]).([A-Z]).([A-Za-z0-9\-]+).html' #D061.P.100.J.B.AP880911-0016.html
        g = re.match(pat,each)
        fullname= manualpeers_dir + '//'+each
        print(each)
        if g:
            multid = g.groups()[0]
            lenstr = g.groups()[1]
            gid = g.groups()[2]
            sid = g.groups()[3]
            fid = g.groups()[4]
            print(fid)
            docid = fid
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

def LoadManualSys(docid,lenstr='100',peeridx=0):
    fname = graph_dir + '//' + 'manualpeer.dict'
    manualpeer = sxpReadFileMan.LoadObject(fname)
    peers= manualpeer[docid]
    mat =[]
    for each in peers:
        if lenstr == each['lenstr']:
            mat.append(each)
    cand = mat[peeridx]
    return cand['sent']
def MakeSubmitSingleSys(peerid):
    submit_peers_dir = r'E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEpeers\submittedpeers\SEE.abstracts.in.sentences'
    submit_peers_list = sxpReadFileMan.GetDirFileList(submit_peers_dir)
    submitpeer={}
  #  pat = r'(D\d\d\d).M.(\d\d\d).([A-Z]).([A-Z]).html'  # D061.M.010.J.I.html
    #    pat = r'(D\d\d\d).P.(\d\d\d).([A-Z]).([A-Z]).([A-Za-z0-9\-]+).html' #D061.P.100.J.B.AP880911-0016.html
    pat = r'(D\d\d\d).P.(\d\d\d).([A-Z]).(%s).([A-Za-z0-9\-]+).html' % (peerid)  # D061.P.100.J.27.AP880911-0016.html

    for each in submit_peers_list:
        g = re.match(pat,each)
        fullname= submit_peers_dir + '//'+each
        print(each)
        if g:
            multid = g.groups()[0]
            lenstr = g.groups()[1]
            gid = g.groups()[2]
            sid = g.groups()[3]
            fid = g.groups()[4]
#            print(fid)
            docid = fid
            submitsys = {}
            submitsys['fid']=fid
            submitsys['lenstr']=lenstr
            submitsys['gid']=gid
            submitsys['sid']=sid #different
            submitsys['docid']=docid
           # manualsys['txt']=sxpReadFileMan.ReadTextUTF(fullname)
            submitsys['sent']=sxpParseDUCText.ParseModelFile(fullname)
            dockey = peerid +'.'+docid
            print(dockey)
            if dockey =='29.AP880217-0100':
                print((submitsys['sent']))
            if docid in submitpeer:
                peers = submitpeer[docid]
                peers.append(submitsys)
                submitpeer[dockey]=peers
            else:
                peers = []
                peers.append(submitsys)
                submitpeer[dockey]=peers
    print((len(list(submitpeer.items()))))
    fname = graph_dir +'//' + 'submitpeer_%s.dict'%(peerid)
    sxpReadFileMan.SaveObject(submitpeer,fname)
def LoadAllSubmitSys(peerid='29',lenstr='100'):
    fname = graph_dir +'//' + 'submitpeer_%s.dict'%(peerid)
    submitpeer=sxpReadFileMan.LoadObject(fname)
    for docid, each in list(submitpeer.items()):
        print(docid)
        one = each[0]
        print((one['sent']))
def LoadOneSubmitSys(peerid,docid):
    pops = LoadSubmitSys(peerid,docid)
    print(pops)
def LoadSubmitSys(peerid,docid,lenstr='100',peeridx=0):
    fname = graph_dir +'//' + 'submitpeer_%s.dict'%(peerid)
    submitpeer=sxpReadFileMan.LoadObject(fname)
    for k,v in list(submitpeer.items()):
        print(k)
    dockey = peerid + '.'+docid
    peers= submitpeer[dockey]
    mat =[]
    for each in peers:
        if lenstr == each['lenstr']:
            mat.append(each)

    cand = mat[peeridx]
    return cand['sent']
def TestParseOne():
    fid = 'LA112790-0154'
    sxptxt = ParseOneDucFID(fid)
    print((sxptxt.sentence_textset))
def MakeFileList(usesub=False):
    fdir
    flist =sxpReadFileMan.GetDirFileList(single_raw_src)
    exc_pk_file =[]
    inc_pk_file =[]
    fdict_list = []
    for i, fn in enumerate(flist):
        fid_name = {}
        fid =  fn
        fid_name['id']= fid
        fid_name['raw']=fn
        if usesub==False:
            pkname = singlepkdir + '//' + fid + '.pk'
        else:
            pkname = singlepkdir_sub+ '//' + fid + '.pk'
        fid_name['single_pk']= pkname#singlepkdir+'//' + fid +  '.pk'

        fdict_list.append(fid_name)
    fname = fdir +'/fdict_list.dict'
    sxpReadFileMan.SaveObject(fdict_list,fname)
    return fdict_list
def LoadDocModelSentence(src='single'):
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir = r'./test/multipaper/papers_graph'
#    data_dir = r'./test/multipaper'
    if src =='single':

        return LoadSingleModelSent()

def GetFileNameDictList():
    fname = fdir +'/fdict_list.dict'
    fdict_list=sxpReadFileMan.LoadObject(fname)
    return fdict_list

def LoadSingleDucData(graph_dict_fid, usesub=False):
 #   fpname = singlepkdir + '\\' + graph_dict_fid + '.pk'
    if usesub == False:
        fpname = singlepkdir + '\\' +  graph_dict_fid + '.pk'
    else:
        fpname = singlepkdir_sub + '\\' +  graph_dict_fid + '.pk'
    sxptxt = sxpReadFileMan.LoadObject(fpname)
    return sxptxt
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
