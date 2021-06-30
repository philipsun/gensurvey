#-------------------------------------------------------------------------------
# Name:        sxpMultiPaperData.py
# Purpose:
#
# Author:      sunxp
#
# Created:     23/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=UTF-8

import json

import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
import pickle
import os
import re
import collections

import sxpReadFileMan
import sxpTextEncode
import sxpExtractText
import sxpFenciMakeTFIDF

from graphengine import sxpGraphEngine
import sxpSegSentWord
import sxpWordNet
import sxpTfidfVar

from rank_bm25 import BM25Okapi
from rank_bm25 import BM25
from rank_bm25 import BM25L
from rank_bm25 import BM25Plus
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

fdir = './test/multipaper/papers_json'
pkdir = r'./test/multipaper/papers_pk'
graph_dir =   './test/multipaper/papers_graph'
data_dir =r'./test/multipaper'
output_dir = r'./test/multipaper/test/out'
def main(runcmd=""):
    if runcmd:
        cmd = runcmd
    else:
        #cmd = 'Work'
        cmd = 'BuildGlobalTFIDF'
        # cmd = "BuildBM25"
     # cmd = 'ShowPaper'
   # cmd = 'TestWork'
    if cmd == 'BuildBM25':
        #BuildBM25('BM25Okapi')
        #BuildBM25('BM25') #this is super class,not implemented
        #BuildBM25('BM25L')
        #BuildBM25('BM25Plus')
        BuildPaperSentenceBM25(bmmodel='BM25Okapi')
    if cmd =='BuildGlobalTFIDF':
        BuildGlobalTFIDF(tfidfmode='tfidf')
        BuildGlobalTFIDF(tfidfmode='tfief')
        BuildGlobalTFIDF(tfidfmode='dtfipf')
    if cmd == 'TestWork':
        TestWork()
    if cmd == 'Work':
        Work()
    if cmd =='LoadDocModelSentence':
      #  print(LoadDocModelSentence())
        print(LoadDocData())
    if cmd == 'ShowPaper':
        ShowPaper()
    if cmd == 'checkdocsent':
        Checkdocsent()
    if cmd == 'makewddist':
        WordDistTestAll()
    if cmd == 'PaperSentenceNum':
        PaperSentenceNum()
def TestWork():
    TestProcessOne()
def Work():
    LoadExtractJsonFiles()
 #   pkdir = r'./test/multipaper/papers_pk'
    ShowTitle(pkdir)
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
def BuildGraph():
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir =   r'./test/multipaper/papers_graph'
#    data_dir =r'./test/multipaper'
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    all_corpus = []
    for fname_dict in graph_fname_list:
        data_dict = sxpReadFileMan.LoadSxptext(fname_dict['fname'])
        jsdict =  data_dict['jsdict']
    #    print(jsdict)
    #    graph_dir =   './test/multipaper/papers_graph'
        print('build graph for',fname_dict['fname'])
        graph_dict, matrix_dict, sentence_data_dict= ParsePaperJson(jsdict,data_dict['id'],graph_dir)
        all_corpus.append(sentence_data_dict['fulltext'])
    alldoc_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(all_corpus)
    fname = data_dir + '/alldoc_tfidf.tfidf'
    sxpReadFileMan.SaveObject(alldoc_tfidf,fname)

def BuildGlobalTFIDF(tfidfmode='tfidf'):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    all_corpus = []
    for fname_dict in graph_fname_list:
        data_dict = sxpReadFileMan.LoadSxptext(fname_dict['fname'])
        jsdict =  data_dict['jsdict']
    #    print(jsdict)
    #    graph_dir =   './test/multipaper/papers_graph'
        print('build global tfidf for',fname_dict['fname'])
        graph_dict, matrix_dict, sentence_data_dict= LoadFileData(fname_dict['fid'])
        all_corpus.append(sentence_data_dict['fulltext'])
        papersent_tfidf = sxpTfidfVar.MakeTFIDFForCorpus(sentence_data_dict['sent_list'],tfidfmode=tfidfmode)
        fname = data_dir + '/alldoc_tfidf.object_'+fname_dict['fid']+'_'+tfidfmode
        sxpReadFileMan.SaveObject(papersent_tfidf,fname)
    #alldoc_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(all_corpus)
    #tfidfmode = 'tf_idf'
    alldoc_tfidf = sxpTfidfVar.MakeTFIDFForCorpus(all_corpus,tfidfmode=tfidfmode)
    fname = data_dir + '/alldoc_tfidf.tfidf'+tfidfmode
    sxpReadFileMan.SaveObject(alldoc_tfidf,fname)
