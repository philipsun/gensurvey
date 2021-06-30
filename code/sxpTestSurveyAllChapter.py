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
from sxpLoadRankPara import MakeMultiPaperPara, GetFName

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
   # rank_para = MakeDemoRankPara(project_name, test_case, model_idname, model_test)
    rank_para = MakeMultiPaperPara(project_name, test_case, model_idname, model_test)
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
def RunGenRouge(idname,testallcase,testcasemethod,cmd = ['rank', 'score']):
    project_name = 'surveychall' #this test is to test one survey paper 2020 12 05
    test_case = 'test'
    model_idname = idname  # sxpRougeConfig.idname
    # model_test =['test_dtfipf_sent_org','test_dual_lr','test_dual_num','test_dtfipf_lr','test_origin_abs','test_origin_simabs','test_origin_diffabs','test_bm25']
    # model_test = ['test_dtfipf_sent_org', 'test_dual_lr', 'test_dual_num', 'test_dtfipf_lr', 'test_origin_abs',
    #               'test_origin_simabs', 'test_origin_diffabs', 'test_bm25_LR']
    model_test = testallcase#['test_dtfipf_sent_org', 'test_dual_lr', 'test_bm25_LR']
    # this is to rank_parameter dict for this demo:
    model_file_case = project_name  # 'inc'
    system_file_case = test_case
    rank_para = MakeMultiPaperPara(project_name, test_case, model_idname, model_test, model_file_case, system_file_case)
    print('project ', project_name, 'test_case', test_case, '***************')
    for k, v in rank_para.items():
        print(k, v)

    #cmd = ['makemodel', 'rank', 'score']
    #cmd = ['makemodel', 'rank']
    #cmd = ['rank', 'score', ]
    #cmd = ['plotscore']
    # cmd = ['rank','score','close'] # note that this program can automatically close os when finished
    # cmd = ['close']
    if 'makemodel' in cmd:
        # this is to make model files for a set of inputting model files:
        print('make model files for ', project_name, 'test_case', test_case, '***************')
        #        doc_model_sent_file_list = sxpSurveyData.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        doc_model_sent_file_list = sxpSurveyData.TestLoadAllChapterModelDoc()  # [[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        sxpTestMan.DoMakeModel(project_name, test_case, doc_model_sent_file_list)

    if 'rank' in cmd:
        # this is to make a testing top-k sentences for the two test methods, they are the same
        print('make a test rank result top sentence files for ', project_name, 'test_case', test_case,
              '***************')
        model_test_output_dict = ProduceTestRankTestRankSet(project_name, test_case, model_test,testcasemethod)
        #    print(model_test_output_dict)
        sxpTestMan.WriteSystemOutput(rank_para, model_test_output_dict)

    if 'score' in cmd:
        print('do ROUGE score for the top sentence files in ', project_name, 'test_case', test_case, '***************')
        # this is to make a testing top-k sentences for the two test methods, they are the same
        rankcmd = 'all'
        sxpTestMan.DoRougeScore(project_name, test_case, rankcmd)
    if 'plotscore' in cmd:
        print('do ROUGE score for the top sentence files in ', project_name, 'test_case', test_case, '***************')
        # this is to make a testing top-k sentences for the two test methods, they are the same
        rankcmd = 'plot'
        sxpTestMan.DoRougeScore(project_name, test_case, rankcmd)
    if 'close' in cmd:
        print('going to close computer')
        os.system('shutdown -s -t 1')
    return None

def ProduceTestRankTestRankSet(project_name,test_case,testset,testcasemethod):
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
    print('eachpk_sys in pk_sys_set, note that in this version,this list is not used because, we use model_list file to product tops')
    for eachpick in pk_sys_set:
        print(eachpick)

    model_test_output_dict ={}
    for eachtest in testset:
        print('---------',eachtest)
        testcasename = testcasemethod[eachtest][0]
        topkname = testcasemethod[eachtest][1]
        system_id= modelidname[eachtest]
        output_dict_list = []
        for model_fname_dict in model_file_list:
