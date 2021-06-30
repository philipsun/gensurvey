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


import sys
sys.path.append('./context')
from context import sxpdorank
import context.sxpPackage
from context.sxpPackage import *

import sxpPyrougeEvaluate
import sxpParseRougeScore
import sxpRankingDoc
import sxpModelFileMan
import sxpLoadRankPara
from sxpLoadRankPara import MakeMultiPaperPara, GetFName

import sxpTestMan
import sxpACLSumData
from sxpACLSumData import sxpNode
import sxpModelDucHybrid
import sxpModelSmallSent

def main():
    #TestDemo() #ok
    project_name = 'acl2014exc'
    test_case = 'exc' #this is to include the abstract and conclusion in the paper
    TestA(project_name,test_case)
def GetTestModel():
    model_test = GetBackFordTest()
    model_test = ['abscon','abstract','conclusion', 'wss300','wordnetwork300', 'wordnetworkback300','wordnetworkendfirst','endfront_debug']
    #   model_test = ['wordnetwork300', 'wordnetworkback300', 'wss300']
    #model_test = Get300()
    #cmd = ['makemodel','rank','score']
    cmd = ['rank','score']
  #  cmd = ['score']
    #cmd = ['plot']
    return model_test,cmd
def GetModelID():

    idname={'abstract': '01', 'conclusion': '02', 'wordnetwork': '03', 'wss100k': '04', 'wss100': '05',
     'wordnetworku': '06',
     'wss200k': '07',
     'wss200': '08',
     'wordnetwork300': '09',
     'wss300k': '10',
     'wss300': '11',
      'wordnetwork300u':'12',
      'wss300ku': '13',
      'wss300u': '14',
      'wordnetwork300k': '15',
        'wordnetwork300no':'16',
        'wss300no':'17',
      'abscon':'18',
       'wordnetworkback300':'19',
        'wordnetworkendfirst':'20',
        'wordnetworkfrondend':'21',
        'endfront_debug':'22',
     }
    return idname
def GetConfig100():
    model_test =['abstract','conclusion','wordnetwork','wss100k','wss100']
    model_test = ['wordnetwork', 'wss100k', 'wss100']
    return model_test
def GetConfig200():
    model_test =['abstract','conclusion','wordnetwork','wss100k','wss100']
    model_test = ['wordnetwork200', 'wss200k', 'wss200']
    return model_test
def GetConfig300():
    model_test =['abstract','conclusion','wordnetwork','wss100k','wss100']
    model_test = ['wordnetwork300', 'wss300k', 'wss300']
    return model_test
def GetConfig300u():
    model_test = ['wordnetwork300u', 'wss300ku', 'wss300u']
    return model_test
def GetNoWord():
    #model_test = [ 'wordnetwork300','wordnetwork300no', 'wss300', 'wss300no']
    model_test = ['wordnetwork300', 'wordnetwork300no']
    return model_test
def GetAbsTest():
    model_test = ['abscon','abstract','conclusion','wordnetwork300']
    return  model_test
def GetBackFordTest():
    # model_test = ['abscon','wordnetwork300','wordnetworkback300']
    model_test = [ 'endfront_debug']
   # model_test = ['abscon','abstract','conclusion','wordnetwork300','wordnetworkendfirst','wordnetworkfrondend']
    return  model_test
def GetPlot():
    model_test = ['wordnetwork', 'wordnetwork300k', 'wss300','wss300k']
    return model_test
def Get300():
    model_test =['wss300','wss300u']
    return model_test