def BuildBM25(bmmodel='BM25Okapi'):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    all_corpus = []
    for fname_dict in graph_fname_list:
        data_dict = sxpReadFileMan.LoadSxptext(fname_dict['fname'])
        jsdict =  data_dict['jsdict']
    #    print(jsdict)
    #    graph_dir =   './test/multipaper/papers_graph'
        print('build global BuildBM25 for',fname_dict['fname'])
        graph_dict, matrix_dict, sentence_data_dict= LoadFileData(fname_dict['fid'])
        all_corpus.append(sentence_data_dict['sent_list'])
    tokenized_corpus = [doc.split(" ") for doc in all_corpus]
    if bmmodel == 'BM25Okapi':
        bm25 = BM25Okapi(tokenized_corpus)
    if bmmodel == 'BM25L':
        bm25 = BM25L(tokenized_corpus)
    if bmmodel == 'BM25Plus':
        bm25 = BM25Plus(tokenized_corpus)
    fname = data_dir + '/alldoc_bm25.object'+bmmodel
    sxpReadFileMan.SaveObject(bm25,fname)
def KeywordQueryOnBM25(newkeywordseq,bmmodel='BM25Okapi'):
    fname = data_dir + '/alldoc_bm25.object'+bmmodel
    bm25 = sxpReadFileMan.LoadObject(fname)
    tokenized_query = newkeywordseq

    doc_scores = bm25.get_scores(tokenized_query).reshape(-1,1)
    return doc_scores
def BuildPaperSentenceBM25(bmmodel='BM25Okapi'):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    all_corpus = []
    for fname_dict in graph_fname_list:
        data_dict = sxpReadFileMan.LoadSxptext(fname_dict['fname'])
        jsdict =  data_dict['jsdict']
    #    print(jsdict)
    #    graph_dir =   './test/multipaper/papers_graph'
        print('build global BuildBM25 for',fname_dict['fname'])
        graph_dict, matrix_dict, sentence_data_dict= LoadFileData(fname_dict['fid'])

        tokenized_corpus = [doc.split(" ") for doc in sentence_data_dict['sent_list']]
        if bmmodel == 'BM25Okapi':
            bm25 = BM25Okapi(tokenized_corpus)
        if bmmodel == 'BM25L':
            bm25 = BM25L(tokenized_corpus)
        if bmmodel == 'BM25Plus':
            bm25 = BM25Plus(tokenized_corpus)
        fname = data_dir + '/alldoc_bm25.object_'+fname_dict['fid']+'_'+bmmodel
        sxpReadFileMan.SaveObject(bm25,fname)
def KeywordQuerySentenceRankOnBM25(newkeywordseq,fid,bmmodel='BM25Okapi'):
  #  BuildPaperSentenceBM25(bmmodel=bmmodel)

    fname = data_dir + '/alldoc_bm25.object_'+fid+'_'+bmmodel
    bm25 = sxpReadFileMan.LoadObject(fname)
    tokenized_query = newkeywordseq
    doc_scores = bm25.get_scores(tokenized_query).reshape(-1,1)
    return doc_scores
def KeywordQuerySentenceRankOnTFIDF(newkeywordseq,fid,tfidfmode='dtfipf'):
  #  BuildPaperSentenceBM25(bmmodel=bmmodel)

    fname = data_dir + '/alldoc_tfidf.object_'+fid+'_'+tfidfmode
    tfidf = sxpReadFileMan.LoadObject(fname)
    doc_scores = sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(newkeywordseq, tfidf, tfidfmode)

    return doc_scores
def LoadAllDocTFIDF(rebuild=True,tfidfmode='tfidf'):
    fname = data_dir + '/alldoc_tfidf.tfidf' + tfidfmode
    if rebuild==False:

        return sxpReadFileMan.LoadObject(fname)
    else:
        Work()
        BuildGlobalTFIDF(tfidfmode)
        return sxpReadFileMan.LoadObject(fname)

def AlldocTFIDF(keywordquery,tfidfmode='tfidf'):
    if tfidfmode == 'tfidf':
        return sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(keywordquery, global_alldoc_tfidf,tfidfmode)
    if tfidfmode == 'tfief':
        return sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(keywordquery, global_alldoc_tfief,tfidfmode)
    if tfidfmode == 'dtfipf':
        return sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(keywordquery, global_alldoc_dtfipf,tfidfmode)

    #return KeyQueryOnTFIDF(keywordquery,global_alldoc_tfidf)
def KeyQueryOnTFIDF(keywordquery,alldoc_tfidf):
    return sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(keywordquery,alldoc_tfidf)

