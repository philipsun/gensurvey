# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 00:19:43 2018

@author: sunxp
"""

#-------------------------------------------------------------------------------
# Name:        sxpTestDucMultSum.py
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

import sxpTestMan
import sxpDUC2007main
from sxpDataDucMultSum import sxpNode
from sxpLoadRankPara import MakeDemoRankPara, GetFName
cwd = os.getcwd()
def main():
    TestDemo()
   # RenameSystem()
def MakePaperPara(project_name,test_case_name,idname,model_test):
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
    rouge_dir =cwd + sxpLoadRankPara.rouge_path
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
        "pickle_path": pk_dir,
        "model_path": model_dir,
        "rouge_dir": rouge_dir,
        "perl_path": perl_path,
        "system_path" : system_dir, #this is to store each system file produced by ranking models
        'modelpattern':  r'#ID#.M.\d\d\d.[A-Z].[A-Z]', #'D061.M.010.J.B'
        'systempattern': r'{0}_(D\d+)[A-Z].html'.format(test_case_name),
        'model_filenames_pattern_id' : r'(D\d+).M.\d\d\d.[A-Z].[A-Z].html',
        'system_filename_pattern_id' : r'{0}_#ID#[A-Z].html'.format(test_case_name), #mult_D061J.html.01
        'pickle_file_pattern_id' :r'{0}_#ID#.pk'.format(test_case_name), # inc_test
        'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    rankpara_fname = test_dir +'/rank_para.pk'
    sxpReadFileMan.StoreSxptext(rank_para,rankpara_fname)
    return rank_para
def TestDemo():
    project_name = 'duc2007mult'
    test_case = 'mult'
    idname ={'head1':'01',
             'head2':'02',
             'random':'03',
             'bymodel0':'04',
             'clustersent':'05'
             }
    model_idname = idname#sxpRougeConfig.idname
    #model_test =['top5','top4','random','manual100']
    model_test = ['head1','head2','bymodel0']

     #this is to rank_parameter dict for this demo:

    rank_para = MakePaperPara(project_name, test_case, model_idname, model_test)
    print(('project ',project_name,'test_case', test_case,'***************'))
    for k,v in list(rank_para.items()):
        print((k, v))
    #  cmd = ['makemodel']
   # cmd = ['makemodel','rank','score']
    cmd = ['rank','score']
    if 'makemodel' in cmd:
        #this is to make model files for a set of inputting model files:
        print(('make model files for ',project_name,'test_case', test_case,'***************'))
        doc_model_sent_file_list = sxpDUC2007main.LoadDocModelSentence()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
        DoMakeModel(project_name,test_case,doc_model_sent_file_list)
    if 'rank' in cmd:
        #this is to make a testing top-k sentences for the two test methods, they are the same
        print(('make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************'))
        model_test_output_dict=ProduceTestRank(project_name,test_case,model_test)
    #    print(model_test_output_dict)
        sxpTestMan.WriteSystemOutput(rank_para,model_test_output_dict)
    if 'score' in cmd:
        print(('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************'))
        #this is to make a testing top-k sentences for the two test methods, they are the same
       # rankcmd = 'plot'
        rankcmd = 'all'
        sxpTestMan.DoRougeScore(project_name,test_case,cmd=rankcmd)

def DoMakeModel(project_name,test_case_name,doc_model_sent_file_list):
    fname_dict=GetFName(project_name,test_case_name)
    rankpara_fname = fname_dict['rankpara_fname']
    model_dir = fname_dict['model_dir']# r'./test/demo/model'

    sxpReadFileMan.StoreSxptext(doc_model_sent_file_list,fname_dict['doc_model_sent_file_list'])

    PrepareModelForRawSentencePk(project_name,test_case_name,doc_model_sent_file_list,model_dir)
def PrepareModelForRawSentencePk(project_name,test_case_name,doc_model_sent_file_list,model_dir):
    # you need to make a model file for a set of files to be evaluated,
    # Each file has one model file in a directory.
    # in eachdoc in raw_doc_dir, it contains sentence sets of each model that have been extracted by other raw data preprocessors
    # this funciton is only to make model file for the each such pk file containing sentence sets.
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
    sxpReadFileMan.CheckMkDir(model_dir)
    model_id = ['A','B','C','D','E','F','G','H']
  #  doc_sent_list = sxpReadFileMan.GetDirFile(raw_doc_dir,'pk')
    i = 0
    model_file_list = []
    model_doc_list = []
    for i, eachdoc in enumerate( doc_model_sent_file_list):
       # fid = '{0:0>4}'.format(i)
        fid = eachdoc['fid']
        file_name = '{0}_{1}'.format(test_case_name,fid)
        sub_models = []
        for i, (model_info,eachmodel) in enumerate( eachdoc['model']):
          #  model_file_name = file_name +'.'+ model_id[i] +'.html'
            model_file_name = model_info['file_name']
            print(model_file_name)
            sent_list =[]
            models={}
            models[model_file_name]=eachmodel

            model_fname_dict = {}
            model_fname_dict['docid']=fid
            model_fname_dict['fid']=model_info['fid']
            model_fname_dict['file_name']=model_file_name
            model_fname_dict['sent_list']=sent_list
            model_fname_dict['models']=models
            model_file_list.append(model_fname_dict)
            sub_models.append(model_fname_dict)
        model_doc_list.append(fid)
    sxpReadFileMan.StoreSxptext(model_file_list,fname_dict['model_file_list'])
    sxpReadFileMan.StoreSxptext(model_doc_list,fname_dict['model_doc_list'])
    sxpTestMan.WriteModelFile(model_file_list,model_dir)
    return model_file_list

def ProduceTestRank(project_name,test_case,testset):
    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']
    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)

    model_dir = fname_dict['model_dir']# r'./test/demo/model'

    model_file_list=sxpReadFileMan.LoadSxptext(fname_dict['model_file_list'])
    model_doc_list=sxpReadFileMan.LoadSxptext(fname_dict['model_doc_list'])
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
        for docid in model_doc_list:
#************************************************************************************
# NOTE That model_fname_dict is produced in sxpTestMan.PrepareModelForRawSentencePk()
#************************************************************************************
##            model_fname_dict = {}
##            model_fname_dict['fid']=fid
##            model_fname_dict['file_name']=file_name
##            model_fname_dict['sent_list']=sent_list
##            model_fname_dict['models']=models
#************************************************************************************
##            s = docid.split('.')
##            subdir = s[0]
##            lens = s[1]
            lens='all'
            print(docid)
            system_name = test_case+'_'+ docid
            topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id
            tops=[]
            st=[]
        #    graph_dict, matrix_dict,sentence_data_dict= sxpMultiPaperData.LoadFileData(graph_dict_fid)
           # sxpdocdict = sxpDataDucMultSum.LoadRawPkByDocId(docid)
            tops = RankDocDemo(eachtest, docid,lens)
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
def RenameSystem():
    dirname = r'E:\pythonworknew\code\sentencerank\test\duc2002mult\mult\system'
    flist = sxpReadFileMan.GetDirFileList(dirname)
    head = 'mult_'
    for each in flist:
        newname =dirname + '\\' + head + each
        oldname = dirname +'\\' + each
        print((oldname,newname))
        os.rename(oldname,newname)
def RankDocDemo(eachtest,docid,lens):
    tops = []
    # if eachtest == 'abstract':
    #     for eachsent in GetAbsConSent(sxptxt.abstract):
    #         tops.append(eachsent)
    # if eachtest == 'conclusion':
    #     for eachsent in GetAbsConSent(sxptxt.conclusion):
    #         tops.append(eachsent)
    if eachtest == 'head1':
        tops = sxpDUC2007main.LoadSys(eachtest, docid)
    if eachtest == 'head2':
        tops = sxpDUC2007main.LoadSys(eachtest, docid)
    if eachtest == 'bymodel0':
        tops = sxpDUC2007main.LoadSys(eachtest,docid)
    print(tops)
    return tops
def GetRandom(sxptxtlist,docid,topk):
    sxplist=sxptxtlist[docid]
    sxptxtdict = sxplist[0]
    sxptxt =sxptxtdict['sxptxt']
    n = len(sxptxt.sentence_textset)
    rd = np.random.choice(n,topk)
    tops=[]
    for i in rd:
        tops.append(sxptxt.sentence_textset[i])
    return tops
def GetTopK(sxptxtlist,docid,topk):
    sxplist=sxptxtlist[docid]
    sxptxtdict = sxplist[0]
    sxptxt =sxptxtdict['sxptxt']
    tops = []
    for i, s in enumerate( sxptxt.sentence_textset[0:topk]):
        tops.append(s)
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