def RankDocDemo(eachtest,sxptxt):
    tops = []
    if eachtest == 'abstract':
        for eachsent in GetAbsConSent(sxptxt.abstract):
            tops.append(eachsent)
    if eachtest == 'conclusion':
        for eachsent in GetAbsConSent(sxptxt.conclusion):
            tops.append(eachsent)
    if eachtest =='abscon':
        tops = GetAbsCon(sxptxt)

    if eachtest == 'wss100':
        #sxptxt,topk,maxword=-1,remove_stopwords=1,undirect=0
        tops = GetWSTop(sxptxt,-1,maxword=100,remove_stopwords=0,undirect=0)
    if eachtest =='wss100k':
        tops = GetWSTop(sxptxt,-1,maxword=100,remove_stopwords=0,undirect=0)
    if eachtest == 'wss200':
        tops = GetWSTop(sxptxt,-1,maxword=200,remove_stopwords=1,undirect=0)
    if eachtest =='wss200k':
        tops = GetWSTop(sxptxt,-1,maxword=200,remove_stopwords=0,undirect=0)
    if eachtest == 'wss300':
        tops = GetWSTop(sxptxt,-1,maxword=300,remove_stopwords=0,undirect=0)
    if eachtest =='wss300no':
        tops = GetWSTopNoWord(sxptxt,-1,maxword=300,remove_stopwords=0,undirect=0)
    if eachtest == 'wss300u':
        tops = GetWSTop(sxptxt, -1, maxword=300, remove_stopwords=1,undirect=1)

    if eachtest =='wss300k':
        tops = GetWSTop(sxptxt,-1,maxword=300,remove_stopwords=1,undirect=0)
    if eachtest == 'wss300ku':
        tops = GetWSTop(sxptxt, -1, maxword=300, remove_stopwords=1,undirect=1)
    if eachtest == 'ss100':
        tops = GetSSTop(sxptxt, -1, maxword=300, remove_stopwords=1)
    if eachtest == 'ss100k':
        tops = GetSSTop(sxptxt, -1, maxword=300, remove_stopwords=0)
    if eachtest == 'ths100':
        tops = GetTHS100(sxptxt,-1, maxword=300, remove_stopwords=1)
    if eachtest == "wordnetwork":
        tops = GetWordNetHybrid(sxptxt,-1, maxword=300, remove_stopwords=0,undirect=0)
    if eachtest == 'wordnetwork300':
        tops = GetWordNetHybrid(sxptxt, -1, maxword=300, remove_stopwords=0, undirect=0)
    if eachtest == "wordnetworku":
        tops = GetWordNetHybrid(sxptxt,-1, maxword=200, remove_stopwords=0,undirect=1)
    if eachtest == "wordnetwork300k":
        tops = GetWordNetHybrid(sxptxt,-1, maxword=300, remove_stopwords=1,undirect=0)
    if eachtest == "wordnetwork300u":
        tops = GetWordNetHybrid(sxptxt,-1, maxword=300, remove_stopwords=0,undirect=1)
    if eachtest == 'wordnetwork300no':
        print(eachtest)
        tops = GetWordNetHybridNoWord(sxptxt,-1, maxword=300, remove_stopwords=0,undirect=0)
    if eachtest == 'wordnetworkback300':
        print(eachtest)
        tops = GetWordNetHybridBackword(sxptxt, -1, maxword=300, remove_stopwords=0, undirect=0)
    if eachtest == 'wordnetworkendfirst':
        print('wordnetworkendfirst')
        tops = GetWordNetHybridEndfirst(sxptxt, -1, maxword=300, remove_stopwords=0, undirect=0)
    if eachtest == 'wordnetworkfrondend':
        print('wordnetworkfrondend')
        tops = GetWordNetHybridEndFront(sxptxt, -1, maxword=300, remove_stopwords=0, undirect=0)
    if eachtest == 'endfront_debug':
        print('endfront_debug')
        tops = GetWordNetHybridEndFrontDebug(sxptxt, -1, maxword=300, remove_stopwords=0, undirect=0)

    return tops
def TestDemo():
    project_name = 'acl2014'
    test_case = 'exc' #this is to include the abstract and conclusion in the paper
    idname = GetModelID()
    model_idname = idname#sxpRougeConfig.idname
#*******************hao to run the test***************************
    model_test=GetPlot()
    #model_test = Get300()
    cmd = ['score']
#_________________________________________________________________
    # cmd = [ 'score']
     #this is to rank_parameter dict for this demo:

    rank_para = MakeMultiPaperPara(project_name, test_case, model_idname, model_test)
    print(('project ',project_name,'test_case', test_case,'***************'))
    for k,v in list(rank_para.items()):
        print((k, v))
  #  cmd = ['makemodel','rank','score']

    if 'makemodel' in cmd:
        #this is to make model files for a set of inputting model files:
        print(('make model files for ',project_name,'test_case', test_case,'***************'))
        doc_model_sent_file_list = sxpACLSumData.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        sxpTestMan.DoMakeModel(project_name,test_case,doc_model_sent_file_list)
    if 'rank' in cmd:
        #this is to make a testing top-k sentences for the two test methods, they are the same
        print(('make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************'))
        data_case = 'exc'
        model_test_output_dict=ProduceTestRank(project_name,test_case,model_test,data_case)
    #    print(model_test_output_dict)
        sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)
    if 'score' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
      #  rankcmd = 'plot'
        rankcmd = 'all'
        sxpTestMan.DoRougeScore(project_name,test_case,cmd=rankcmd)

    if 'plot' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
        sxpTestMan.DoRougeScore(project_name,test_case, cmd='plot')
