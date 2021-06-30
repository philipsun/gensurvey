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

import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
import pickle
import os
from sxpComputeCloseDist import *
from numpy import argsort
import sxpReadFileMan

import sxpSegSentWord
import sxpJudgeCharacter
import sxpMultiPaperData
from sxpMultiPaperData import sxpNode
import pandas as pd
import matplotlib.pyplot as plt
import sxpTestCluster
import re
from nltk.corpus import stopwords
import sxpMMR
import sxpTfidfBM25
#import nltk

def stop_words():
    sw = stopwords.words("english")
    return sw

def MakeShowWdKeyDist(wd_dist_tuple):
    fid = wd_dist_tuple[0]
    title = wd_dist_tuple[1]
    fname = wd_dist_tuple[2]
    wd_dist=wd_dist_tuple[3]
    nk = len(wd_dist.keys())+1
    nr = 2
    rwlist,nr,nc = sxpReadFileMan.makerowcolnum(nk,nr)
    mr = len(rwlist)
    fig, axes = plt.subplots(nr, nc)
    axes=axes.reshape((nr,nc))
    df = pd.DataFrame(wd_dist)
    ax0=df.plot(ax=axes[0, 0])
    ax0.legend(fontsize=6)
    i = 1
    for keys in wd_dist.keys():
        kdf = pd.DataFrame(wd_dist[keys])
        axispos =rwlist[i]
        i = i + 1
        ax1 = kdf.plot(ax=axes[axispos[0], axispos[1]], legend=True, ylim=[0, 2])
        ax1.legend([keys],fontsize=6)
 #   plt.title(title)
    fig.suptitle(title)
    figname = fname + '.png'
    plt.savefig(figname)
    plt.show()


    plt.close(fig)
def MakeXFromWdDistDict(wd_dist_dict,line):
    n = 0
    for keys, wd_dist in wd_dist_dict.items():
        n = len(wd_dist)
        break
    xdict={}
    all_keys=np.zeros((n,2))
    print(all_keys.shape)
    if line == 'v':
        all_keys[:, 0] = all_keys[:, 0] * 0.5
    if line == 'h':
        all_keys[:, 1] = all_keys[:, 1] * 0.5
    for keys,wd_dist in wd_dist_dict.items():
        a = np.zeros((n,2))

        for i,v in enumerate(wd_dist):
            if v > 0:
                if line == 'v':
                    a[i,1]=i#wd_dist[i]
                    all_keys[i,1] =i
                if line == 'h':
                    a[i,0]=i#wd_dist[i]
                    all_keys[i,0] =i
        xdict[keys]=a
    xdict['allkey']=all_keys
    return xdict
def ClusterWdDist(xdict,fname):
    x = xdict['allkey']
    cname = fname + '_keys'
    sxpTestCluster.clustertestoneset(x, cname)
    # for keys,X in xdict.items():
    #     cname = fname + '_keys'
    #     sxpTestCluster.clustertestoneset(X,cname)

def MakeSentXDict(wd_dist_tuple,line='h'):
    fid = wd_dist_tuple[0]
    title = wd_dist_tuple[1]
    fname = wd_dist_tuple[2] + '_'+line
    print('makesentxdict',fname)
    wd_dist_dict=wd_dist_tuple[3]
    xdict=MakeXFromWdDistDict(wd_dist_dict,line)
    xname = fname +'_xdict.dict'
    sxpReadFileMan.SaveObject(xdict,xname)
def ClusterSentPara(wd_dist_tuple,line):
    fid = wd_dist_tuple[0]
    title = wd_dist_tuple[1]
    fname = wd_dist_tuple[2] + '_'+line
    print('ClusterSentPara', fname)
    wd_dist_dict=wd_dist_tuple[3]
    xname = fname +'_xdict.dict'
    xdict = sxpReadFileMan.LoadObject(xname)
    ClusterWdDist(xdict, fname)
def ClusterSentKeyTest(wd_dist_tuple,line='h'):
    fid = wd_dist_tuple[0]
    title = wd_dist_tuple[1]
    fname = wd_dist_tuple[2] + '_'+line
    print('ClusterSentXDict', fname)
    wd_dist_dict=wd_dist_tuple[3]
    xname = fname +'_xdict.dict'
    xdict = sxpReadFileMan.LoadObject(xname)
    xname = fname +'_keys_cluster'
    sxpTestCluster.clusterXSet(xdict,xname)
def ShowWdTest(wd_dist_tuple):
    fid = wd_dist_tuple[0]
    title = wd_dist_tuple[1]
    fname = wd_dist_tuple[2]
    wd_dist=wd_dist_tuple[3]
    fig, axes = plt.subplots(2, 2)

    df = pd.DataFrame(wd_dist)
    ax0=df.plot(ax=axes[0,0])

    keys = 'summarization'
    kdf = pd.DataFrame(wd_dist[keys])
    ax1=kdf.plot(ax = axes[0,1],legend=True,ylim=[0,2])
    ax1.legend([keys])



    keys= 'extractive'
    kdf = pd.DataFrame(wd_dist[keys])
    ax2=kdf.plot(ax = axes[1,0],legend=True,ylim=[0,2])
    ax2.legend([keys])


    keys= 'method'
    kdf = pd.DataFrame(wd_dist[keys])
    ax3=kdf.plot(ax = axes[1,1],legend=True,ylim=[0,2])
    ax3.legend([keys])

 #   plt.title(title)
    fig.suptitle(title)
  #  plt.show()
    figname = fname + '.png'
    plt.savefig(figname)
def WordDistTest():
    keywordseq=['summarization','method','extractive']
    fidlist=['0000','0001','0004','0010']
    testname ='extrative'
    sxpMultiPaperData.MakeWordDist(testname,keywordseq,fidlist)
def WordDistTestAll():
    testname = 'extrative'
    keywordseq=['summarization','method','extractive']
    sxpMultiPaperData.MakeWordDist(testname,keywordseq,fidlist=[])