def LoadDocModelSentence():
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir = r'./test/multipaper/papers_graph'
#    data_dir = r'./test/multipaper'
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    for fname_dict in graph_fname_list:
        fname_dict = graph_fname_list[0]

        sentence_data_dict = sxpReadFileMan.LoadSxptext(fname_dict['sentence_data_dictname'])
        abstract = sentence_data_dict['abstract']
        conclusion = sentence_data_dict['conclusion']
        doc_dict ={}
        doc_dict['model']=[abstract,conclusion]
        doc_dict['title']=fname_dict['title']
        doc_dict['fid']=fname_dict['fid']
        doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list
def LoadDocFileName():
    graph_fname_list = LoadGraphFileName(pkdir, graph_dir)
    doc_info_list = []
    for fname_dict in graph_fname_list:
        #      fname_dict = graph_fname_list[0]
        graph_dict, matrix_dict, sentence_data_dict = LoadFileData(fname_dict['fid'])
        doc_dict = {}
        abstract = sentence_data_dict['abstract']
        conclusion = sentence_data_dict['conclusion']
        doc_dict['model'] = [abstract, conclusion]
        doc_dict['title'] = fname_dict['title']
        doc_dict['fid'] = fname_dict['fid']
        doc_info_list.append(doc_dict)
    return doc_info_list


def LoadDocData():
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    for fname_dict in graph_fname_list:
  #      fname_dict = graph_fname_list[0]
        graph_dict, matrix_dict,sentence_data_dict=LoadFileData(fname_dict['fid'])
        doc_dict ={}
        abstract =sentence_data_dict['abstract']
        conclusion=sentence_data_dict['conclusion']
        doc_dict['model']=[abstract,conclusion]
        doc_dict['title']=fname_dict['title']
        doc_dict['fid']=fname_dict['fid']
        doc_dict['graph_dict']=graph_dict
        doc_dict['matrix_dict']=matrix_dict
        doc_dict['sent_list']=sentence_data_dict['sent_list']
        doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list
def Checkdocsent():
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    fname_dict = graph_fname_list[0]
    graph_dict, matrix_dict, sentence_data_dict = LoadFileData(fname_dict['fid'])
    print(fname_dict['fid'])
    print(graph_dict['title'])

    sentlist = sentence_data_dict['sent_list']
    for i,sent in enumerate( sentlist):
        print(i,sent)
def PaperSentenceNum(fidlist=[]):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    outsubdir = output_dir
    sxpReadFileMan.CheckMkDir(outsubdir)
    stlen_dict={}
    stlen_list = []
    for fname_dict in graph_fname_list:
        if len(fidlist)>0:
            if fname_dict['fid'] not in fidlist:
                continue
        graph_dict, matrix_dict, sentence_data_dict = LoadFileData(fname_dict['fid'])
        sl = len(sentence_data_dict['sent_list'])
        wl = 0
        for s in sentence_data_dict['sent_list']:
            wl = wl + len(s)
        stlen_dict[fname_dict['fid']]=[sl, wl]
        stlen_list.append(sl)
    fname = output_dir + '/' + 'all_paper_sent_num.dict'
    data_dict={}
    data_dict['sent_dict']=stlen_dict
    data_dict['stlen_list'] = stlen_list
    sxpReadFileMan.SaveObject(data_dict,fname)
def LoadAllPaperSentNum():
    fname = output_dir + '/' + 'all_paper_sent_num.dict'
    data_dict = sxpReadFileMan.LoadObject(fname)
    return data_dict
def MakeWordDist(test_name,keywordseq,fidlist=[]):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    outsubdir = output_dir +'/'+test_name
    sxpReadFileMan.CheckMkDir(outsubdir)
    for fname_dict in graph_fname_list:
        if len(fidlist)>0:
            if fname_dict['fid'] not in fidlist:
                continue
        graph_dict, matrix_dict, sentence_data_dict = LoadFileData(fname_dict['fid'])

        fid = fname_dict['fid']
        if fid == '0008':
            br =1;

        print('MakeWordDist',fname_dict['fid'])
        print(graph_dict['title'])
        title = graph_dict['title']
        title = re.sub('\:','_',title)
        wd_dist = sxpSegSentWord.worddist(keywordseq,sentence_data_dict['sent_list'])
        print(fname_dict['fname'])
        wd_dist_fname = outsubdir +'/'+test_name+'_'+fid+'_'+title+'_wdist.pk'

        sxpReadFileMan.StoreSxptext(wd_dist,wd_dist_fname)
def LoadWdDist(test_name,fidlist=[]):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    wd_list = []
    outsubdir = output_dir +'/'+test_name
    for fname_dict in graph_fname_list:
        if len(fidlist)>0:
            if fname_dict['fid'] not in fidlist:
                continue
        print(fname_dict)
        fid = fname_dict['fid']
        print('LoadWdDist',fid)
        print(fname_dict['fname'])
        title = fname_dict['title']
        title = re.sub('\:','_',title)
