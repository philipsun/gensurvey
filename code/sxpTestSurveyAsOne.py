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
from context import sxpdorank
import sxpReadFileMan


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
from sxpLoadRankPara import MakeMultiPaperPara, GetFName
import sxpSurveyData
import sxpTestMan
from sxpSurveyData import sxpNode
import sxpSurveyData
def main():
    TestDemo()
def RunGenRouge(idname,testallcase,testcasemethod,cmd =['rank', 'score', ]):
    project_name = 'surveyone' #this test is to test one survey paper 2020 12 05
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
def TestDemo():
    project_name = 'surveyone' #this test is to test one survey paper 2020 12 05
    test_case = 'test'
    idname ={'test_dual_num':'01'
            ,'test_dual_abs':'02'
            ,'test_tfidf_num':'03'
            ,'test_dtfipf_sent_org':'04',
            'test_dual_lr':'05',
             'test_dtfipf_lr':'06',
             'test_origin_abs':'07',
             'test_origin_simabs': '08',
             'test_origin_diffabs': '09',
             'test_bm25_LR':'10'
            }
    model_idname = idname#sxpRougeConfig.idname
    #model_test =['test_dtfipf_sent_org','test_dual_lr','test_dual_num','test_dtfipf_lr','test_origin_abs','test_origin_simabs','test_origin_diffabs','test_bm25']
    # model_test = ['test_dtfipf_sent_org', 'test_dual_lr', 'test_dual_num', 'test_dtfipf_lr', 'test_origin_abs',
    #               'test_origin_simabs', 'test_origin_diffabs', 'test_bm25_LR']
    model_test = ['test_dtfipf_sent_org','test_dual_lr', 'test_bm25_LR']
     #this is to rank_parameter dict for this demo:
    model_file_case= project_name#'inc'
    system_file_case=test_case
    rank_para = MakeMultiPaperPara(project_name, test_case, model_idname, model_test,model_file_case,system_file_case)
    print('project ',project_name,'test_case', test_case,'***************')
    for k,v in rank_para.items():
        print (k, v)

    cmd = ['makemodel','rank','score']
    cmd = ['makemodel','rank']
    cmd = ['rank','score',]
   # cmd = ['rank','score','close'] # note that this program can automatically close os when finished
   # cmd = ['close']
    if 'makemodel' in cmd:
        #this is to make model files for a set of inputting model files:
        print('make model files for ',project_name,'test_case', test_case,'***************')
#        doc_model_sent_file_list = sxpSurveyData.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        doc_model_sent_file_list = sxpSurveyData.TestLoadAllChapterModelDoc()  # [[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        sxpTestMan.DoMakeModel(project_name,test_case,doc_model_sent_file_list)

    if 'rank' in cmd:
        #this is to make a testing top-k sentences for the two test methods, they are the same
        print('make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************')
        model_test_output_dict=ProduceTestRank(project_name,test_case,model_test)
#    print(model_test_output_dict)
        sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)

    if 'score' in cmd:
        print('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************')
        #this is to make a testing top-k sentences for the two test methods, they are the same
        rankcmd = 'all'
        sxpTestMan.DoRougeScore(project_name,test_case,rankcmd)
    if 'close' in cmd:
        print('going to close computer')
        os.system('shutdown -s -t 1')

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
            graph_name = model_fname_dict['fid'] #here fid is p_0000, but in our surveydata it is p_0000.pk that is to used
         #   system_name = model_fname_dict['file_name']

            system_name = rank_para['systempattern']
            system_name = system_name.replace("(\\d+)", model_fname_dict['fid'])
            topksent_path = system_path + '\\' + system_name + '.'+system_id
            #topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

            graph_dict, matrix_dict,sentence_data_dict=sxpSurveyData.LoadFileDataByGraphFid(graph_name)

#************************************************************************************
# NOTE That sxpRankingDoc.RankDocUseSentenceDict is to use abstract, conclusion, and both to produce
# a test result without actually ranking sentences.
#************************************************************************************
       #     tops = sxpRankingDoc.RankDocDemo(eachtest,model_fname_dict)
            tops = RankDocUseSentenceDictTestCaseNameTopkName(testcasename,topkname,sentence_data_dict)
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
def RankDocUseSentenceDictTestCaseNameTopkName(TestCaseName,TopkName,sentence_data_dict):
    if TestCaseName == 'test_abs':
        tops = []
#        for kid in sorted(sentence_data_dict['abstract'].keys()):
        for (sid, sent) in sentence_data_dict['abstract']:
            tops.append(sent)
  #         print(kid, sentence_data_dict['abstract'][kid])
#           tops.append(sentence_data_dict['abstract'][kid])
        return tops
    if TestCaseName == 'test_con':
        tops = []
        for (sid, sent) in sentence_data_dict['conclusion']:
            tops.append(sent)
  #      for kid in sorted(sentence_data_dict['conclusion'].keys()):
  #         print(kid, sentence_data_di鼻子ct['abstract'][kid])
  #         tops.append(sentence_data_dict['conclusion'][kid])
        return tops
    if TestCaseName == 'test_abscon':
        tops = []
        for (sid, sent) in sentence_data_dict['abstract']:
            tops.append(sent)
        for (sid, sent) in sentence_data_dict['conclusion']:
            tops.append(sent)

#        for kid in sorted(sentence_data_dict['abstract'].keys()):
  #         print(kid, sentence_data_dict['abstract'][kid])