def MakeWordDist(test_name,keywordseq,fidlist=[],version='v3'):
    graph_fname_list=sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir,sxpMultiPaperData.graph_dir)
    outsubdir = sxpMultiPaperData.output_dir +'/'+test_name
    sxpReadFileMan.CheckMkDir(outsubdir)
    wdlist = []
    newnk = ProcessKeyword(keywordseq,prefix=[],removestop = True)
    for fname_dict in graph_fname_list:
        if len(fidlist)>0:
            if fname_dict['fid'] not in fidlist:
                continue
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        fid = fname_dict['fid']
        if fid == '0051':
            br =1;
 #           print(sentence_data_dict['sent_list'])
        print('--------------makeworddist-------------')
        print('MakeWordDist',fname_dict['fid'])
        print(graph_dict['title'])
        title = graph_dict['title']
        title = re.sub('\:','_',title)

        wd_dist = sxpSegSentWord.worddist(newnk,sentence_data_dict['sent_list'])
        sentposwd_dist = sxpSegSentWord.wordsentposdist(newnk, sentence_data_dict['sent_list'])
        print(sentposwd_dist)
        nl = len(sentence_data_dict['sent_list']) / 1.0

        g = re.match('(v\d+)',version)
        if g:
            v =g.groups()[0]
            if version == 'v4test':
                score = testcomputedist(newnk, sentposwd_dist, nl, version=v)
            else:
                score = computeclosenesstwo(newnk, sentposwd_dist, nl, version=v)
        g =re.match('b(v\d+)',version)
        if g:
            v =g.groups()[0]
            score = computeclosenessbiascover(newnk, sentposwd_dist, nl, version=v)
        #score = computeworddistscore(newnk, wd_dist)
        print('score:',score)
        print(fname_dict['fname'])
        wd_dist_fname = outsubdir +'/'+test_name+'_'+fid+'_'+title+'_wdist.pk'
        wdlist.append([fid, fname_dict['title'], wd_dist_fname, wd_dist])
       # print(wd_dist)
        sxpReadFileMan.StoreSxptext(wd_dist,wd_dist_fname)
    for each in wdlist:
        MakeShowWdKeyDist(each)
def testcase():

    testnaem ='extrative'
    fidlist = ['0000', '0001', '0004', '0010']
    wdlist=sxpMultiPaperData.LoadWdDist(testnaem,fidlist)
    ShowWdTest(wdlist[0])
    ShowWdTest(wdlist[1])
    ShowWdTest(wdlist[2])
    ShowWdTest(wdlist[3])
def KeywordRankWordDist(test_name,keywordseq,fidlist=[]):
    graph_fname_list=sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir,sxpMultiPaperData.graph_dir)
    outsubdir = sxpMultiPaperData.output_dir +'/'+test_name
    sxpReadFileMan.CheckMkDir(outsubdir)
    score_list=[]
    for fname_dict in graph_fname_list:
        if len(fidlist)>0:
            if fname_dict['fid'] not in fidlist:
                continue
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        fid = fname_dict['fid']
        if fid == '0008':
            br =1


        title = graph_dict['title']
        title = re.sub('\:','_',title)
        wd_dist = sxpSegSentWord.worddist(keywordseq,sentence_data_dict['sent_list'])
        score =computeworddistscore(keywordseq,wd_dist)
        score_list.append(score)

        wd_dist_fname = outsubdir +'/'+test_name+'_'+fid+'_'+title+'_wdist.pk'
    pr = np.array(score_list).reshape((-1,1))
    idx_s = list(argsort(-pr, axis=0).flat)
    i = 0;
    for id in idx_s:
        fname_dict = graph_fname_list[id]
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])
        title = graph_dict['title']
        print(i,id, score_list[id],title)
        i = i + 1
    return idx_s
def ListPaperTitle():
    graph_fname_list=sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir,sxpMultiPaperData.graph_dir)

    i = 0
    for fname_dict in graph_fname_list:

        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        fid = fname_dict['fid']


        title = graph_dict['title']
        print(i, title)
        i = i + 1;
def ProcessKeyword(keywordseq,prefix=[],removestop=True):
    nk = []

    for each in keywordseq:
        sk = re.split('\s+', each)
        for eachw in sk:
            if len(eachw.strip()) == 0:
                continue
            if removestop:
                if eachw.lower() in global_stopwords:
                    continue
            nk.append(eachw.lower())
    newnk = []
    for pk in prefix:
        newnk.append(pk)
    for pk in nk:

        lpk = pk.lower()
        if lpk == pk:
            s = re.split('\-', pk)
            hs = " ".join(s)
            newnk.append(hs)
        else:
            #newnk.append('({0}|{1})'.format(pk,lpk))
            s = re.split('\-', lpk)
            hs = " ".join(s)
            newnk.append(hs)
    return newnk
global_stopwords= stop_words()
def KeywordRankCloseWordDist(test_name, keywordseq, prefix=[], fidlist=[],removestop=False,version='v2'):
    graph_fname_list = sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir, sxpMultiPaperData.graph_dir)
    outsubdir = sxpMultiPaperData.output_dir + '/' + test_name
  #  sxpReadFileMan.CheckMkDir(outsubdir)

    score_list = []
    sent_rank_result ={}
    newnk = ProcessKeyword(keywordseq, prefix,removestop=removestop)
    print('keyword to be query', newnk)
    for fname_dict in graph_fname_list:
        if len(fidlist) > 0:
            if fname_dict['fid'] not in fidlist:
                continue
        #   print('process fid',fname_dict['fid'] )
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        fid = fname_dict['fid']
        if fid == '0051':
            br = 1
        #     print(sentence_data_dict['sent_list'])

        title = graph_dict['title']
        title = re.sub('\:', '_', title)
        # wd_dist = sxpSegSentWord.worddist(nk, sentence_data_dict['sent_list'],skipzero=True)
        # txt = ' '.join(sentence_data_dict['sent_list'])
        # print(sentence_data_dict['sent_list'])
        wd_dist = sxpSegSentWord.wordsentposdist(newnk, sentence_data_dict['sent_list'])
      #  print('word dist',wd_dist)
        # score = computeworddistscore(keywordseq, wd_dist)
        nl = len(sentence_data_dict['sent_list']) / 1.0
        # score = computecloseness(nk, wd_dist,nl)
        score,dual_sent_score = computeclosenesstwo(newnk, wd_dist, nl,version=version)
        score_list.append(score)


        idx_sent = list(argsort(-dual_sent_score, axis=0).flat)
        ranked_sent = [sentence_data_dict['sent_list'][idx] for idx in idx_sent]
        sent_rank_dict= {}
        sent_rank_dict['score']=dual_sent_score
        sent_rank_dict['ranked_sent'] = ranked_sent
        sent_rank_dict['idx_sent'] = idx_sent
        sent_rank_result[fname_dict['fid']]=sent_rank_dict
        wd_dist_fname = outsubdir + '/' + test_name + '_' + fid + '_' + title + '_wdist.pk'
    pr = np.array(score_list).reshape((-1,1))
    idx_s = list(argsort(-pr, axis=0).flat)
    i = 0
    resultid=[]

    for id in idx_s:
        if len(fidlist)>0:
            rid = id;
            fid = fidlist[id]
        else:
            rid = id;
            fname_dict = graph_fname_list[rid]
            fid =fname_dict['fid']
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fid)
        title = graph_dict['title']
       # print(i, id, score_list[id], title)
        resultid.append((rid,fid, score_list[id], title))
        i = i + 1;
    return resultid,sent_rank_result
