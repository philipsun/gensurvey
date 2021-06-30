# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 00:19:43 2018

@author: sunxp
"""

#-------------------------------------------------------------------------------
# Name:        sxpTestMultiPaper.py
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
import sxpMultiPaperData
from sxpMultiPaperData import sxpNode

def main():
    TestDemo()

def TestDemo():
    project_name = 'multipaper'
    test_case = 'test'
    idname ={'test':'01','graph':'02'}
    model_idname = idname#sxpRougeConfig.idname
    model_test =['test','graph']

     #this is to rank_parameter dict for this demo:
    rank_para = MakeMultiPaperPara(project_name, test_case, model_idname, model_test)
    print(('project ',project_name,'test_case', test_case,'***************'))
    for k,v in list(rank_para.items()):
        print(k, v)

    cmd = ['makemodel','rank','score']
    cmd = ['score']
    if 'makemodel' in cmd:
        #this is to make model files for a set of inputting model files:
        print(('make model files for ',project_name,'test_case', test_case,'***************'))
        doc_model_sent_file_list = sxpMultiPaperData.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
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
        rankcmd = 'plot'
        sxpTestMan.DoRougeScore(project_name,test_case,rankcmd)



def ProduceTestRank(project_name,test_case,testset):
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

            graph_dict, matrix_dict,sentence_data_dict= sxpMultiPaperData.LoadFileData(graph_dict_fid)

            tops = sxpRankingDoc.RankDocDemo(eachtest, model_fname_dict)
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
