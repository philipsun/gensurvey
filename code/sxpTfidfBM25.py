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
import numpy as np
import sxpReadFileMan
import sxpTextEncode
import sxpExtractText
import sxpFenciMakeTFIDF
import sxpJudgeCharacter
from graphengine import sxpGraphEngine
import sxpSegSentWord
import sxpWordNet
import sxpTfidfVar
from nltk.corpus import stopwords

from rank_bm25 import BM25Okapi
from rank_bm25 import BM25
from rank_bm25 import BM25L
from rank_bm25 import BM25Plus
data_dir =r'./test/tfidfbm25'
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
def stop_words():
    sw = stopwords.words("english")
    return sw
def processkeyword(keywordseq,removestop = True):
    stopwords= stop_words()
    score_list = []
    nk = []

    for each in keywordseq:
        sk = re.split('\s+', each)
        for eachw in sk:
            if len(eachw.strip()) == 0:
                continue
            if removestop:
                if eachw.lower() in stopwords:
                    continue
            nk.append(eachw.lower())
    return nk
def BuildTFIDF(all_corpus,testname,tfidfmode='tfidf',rebuild=False):
    fname = data_dir + '/alldoc_tfidf.tfidf' + '_'+testname+'_'+ tfidfmode
    print('build global Tfidf for', fname)
    if rebuild==False:
        tfidf =  sxpReadFileMan.LoadObject(fname)
        if tfidf is not None:
            return tfidf
    alldoc_tfidf = sxpTfidfVar.MakeTFIDFForCorpus(all_corpus, tfidfmode=tfidfmode)
    sxpReadFileMan.SaveObject(alldoc_tfidf, fname)
    return sxpReadFileMan.LoadObject(fname)
def BuildBM25(all_corpus,testname,bmmodel='BM25Okapi',rebuild=False):
    fname = data_dir + '/alldoc_bm25.object' + '_' + testname + '_' + bmmodel
    #print('build global BuildBM25 for',fname)
    if rebuild==False:
        tfidf =  sxpReadFileMan.LoadObject(fname)
        if tfidf is not None:
            return tfidf
    tokenized_corpus = [doc.split(" ") for doc in all_corpus]
    if bmmodel == 'BM25Okapi':
        bm25 = BM25Okapi(tokenized_corpus)
    if bmmodel == 'BM25L':
        bm25 = BM25L(tokenized_corpus)
    if bmmodel == 'BM25Plus':
        bm25 = BM25Plus(tokenized_corpus)
    sxpReadFileMan.SaveObject(bm25,fname)
    return bm25
def KeywordQueryOnTFIDF(querykeyword,all_corpus,testname,tfidfmode='tfidf',global_alldoc_tfidf = None, tfidfbm=None):
    newkeywordseq = processkeyword(querykeyword)
    if tfidfbm is None:
        tfidfbm = BuildTFIDF(all_corpus,testname,tfidfmode=tfidfmode,rebuild=True)

    if tfidfmode == 'tfidf':
        return sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(newkeywordseq, tfidfbm,tfidfmode)
    if tfidfmode == 'tfief':
        return sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(newkeywordseq, tfidfbm,tfidfmode)
    if tfidfmode == 'dtfipf':
        return sxpFenciMakeTFIDF.KeywordQueryOnTFIDF(newkeywordseq, tfidfbm,tfidfmode)

def KeywordQueryOnBM25(querykeyword,all_corpus,testname,bmmodel='BM25Okapi',tfidfbm = None):
    newkeywordseq = processkeyword(querykeyword)
    if tfidfbm is None:
        tfidfbm = BuildBM25(all_corpus, testname, bmmodel, rebuild=True)
    tokenized_query = newkeywordseq
    doc_scores = tfidfbm.get_scores(tokenized_query).reshape(-1,1)
    return doc_scores

def RankSentence(querykeyword,sent_list,testname,bmmodel='BM25Okapi',selectbydiff = 'NO',wdlen=250):
    if bmmodel in ['BM25Okapi','BM25L','BM25Plus']:
        return RankSentenceByBM25(querykeyword, sent_list, testname, bmmodel=bmmodel, selectbydiff=selectbydiff,wdlen=wdlen)
    if bmmodel in ['tfidf','tfief','dtfipf']:
        return RankSentenceByTFIDF(querykeyword, sent_list, testname, tfidfmode=bmmodel, selectbydiff=selectbydiff,wdlen=wdlen)
def RankDoclist(querykeyword,doc_list,testname,bmmodel='BM25Okapi',selectbydiff = 'NO',wdlen=250,tfidfbm = None):
    if bmmodel in ['BM25Okapi','BM25L','BM25Plus']:
        return RankSentenceByBM25(querykeyword, doc_list, testname, bmmodel=bmmodel, selectbydiff=selectbydiff,wdlen=wdlen,tfidfbm = tfidfbm)
    if bmmodel in ['tfidf','tfief','dtfipf']:
        return RankSentenceByTFIDF(querykeyword, doc_list, testname, tfidfmode=bmmodel, selectbydiff=selectbydiff,wdlen=wdlen,tfidfbm = tfidfbm)
