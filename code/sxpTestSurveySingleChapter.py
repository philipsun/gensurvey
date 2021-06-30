# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 00:19:43 2018

@author: sunxp
"""

#-------------------------------------------------------------------------------
# Name:        sxpTestSurvey.py
# Purpose:
#
# Author:      sunxp
#
# Created:     22/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <MIT License>
#-------------------------------------------------------------------------------
import re
import os
import sxpReadFileMan
import sxpSGTree

##import sys
##sys.path.append('./context')
##from context import sxpdorank
##import context.sxpPackage
##from context.sxpPackage import *

import sxpPyrougeEvaluate
import sxpParseRougeScore
import sxpRankingDoc
import sxpModelFileMan
import sxpLoadRankPara
from context import sxpdorank
from sxpLoadRankPara import MakeDemoRankPara, GetFName
import sxpSurveyData
import sxpMultiPaperData

import sxpTestMan
from sxpSurveyData import sxpNode
import sxpSurveyData
import sxpJudgeCharacter

import sxpCh4Ranking
def main():
    cmd = 'TestSystemRank'
    if cmd == 'TestDemo':
        TestDemo()
    if cmd== 'TestSystemRank':
        TestSystemRank()
def TestDemo():
    project_name = 'surveychall'
    test_case = 'testall'
    idname ={'test_abs':'01','test_con':'02','test_abscon':'03'}
    model_idname = idname#sxpRougeConfig.idname
    model_test =['test_abs','test_con','test_abscon']

     #this is to rank_parameter dict for this demo:
    rank_para = MakeDemoRankPara(project_name, test_case, model_idname, model_test)
    print(('project ',project_name,'test_case', test_case,'***************'))
    for k,v in list(rank_para.items()):
        print(k, v)

    cmd = ['makemodel','rank','score']
  #  cmd = ['score']
    if 'makemodel' in cmd:
        #this is to make model files for a set of inputting model files:
        print(('make model files for ',project_name,'test_case', test_case,'***************'))
    #    doc_model_sent_file_list = sxpSurveyData.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        doc_model_sent_file_list = sxpSurveyData.LoadChapter4ModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        sxpTestMan.DoMakeModel(project_name,test_case,doc_model_sent_file_list)

    if 'rank' in cmd:
        #this is to make a testing top-k sentences for the two test methods, they are the same
        print(('make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************'))
        model_test_output_dict=ProduceTestRank(project_name,test_case,model_test)
    #    print(model_test_output_dict)
        sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)

    if 'score' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
        sxpTestMan.DoRougeScore(project_name,test_case)

def TestSystemRank():
    project_name = 'surveychall'
    test_case = 'testallsingleone'#old new by sxpTestSurveyAllChapter
    idname ={'allchsent':'01',
             'allchtitle':'02',
             'v6_abstract':'03',
             'tfidf_all_abstract': '04',
             'wordquery_allv2_abstract':'05',
             'v6_abstract_top2':'06',
             'tfidf_all_abstract_top2':'07',
             'v6_abstractks':'08',
             'sgt5':'09'
             }
    model_idname = idname  # sxpRougeConfig.idname

    dowhat='rankscore'
    model_test =['allchsent','allchtitle','v6_abstractks','v6_abstract','tfidf_all_abstract']

  #  model_test =['allch4sent','allch4title','randomfromall','sgt'] #this must be choosed from idname keys
     #this is to rank_parameter dict for this demo:
    rank_para = MakeDemoRankPara(project_name, test_case, model_idname, model_test)
    print(('project ',project_name,'test_case', test_case,'***************'))
    for k,v in list(rank_para.items()):
        print(k, v)

    if dowhat=='all':
      cmd = ['makemodel','rank','score']
    if dowhat =='rankscore':
       cmd = ['rank','score']
    if dowhat =='score':
       cmd = [ 'score']
    if dowhat == 'plot':
        cmd=['plot']
    if 'makemodel' in cmd:
        #In this function, we do not have to make model files first :
    #    print('make model files for ',project_name,'test_case', test_case,'***************')
    #    doc_model_sent_file_list = sxpSurveyData.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        doc_model_sent_file_list = sxpSurveyData.LoadAllChapterModelDoc()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        sxpTestMan.DoMakeModel(project_name,test_case,doc_model_sent_file_list)
    if 'rank' in cmd:
        #this is to make a testing top-k sentences for the two test methods, they are the same
        print(('*****make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************'))

        model_test_output_dict=ProduceTestRank(project_name,test_case,model_test)
    #    print(model_test_output_dict)
    #    sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)
    #
    # if 'score' in cmd:
    #     print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
    #     #this is to make a testing top-k sentences for the two test methods, they are the same
    #     sxpTestMan.DoRougeScore(project_name,test_case, cmd='all')
    # if 'plot' in cmd:
    #     print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
    #     #this is to make a testing top-k sentences for the two test methods, they are the same
    #     sxpTestMan.DoRougeScore(project_name,test_case, cmd='plot')


def ProduceTestRank(project_name,test_case,testset):

    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']
    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)

    model_dir = fname_dict['model_dir']# r'./test/demo/model'
    #this model_file_list is produced in sxpTestMan.PrepareModelForRawSentencePk() where fid is p_0000,
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

    k = 0;
    #total 42, 29 larger,13 smaller, but for 0045 0043, 0041 they have the same summary but different
    #score
    for model_fname_dict in model_file_list:
        model_test_output_dict ={}
        graph_name = model_fname_dict['fid'] + '.pk'  # here fid is p_0000, but in our surveydata it is p_0000.pk that is to used
        print('processing...',graph_name,test_case)
        k = k + 1
        # if model_fname_dict['fid'] != '0043':
        #     continue;
        onlyid = []
        onlyid.append(model_fname_dict['fid'])
        singletest_case = test_case + model_fname_dict['fid']
        for eachtest in testset:
            system_id = modelidname[eachtest]
            output_dict_list = []
#************************************************************************************
# NOTE That model_fname_dict is produced in sxpTestMan.PrepareModelForRawSentencePk()
#************************************************************************************
##            model_fname_dict = {}
##            model_fname_dict['fid']=fid
##            model_fname_dict['file_name']=file_name
##            model_fname_dict['sent_list']=sent_list #here is all the sentence of abstraction and conclusion
##            model_fname_dict['models']=models
#************************************************************************************

            system_name = rank_para['systempattern']
            system_name = system_name.replace("(\\d+)",model_fname_dict['fid'])
            topksent_path = system_path + '\\' + system_name + '.'+system_id

          #  graph_dict, matrix_dict,sentence_data_dict=sxpSurveyData.LoadFileDataByGraphFid(graph_name)
            #this will only load all sent and title sent from chapter 4.
          #  sentence_data_dict=sxpSurveyData.LoadChapter4AllSentTitleSent()
          #  sentence_data_dict = sxpCh4Ranking.LoadRandomRankSent()
#************************************************************************************
# NOTE That sxpRankingDoc.RankDocUseSentenceDict is to use abstract, conclusion, and both to produce
# a test result without actually ranking sentences.
#************************************************************************************
       #     tops = sxpRankingDoc.RankDocDemo(eachtest,model_fname_dict)

            tops = RankDocUseSentenceDict(eachtest,model_fname_dict['fid'])

            if tops is None:
                print(('no sent for this test', eachtest))
                continue
            print('test',eachtest)
            print('test', tops)
       #     print(tops)
#************************************************************************************
           # tops=sxpJudgeCharacter.removestops(tops)

            st = sxpTestMan.ProduceSystem(tops,system_name,1)

            allsent = tops

            output_dict ={}
            output_dict['topksent_path']=topksent_path
            output_dict['tops']=tops
            output_dict['st']=st
            output_dict['allsent']=allsent
            output_dict_list.append(output_dict)
            print('result is ok')
            model_test_output_dict[eachtest] = output_dict_list
        rank_para['rougetxthead']=singletest_case
        sxpTestMan.WriteSystemOutput(rank_para, model_test_output_dict)


        print(('do ROUGE score for the top sentence files in ', project_name, 'test_case', test_case, '***************'))
                # this is to make a testing top-k sentences for the two test methods, they are the same
#        sxpTestMan.DoRougeScore(project_name, test_case, cmd='all')
        txtf,pkf =  sxpTestMan.DoPyrougeScoreByRankPara(rank_para,onlyid=onlyid)
        print(txtf,pkf)
        sxpTestMan.PlotScoreRankPara(rank_para,project_name,test_case)
   # sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
    return model_test_output_dict

def RankDocUseSentenceDict(eachtest,fid):
    tops=None

    if eachtest == 'allchsent':
        tops = []
        sentlist=sxpSurveyData.GetChapterSentByFID(fid)
        for sent in sentlist:
            tops.append(sent)
        return tops
    if eachtest == 'allchtitle':
        tops = []
        sentlist = sxpSurveyData.GetAllChapterTitle()
        for sent in sentlist:
            tops.append(sent)
        return tops
    if eachtest == 'v6_abstract':
        tops = sxpSurveyData.LoadGenSurvey(fid,survgenmethod='abstract',testname='wordquery_allv6')
    if eachtest == 'v6_abstractks':
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod='abstract', testname='wordquery_allv6ks')
    if eachtest == 'tfidf_all_abstract':
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod='abstract', testname='tfidf_all')
    if eachtest == 'wordquery_allv2_abstract':
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod='abstract', testname='wordquery_allv2')
    if eachtest == 'v6_abstract_top2':
        survgenmethod = 'abstract_top2'
        testname = 'wordquery_allv6'
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod='abstract_top2', testname='wordquery_allv6')
    if eachtest == 'tfidf_all_abstract_top2':
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod='abstract_top2', testname='tfidf_all')
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