#        wd_dist_fname = fname_dict['fname'] +'_'+test_name+ '_wdist.pk'
        wd_dist_fname = outsubdir +'/'+test_name+'_'+fid+'_'+title+'_wdist.pk'

        wd_list.append([fid,fname_dict['title'],wd_dist_fname,sxpReadFileMan.LoadSxptext(wd_dist_fname)])

    return wd_list
def LoadGraphMatrixSentence(fid=[]):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    for fname_dict in graph_fname_list:
     #   fname_dict = graph_fname_list[0]
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

    fname_dict=graph_fname_list[43]

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
def CorrectJson():
    #    fdir = './test/multipaper/papers_json'
    fnamelist = sxpReadFileMan.GetDirFileListType(fdir, 'json')
    #    pkdir = './test/multipaper/papers_pk'
    for i, each in enumerate(fnamelist):
        print('******', i)
        print(each)
        jstr = sxpReadFileMan.ReadTextUTF(each)
        if jstr is None:
            print('wrong in open')
            break
        us = sxpTextEncode.GetUnicode(jstr)

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
    #---------this is the core function to parse the node text out-----------------
    graph_root = ParseTree(jsdict,root)
    #------------------------------------------------------------------------------
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
            #sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            sentenceset = sxpExtractText.MySegSent(eachpara.node_title)
            # print('in ParseJons---------')
            # print(eachpara.node_title)
            # for i, s in enumerate(sentenceset):
            #     print(i,s)
            for i, eachsent in enumerate( sentenceset):
                if len(eachsent.strip())==0:
                    continue
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
    sentence_data_dict['sent_list']=sentence_doc
    fulltextlist = []
    print('-----abstract')
    for each in sentence_data_dict['abstract']:

        fulltextlist.append(each[1])
    for each in sentence_data_dict['sent_list']:
        fulltextlist.append(each)
    print('-----conclusion')
    for each in sentence_data_dict['conclusion']:
        fulltextlist.append(each[1])
    sentence_data_dict['fullsent']= fulltextlist
    sentence_data_dict['fulltext']= ' '.join(fulltextlist)
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
    print( 'd_c matrix')
    d_c = csr_matrix(np.ones((1,cs), dtype=np.float64))

    print('building c_c matrix')
    c_c = csr_matrix((cs,cs), dtype=np.float64)
    for i, secid in enumerate( section_vec):
        f=section_father_vec[i]
        c_c[f,i]=1.0
    print('building c_p matrix')
    c_p = csr_matrix((cs,ps), dtype=np.float64)
    for i, paraid in enumerate( paragraph_vec):
        f=paragraph_father[i]
        c_p[f,i]=1.0
    print('building p_s matrix')
    p_s = csr_matrix((ps,ss), dtype=np.float64)
    for i, sentid in enumerate( sentence_vec):
        f=sentence_vec_father[i]
        p_s[f,i]=1.0

    print('building s_w matrix')
    s_k = csr_matrix((ss,ks), dtype=np.float64)

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
def MakeAllDocTFIDF(sentence_data_dict_list):
    corpus = []
    for sentence_data_dict in sentence_data_dict_list:
        corpus.append(())
def ParseTree(jsdict,root):
    subnodes = []
    subnd = None
    txt_id =0
    if jsdict['kind'] == 'Chapter':
        if 'title' in jsdict.keys():#python3 comment
            title = jsdict['title']
            subnd = sxpNode('Chapter')
            subnd.node_title= title
            root.AddSubNode(subnd)
        #    print('find sub node',title)
        if 'content' in jsdict.keys():
            subnodes.append(jsdict['content'])
    if jsdict['kind']=='Paragraph':
        if 'content' in jsdict.keys(): #python3 comment
            txt = sxpWordNet.correctjsontxt(jsdict['content'])
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
def WordDistTest():
    keywordseq=['summarization','method','extractive']
    fidlist=['0000','0001','0004','0010']
    MakeWordDist('extrative',keywordseq,fidlist)
def WordDistTestAll():
    keywordseq=['summarization','method','extractive']
    MakeWordDist('extrative',keywordseq,fidlist=[])
def ShowPaper():
    fid =['0043']
    doc_model_sent_list=LoadGraphMatrixSentence(fid)
    for doc_dict in doc_model_sent_list:
        for i,s in enumerate(doc_dict['sentence_data_dict']['sent_list']):
            print(i,s)
global_alldoc_tfidf = LoadAllDocTFIDF(rebuild=False,tfidfmode='tfidf')
global_alldoc_tfief = LoadAllDocTFIDF(rebuild=False,tfidfmode='tfief')
global_alldoc_dtfipf = LoadAllDocTFIDF(rebuild=False,tfidfmode='dtfipf')
if __name__ == '__main__':
    main()