#---------------------The best implementation -----------------
def DualKeywordSentRankCloseWordDist(test_name, keywordseq, prefix=[], fidlist=[],removestop=False,version = 'dual_v6'):
    graph_fname_list = sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir, sxpMultiPaperData.graph_dir)
    outsubdir = sxpMultiPaperData.output_dir + '/' + test_name
  #  sxpReadFileMan.CheckMkDir(outsubdir)

    score_list = []
    newnk = ProcessKeyword(keywordseq, prefix,removestop=removestop)
    print('keyword to be query', newnk)
    sent_rank_result = {}
    for fname_dict in graph_fname_list:
        if len(fidlist) > 0:
            if fname_dict['fid'] not in fidlist:
                continue
        #   print('process fid',fname_dict['fid'] )
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        fid = fname_dict['fid']
        if fid == '0051':
            br = 1
        #     print(sentence_data_dict['sent_list'])

        title = graph_dict['title']
        title = re.sub('\:', '_', title)
        # wd_dist = sxpSegSentWord.worddist(nk, sentence_data_dict['sent_list'],skipzero=True)
        # txt = ' '.join(sentence_data_dict['sent_list'])
        # print(sentence_data_dict['sent_list'])
        wd_dist,sent_dist_dict = sxpSegSentWord.dualwordsentposdist(newnk, sentence_data_dict['sent_list'])
      #  print('word dist',wd_dist)
        # score = computeworddistscore(keywordseq, wd_dist)
        nl = len(sentence_data_dict['sent_list']) / 1.0
        # score = computecloseness(nk, wd_dist,nl)
    #    score = computeclosenesstwo(newnk, wd_dist, nl,version=version) #only score of paper, 20200808 the best one
       # version = 'dual_v6'
        #print('-----this ranking dual sentence and word,version = dual_v6---')
        #----------------------this is to compute closeness-------------------------------
        score,dual_sent_score = dualcomputeclosenesstwo(newnk, wd_dist, nl,version=version)
        #---------------------------------------------------------------------------------
        score_list.append(score)
        idx_sent = list(argsort(-dual_sent_score, axis=0).flat)
        ranked_sent = [sentence_data_dict['sent_list'][idx] for idx in idx_sent]
        sent_rank_dict= {}
        sent_rank_dict['score']=dual_sent_score
        sent_rank_dict['ranked_sent'] = ranked_sent
        sent_rank_dict['idx_sent'] = idx_sent
        sent_rank_result[fname_dict['fid']]=sent_rank_dict

        wd_dist_fname = outsubdir + '/' + test_name + '_' + fid + '_' + title + '_wdist.pk'
    pr = np.array(score_list).reshape((-1,1))
    idx_s = list(argsort(-pr, axis=0).flat)
    i = 0
    resultid=[]

    for id in idx_s:
        if len(fidlist)>0:
            rid = id;
            fid = fidlist[id]
        else:
            rid = id;
            fname_dict = graph_fname_list[rid]
            fid =fname_dict['fid']
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fid)
        title = graph_dict['title']
       # print(i, id, score_list[id], title)
        resultid.append((rid,fid, score_list[id], title))
        i = i + 1;
    return resultid,sent_rank_result
#---------------------The best implementation -----------------
def DualKeywordSentRankCloseWordDistOnDocList(test_name, keywordseq, graph_fname_list, outsubdir, prefix=[], fidlist=[],removestop=False,version = 'dual_v6'):
 #   graph_fname_list = sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir, sxpMultiPaperData.graph_dir)
 #   outsubdir = sxpMultiPaperData.output_dir + '/' + test_name


    score_list = []
    newnk = ProcessKeyword(keywordseq, prefix,removestop=removestop)
    print('keyword to be query', newnk)
    sent_rank_result = {}
    for fname_dict in graph_fname_list:
        if len(fidlist) > 0:
            if fname_dict['fid'] not in fidlist:
                continue
        #   print('process fid',fname_dict['fid'] )
        # graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        #matrix_dict= fname_dict['matrix_dict']
        sentence_textset = fname_dict['sentence_textset']
        fid = fname_dict['fid']
        if fid == '0051':
            br = 1
        #     print(sentence_data_dict['sent_list'])

        title = fname_dict['title']
        title = re.sub('\:', '_', title)
        # wd_dist = sxpSegSentWord.worddist(nk, sentence_data_dict['sent_list'],skipzero=True)
        # txt = ' '.join(sentence_data_dict['sent_list'])
        # print(sentence_data_dict['sent_list'])
        wd_dist,sent_dist_dict = sxpSegSentWord.dualwordsentposdist(newnk, sentence_textset)
      #  print('word dist',wd_dist)
        # score = computeworddistscore(keywordseq, wd_dist)
        nl = len(sentence_textset) / 1.0
        # score = computecloseness(nk, wd_dist,nl)
    #    score = computeclosenesstwo(newnk, wd_dist, nl,version=version) #only score of paper, 20200808 the best one
       # version = 'dual_v6'
        #print('-----this ranking dual sentence and word,version = dual_v6---')
        #----------------------this is to compute closeness-------------------------------
        score,dual_sent_score = dualcomputeclosenesstwo(newnk, wd_dist, nl,version=version)
        #---------------------------------------------------------------------------------
        score_list.append(score)
        idx_sent = list(argsort(-dual_sent_score, axis=0).flat)
        ranked_sent = [sentence_textset[idx] for idx in idx_sent]
        sent_rank_dict= {}
        sent_rank_dict['score']=dual_sent_score
        sent_rank_dict['ranked_sent'] = ranked_sent
        sent_rank_dict['idx_sent'] = idx_sent
        sent_rank_result[fname_dict['fid']]=sent_rank_dict

        wd_dist_fname = outsubdir + '/' + test_name + '_' + fid + '_wdist.pk'
        sxpReadFileMan.SaveObject(sent_rank_dict,wd_dist_fname)
    pr = np.array(score_list).reshape((-1,1))
    idx_s = list(argsort(-pr, axis=0).flat)
    i = 0
    resultid=[]

    for id in idx_s:
        if len(fidlist)>0:
            rid = id;
            fid = fidlist[id]
        else:
            rid = id;

        fname_dict = graph_fname_list[rid]
        fid = fname_dict['fid']

        title = fname_dict['title']
       # print(i, id, score_list[id], title)
        resultid.append((rid,fid, score_list[id], title))
        i = i + 1;
    return resultid,sent_rank_result