def TestA(project_name,test_case):
 #   project_name = 'acl2014inc'
 #   test_case = 'inc' #this is to include the abstract and conclusion in the paper
    idname = GetModelID()
    model_idname = idname#sxpRougeConfig.idname
#*******************hao to run the test***************************
    #model_test=GetPlot()
    #model_test=GetNoWord()
    #model_test=GetAbsTest()
    # model_test = GetBackFordTest()
    # #model_test = Get300()
    # #cmd = ['makemodel','rank','score']
    # # cmd = [ 'rank', 'score']
    # cmd = ['score']
    model_test, cmd = GetTestModel()
    TestModel(project_name, model_idname, test_case, model_test, cmd, RankDocDemo,data_case='inc')
def TestModel(project_name,model_idname, test_case,model_test,cmd,rankmethod,data_case='inc'):
#     project_name = 'acl2014'
#     test_case = 'inc' #this is to include the abstract and conclusion in the paper
#     idname = GetModelID()
#     model_idname = idname#sxpRougeConfig.idname
# #*******************hao to run the test***************************
#     model_test=GetPlot()
#     #model_test = Get300()
#     cmd = ['score']
#
#_________________________________________________________________
    # cmd = [ 'score']
     #this is to rank_parameter dict for this demo:
    model_file_case= project_name#'inc'
    system_file_case=test_case
    rank_para = MakeMultiPaperPara(project_name, test_case, model_idname, model_test,model_file_case,system_file_case)
    print(('project ',project_name,'test_case', test_case,'***************'))
    for k,v in list(rank_para.items()):
        print(( k, v))
  #  cmd = ['makemodel','rank','score']

    if 'makemodel' in cmd:
        #this is to make model files for a set of inputting model files:
        print(('make model files for ',project_name,'test_case', test_case,'***************'))
        doc_model_sent_file_list = sxpACLSumData.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        sxpTestMan.DoMakeModel(project_name,test_case,doc_model_sent_file_list)
    if 'rank' in cmd:
        #this is to make a testing top-k sentences for the two test methods, they are the same
        print(('make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************'))
        model_test_output_dict=ProduceTestRankByRank(project_name,test_case,model_test,rankmethod,data_case,rank_para)
    #    print(model_test_output_dict)
     #   sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)
    if 'score' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
      #  rankcmd = 'plot'
        rankcmd = 'all'
        sxpTestMan.DoRougeScore(project_name,test_case,cmd=rankcmd)

    if 'plot' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
        sxpTestMan.DoRougeScore(project_name,test_case, cmd='plot')

def ProduceTestRank(project_name,test_case,testset,data_case='inc'):
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
            sxptxt = sxpACLSumData.LoadACLData(graph_dict_fid,data_case)
            tops = RankDocDemo(eachtest, sxptxt)
            st = sxpTestMan.ProduceSystem(tops,system_name,1)
            allsent = tops

            output_dict ={}
            output_dict['topksent_path']=topksent_path
            output_dict['tops']=tops
            output_dict['st']=st
            output_dict['allsent']=allsent
            output_dict_list.append(output_dict)
            print( 'result is ok')
        model_test_output_dict[eachtest]=output_dict_list

    sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
    return model_test_output_dict

