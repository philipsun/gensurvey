# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 00:19:43 2018

@author: sunxp
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
import os
import sxpReadFileMan

import numpy as np

##import sys
##sys.path.append('./context')
from context import sxpdorank
import context.sxpPackage
from context.sxpPackage import *

import sxpPyrougeEvaluate
import sxpParseRougeScore
import sxpRankingDoc
import sxpModelFileMan
import sxpLoadRankPara
from sxpLoadRankPara import GetFName
import sxpJudgeCharacter

import sxpTestMan
import sxpDataDUCSum
from sxpDataDUCSum import sxpNode
import sxpModelDucHybrid
import sxpModelSmallSent
import sxpModelSmallSubsent
def main():
    TestDemo()
def TestDemo():
    project_name = 'duc2002single'
    test_case = 'singledir'
    idname ={
              'top5':'01',
              'top4':'02',
              'random':'03',
              'manual100':'04',
              'wss':'06',
              'top100':'07',
              'wss100':'08',#remove keywords, no more than 100 words
              'wss100k':'09',# do not remove keywords, no more than 100 words
              'top6':'10',
              'submit27':'11',#this is to test submitted peers with id 27
              'submit29': '12',#this is to test submitted peers with id 29
              'ss100':'13', #this use s-s matrix with pagerank
              'ths100':'14',#this use a trained sequence rank and a hits rank to rank sentence using sxpModelLenTopPred.py
              'wordnetwork':'15',#this use a small-word word network with a sent-sent network
              'subsentnet':'16', #this use
              'wordnetworkk':'17',  # this use
              'wss100u':'18',  # this use
              'wss100uk': '19',  # this use
              'wordnetworku': '20',  # this use
              'wordnetworkuk': '21',  # this use
        'wordnetworkback100': '22',
        'wordnetworkendfirst': '23',
        'wordnetworkfrondend': '24',
        'endfront_debug': '25',
        'endfront_debugk': '26',

        # this use

    }
    model_idname = idname#sxpRougeConfig.idname
 #   model_test =['wss100']
 #   model_test = ['subsentnet']
  #  model_test = ['manual100','wss','wss100','wss100k','ss100','wordnetwork']
     #this is to rank_parameter dict for this demo:
    # model_test = [ 'wordnetwork', 'wordnetworkk','wss100','wss100k',
    #                'wordnetworkback100',
    #                 'wordnetworkendfirst',
    #                 'wordnetworkfrondend',
    #                 'endfront_debug',
    #                'endfront_debugk',
    # ]
    model_test = [ 'wss100','wss100k','wordnetwork','wordnetworkk',
                   'endfront_debug','endfront_debugk',
    ]
                   #    model_test = [ 'endfront_debug']
    #   model_test = ['ss100','wordnetworkk']
    #cmd = ['rank','score']
   # cmd = ['makemodel', 'rank', 'score']
    cmd = ['rank', 'score']
  #  cmd = ['rank', 'score']
    rankmethod=RankDocDemo
    TestModel(project_name,test_case,model_idname,model_test,cmd,rankmethod)
def MakePaperPara(project_name,test_case_name,idname,model_test,model_file_case,system_file_case):
    # In this

    fname_dict=GetFName(project_name,test_case_name)
    main_dir = fname_dict['main_dir']
    sxpReadFileMan.CheckMkDir(main_dir)
  #  test_case_name= main_dir+'/' + test_case_name
    test_dir =   fname_dict['test_dir']
    sxpReadFileMan.CheckMkDir(test_dir)
    model_dir =  fname_dict['model_dir']
    system_dir = fname_dict['system_dir']
    pk_dir =  fname_dict['pk_dir']
    out_dir = fname_dict['out_dir']
    conf_path = fname_dict['conf_path']
    sxpReadFileMan.CheckMkDir(model_dir)
    sxpReadFileMan.CheckMkDir(system_dir)
    sxpReadFileMan.CheckMkDir(pk_dir)
    sxpReadFileMan.CheckMkDir(out_dir)
    rouge_dir =r'./ROUGE-1.5.5/RELEASE-1.5.5'