def tfidfquerydoclist(test_name, keywordseq, graph_fname_list, outdir, fidlist=[],removestop=True,tfidfmode='tfidf',tfidfbm = None):
    # graph_fname_list = sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir, sxpMultiPaperData.graph_dir)
    # outsubdir = outdir + '/' + test_name+ '/' + tfidfmode
    # sxpReadFileMan.CheckMkEachLevelSub(outsubdir)

    stopwords= stop_words()
    score_list = []
    nk = []

    for each in keywordseq:
        sk = re.split('\s+', each)
        for eachw in sk:
            if len(eachw.strip()) == 0:
                continue
            if removestop:
                if eachw in stopwords:
                    continue
            nk.append(eachw)
    doc_list = []
    print('to be query',nk)
    for fname_dict in graph_fname_list:
        if len(fidlist) > 0:
            if fname_dict['fid'] not in fidlist:
                continue
        #   print('process fid',fname_dict['fid'] )
        # graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        #matrix_dict= fname_dict['matrix_dict']
        sentence_textset = fname_dict['sentence_textset']
        fulltxt = ' '.join(sentence_textset)
        doc_list.append(fulltxt)

    if tfidfmode in ['BM25Okapi', "BM25L", "BM25Plus"]:
        sent_rank_dict = sxpTfidfBM25.RankDoclist(nk,doc_list,testname=tfidfmode,bmmodel=tfidfmode,tfidfbm=tfidfbm)
    else:
        sent_rank_dict = sxpTfidfBM25.RankDoclist(nk,doc_list,testname=tfidfmode,bmmodel=tfidfmode,tfidfbm = tfidfbm)
    pr = sent_rank_dict['doc_score']
  #  print(pr)
  #  idx_s = list(argsort(-pr, axis=0).flat)
    idx_s = sent_rank_dict['idx_sent']
    i = 0
    resultid=[]

    sent_rank_result = {}
    for id in idx_s:
        fname_dict = graph_fname_list[id]
       # graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])
        sentence_textset = fname_dict['sentence_textset']
        title = fname_dict['title']

   #     print(i, id, pr[id,0], title)
        resultid.append((id,fname_dict['fid'], pr[id,0], title))

        if tfidfmode in ['BM25Okapi', "BM25L", "BM25Plus",'tfidf','tfief','dtfipf']:
           # dual_sent_score = sxpMultiPaperData.KeywordQuerySentenceRankOnBM25(nk,fname_dict['fid'], tfidfmode)
            rank_dict = sxpTfidfBM25.RankDoclist(nk, sentence_textset, tfidfmode)
            dual_sent_score = rank_dict['sent_score']
            # sent_rank_dict['doc_score'] = dual_sent_score
            # sent_rank_dict['sent_score'] = dual_sent_score
            # sent_rank_dict['ranked_sent'] = ranked_sent
            # sent_rank_dict['idx_sent'] = idx_sent
        else:
            dual_sent_score = computesentscoreforonepaperindoclist(nk,sentence_textset)

        idx_sent = list(argsort(-dual_sent_score, axis=0).flat)
        ranked_sent = [sentence_textset[idx] for idx in idx_sent]
        sent_rank_dict= {}
        sent_rank_dict['score']=dual_sent_score
        sent_rank_dict['ranked_sent'] = ranked_sent
        sent_rank_dict['idx_sent'] = idx_sent
        sent_rank_result[fname_dict['fid']]=sent_rank_dict

        i = i + 1
    return resultid,sent_rank_result