def ProduceTestRankByRank(project_name,test_case,testset,rankmethod,data_case,rank_para):
    fname_dict=GetFName(project_name,test_case)
    # rankpara_fname = fname_dict['rankpara_fname']
    # rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)

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
#please note, here graph_dict_fid will be .pk end, so it affects the system file name
# each has a .pk in system_name, so in topksent_path, so
            graph_dict_fid = model_fname_dict['fid']+'.pk'
            #system_name = model_fname_dict['file_name'] #this is old version, using model file name pattern
            system_name = test_case + '_' + graph_dict_fid # this is new version which use test_case name as pattern
            topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

        #    graph_dict, matrix_dict,sentence_data_dict= sxpMultiPaperData.LoadFileData(graph_dict_fid)
            sxptxt = sxpACLSumData.LoadACLData(graph_dict_fid,data_case)
            tops = rankmethod(eachtest, sxptxt)
            st = sxpTestMan.ProduceSystem(tops,system_name,1)
            allsent = tops

            output_dict ={}
            output_dict['topksent_path']=topksent_path
            output_dict['tops']=tops
            output_dict['st']=st
            output_dict['allsent']=allsent
            output_dict_list.append(output_dict)
            print( 'result is ok')
#---------------save file-------------
            topksent_path = output_dict['topksent_path']
            sxpReadFileMan.WriteStrFile(topksent_path, output_dict['st'], 'utf-8')

            topsent_pk_file = topksent_path + '.topsent.pk'
            sxpReadFileMan.StoreSxptext(output_dict['tops'], topsent_pk_file)

            pkfname = topksent_path + '.allsent.pk'
            sxpReadFileMan.StoreSxptext(output_dict['allsent'], pkfname)
            model_test_output_dict[eachtest]=output_dict_list

    sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
    return model_test_output_dict

def GetWordNetHybrid(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5
    sxpModelDucHybrid.global_para['undirect'] = undirect
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['mode'] = 'wd_ss'
    sxpModelDucHybrid.global_para['alpha_beta'] = [0.8, 0.2]
    sxpModelDucHybrid.global_para['maxword'] = maxword
    sxpModelDucHybrid.global_para['topksent'] = topk

    model = sxpModelDucHybrid.WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
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
def GetWordNetHybridNoWord(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5


    sxpModelDucHybrid.global_para['undirect'] = undirect
    sxpModelDucHybrid.global_para['remove_stopwords'] = remove_stopwords
    sxpModelDucHybrid.global_para['addseq'] = 0
    sxpModelDucHybrid.global_para['mode'] = 'wd_ss'
    sxpModelDucHybrid.global_para['alpha_beta'] = [1, 0]
    sxpModelDucHybrid.global_para['maxword'] = maxword
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
def GetWSTopNoWord(sxptxt,topk,maxword=-1,remove_stopwords=1,undirect=0):
    mode= "ws_pr"
    sxpModelSmallSent.global_para['undirect'] = undirect
    sxpModelSmallSent.global_para['remove_stopwords'] = remove_stopwords
    sxpModelSmallSent.global_para['addseq'] = 0
    sxpModelSmallSent.global_para['mode'] = 'ws_pr'
    sxpModelSmallSent.global_para['alpha_beta'] = [1, 0]
    sxpModelSmallSent.global_para['maxword'] = maxword
    sxpModelSmallSent.global_para['topksent'] = topk

    model = sxpModelSmallSent.SmallSent(sxptxt,undirect=undirect,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
    topksent = topk#-1
    useabstr = 0

    strictmax=0
    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    return tops
def GetWSTop(sxptxt,topk,maxword=-1,remove_stopwords=1,undirect=0):
    mode= "ws_pr"
    sxpModelSmallSent.global_para['undirect'] = undirect
    sxpModelSmallSent.global_para['remove_stopwords'] = remove_stopwords
    sxpModelSmallSent.global_para['addseq'] = 0
    sxpModelSmallSent.global_para['mode'] = 'ws_pr'
    sxpModelSmallSent.global_para['alpha_beta'] = [0.8, 0.2]
    sxpModelSmallSent.global_para['maxword'] = maxword
    sxpModelSmallSent.global_para['topksent'] = topk


    model = sxpModelSmallSent.SmallSent(sxptxt,undirect=undirect,remove_stopwords=remove_stopwords,iteration_times=30,mode=mode)
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
def GetAbsCon(sxptxt):
    tops = []

    for eachsent in GetAbsConSent(sxptxt.abstract):
        tops.append(eachsent)

    for eachsent in GetAbsConSent(sxptxt.conclusion):
        tops.append(eachsent)
    return tops
def DoRank(project_name,test_case):

    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']
    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)
#    sxpdorank.RankPara(rankpara)
    model_test_output_dict=sxpdorank.RankParaOutput(rankpara_fname)

    sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
    return model_test_output_dict


if __name__ == '__main__':
    main()