def RankSentenceByBM25(querykeyword,sent_list,testname,bmmodel='BM25Okapi',selectbydiff = 'NO',wdlen = 250,tfidfbm = None):
    dual_sent_score = KeywordQueryOnBM25(querykeyword, sent_list, testname, bmmodel=bmmodel, tfidfbm=tfidfbm)
    idx_sent = list(np.argsort(-dual_sent_score, axis=0,kind='mergesort',).flat)
    ranked_sent = [sent_list[idx] for idx in idx_sent]
    sent_rank_dict= {}
    sent_rank_dict['doc_score']=dual_sent_score
    sent_rank_dict['sent_score']=dual_sent_score
    sent_rank_dict['ranked_sent'] = ranked_sent
    sent_rank_dict['idx_sent'] = idx_sent
    #Qwdlen = 250
    simr=0.4
    groupsim=False
    if selectbydiff == 'OK':
        sent_txt_set, top_idx=OutputAllRankSentenceByDiff(idx_sent,sent_list,wdlen,simr,groupsim)
    else:
        sent_txt_set,top_idx = OutputBoundTopk(ranked_sent,idx_sent,wdlen)
        #top_idx = idx_sent
    sent_rank_dict['topsent']=sent_txt_set
    sent_rank_dict['topidx'] = top_idx
    sent_rank_dict['rawtopscore']=dual_sent_score[top_idx,0]
    sent_rank_dict['topscore'] = normalize(dual_sent_score[top_idx,0])
    return sent_rank_dict
def RankSentenceByTFIDF(querykeyword,sent_list,testname,tfidfmode='tfidf',selectbydiff = 'NO',wdlen = 250,tfidfbm = None):

    dual_sent_score = KeywordQueryOnTFIDF(querykeyword, sent_list, testname, tfidfmode=tfidfmode,tfidfbm=tfidfbm)


    idx_sent = list(np.argsort(-dual_sent_score, axis=0,kind='mergesort',).flat)
    ranked_sent = [sent_list[idx] for idx in idx_sent]
    sent_rank_dict= {}
    sent_rank_dict['doc_score']=dual_sent_score
    sent_rank_dict['sent_score']=dual_sent_score
    sent_rank_dict['ranked_sent'] = ranked_sent
    sent_rank_dict['idx_sent'] = idx_sent
    #wdlen = 250
    simr=0.4
    groupsim=False
    if selectbydiff == 'OK':
        sent_txt_set, top_idx=OutputAllRankSentenceByDiff(idx_sent,sent_list,wdlen,simr,groupsim)
    else:
        sent_txt_set,top_idx = OutputBoundTopk(ranked_sent,idx_sent,wdlen)
        #top_idx = idx_sent
    sent_rank_dict['topsent']=sent_txt_set
    sent_rank_dict['topidx'] = top_idx
    sent_rank_dict['rawtopscore']=dual_sent_score[top_idx,0]
    sent_rank_dict['topscore'] = normalize(dual_sent_score[top_idx,0])
    return sent_rank_dict
def OutputBoundTopk(sent_list,idx_sent,wdlen):
    select = []
    topk_idx = []
    s = 0
    for i,each in enumerate(sent_list):
        wd = re.split('\s+',each)
        for eachw in wd:
            ws = eachw.strip()
            if len(ws)==0:
                continue
            if ws in ['.',',',':',"'",'"']:
                continue
            s = s + 1
        if s > wdlen:
            break
        select.append(each)
        topk_idx.append(idx_sent[i])
    return select,topk_idx

def normalize(score):
    a = np.array(score).reshape(-1,1)
    r = np.sum(a,0)
    if r == 0:
        r = 1
    a = a /r
    return a

def OutputAllRankSentenceByDiff(idx_s,sentenceset,wlen=500,simr=0.4,groupsim=True):
    print('output ranked sent',len(sentenceset))
    sent_txt_set = []
    i = 0
    n = len(idx_s)
    t = 0
    skiped = 0
    top_idx = []
    for i in range(n):
        sent = sentenceset[idx_s[i]]
        if t > wlen:
            break
        print(i,sent)
        if groupsim == False and simsent(sent,sent_txt_set,simr):
            skiped +=1
            continue
        if groupsim and simsentgroup(sent,sent_txt_set,simr):
            skiped +=1
            continue
        sent_txt_set.append(sent)
        top_idx.append(idx_s[i])

        t = t + len(re.split('\s+',sent.strip()))
    print('finished ranked','skiped',skiped)
    return sent_txt_set,top_idx
def simsent(sent,sent_txt_set,simr=0.4):
    for each in sent_txt_set:
        sim = sxpJudgeCharacter.jaccard_similarity(sent,each)
        if sim>simr:
            return True
    return False
def simsentgroup(sent,sent_txt_set,simr=0.4):
    ds = []
    for each in sent_txt_set:
        sim = sxpJudgeCharacter.jaccard_similarity(sent,each)
        ds.append(sim)
    sim = np.mean(ds)
    if sim >= simr:
        return True;
    return False