def densquery(test_name,keywordseq,removestop = True,prefix = [],fidlist=[], version='dens'):
    graph_fname_list = sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir, sxpMultiPaperData.graph_dir)
    outsubdir = sxpMultiPaperData.output_dir + '/' + test_name
    #  sxpReadFileMan.CheckMkDir(outsubdir)

    score_list = []
    newnk = ProcessKeyword(keywordseq, prefix, removestop=removestop)
    print('keyword to be query', newnk)
    sent_rank_result = {}
    for fname_dict in graph_fname_list:
        if len(fidlist) > 0:
            if fname_dict['fid'] not in fidlist:
                continue
        #   print('process fid',fname_dict['fid'] )
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])

        fid = fname_dict['fid']
        if fid == '0051':
            br = 1
        #     print(sentence_data_dict['sent_list'])

        title = graph_dict['title']
        title = re.sub('\:', '_', title)
        # wd_dist = sxpSegSentWord.worddist(nk, sentence_data_dict['sent_list'],skipzero=True)
        # txt = ' '.join(sentence_data_dict['sent_list'])
        # print(sentence_data_dict['sent_list'])
        wd_dist, sent_dist_dict = sxpSegSentWord.dualwordsentposdist(newnk, sentence_data_dict['sent_list'])
        #  print('word dist',wd_dist)
        # score = computeworddistscore(keywordseq, wd_dist)
        nl = len(sentence_data_dict['sent_list']) / 1.0
        # score = computecloseness(nk, wd_dist,nl)
        #    score = computeclosenesstwo(newnk, wd_dist, nl,version=version) #only score of paper, 20200808 the best one

       # print('-----this ranking dual sentence and word,version = dens+span---')
        #score, dual_sent_score = dualcomputeclosenesstwo(newnk, wd_dist, nl, version=version)
        score, dual_sent_score = denscoverscore(newnk, wd_dist, nl, version=version)
      #  print('----------------------------------------------------------------')

        score_list.append(score)
        idx_sent = list(argsort(-dual_sent_score, axis=0).flat)
        ranked_sent = [sentence_data_dict['sent_list'][idx] for idx in idx_sent]
        sent_rank_dict = {}
        sent_rank_dict['score'] = dual_sent_score
        sent_rank_dict['ranked_sent'] = ranked_sent
        sent_rank_dict['idx_sent'] = idx_sent
        sent_rank_result[fname_dict['fid']] = sent_rank_dict

        wd_dist_fname = outsubdir + '/' + test_name + '_' + fid + '_' + title + '_wdist.pk'
    pr = np.array(score_list).reshape((-1,1))
    idx_s = list(argsort(-pr, axis=0).flat)
    i = 0
    resultid = []

    for id in idx_s:
        if len(fidlist) > 0:
            rid = id;
            fid = fidlist[id]
        else:
            rid = id;
            fname_dict = graph_fname_list[rid]
            fid = fname_dict['fid']
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fid)
        title = graph_dict['title']
        # print(i, id, score_list[id], title)
        resultid.append((rid, fid, score_list[id], title))
        i = i + 1;
    return resultid, sent_rank_result
def mmrmaxdf(test_name,keywordseq,removestop = True,prefix = [],fidlist=[], version='mmrmaxdf'):
    graph_fname_list = sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir, sxpMultiPaperData.graph_dir)
    outsubdir = sxpMultiPaperData.output_dir + '/' + test_name
    #  sxpReadFileMan.CheckMkDir(outsubdir)

    score_list = []
    newnk = ProcessKeyword(keywordseq, prefix, removestop=removestop)
    print('keyword to be query', newnk)
    sent_rank_result = {}
    corpus = []
    for fname_dict in graph_fname_list:
        if len(fidlist) > 0:
            if fname_dict['fid'] not in fidlist:
                continue
  #      if fname_dict['fid']!='0110':
  #          continue


        print('process fid',fname_dict['fid'] )
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])
        print('abstract,*************',len(sentence_data_dict['abstract']))
        if len(sentence_data_dict['abstract']) == 0:
            print('no abstract')
            doc = [(1,graph_dict['title'])]
        else:
            doc = sentence_data_dict['abstract']
        docstr = ""
        for each in doc:
            docstr = docstr + each[1] + ' '
        corpus.append(docstr)
        # for sent in sentence_data_dict['abstract']:
        #     print(sent)
        print('conclusion,*************',len(sentence_data_dict['conclusion']))
        if len(sentence_data_dict['conclusion']) == 0:
            print('no conclusion')
        # for sent in sentence_data_dict['conclusion']:
        #     print(sent)
        fid = fname_dict['fid']
        if fid == '0051':
            br = 1
        #     print(sentence_data_dict['sent_list'])

        title = graph_dict['title']
        title = re.sub('\:', '_', title)
        # wd_dist = sxpSegSentWord.worddist(nk, sentence_data_dict['sent_list'],skipzero=True)
        # txt = ' '.join(sentence_data_dict['sent_list'])
        # print(sentence_data_dict['sent_list'])
        wd_dist, sent_dist_dict = sxpSegSentWord.dualwordsentposdist(newnk, sentence_data_dict['sent_list'])
        #  print('word dist',wd_dist)
        # score = computeworddistscore(keywordseq, wd_dist)
        nl = len(sentence_data_dict['sent_list']) / 1.0
        # score = computecloseness(nk, wd_dist,nl)
        #    score = computeclosenesstwo(newnk, wd_dist, nl,version=version) #only score of paper, 20200808 the best one

       # print('-----this ranking dual sentence and word,version = dens+span---')
        #score, dual_sent_score = dualcomputeclosenesstwo(newnk, wd_dist, nl, version=version)
     #   score, dual_sent_score,senttopk = sxpMMR.mmr(" ".join(newnk), sentence_data_dict['sent_list'])
        idx_sent, topkscore, maxdf = sxpMMR.mmr(" ".join(newnk), sentence_data_dict['sent_list'])
      #  print('----------------------------------------------------------------')

     #   score_list.append(score)
     #   idx_sent = list(argsort(-dual_sent_score, axis=0).flat)
        ranked_sent = [sentence_data_dict['sent_list'][idx] for idx in idx_sent]
        sent_rank_dict = {}
        sent_rank_dict['score'] = topkscore
        sent_rank_dict['ranked_sent'] = ranked_sent
        sent_rank_dict['idx_sent'] = idx_sent
        sent_rank_dict['sent_topk'] = maxdf
        sent_rank_result[fname_dict['fid']] = sent_rank_dict

        wd_dist_fname = outsubdir + '/' + test_name + '_' + fid + '_' + title + '_wdist.pk'
    idx_s, topkscore_doc, maxdf_doc = sxpMMR.mmr(" ".join(newnk), corpus)
  #  pr = np.array(score_list)
  #  idx_s = list(argsort(-pr, axis=0).flat)
    i = 0
    resultid = []

    for i,id in enumerate(idx_s):
        if len(fidlist) > 0:
            rid = id;
            fid = fidlist[id]
        else:
            rid = id;
            fname_dict = graph_fname_list[rid]
            fid = fname_dict['fid']
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fid)
        title = graph_dict['title']
        # print(i, id, score_list[id], title)
        resultid.append((rid, fid, topkscore_doc[i], title))

    return resultid, sent_rank_result,maxdf_doc