#           tops.append(sentence_data_dict['abstract'][kid])
#        for kid in sorted(sentence_data_dict['conclusion'].keys()):
  #         print(kid, sentence_data_dict['abstract'][kid])
#           tops.append(sentence_data_dict['conclusion'][kid])
        return tops
    if TestCaseName == 'test_raw':
        tops = []
        for each in sentence_data_dict['sent_list']:
            tops.append(each)
        return tops;

    tops = []
    testname = TestCaseName #'wordquery_allv6ks_dual_sentrank'
    survgenmethod = TopkName #'opt_num'
    #so, this function will load the whole survey gen sentences as one paper
    #it is obtained in TraverseMakeSurvey() function in sxpSurveyData
    tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
    return tops


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
    print('eachpk_sys in pk_sys_set, note that in this version,this list is not used because, we use model_list file to product tops')
    for eachpick in pk_sys_set:
        print(eachpick)

    model_test_output_dict ={}
    for eachtest in testset:
        print('---------',eachtest)
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
            graph_name = model_fname_dict['fid'] #here fid is p_0000, but in our surveydata it is p_0000.pk that is to used
         #   system_name = model_fname_dict['file_name']

            system_name = rank_para['systempattern']
            system_name = system_name.replace("(\\d+)", model_fname_dict['fid'])
            topksent_path = system_path + '\\' + system_name + '.'+system_id
            #topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

            graph_dict, matrix_dict,sentence_data_dict=sxpSurveyData.LoadFileDataByGraphFid(graph_name)

#************************************************************************************
# NOTE That sxpRankingDoc.RankDocUseSentenceDict is to use abstract, conclusion, and both to produce
# a test result without actually ranking sentences.
#************************************************************************************
       #     tops = sxpRankingDoc.RankDocDemo(eachtest,model_fname_dict)
            tops = RankDocUseSentenceDict(eachtest,sentence_data_dict)
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

def RankDocUseSentenceDict(eachtest,sentence_data_dict):
    if eachtest == 'test_abs':
        tops = []
#        for kid in sorted(sentence_data_dict['abstract'].keys()):
        for (sid, sent) in sentence_data_dict['abstract']:
            tops.append(sent)
  #         print(kid, sentence_data_dict['abstract'][kid])
#           tops.append(sentence_data_dict['abstract'][kid])
        return tops
    if eachtest == 'test_con':
        tops = []
        for (sid, sent) in sentence_data_dict['conclusion']:
            tops.append(sent)
  #      for kid in sorted(sentence_data_dict['conclusion'].keys()):
  #         print(kid, sentence_data_di鼻子ct['abstract'][kid])
  #         tops.append(sentence_data_dict['conclusion'][kid])
        return tops
    if eachtest == 'test_abscon':
        tops = []
        for (sid, sent) in sentence_data_dict['abstract']:
            tops.append(sent)
        for (sid, sent) in sentence_data_dict['conclusion']:
            tops.append(sent)

#        for kid in sorted(sentence_data_dict['abstract'].keys()):
  #         print(kid, sentence_data_dict['abstract'][kid])
#           tops.append(sentence_data_dict['abstract'][kid])
#        for kid in sorted(sentence_data_dict['conclusion'].keys()):
  #         print(kid, sentence_data_dict['abstract'][kid])
#           tops.append(sentence_data_dict['conclusion'][kid])
        return tops
    if eachtest == 'test_raw':
        tops = []
        for each in sentence_data_dict['sent_list']:
            tops.append(each)
        return tops;
    if eachtest == 'test_dual_num':
        tops = []
        testname = 'wordquery_allv6ks_dual_sentrank'
        survgenmethod ='opt_num'
        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        return tops;
    if eachtest == 'test_dual_abs':
        tops = []
        testname = 'wordquery_allv6ks_dual_sentrank'
        survgenmethod ='abstract'
        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        return tops;
    if eachtest == 'test_tfidf_num':
        testname = 'tfidf_all'
        survgenmethod ='abstract'

        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        return tops;
    if eachtest == 'test_dtfipf_sent_org':
        testname = 'dtfipf_all_stop'
        survgenmethod ='orig'
        tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
        return tops
    if eachtest == 'test_bm25_LR':
        testname = 'tfidf_BM25'
        survgenmethod = 'LR'
        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        return tops;
    if eachtest == 'test_dual_lr':
        testname = 'wordquery_allv6ks_dual_sentrank'
        survgenmethod ='LR'

        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        return tops;
    if eachtest == 'test_dtfipf_lr':
        testname = 'dtfipf_all_stop'
        survgenmethod ='LR'
        tops = sxpSurveyData.LoadGenSurveySentList(testname,survgenmethod)
        return tops;
    if eachtest == 'test_origin_abs':
        testname = 'test_origin'
        survgenmethod ='origin_abs'
        #tops = sxpSurveyData.LoadGenSurveySentList(fid, survgenmethod=survgenmethod, testname=testname)
        tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
        return tops;
    if eachtest == 'test_origin_diffabs':
        testname = 'test_origin'
        survgenmethod ='diff_abs'
        #tops = sxpSurveyData.LoadGenSurveySentList(fid, survgenmethod=survgenmethod, testname=testname)
        tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
        return tops;
    if eachtest == 'test_origin_simabs':
        testname = 'test_origin'
        survgenmethod ='sim_abs'
        #tops = sxpSurveyData.LoadGenSurveySentList(fid, survgenmethod=survgenmethod, testname=testname)
        tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
        return tops;


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