#************************************************************************************
# NOTE That model_fname_dict is produced in sxpTestMan.PrepareModelForRawSentencePk()
#************************************************************************************
##            model_fname_dict = {}
##            model_fname_dict['fid']=fid
##            model_fname_dict['file_name']=file_name
##            model_fname_dict['sent_list']=sent_list #here is all the sentence of abstraction and conclusion
##            model_fname_dict['models']=models
#************************************************************************************
            graph_name = model_fname_dict[
                             'fid'] + '.pk'  # here fid is p_0000, but in our surveydata it is p_0000.pk that is to used
            system_name = rank_para['systempattern']
            system_name = system_name.replace("(\\d+)", model_fname_dict['fid'])
            topksent_path = system_path + '\\' + system_name + '.' + system_id
#here fid is p_0000, but in our surveydata it is p_0000.pk that is to used
         #   system_name = model_fname_dict['file_name']

            system_name = rank_para['systempattern']
            system_name = system_name.replace("(\\d+)", model_fname_dict['fid'])
            topksent_path = system_path + '\\' + system_name + '.'+system_id
            #topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

           # graph_dict, matrix_dict,sentence_data_dict=sxpSurveyData.LoadFileDataByGraphFid(graph_name)

#************************************************************************************
# NOTE That sxpRankingDoc.RankDocUseSentenceDict is to use abstract, conclusion, and both to produce
# a test result without actually ranking sentences.
#************************************************************************************
       #     tops = sxpRankingDoc.RankDocDemo(eachtest,model_fname_dict)
            tops = RankDocUseSentenceDictTestCaseNameTopkName(testcasename,topkname,model_fname_dict['fid'])

            print(tops)
#************************************************************************************
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

def RankDocUseSentenceDictTestCaseNameTopkName(TestCaseName,TopkName,fid):
    tops=None

    if TestCaseName == 'allchsent':
        tops = []
        sentlist=sxpSurveyData.GetChapterSentByFID(fid)
        for sent in sentlist:
            tops.append(sent)
        return tops

        return tops
    if TestCaseName == 'allchtitle':
        tops = []
        sentlist = sxpSurveyData.GetAllChapterTitle()
        for sent in sentlist:
            tops.append(sent)
        return tops

        return tops
    if TestCaseName == 'test_origin':
        testname = 'test_origin'
        survgenmethod ='origin_abs'
        tops = sxpSurveyData.LoadChapterOriginRefAbs(fid, survgenmethod=survgenmethod, testname=testname)
        return tops

    if TestCaseName == 'test_diffabs':
        testname = 'test_origin'
        survgenmethod ='diff_abs'
        tops = sxpSurveyData.LoadChapterOriginRefAbs(fid, survgenmethod=survgenmethod, testname=testname)
        return tops

    if TestCaseName == 'test_simabs':
        testname = 'test_origin'
        survgenmethod ='sim_abs'
        tops = sxpSurveyData.LoadChapterOriginRefAbs(fid, survgenmethod=survgenmethod, testname=testname)
        return tops

    testname = TestCaseName
    survgenmethod = TopkName #'orig'
    #this LoadGenSurvey will load each chapter's generation of papers.
    #it is obtained in sxpSurveyData.MakeDiffSimSurvByAbs(),MakeChapterOriginRefAbs() and MakeSurveyByOriginResult()
    #and MakeSurveyByRankTopkResult(), so , you need to run those functions before loading them in this proc.
    tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod=survgenmethod, testname=testname)
    sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
    return tops