def tfidfquery(test_name, keywordseq, fidlist=[],removestop=True,tfidfmode='tfidf'):
    graph_fname_list = sxpMultiPaperData.LoadGraphFileName(sxpMultiPaperData.pkdir, sxpMultiPaperData.graph_dir)
    outsubdir = sxpMultiPaperData.output_dir + '/' + test_name
 #   sxpReadFileMan.CheckMkDir(outsubdir)

    stopwords= stop_words()
    score_list = []
    nk = []

    for each in keywordseq:
        sk = re.split('\s+', each)
        for eachw in sk:
            if len(eachw.strip()) == 0:
                continue
            if removestop:
                if eachw in stopwords:
                    continue
            nk.append(eachw)
    if tfidfmode in ['BM25Okapi', "BM25L", "BM25Plus"]:
        pr = sxpMultiPaperData.KeywordQueryOnBM25(nk,tfidfmode)
    else:
        pr = sxpMultiPaperData.AlldocTFIDF(nk,tfidfmode)
  #  print(pr)
    idx_s = list(argsort(-pr, axis=0).flat)
    i = 0
    resultid=[]

    sent_rank_result = {}
    for id in idx_s:
        fname_dict = graph_fname_list[id]
        graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fname_dict['fid'])
        title = graph_dict['title']
   #     print(i, id, pr[id,0], title)
        resultid.append((id,fname_dict['fid'], pr[id,0], title))

        if tfidfmode in ['BM25Okapi', "BM25L", "BM25Plus"]:
            dual_sent_score = sxpMultiPaperData.KeywordQuerySentenceRankOnBM25(nk,fname_dict['fid'], tfidfmode)
        else:
            dual_sent_score = computesentscoreforonepaper(nk,sentence_data_dict)
            dual_sent_score = sxpMultiPaperData.KeywordQuerySentenceRankOnTFIDF(nk,fname_dict['fid'], tfidfmode)
        idx_sent = list(argsort(-dual_sent_score, axis=0).flat)
        ranked_sent = [sentence_data_dict['sent_list'][idx] for idx in idx_sent]
        sent_rank_dict= {}
        sent_rank_dict['score']=dual_sent_score
        sent_rank_dict['ranked_sent'] = ranked_sent
        sent_rank_dict['idx_sent'] = idx_sent
        sent_rank_result[fname_dict['fid']]=sent_rank_dict

        i = i + 1
    return resultid,sent_rank_result

def computesentscoreforonepaper(nk,sentence_data_dict):
    sentscore = []
    for i,st in enumerate(sentence_data_dict['fulltext']):
        sentscore.append(computekeytosent(nk,st))
    return np.array(sentscore).reshape(-1,1)
def computesentscoreforonepaperindoclist(nk,sent_doc_list):
    sentscore = []
    for i,st in enumerate(sent_doc_list):
        sentscore.append(computekeytosent(nk,st))
    return np.array(sentscore).reshape(-1,1)
def computekeytosent(nk,st):
    s = 0
    lst = st.lower()
    sl = len(lst)*1.0
    for eachk in nk:
        g = re.search(eachk.lower(),lst)
        if g:
            s = s + 1
    return s/sl

def AllWordSentMatrix(sent_list):
    word_dict={}
    wdss = []
    for eachsent in sent_list:
    #    wds = eachsent.split('\s+')
        wds = sxpJudgeCharacter.segsenttowords(eachsent)
        wdss.append(wds)
        if len(wds)==0:
            continue
        for wd in wds:
            if word_dict.has_key(wd):
                continue
                word_dict[wd]=word_dict[wd]+1
            else:
                word_dict[wd]=1
    word_idx = {}
    i = 0
    for wd,n in word_dict.items():
        word_idx[wd]=i
        i = i + 1

    nw = len(word_dict)
    w_w = np.zeros((nw,nw))
    for wds in wdss:

        if len(wds) == 0:
            continue
        m = len(wds)
        for i in range(m-1):
            ni =word_idx[wds[i]]
            nj = word_idx[wds[i+1]]
            w_w[nj,ni]=w_w[nj,ni] + 1
    ns = len(sent_list)
    s_s = np.zeros((ns,ns))
    for i, si in enumerate(sent_list):
        for j, sj in enumerate(sent_list):
            ss,s1,s2=computesentdir(si,sj,word_dict)
            if s1 >= s2:
                s_s[j,i]=ss;
            else:
                s_s[i,j]=ss;
    return w_w, s_s
def computesentdir(s1,s2,word_dict):
    stopwords = open('stopwords.txt', 'r').readlines()
    stopwords = []
    word_list1 = []
    word_list2 = []
    si1 = 0
    for word in s1:
        if word not in stopwords:
            word_list1.append(word)
            s1 =s1 + word_dict[word]
    #    print(word_list1)
    si2 = 0
    for word in s2:
        if word not in stopwords:
            word_list2.append(word)
            si2 = si2 + word_dict[word]
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
    return a/b,s1,s2;

def test_extractive():
    testname = 'absext'
    keywordseq = ['extractive summarization']
    print('-----------KeywordRankWordDist', keywordseq)
    idx = KeywordRankWordDist(testname,keywordseq,fidlist=[])

    keywordseq = ['extractive summarization']
    print('-----------KeywordRankCloseWordDist', keywordseq)
    idx = KeywordRankCloseWordDist(testname, keywordseq,prefix=[], fidlist=[])

    keywordseq = ['extractive summarization']
    print('-----------KeywordRankCloseWordDist With Prefix', keywordseq)
    Prefix = ['in this|we|our|this']
    idx = KeywordRankCloseWordDist(testname, keywordseq,prefix=Prefix, fidlist=[])
