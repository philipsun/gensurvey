# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 00:19:43 2018

@author: sunxp
@new bsd licence
"""

#-------------------------------------------------------------------------------
# Name:        sxpTestACLSum.py
# Purpose:
#
# Author:      sunxp
#
# Created:     22/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re


import sys
sys.path.append('./context')

import sxpTestACLSum
import sxpModelDucHybrid
import sxpModelSmallSent
import sxpModelSmallSentSeq
def main():
    #TestDemo() #ok
    #TestA()
    TestWordNetLen()

def TestWordNetLen():
    project_name = 'acl2014exc'
    test_case = 'lentest'  # this is to include the abstract and conclusion in the paper
    model_idname = GetAlphaModelID()
    # *******************hao to run the test***************************
    # model_test = GetConfigwdnet()
    model_test,cmstr = GetConfigwdnetU()
    # model_test = Get300()
    #cmstr = 'rs'
    if cmstr =='mrs':
        cmd = ['makemodel', 'rank', 'score']  # -**----+
    if cmstr =='rs':
        cmd = ['rank','score']
    if cmstr =='s':
        cmd = [ 'score']  # -**----+
    #cmd = ['score']
    sxpTestACLSum.TestModel(project_name, model_idname, test_case, model_test, cmd, RankDocDemoWordNet,data_case='exc')

def GetModelID():

    idname={'abstract': '01', 'conclusion': '02', 'wordnetwork': '03', 'wss100k': '04', 'wss100': '05',
     'wordnetwork200': '06',
     'wss200k': '07',
     'wss200': '08',
     'wordnetwork300': '09',
     'wss300k': '10',
     'wss300': '11',
      'wordnetwork300u':'12',
      'wss300ku': '13',
      'wss300u': '14',
     }
    return idname
def GetAlphaModelID():
    idname = {
        'wss300':'01',
        'wss400':'02',
        'wss500':'03',
        'wd300': '04',
        'wd400': '05',
        'wd500': '06',
        'wss300u': '07',
        'wss400u': '08',
        'wss500u': '09',
        'wd300u': '10',
        'wd400u': '11',
        'wd500u': '12',
        'wsseq300u':'13',
        'wsseq400u':'14',
        'wsseq500u':'15',
        'wsseq300': '16',
        'wsseq400': '17',
        'wsseq500': '18'
    }
    return idname
def GetConfigwdnet():

 #   model_test =['wss300','wss400','wss500','wd300','wd400','wd500']
    #  model_test =['wd300','wd400','wd500']
    model_test = ['wsseq300', 'wsseq400', 'wsseq500']
    return model_test
def GetConfigwdnetU():
    #model_test =['wss300u','wss400u','wss500u','wd300u','wd400u','wd500u']
  #  model_test = ['wsseq300u', 'wsseq400u', 'wsseq500u']
    model_test = ['wsseq300', 'wsseq400', 'wsseq500']
    # model_test = ['wss300','wss400','wss500','wd300','wd400','wd500','wsseq300', 'wsseq400', 'wsseq500']
    #  model_test =['wdnet1']
    cmdstr='rs'
    return model_test, cmdstr
def matchtestname(testname):
    mode_dict= {}
    mode_dict['ws_pr']=r'wss(\d+)(u?)(k?)'
    mode_dict['wd_ss']=r'wd(\d+)(u?)(k?)'
    mode_dict['ws_seq_pr']=r'wsseq(\d+)(u?)(k?)'
    for eachmode, pat in list(mode_dict.items()):
        g = re.match(pat, testname)
        if g is not None:
            return eachmode,g

    return None,None

def ParseTest(testname):
    topk = -1
    maxword = 300
    remove_stopwords = 0
    undirect = 0

    mode,g =matchtestname(testname)

    if g:
        g = g.groups()
        if len(g[0])==0:
            maxword = 300
        else:
            maxword = int(g[0])
        if len(g[1])>0:
            if g[1]=='u':
                undirect = 1
            else:
                undirect = 0
            if g[1]=='k':
                remove_stopwords = 1
            else:
                remove_stopwords = 0
        else:
            undirect = 0
        if len(g[2])>0:
            if g[2]=='k':
                remove_stopwords = 1
            else:
                remove_stopwords = 0
        else:
            remove_stopwords = 0
    para ={}
    para['undirect'] = undirect #so when 0, the graph is directed, when 1, the graph will be undirected
    para['remove_stopwords'] = remove_stopwords
    para['addseq'] = 0
    para['mode'] = mode #'wd_ss'
    para['alphabeta'] = [0.6, 0.4]
    para['maxword'] = maxword
    para['topk'] = topk  # -1 means that not to use top k sents, but use maxword mode

    return para

def RankDocDemoWordNet(eachtest,sxptxt):
    para = ParseTest(eachtest)
    print(para)

    if para['mode'] == 'ws_seq_pr':
        topk = para['topk']
        maxword = para['maxword']
        remove_stopwords = para['remove_stopwords']
        undirect = para['undirect']
        #tops = GetWSTop(sxptxt, topk, maxword=maxword, remove_stopwords=remove_stopwords, undirect=undirect)
        tops = GetWSSeqTop(sxptxt, topk, maxword=maxword, remove_stopwords=remove_stopwords, undirect=undirect)
        return tops

    if para['mode']=='ws_pr':
        topk = para['topk']
        maxword = para['maxword']
        remove_stopwords = para['remove_stopwords']
        undirect = para['undirect']
        tops = GetWSTop(sxptxt, topk, maxword=maxword, remove_stopwords=remove_stopwords, undirect=undirect)
        return tops
    if para['mode']=='wd_ss':
        topk = para['topk']
        maxword = para['maxword']
        remove_stopwords = para['remove_stopwords']
        undirect = para['undirect']
        alphabeta = para['alphabeta']
        tops = GetWordNetHybrid(sxptxt, topk, maxword=maxword, remove_stopwords=remove_stopwords, undirect=undirect, alphabeta=alphabeta, addseq=0)
        return tops

    return None

def GetWordNetHybrid(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0, alphabeta=[0.6, 0.4],addseq=0):
    mode = "wd_ss"  # 0.5

    sxpModelDucHybrid.global_para['undirect']=undirect
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['mode'] = mode
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['alpha_beta'] =alphabeta# [0.6, 0.4]
    sxpModelDucHybrid.global_para['maxword'] = maxword  # [0.6, 0.4]
    sxpModelDucHybrid.global_para['topksent'] = topk
    model = sxpModelDucHybrid.WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops

def GetTHS100(sxptxt, topk, maxword=100, remove_stopwords=0):
    mode = "ss_hits" #0.5
    model = sxpModelSmallSent.SmallSent(sxptxt,undirect=1,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
    topksent = -1
    useabstr = 0

    strictmax=0

    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    return tops
def GetSSTop(sxptxt, topk, maxword=100, remove_stopwords=0):
    mode = "ss_dir_pr" #0.5
     # mode ="ss_seq_pr" #0.49
    model = sxpModelSmallSent.SmallSent(sxptxt,undirect=1,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
    topksent = -1
    useabstr = 0

    strictmax=0
    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    return tops
def GetWSTop(sxptxt,topk,maxword=-1,remove_stopwords=1,undirect=0):

    mode= "ws_pr"
    sxpModelSmallSent.global_para['undirect']=undirect
    sxpModelSmallSent.global_para['remove_stopwords'] = remove_stopwords
    sxpModelSmallSent.global_para['mode'] = mode
    sxpModelSmallSent.global_para['addseq'] = 0
    sxpModelSmallSent.global_para['alpha_beta'] = [0.6, 0.4]
    model = sxpModelSmallSent.SmallSent(sxptxt,undirect=undirect,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
    topksent = topk#-1
    useabstr = 0

    strictmax=0
    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    return tops
def GetWSSeqTop(sxptxt,topk,maxword=300,remove_stopwords=0,undirect=1):

    mode= "ws_seq_pr"
    sxpModelSmallSentSeq.global_para['undirect']=undirect
    sxpModelSmallSentSeq.global_para['remove_stopwords'] = remove_stopwords
    sxpModelSmallSentSeq.global_para['mode'] = mode
    sxpModelSmallSentSeq.global_para['addseq'] = 0
    sxpModelSmallSentSeq.global_para['alpha_beta'] = [0.6, 0.4]
    model = sxpModelSmallSentSeq.SmallSentSeq(sxptxt,undirect=undirect,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
    topksent = topk#-1
    useabstr = 0

    strictmax=0
    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    return tops
def GetAbsConSent(abs_con):
    con_sent = abs_con.split('.**.\n')
    con_sent_f =[]
    for s in con_sent:
        s = s.strip()
        if len(s)==0:
            continue
        else:
            con_sent_f.append(s)
    return con_sent_f
def teststring():
    ptwd = r'wd(\d+)(u?)(k?)'
    testname = 'wss300u'
    g = re.match(ptwd, testname)

    if g:
        print((g.groups()))
    mdname = GetConfigwdnet()
    for each in mdname:
        para = ParseTest(each)
        print(para)
if __name__ == '__main__':
    main()
  #  teststring()