def TestSystemRank():
    project_name = 'surveychall' #this test is to test each chapter of survey paper as one doc
    # this test is to test each chapter survey paper 2020 12 05
    test_case = 'testall'
    idname ={'allchsent':'01',
             'allchtitle':'02',
             'v6_abstract':'03',
             'tfidf_all_abstract': '04',
             'wordquery_allv2_abstract':'05',
             'v6_abstract_top2':'06',
             'tfidf_all_abstract_top2':'07',
             'v6_abstractks':'08',
             'v6_abstractks_dualsent':'09',
             'v6_abstractks_dualsent_num':'10',
             'test_dtfipf_sent_org':'11',
             'v6_abstractks_dualsent_LR':'12',
             'test_dtfipf_lr': '13',
             'orgin_abstract': '14',
             'orgin_simabs':'15',
             'orgin_diffabs':'16'
             }
    model_idname = idname  # sxpRougeConfig.idname

    dowhat='rankscore'
    # model_test =['allchsent','allchtitle','v6_abstract','v6_abstractks','tfidf_all_abstract','v6_abstractks_dualsent']
    model_test = ['allchsent','allchtitle','v6_abstract','v6_abstractks','tfidf_all_abstract','v6_abstractks_dualsent','v6_abstractks_dualsent_num']
  #  model_test = ['v6_abstractks_dualsent_num','v6_abstractks_dualsent_LR','test_dtfipf_sent_org','test_dtfipf_lr']
    model_test = [ 'v6_abstractks_dualsent_LR','test_dtfipf_lr','v6_abstractks_dualsent_num','test_dtfipf_sent_org','orgin_abstract','orgin_diffabs','orgin_simabs']
  #  model_test =['allch4sent','allch4title','randomfromall','sgt'] #this must be choosed from idname keys
     #this is to rank_parameter dict for this demo:
    rank_para = MakeMultiPaperPara(project_name, test_case, model_idname, model_test)
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
        sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)

    if 'score' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
        sxpTestMan.DoRougeScore(project_name,test_case, cmd='all')
    if 'plot' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
        sxpTestMan.DoRougeScore(project_name,test_case, cmd='plot')


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
##            model_fname_dict['sent_list']=sent_list #here is all the sentence of abstraction and conclusion
##            model_fname_dict['models']=models
#************************************************************************************
            graph_name = model_fname_dict['fid']+'.pk' #here fid is p_0000, but in our surveydata it is p_0000.pk that is to used
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
        model_test_output_dict[eachtest]=output_dict_list

    sxpReadFileMan.StoreSxptext(model_test_output_dict,fname_dict['model_test_output_dict'])
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
    if eachtest == 'orgin_abstract':
        testname = 'test_origin'
        survgenmethod ='origin_abs'
        tops = sxpSurveyData.LoadChapterOriginRefAbs(fid, survgenmethod=survgenmethod, testname=testname)
    if eachtest == 'orgin_diffabs':
        testname = 'test_origin'
        survgenmethod ='diff_abs'
        tops = sxpSurveyData.LoadChapterOriginRefAbs(fid, survgenmethod=survgenmethod, testname=testname)
    if eachtest == 'orgin_simabs':
        testname = 'test_origin'
        survgenmethod ='sim_abs'
        tops = sxpSurveyData.LoadChapterOriginRefAbs(fid, survgenmethod=survgenmethod, testname=testname)

    if eachtest == 'v6_abstract':
        tops = sxpSurveyData.LoadGenSurvey(fid,survgenmethod='abstract',testname='wordquery_allv6')
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
    if eachtest == 'v6_abstractks':
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod='abstract', testname='wordquery_allv6ks')
    if eachtest == 'v6_abstractks_dualsent':
      #  "survgenmethod": 'opt',
      #  "testname": 'wordquery_allv6ks_dual_sentrank'
        survgenmethod = 'opt'
        testname = 'wordquery_allv6ks_dual_sentrank'
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod=survgenmethod, testname=testname)
    if eachtest == 'v6_abstractks_dualsent_num':
      #  "survgenmethod": 'opt',
      #  "testname": 'wordquery_allv6ks_dual_sentrank'
        survgenmethod = 'opt_num'
        testname = 'wordquery_allv6ks_dual_sentrank'
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod=survgenmethod, testname=testname)
    if eachtest == 'test_dtfipf_sent_org':
        testname = 'dtfipf_all_stop'
        survgenmethod ='orig'
#        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod=survgenmethod, testname=testname)
        return tops
    if eachtest == 'v6_abstractks_dualsent_LR':
        testname = 'wordquery_allv6ks_dual_sentrank'
        survgenmethod = 'LR'
        #        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod=survgenmethod, testname=testname)
        return tops
    if eachtest == 'test_dtfipf_lr':
        testname = 'dtfipf_all_stop'
        survgenmethod ='LR'
        tops = sxpSurveyData.LoadGenSurvey(fid, survgenmethod=survgenmethod, testname=testname)
        return tops;

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