def testchapter8():
    testname = 'sumeval'
    #summarization evaluation
    #  keywordseq = ['summarization evaluation']
    keywordseq = ['summary evaluation']
    # keywordseq = ['summarization', 'evaluation']
    # keywordseq = ['summary|summarization','evaluation']
    #distversion='v6'#the best score ever since 20200820
    distversion = 'bv7'
    test = 'all'
    if test =='fid':
        #fidlist = ['0015','0074','0044','0027']
        fidlist = ['0012','0002','0035','0045','0094','0089']
        for fid in fidlist:
            print('-----------',fid)
            tfid = [fid]
            print('--------------testquery-------------')
            rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=tfid, version=distversion)
            for each in rankresult:
                print(each)

        # tfid = ['0035','0025','0045','0015']
        # rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=tfid, version=distversion)
        # for each in rankresult:
        #
        #     print(each)
    if test =='all':
        tfid =[]
        rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=tfid, version=distversion)
        for each in rankresult:

            print(each)

    if test == 'makeword':
        # (20, '0020', 3.0, u'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory')
        # (15, '0015', 2.927777777777778, u'Automated Summarization Evaluation with Basic Elements')
        # (14, '0014', 2.898785425101215, u'Assessing sentence scoring techniques for extractive text summarization')
        # (86, '0086', 2.895115332428765,
        #  u'Single-document and multi-document summarization techniques for email threads using sentence compression')
        # (108, '0108', 2.8745572009291522, u'Using Topic Themes for Multi-Document Summarization')
        # (24, '0024', 2.829462659380692,
        #  u'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization')
        # (74, '0074', 2.818276807125728, u'QARLA:A Framework for the Evaluation of Text Summarization Systems')
        # (80, '0080', 2.818036529680365, u'ROUGE_ a package for automatic evaluation of summaries')
        #fidlist=['0020','0015','0086','0108']
        #fidlist=['0012', '0002', '0035', '0045', '0094', '0089']
        fidlist = ['0012', '0002', '0035', '0045', '0094', '0089']
      #  fidlist = ['0094', '0089']
        #  fidlist = ['0012',  '0089']
        MakeWordDist(testname,keywordseq,fidlist,version='bv7')
def test_chapter4237():
    testname = 'sumeval'
    #summarization evaluation
    #  keywordseq = ['summarization evaluation']
    keywordseq = ['Graph-based extractive summarization by considering importance, non-redundancy and coherence']
    # keywordseq = ['summarization', 'evaluation']
    # keywordseq = ['summary|summarization','evaluation']
    #distversion='v6'#the best score ever since 20200820
    distversion = 'v6'
    test = 'makeword'
    if test =='fid':
        #fidlist = ['0015','0074','0044','0027']
        fidlist = ['0093','0051','0030']
        for fid in fidlist:
            print('-----------',fid)
            tfid = [fid]
            print('--------------testquery-------------')
            rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=tfid, version=distversion)
            for each in rankresult:
                print(each)

        # tfid = ['0035','0025','0045','0015']
        # rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=tfid, version=distversion)
        # for each in rankresult:
        #
        #     print(each)
    if test =='all':
        tfid =[]
        rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=tfid, version=distversion)
        for each in rankresult:

            print(each)

    if test == 'makeword':
        # (20, '0020', 3.0, u'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory')
        # (15, '0015', 2.927777777777778, u'Automated Summarization Evaluation with Basic Elements')
        # (14, '0014', 2.898785425101215, u'Assessing sentence scoring techniques for extractive text summarization')
        # (86, '0086', 2.895115332428765,
        #  u'Single-document and multi-document summarization techniques for email threads using sentence compression')
        # (108, '0108', 2.8745572009291522, u'Using Topic Themes for Multi-Document Summarization')
        # (24, '0024', 2.829462659380692,
        #  u'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization')
        # (74, '0074', 2.818276807125728, u'QARLA:A Framework for the Evaluation of Text Summarization Systems')
        # (80, '0080', 2.818036529680365, u'ROUGE_ a package for automatic evaluation of summaries')
        #fidlist=['0020','0015','0086','0108']
        #fidlist=['0012', '0002', '0035', '0045', '0094', '0089']
        fidlist = ['0093','0051','0030']
      #  fidlist = ['0094', '0089']
        #  fidlist = ['0012',  '0089']
        MakeWordDist(testname,keywordseq,fidlist,version=distversion)
def test_chapter421():
    testname = 'testchapter421'
    # fidlist=['0102']
    #fidlist = []
    # fidlist = ['0057','0102']
    fidlist = ['0027', '0102']
    #keywordseq = ['Topic aspect  summarization  selection  groups']
    keywordseq = ['Topic aspect']
    rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=fidlist,version='v1')
    for each in rankresult:
        print(each)
    print('------------',testname)
    rankresult = KeywordRankCloseWordDist(testname, keywordseq, prefix=[], fidlist=fidlist,version='v5')
    for each in rankresult:
        print(each)
    MakeWordDist(testname, keywordseq, fidlist, version='v5')
def test_tfidf():
    testname = 'absext'
    keywordseq = ['extractive summarization']
    print('-----------tfidfquery', keywordseq)
    idx = tfidfquery(testname,keywordseq)
def test_keywordrank():
    testname = 'absext'
    keywordseq=['extractive summarization']
    print('-----------KeywordRankWordDist',keywordseq)
  #  idx = KeywordRankWordDist(testname,keywordseq,fidlist=[])
    print('-----------KeywordRankCloseWordDist', keywordseq)
    keywordseq = ['summarization extractive ']
    idx = KeywordRankCloseWordDist(testname,keywordseq,prefix=[],fidlist=[])
    keywordseq=['abstractive summarization']
    print('-----------KeywordRankWordDist',keywordseq)
 #   idx = KeywordRankWordDist(testname,keywordseq,fidlist=[])
    print('-----------KeywordRankCloseWordDist', keywordseq)
    idx = KeywordRankCloseWordDist(testname, keywordseq,prefix=[], fidlist=[])

    # keywordseq=['extractive summarization']
    # print('-----------',keywordseq)
    # idx = KeywordRankWordDist(testname,keywordseq,fidlist=[])
    #
    # keywordseq=['abstractive summarization']
    # print('-----------',keywordseq)
    # idx = KeywordRankWordDist(testname,keywordseq,fidlist=[])