#    rouge_dir =cwd + sxpLoadRankPara.rouge_path
    perl_path = sxpLoadRankPara.perl_path

    rank_para={
        'idname':idname,
        'useabstr':0,
        'maxword' : -1,
        'strictmax': 0,
        'topksent': 5,
        'outdir': out_dir, # this is to store rouge score out puts and figures #os.path.join(system_dir,'duc_withstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        'rougetxthead':test_case_name,#'duc_withstop_topk',
        'model_test':model_test,#['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        'plotwho':test_case_name,#'duc',
        'conf_path':conf_path,
        'dataroot':main_dir,
        "pickle_path" : pk_dir,
        "model_path": model_dir,
        "rouge_dir": rouge_dir,
        "perl_path": perl_path,
        "system_path" : system_dir, #this is to store each system file produced by ranking models
        'modelpattern':  r'{0}_#ID#.[A-Z].html'.format(model_file_case),
        'systempattern': r'{0}_([A-Za-z0-9\-]+).html'.format(system_file_case),
        'model_filenames_pattern_id' : r'{0}_([A-Za-z0-9\-]+).[A-Z].html'.format(model_file_case),
        'system_filename_pattern_id' : r'{0}_#ID#.html'.format(system_file_case),
        'pickle_file_pattern_id' :r'{0}_#ID#.pk'.format(test_case_name), # inc_test
        'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    rankpara_fname = test_dir +'/rank_para.pk'
    sxpReadFileMan.StoreSxptext(rank_para,rankpara_fname)
    return rank_para

notethat ='''
model_file_list are read from model director, but model_file_name_pattern is made by test_case name,
so, when you change test case name, model_file_name_pattern is changed, but the actual model_file_names
are not changed in model dir, so when runing pyrouge, it use new model_file_name with new test_case_naem, but 
those in model_dire still not changed, in this case, it will go wrong. you need to keep model_file_patten-name
for different test_cases. So, I need to set model_file_pattern
'''#note that
def TestModel(project_name,test_case,model_idname,model_test,cmd,rankmethod):
    model_file_case=project_name
    system_file_case = test_case
    rank_para = MakePaperPara(project_name, test_case, model_idname, model_test,model_file_case,system_file_case)

    #cmd = ['makemodel','rank','score']
    #cmd = ['rank','score']
  #  cmd = ['rank','score']
  #  cmd = ['score']
    if 'makemodel' in cmd:
        #this is to make model files for a set of inputting model files:
        print(('make model files for ',project_name,'test_case', test_case,'***************'))
        doc_model_sent_file_list = sxpDataDUCSum.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        sxpTestMan.DoMakeModel(project_name,test_case,doc_model_sent_file_list)
    if 'rank' in cmd:
        #this is to make a testing top-k sentences for the two test methods, they are the same
        print(('make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************'))
      #  model_test_output_dict=ProduceTestRank(project_name,test_case,model_test)
        model_test_output_dict=ProduceTestRankByRankPara(project_name,test_case,model_test,rankmethod,rank_para)
    #    print(model_test_output_dict)
    #in this case, the producetestrankbyrankpara already save it to the path
    #    sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)
    if 'score' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
       # rankcmd = 'plot'
        print(('project ', project_name, 'test_case', test_case, '***************'))
        for k, v in list(rank_para.items()):
            print((k, v))
        rankcmd = 'all'
        sxpTestMan.DoRougeScore(project_name,test_case,cmd=rankcmd)


def RankDocDemo(eachtest,sxptxt):
    tops = []
    if eachtest == 'abstract':
        for eachsent in GetAbsConSent(sxptxt.abstract):
            tops.append(eachsent)
    if eachtest == 'conclusion':
        for eachsent in GetAbsConSent(sxptxt.conclusion):
            tops.append(eachsent)
    if eachtest == 'top6':
         tops = GetTopK(sxptxt,6)
    if eachtest == 'top5':
         tops = GetTopK(sxptxt,5)
    if eachtest == 'top4':
         tops = GetTopK(sxptxt,4)
    if eachtest == 'random':
        tops = GetRandom(sxptxt,4)
    if eachtest == 'wss':
        tops = GetWSTop(sxptxt,-1,maxword=100)
    if eachtest =='top100':
        allsent = sxptxt.sentence_textset
        tops = GetMaxword(allsent,maxword=100)
    if eachtest == 'wss100':
        tops = GetWSTop(sxptxt,-1,maxword=100,remove_stopwords=1,undirect=0)
    if eachtest =='wss100k':
        tops = GetWSTop(sxptxt,-1,maxword=100,remove_stopwords=0,undirect=0)
    if eachtest == 'wss100u':
        tops = GetWSTop(sxptxt,-1,maxword=100,remove_stopwords=1,undirect=1)
    if eachtest =='wss100uk':
        tops = GetWSTop(sxptxt,-1,maxword=100,remove_stopwords=0,undirect=1)
    if eachtest == 'ss100':
        tops = GetSSTop(sxptxt, -1, maxword=100, remove_stopwords=1)
    if eachtest == 'ths100':
        tops = GetTHS100(sxptxt,4, maxword=100, remove_stopwords=1)
    if eachtest == "wordnetwork":
        tops = GetWordNetHybrid(sxptxt,-1, maxword=100, remove_stopwords=0)
    if eachtest == "wordnetworku":
        tops = GetWordNetHybrid(sxptxt,-1, maxword=100, remove_stopwords=0,undirect=1)
    if eachtest == 'wordnetworkk':
        tops = GetWordNetHybrid(sxptxt,-1, maxword=100, remove_stopwords=1)

    if eachtest == 'subsentnet':
        tops = GetSubSentNetwork(sxptxt,4, maxword=100, remove_stopwords=1)

    #print(tops)
    if eachtest == 'wordnetworkback100':
        print(eachtest)
        tops = GetWordNetHybridBackword(sxptxt, -1, maxword=100, remove_stopwords=0, undirect=0)
    if eachtest == 'wordnetworkendfirst':
        print('wordnetworkendfirst')
        tops = GetWordNetHybridEndfirst(sxptxt, -1, maxword=100, remove_stopwords=0, undirect=0)
    if eachtest == 'wordnetworkfrondend':
        print('wordnetworkfrondend')
        tops = GetWordNetHybridEndFront(sxptxt, -1, maxword=100, remove_stopwords=0, undirect=0)
    if eachtest == 'endfront_debug':
        print('endfront_debug')
        tops = GetWordNetHybridEndFrontDebug(sxptxt, -1, maxword=100, remove_stopwords=0, undirect=0)
    if eachtest == 'endfront_debugk':
        print('endfront_debug')
        tops = GetWordNetHybridEndFrontDebug(sxptxt, -1, maxword=100, remove_stopwords=1, undirect=0)
    return tops
def GetWordNetHybridBackword(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5
    sxpModelDucHybrid.global_para['undirect'] = undirect
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['mode'] = 'wd_ss'
    sxpModelDucHybrid.global_para['alpha_beta'] = [0.8, 0.2]
    sxpModelDucHybrid.global_para['maxword'] = maxword
    sxpModelDucHybrid.global_para['topksent'] = topk
    sxpModelDucHybrid.global_para['sent_dir'] = 'frontfirst'
    sxpModelDucHybrid.global_para['transpose'] = True
    model = sxpModelDucHybrid.WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops
def GetWordNetHybridEndFront(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5
    sxpModelDucHybrid.global_para['undirect'] = undirect
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['mode'] = 'wd_ss'
    sxpModelDucHybrid.global_para['alpha_beta'] = [0.8, 0.2]
    sxpModelDucHybrid.global_para['maxword'] = maxword
    sxpModelDucHybrid.global_para['topksent'] = topk
    sxpModelDucHybrid.global_para['sent_dir'] = 'endfront'
    sxpModelDucHybrid.global_para['transpose'] = False
    model = sxpModelDucHybrid.WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops
def GetWordNetHybridEndFrontDebug(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5
    sxpModelDucHybrid.global_para['undirect'] = undirect
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['mode'] = 'wd_ss'
    sxpModelDucHybrid.global_para['alpha_beta'] = [0.8, 0.2]
    sxpModelDucHybrid.global_para['maxword'] = maxword
    sxpModelDucHybrid.global_para['topksent'] = topk
    sxpModelDucHybrid.global_para['sent_dir'] = 'endfront_debug'
    sxpModelDucHybrid.global_para['transpose'] = False
    model = sxpModelDucHybrid.WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops
def GetWordNetHybridEndfirst(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5
    sxpModelDucHybrid.global_para['undirect'] = undirect
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['mode'] = 'wd_ss'
    sxpModelDucHybrid.global_para['alpha_beta'] = [0.8, 0.2]
    sxpModelDucHybrid.global_para['maxword'] = maxword
    sxpModelDucHybrid.global_para['topksent'] = topk
    sxpModelDucHybrid.global_para['sent_dir'] = 'endfirst'
    sxpModelDucHybrid.global_para['transpose'] = False
    model = sxpModelDucHybrid.WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops
def GetSubSentNetwork(sxptxt, topk, maxword=100, remove_stopwords=0):
    mode = "wd_ss"  # 16 ROUGE-1 Average_R: 0.48299 (95%-conf.int. 0.47534 - 0.49006)
    model = sxpModelSmallSubsent.SubSentWordNetwork(sxptxt, undirect=1, remove_stopwords=remove_stopwords, iteration_times=30,
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
def GetSSTop(sxptxt, topk, maxword=100, remove_stopwords=0,undirect= 0, alpha_beta=[0.5, 0.5]):
    mode = "ss_dir_pr" #0.5
     # mode ="ss_seq_pr" #0.49
    sxpModelSmallSent.global_para = {}
    sxpModelSmallSent.global_para['undirect'] = undirect
    sxpModelSmallSent.global_para['remove_stopwords'] = remove_stopwords
    sxpModelSmallSent.global_para['addseq'] = 0
    sxpModelSmallSent.global_para['mode'] = mode
    sxpModelSmallSent.global_para['alpha_beta'] = alpha_beta
    sxpModelSmallSent.global_para['maxword'] = maxword
    sxpModelSmallSent.global_para['topksent'] = topk

    model = sxpModelSmallSent.SmallSent(sxptxt,undirect=1,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
    topksent = -1
    useabstr = 0

    strictmax=0
    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    return tops
def GetWSTop(sxptxt,topk,maxword=-1,remove_stopwords=1,undirect=0,alpha_beta=[0.5, 0.5]):

    mode= "ws_pr"
    sxpModelSmallSent.global_para = {}
    sxpModelSmallSent.global_para['undirect'] = undirect
    sxpModelSmallSent.global_para['remove_stopwords'] = remove_stopwords
    sxpModelSmallSent.global_para['addseq'] = 0
    sxpModelSmallSent.global_para['mode'] = mode
    sxpModelSmallSent.global_para['alpha_beta'] = alpha_beta
    sxpModelSmallSent.global_para['maxword'] = maxword
    sxpModelSmallSent.global_para['topksent'] = topk

    model = sxpModelSmallSent.SmallSent(sxptxt,undirect=1,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
    topksent = topk#-1
    useabstr = 0

    strictmax=0
    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    return tops

def GetWordNetHybrid(sxptxt, topk, maxword=100, remove_stopwords=0,undirect = 0):
    mode = "wd_ss"  # 0.5

    sxpModelDucHybrid.global_para['undirect'] = undirect #so when 0, the graph is directed, when 1, the graph will be undirected
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['mode'] = mode
    sxpModelDucHybrid.global_para['alpha_beta'] = [0.8, 0.2]
    sxpModelDucHybrid.global_para['maxword'] = maxword
    sxpModelDucHybrid.global_para['topksent'] = topk  # -1 means that not to use top k sents, but use maxword mode
    model = sxpModelDucHybrid.WordNetwork(sxptxt, undirect=1, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops
def GetRandom(sxptxt,topk):

    n = len(sxptxt.sentence_textset)
    rd = np.random.choice(n,topk)
    tops=[]
    for i in rd:
        tops.append(sxptxt.sentence_textset[i])
    return tops
def GetTopK(sxptxt,topk):
    tops = []
    for i, s in enumerate( sxptxt.sentence_textset[0:topk]):
        tops.append(s)
    return tops

def GetMaxword(tops,maxword=100):
    ss =[]
    n = 0
    for sent in tops:
        wd = sxpJudgeCharacter.segsenttowords(sent)
        if len(wd)==0:
            continue
        n = n + len(wd)
        if n>=maxword:
            break
        ss.append(sent)
    return ss
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

def ProduceTestRankByRankPara(project_name,test_case,testset,rankmethod,rank_para):
    fname_dict = GetFName(project_name, test_case)
    # rankpara_fname = fname_dict['rankpara_fname']
    # rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)
    #   rank_para = MakePaperPara(project_name,test_case,idname,model_test)
    model_dir = fname_dict['model_dir']  # r'./test/demo/model'

    # this is from sxpTestMan.PrepareModelForRawSentencePk()
    model_file_list = sxpReadFileMan.LoadSxptext(fname_dict['model_file_list'])
    modelidname = rank_para['idname']
    pickle_path = rank_para['pickle_path']  # 'papers\duc\txt\pickle')
    model_path = rank_para['model_path']  # ,r'papers\duc\txt\model_html')
    system_path = rank_para['system_path']  # ',r'papers\duc\txt\system_html1')

    model_filenames_pattern_id = rank_para['model_filenames_pattern_id']  # r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
    system_filename_pattern_id = rank_para['system_filename_pattern_id']  # r'#ID#.html',
    pickle_file_pattern_id = rank_para['pickle_file_pattern_id']  # r'#ID#' # inc_test

    pk_sys_set = sxpTestMan.PreparePickleByModelFileSet(model_path, model_filenames_pattern_id,
                                                        pickle_file_pattern_id, system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)

    model_test_output_dict = {}
    for eachtest in testset:
        system_id = modelidname[eachtest]
        output_dict_list = []
        for model_fname_dict in model_file_list:
            # ************************************************************************************
            # NOTE That model_fname_dict is produced in sxpTestMan.PrepareModelForRawSentencePk()
            # ************************************************************************************
            ##            model_fname_dict = {}
            ##            model_fname_dict['fid']=fid
            ##            model_fname_dict['file_name']=file_name
            ##            model_fname_dict['sent_list']=sent_list
            ##            model_fname_dict['models']=models
            # ************************************************************************************
            graph_dict_fid = model_fname_dict['fid']
       #     system_name = model_fname_dict['file_name']
            system_name = test_case +'_'+graph_dict_fid
            topksent_path = system_path + '\\' + system_name + '.html' + '.' + system_id
            # if graph_dict_fid =='AP880217-0100':
            #     print('AP880217-0100 is debuging')
            #     br = 1;
            # else:
            #     continue
            #    graph_dict, matrix_dict,sentence_data_dict= sxpMultiPaperData.LoadFileData(graph_dict_fid)
            if eachtest == "submit27":
                peerid = '27'
                tops = sxpDataDUCSum.LoadSubmitSys(peerid, model_fname_dict['fid'], lenstr='100', peeridx=0)
            elif eachtest == "submit29":
                peerid = '29'
                tops = sxpDataDUCSum.LoadSubmitSys(peerid, model_fname_dict['fid'], lenstr='100', peeridx=0)
            elif eachtest == 'manual100':
                tops = sxpDataDUCSum.LoadManualSys(model_fname_dict['fid'], lenstr='100', peeridx=0)
            else:
                sxptxt = sxpDataDUCSum.LoadSingleDucData(graph_dict_fid,usesub=False)
                print((sxptxt.title))
                tops = rankmethod(eachtest, sxptxt)
            st = sxpTestMan.ProduceSystem(tops, system_name, 1)
            allsent = tops

            output_dict = {}
            output_dict['topksent_path'] = topksent_path
            output_dict['tops'] = tops
            output_dict['st'] = st
            output_dict['allsent'] = allsent
            output_dict_list.append(output_dict)
#-------------------save those pk---------------
            topksent_path = output_dict['topksent_path']
            sxpReadFileMan.WriteStrFile(topksent_path, output_dict['st'], 'utf-8')

            topsent_pk_file = topksent_path + '.topsent.pk'
            sxpReadFileMan.StoreSxptext(output_dict['tops'], topsent_pk_file)

            pkfname = topksent_path + '.allsent.pk'
            sxpReadFileMan.StoreSxptext(output_dict['allsent'], pkfname)
            ##            output_dict ={}
            ##            output_dict['topksent_path']=topksent_path
            ##            output_dict['tops']=tops
            ##            output_dict['st']=st
            ##            output_dict['allsent']=allsent
            ##            output_dict_list.append(output_dict)
            # save text abstact text and conclusion text
#----------------------------------------------
            print('result is ok')
        model_test_output_dict[eachtest] = output_dict_list

    sxpReadFileMan.StoreSxptext(model_test_output_dict, fname_dict['model_test_output_dict'])
    return model_test_output_dict


def ProduceTestRankByRank(project_name,test_case,testset,rankmethod):
    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']
    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)
 #   rank_para = MakePaperPara(project_name,test_case,idname,model_test)
    model_dir = fname_dict['model_dir']# r'./test/demo/model'

    # this is from sxpTestMan.PrepareModelForRawSentencePk()
    model_file_list=sxpReadFileMan.LoadSxptext(fname_dict['model_file_list'])
    modelidname=rank_para['idname']
    pickle_path = rank_para['pickle_path']#'papers\duc\txt\pickle')
    model_path =  rank_para['model_path']#,r'papers\duc\txt\model_html')
    system_path = rank_para['system_path']#',r'papers\duc\txt\system_html1')

    model_filenames_pattern_id = rank_para['model_filenames_pattern_id']# r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
    system_filename_pattern_id = rank_para['system_filename_pattern_id']#r'#ID#.html',
    pickle_file_pattern_id = rank_para['pickle_file_pattern_id']#r'#ID#' # inc_test

    pk_sys_set = sxpTestMan.PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,
        pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)

    model_test_output_dict ={}
    for eachtest in testset:
        system_id= modelidname[eachtest]
        output_dict_list = []
        for model_fname_dict in model_file_list:
#************************************************************************************
# NOTE That model_fname_dict is produced in sxpTestMan.PrepareModelForRawSentencePk()
#************************************************************************************
##            model_fname_dict = {}
##            model_fname_dict['fid']=fid
##            model_fname_dict['file_name']=file_name
##            model_fname_dict['sent_list']=sent_list
##            model_fname_dict['models']=models
#************************************************************************************
            graph_dict_fid = model_fname_dict['fid']
            system_name = model_fname_dict['file_name']
            topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

        #    graph_dict, matrix_dict,sentence_data_dict= sxpMultiPaperData.LoadFileData(graph_dict_fid)
            if eachtest == "submit27":
                peerid = '27'
                tops = sxpDataDUCSum.LoadSubmitSys(peerid, model_fname_dict['fid'],lenstr='100',peeridx=0)
            elif eachtest == "submit29":
                peerid = '29'
                tops = sxpDataDUCSum.LoadSubmitSys(peerid, model_fname_dict['fid'],lenstr='100',peeridx=0)
            elif eachtest == 'manual100':
                tops = sxpDataDUCSum.LoadManualSys(model_fname_dict['fid'],lenstr='100',peeridx=0)
            else:
                sxptxt = sxpDataDUCSum.LoadSingleDucData(graph_dict_fid)
                print((sxptxt.title))
                tops = rankmethod(eachtest, sxptxt)
            st = sxpTestMan.ProduceSystem(tops,system_name,1)
            allsent = tops

            output_dict ={}
            output_dict['topksent_path']=topksent_path
            output_dict['tops']=tops
            output_dict['st']=st
            output_dict['allsent']=allsent
            output_dict_list.append(output_dict)
            print('result is ok')
        model_test_output_dict[eachtest]=output_dict_list

    sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
    return model_test_output_dict

def ProduceTestRank(project_name,test_case,testset):
    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']
    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)

    model_dir = fname_dict['model_dir']# r'./test/demo/model'

    # this is from sxpTestMan.PrepareModelForRawSentencePk()
    model_file_list=sxpReadFileMan.LoadSxptext(fname_dict['model_file_list'])
    modelidname=rank_para['idname']
    pickle_path = rank_para['pickle_path']#'papers\duc\txt\pickle')
    model_path =  rank_para['model_path']#,r'papers\duc\txt\model_html')
    system_path = rank_para['system_path']#',r'papers\duc\txt\system_html1')

    model_filenames_pattern_id = rank_para['model_filenames_pattern_id']# r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
    system_filename_pattern_id = rank_para['system_filename_pattern_id']#r'#ID#.html',
    pickle_file_pattern_id = rank_para['pickle_file_pattern_id']#r'#ID#' # inc_test

    pk_sys_set = sxpTestMan.PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,
        pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)

    model_test_output_dict ={}
    for eachtest in testset:
        system_id= modelidname[eachtest]
        output_dict_list = []
        for model_fname_dict in model_file_list:
#************************************************************************************
# NOTE That model_fname_dict is produced in sxpTestMan.PrepareModelForRawSentencePk()
#************************************************************************************
##            model_fname_dict = {}
##            model_fname_dict['fid']=fid
##            model_fname_dict['file_name']=file_name
##            model_fname_dict['sent_list']=sent_list
##            model_fname_dict['models']=models
#************************************************************************************
            graph_dict_fid = model_fname_dict['fid']
            system_name = model_fname_dict['file_name']
            topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

        #    graph_dict, matrix_dict,sentence_data_dict= sxpMultiPaperData.LoadFileData(graph_dict_fid)
            if eachtest == "submit27":
                peerid = '27'
                tops = sxpDataDUCSum.LoadSubmitSys(peerid, model_fname_dict['fid'],lenstr='100',peeridx=0)
            elif eachtest == "submit29":
                peerid = '29'
                tops = sxpDataDUCSum.LoadSubmitSys(peerid, model_fname_dict['fid'],lenstr='100',peeridx=0)
            elif eachtest == 'manual100':
                tops = sxpDataDUCSum.LoadManualSys(model_fname_dict['fid'],lenstr='100',peeridx=0)
            else:
                sxptxt = sxpDataDUCSum.LoadSingleDucData(graph_dict_fid)
                print((sxptxt.title))
                tops = RankDocDemo(eachtest, sxptxt)
            st = sxpTestMan.ProduceSystem(tops,system_name,1)
            allsent = tops

            output_dict ={}
            output_dict['topksent_path']=topksent_path
            output_dict['tops']=tops
            output_dict['st']=st
            output_dict['allsent']=allsent
            output_dict_list.append(output_dict)
            print('result is ok')
        model_test_output_dict[eachtest]=output_dict_list

    sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
    return model_test_output_dict
def ProduceTopsBySystemDir(project_name,test_case,testset):
    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']
    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)

    model_dir = fname_dict['model_dir']# r'./test/demo/model'

    model_file_list=sxpReadFileMan.LoadSxptext(fname_dict['model_file_list'])
    modelidname=rank_para['idname']
    pickle_path = rank_para['pickle_path']#'papers\duc\txt\pickle')
    model_path =  rank_para['model_path']#,r'papers\duc\txt\model_html')
    system_path = rank_para['system_path']#',r'papers\duc\txt\system_html1')

    model_filenames_pattern_id = rank_para['model_filenames_pattern_id']# r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
    system_filename_pattern_id = rank_para['system_filename_pattern_id']#r'#ID#.html',
    pickle_file_pattern_id = rank_para['pickle_file_pattern_id']#r'#ID#' # inc_test

    pk_sys_set = sxpTestMan.PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,
        pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)

    model_test_output_dict ={}
    for eachtest in testset:
        system_id= modelidname[eachtest]
        output_dict_list = []
        for model_fname_dict in model_file_list:
#************************************************************************************
# NOTE That model_fname_dict is produced in sxpTestMan.PrepareModelForRawSentencePk()
#************************************************************************************
##            model_fname_dict = {}
##            model_fname_dict['fid']=fid
##            model_fname_dict['file_name']=file_name
##            model_fname_dict['sent_list']=sent_list
##            model_fname_dict['models']=models
#************************************************************************************
            graph_dict_fid = model_fname_dict['fid']+'.pk'
            system_name = model_fname_dict['file_name']
            topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

        #    graph_dict, matrix_dict,sentence_data_dict= sxpMultiPaperData.LoadFileData(graph_dict_fid)
            sxptxt = sxpDataDUCSum.LoadSingleDucData(graph_dict_fid,test_case)
            tops = RankDocDemo(eachtest, sxptxt)
            st = sxpTestMan.ProduceSystem(tops,system_name,1)
            allsent = tops

            output_dict ={}
            output_dict['topksent_path']=topksent_path
            output_dict['tops']=tops
            output_dict['st']=st
            output_dict['allsent']=allsent
            output_dict_list.append(output_dict)
            print('result is ok')
        model_test_output_dict[eachtest]=output_dict_list

    sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
    return model_test_output_dict
if __name__ == '__main__':
    main()