def TestKeywordRank1():
    testname = 'extractive1'
    keywordseq=['extractive|extraction']
    print('-----------',keywordseq)
    idx = KeywordRankWordDist(testname,keywordseq,fidlist=[])

    # keywordseq=['abstractive|abstraction']
    # print('-----------', keywordseq)
    # idx = KeywordRankWordDist(testname, keywordseq, fidlist=[])
    #
    # keywordseq=['summarization','extractive|extraction']
    # print('-----------',keywordseq)
    # idx = KeywordRankWordDist(testname,keywordseq,fidlist=[])
    #
    # keywordseq=['summarization','abstractive|abstraction']
    # print('-----------', keywordseq)
    # idx = KeywordRankWordDist(testname, keywordseq, fidlist=[])

def test_extabs():
    testname = 'extabs'
    keywordseq=['summarization','method','extractive','abstractive']
    sxpMultiPaperData.MakeWordDist(testname,keywordseq,fidlist=[])
def test_ext_abs():
    testname = 'absext'
    keywordseq=['extractive|extraction','abstractive|abstraction']

    sxpMultiPaperData.MakeWordDist(testname,keywordseq,fidlist=[])
    fidlist = []
    wdlist=sxpMultiPaperData.LoadWdDist(testname,fidlist)
    makexdict = True
    if makexdict:
        MakeSentXDict(wdlist[1])

        # ClusterSent(wdlist[1])
        clustersent = False
        for i, wd_dist_tuple in enumerate(wdlist):

            line = 'h'
            MakeSentXDict(wd_dist_tuple,line)
            MakeShowWdKeyDist(wd_dist_tuple)
            if clustersent:
                if line == 'v':
                    ClusterSentPara(wd_dist_tuple,line)
                if line == 'h':
                    ClusterSentKeyTest(wd_dist_tuple,'h')
    else:
        for wd_dist_tuple in wdlist:

            ClusterSentPara(wd_dist_tuple,'h')
def test_cluster_extabs():
    testname = 'extabs'
    keywordseq=['summarization','method','extractive','abstractive']
  #  sxpMultiPaperData.MakeWordDist(testname,keywordseq,fidlist=[])
    fidlist = []
    wdlist=sxpMultiPaperData.LoadWdDist(testname,fidlist)
    makexdict = True
    if makexdict:
        # MakeSentXDict(wdlist[1])
        # ClusterSent(wdlist[1])
        for i, wd_dist_tuple in enumerate(wdlist):
            line = 'v'
            MakeSentXDict(wd_dist_tuple,line)
            if line == 'v':
                ClusterSentPara(wd_dist_tuple,line)
            if line == 'h':
                ClusterSentKeyTest(wd_dist_tuple,'h')
    else:
        for wd_dist_tuple in wdlist:

            ClusterSentPara(wd_dist_tuple,'h')
def test_extabs1():
    testname = 'extabs1'
    keywordseq=['summarization','method','extract','abstract']
    sxpMultiPaperData.MakeWordDist(testname,keywordseq,fidlist=[])
def testshow_extabs():
    #testname ='extrative'
    testname = 'extabs1'
 #   fidlist = ['0000', '0001', '0004','0005','0008', '0010']
    fidlist = []
    wdlist=sxpMultiPaperData.LoadWdDist(testname,fidlist)
    for each in wdlist:
        MakeShowWdKeyDist(each)
def test_graphml():
    testname = 'graphml'
    keywordseq=['summarization','method','graph|network','machine\s+learning']
    sxpMultiPaperData.MakeWordDist(testname,keywordseq,fidlist=[])
def testshow_graphml():
    #testname ='extrative'
    testname = 'graphml'
 #   fidlist = ['0000', '0001', '0004','0005','0008', '0010']
    fidlist = []
    wdlist=sxpMultiPaperData.LoadWdDist(testname,fidlist)
    for each in wdlist:
        MakeShowWdKeyDist(each)
def RankOnePaper(fid,chid,keywords,survgenmethod,prefix = [],removestop = True):
    graph_dict, matrix_dict, sentence_data_dict = sxpMultiPaperData.LoadFileData(fid)

    title = graph_dict['title']
    title = re.sub('\:', '_', title)
    newnk = ProcessKeyword(keywords, prefix,removestop=removestop)
    print('keyword to be query', newnk)
    # wd_dist = sxpSegSentWord.worddist(nk, sentence_data_dict['sent_list'],skipzero=True)
    # txt = ' '.join(sentence_data_dict['sent_list'])
    # print(sentence_data_dict['sent_list'])
    #wd_dist = sxpSegSentWord.wordsentposdist(newnk, sentence_data_dict['sent_list'])
    #  print('word dist',wd_dist)
    # score = computeworddistscore(keywordseq, wd_dist)
    #nl = len(sentence_data_dict['sent_list']) / 1.0
    # score = computecloseness(nk, wd_dist,nl)
    rank_sent_result = computersent2titlesim(newnk,sentence_data_dict['sent_list'])
    paper_sent_result = {}
    paper_sent_result['fid']=fid
    paper_sent_result['chname'] = chid
    paper_sent_result['survgenmethod'] = survgenmethod
    paper_sent_result['ranksent']=rank_sent_result
    return paper_sent_result
def computersent2titlesim(titlekey_list,sent_list):
    title = ' '.join(titlekey_list)
    score_list = []
    for eachsent in sent_list:
        score = sxpSegSentWord.jaccard_similarity(eachsent,title)
        score_list.append(score)


    pr = np.array(score_list).reshape((-1,1))
    idx_s = list(argsort(-pr, axis=0).flat)
    i = 0
    resultid=[]

    for rid in idx_s:
        resultid.append((rid,sent_list[rid]))

    return resultid
if __name__=="__main__":
    #WordDistTest()
 #   testcase()
    #testshow()

  #  test_extabs1()
  #  testshow_extabs()
 #    test_graphml()
  #  testshow_graphml()

    #test_cluster_extabs()
    #    test_ext_abs()
    # TestKeywordRank1() #20200529 this make textrank higher score
   # test_keywordrank() #20200529 this still work
    #test_extractive()
  #  testchapter8()
    test_chapter4237()
  #  test_chapter421()
    #test_tfidf() #20200630
    # ListPaperTitle()