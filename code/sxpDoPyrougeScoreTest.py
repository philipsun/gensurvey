#coding=utf-8
# Name:        sxpCallPyrougeScore
# Purpose:
#
# Author:      kgxp
#
# Created:     10-11-2015
# Copyright:   (c) kgxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import sxpTimeManage
from pyrouge import Rouge155
from pyrouge import MyRouge155
from graphengine import sxpGraphEngine
from graphengine.sxpGraphEngine import *
from graphengine import sxpParseMyNet

#-------------------------------------------------------------------------------
import subprocess
from subprocess import check_output
import sxpReadFileMan
import xlrd
import xlsxwriter
import os
import re
import codecs
import sxpPyrougeEvaluate
import sxpRougeConfig
import pandas as pd
import sxpKeywordEvaluate
idname = sxpRougeConfig.GetNameID()
print 'idname',idname
nameid = {}
for eachkey,eachv in idname.items():
    nameid[eachv]=eachkey
print 'nameid',nameid
def GetSystemID(testset):
    test_id =[]
    for eachtest in testset:
        test_id.append(idname[eachtest])
    return test_id

dataroot = r'E:\pythonwork\code\paperparse\paper'
if os.path.exists(dataroot)==False:
    dataroot = r'E:\pythonworknew\code\paperparse\paper'
sxpPyrougeEvaluate.conf_path = r'.\rouge_conf.xml'
sxpPyrougeEvaluate.perlpathname=r'C:\Perl\bin\perl'

def PrintModelName(testlist):
    for each in testlist:
        print idname[each]
def DoPyrougeScoreByRankPara(rankpara,onlyid=[]):
    fhead=PrepareFilePrefix(rankpara)
    system_model_id = sxpRougeConfig.GetSystemID(rankpara['model_test'])
    output_fname = fhead+'.pk'#"output_set_model1_inc.pk"
    out_dir = rankpara['outdir']
    system_path =rankpara['system_path']
    model_path = rankpara['model_path']
    modelpattern =rankpara['modelpattern']
    systempattern =rankpara['systempattern']
    sxpReadFileMan.CheckMkDir(system_path)
    sxpReadFileMan.CheckMkDir(out_dir)
    if not rankpara.has_key('conf_path'):
        conf_path = r'E:\pythonworknew\code\paperparse\paper\rouge_conf.xml'
    else:
        conf_path =rankpara['conf_path']
    full_rouge_set_txtfile_name, full_rouge_set_pkfile_name = sxpPyrougeEvaluate.CallMyPyrougeOut(system_path,
    model_path,modelpattern,systempattern,out_dir,fhead,system_model_id,conf_path,onlyid=onlyid)
    return  full_rouge_set_txtfile_name, full_rouge_set_pkfile_name
def MakeAllFileCSV(dict_conf_name):
    rankpara = sxpRougeConfig.GetRankPara(dict_conf_name)
    out_dir = rankpara['outdir']
    system_path =rankpara['system_path']
    system_model_id = sxpRougeConfig.GetSystemID(rankpara['model_test'])
    systempattern =rankpara['systempattern']
##    all_mode_files = sxpdorank.GetSystemModelFilePair(rankpara)
##    for eachmodel in all_mode_files:
##        for eachfiles in eachmodel:
##            print eachfiles
    system_dir = rankpara['system_path']
    print system_dir
    model_dir = rankpara['model_path']
    print model_dir
    system_idset = system_model_id
    model_filenames_pattern = rankpara['modelpattern']
    print model_filenames_pattern
    system_filename_pattern = rankpara['systempattern']#system_filename_pattern_id
    print system_filename_pattern
    mod_sys=sxpPyrougeEvaluate.ProduceSysModPair(system_dir,model_dir,system_idset,model_filenames_pattern,system_filename_pattern)
    print len(mod_sys)
    pickle_file_pattern_id = rankpara['pickle_file_pattern_id']

    pickle_path = rankpara['pickle_path']#'papers\duc\txt\pickle')
    model_path =  rankpara['model_path']#,r'papers\duc\txt\model_html')
    system_path = rankpara['system_path']#',r'papers\duc\txt\system_html1')
    print pickle_path
    print model_path
    print system_path
    print nameid
    allmodel_file_list=[]
    for eachone in mod_sys:
        print "--"
        print eachone
        sys_file_model_list = eachone[0]
        print sys_file_model_list
        model_file_list=eachone[1]
        print model_file_list
        model_filename_list =[]
        for eachmodel in model_file_list:
            modelf = os.path.join(model_dir,eachmodel)
            model_filename_list.append(modelf)
        for each_model in sys_file_model_list:
            print each_model
            fid = each_model[0]
            model_id = each_model[1]
#            print nameid[model_id]
            sys_file = each_model[2]
            file_dict = {}
            file_dict['fid']=fid
            file_dict['model_id']=str(model_id)
            file_dict['model_name']=nameid[model_id]
            file_dict['sysfname']=system_path + '\\' + sys_file
            pkfname =pickle_file_pattern_id.replace('#ID#',fid)
            file_dict['pkfnameid']=pkfname
            file_dict['pkfname']=os.path.join(pickle_path,pkfname)
            file_dict['allsent']= file_dict['sysfname'] + 'allsent.pk'
            file_dict['topsentpk']=file_dict['sysfname'] + 'topsent.pk'
            file_dict['keywordfile']=os.path.join(rankpara['keyword_path'],pkfname +'.keytree')
            file_dict['modelfiles']=model_filename_list
            allmodel_file_list.append(file_dict)
    for each in allmodel_file_list:
        print each
    df =pd.DataFrame(allmodel_file_list)
    print df.head()
    print df['modelfiles'][0]
    allfilename = os.path.join(out_dir,'allfilelist.csv')
    df.to_csv(allfilename)
def GetModSysFileNames(dict_conf_name,cmd="pkfilename",model_id=[]):
    rankpara = sxpRougeConfig.GetRankPara(dict_conf_name)
    out_dir = rankpara['outdir']
    system_path =rankpara['system_path']
    system_model_id = sxpRougeConfig.GetSystemID(rankpara['model_test'])
    systempattern =rankpara['systempattern']
    allfilename = os.path.join(out_dir,'allfilelist.csv')
    model_test = rankpara['model_test']

    df = pd.read_csv(allfilename)
    if cmd == 'all':
        return df
    if cmd =="pkfnameid":
        return df['pkfnameid']
    if cmd == "modelfiles":
        return df['modelfiles']
    if cmd=='pkfilename':
        return df['pkfname'].unique()
    if cmd=='keywordfile':
        uniquekey= df['pkfnameid'].unique()
        keyf_list=[]
      #  print uniquekey
        for each in uniquekey:
            keyf =[each,os.path.join(rankpara['keyword_path'],each+'.keytree')]
            keyf_list.append(keyf)
        return keyf_list
    if cmd =='sysfname':
        return df['sysfname']
    if cmd == 'topkfname':
        return df['topsentpk']
    if cmd == 'modeltopk':
        print df['model_id']
        model_sys_dict={}
        print model_test
        for eachtest in model_test:
            model_sys= df[df['model_id']==int(idname[eachtest])]
            model_sys_dict[idname[eachtest]]=model_sys#model_sys['topsentpk']
         #   print model_sys['topsentpk'].size
        return model_sys_dict
def CompareTopkWithKeyword(dict_conf_name,buildtree=False):
    rankpara = sxpRougeConfig.GetRankPara(dict_conf_name)
    out_dir = rankpara['outdir']
    system_path =rankpara['system_path']
    system_model_id = sxpRougeConfig.GetSystemID(rankpara['model_test'])

    model_sys_file_dict = GetModSysFileNames(dict_conf_name,'modeltopk')
    model_score = []
    keydb_store = rankpara['keyword_path']
    if buildtree==True:
        keyfiles=GetModSysFileNames(dict_conf_name,'keywordfile')
        for each in keyfiles:
            print '----build keytree db-----:',each[0],each[1],keydb_store
            sxpKeywordEvaluate.BuildTree(keydb_store,each[1],each[0])
            print '--------------------------:'
    for eachmodel,sysfile_df in model_sys_file_dict.items(): #for each model/method
         for row_index, row in sysfile_df.iterrows():       # we collect each system file's score
             print '---------distance computing------------'

             model_score_dict ={}
             model_score_dict['model_id']=eachmodel
             model_score_dict['pkfnameid']=row['pkfnameid']
             model_score_dict['model_name']=row['model_name']

             fid = row['pkfnameid']
             topkfilepk = row['topsentpk']
             sentlist = sxpReadFileMan.LoadSxptext(topkfilepk)
             print(fid)
             print sentlist
             doc_sent_list=[sentlist]
             score_val = sxpKeywordEvaluate.ComputeOneDistance(doc_sent_list,keydb_store,fid)
             model_score_dict['score']=score_val
             model_score.append(model_score_dict)
             print '--------------------------:'
    df = pd.DataFrame(model_score)
    fname = os.path.join(out_dir,dict_conf_name+'.keyscore.csv')
    df.to_csv(fname)

 #   print scipy.spatial.distance.jaccard(str1,str2)
def PrepareFilePrefix(rankpara):
    mid = []
    for eachmod in rankpara['model_test']:
        mid.append( idname[eachmod])
    smid = '_'.join(mid)
    shead = rankpara['rougetxthead']
    fileprefix = shead+'_'+smid
    return fileprefix
def RunConfig(dict_conf_name,rankthem =0,rougethem = 0,ifshow =0,onlyid=[]):
    rankpara = sxpRougeConfig.GetRankPara(dict_conf_name)
    PrintModelName(rankpara['model_test'])
    if rankthem == 1:
      #RunRankTest(rankpara,rankwho=rankpara['plotwho'])
      DoRank(rankpara)
    if rougethem == 1:
        txtf,pkf = DoPyrougeScoreByRankPara(rankpara,onlyid=onlyid)
        print txtf,pkf
        if ifshow:
            sxpRougeConfig.PlotScore(dict_conf_name,ifshow =ifshow)
    else:
        sxpRougeConfig.PlotScore(dict_conf_name,ifshow =ifshow)

import sys
sys.path.append('./context')
from context import sxpdorank
import context.sxpPackage
from context.sxpPackage import *
def DoRank(rankpara):
    dataroot = rankpara['dataroot']
    CheckDataRootDir(dataroot,rankpara)
    sxpdorank.RankPara(rankpara)
def CheckDataRootDir(dataroot,rankpara):
    sxpReadFileMan.CheckMkDir(rankpara['outdir'])
    sxpReadFileMan.CheckMkDir(os.path.join(dataroot,rankpara['pickle_path']))
    sxpReadFileMan.CheckMkDir(os.path.join(dataroot,rankpara['model_path']))
    sxpReadFileMan.CheckMkDir(os.path.join(dataroot,rankpara['system_path']))

if __name__ == '__main__':
    cmdstr = "RunRankAndParseScore"
    if cmdstr == 'RunRankAndParseScore':
##        RunConfig('single_withstop',1,0)
        rankthem =0
        rougethem =0
        RunConfig('duc_withoutstop_max100',rankthem,rougethem)
##        RunConfig('duc_withstop_max100',rankthem,rougethem)
##        RunConfig('duc_withoutstop_topk',rankthem,rougethem)
##        RunConfig('duc_withstop_topk',rankthem,rougethem)
        ifshow = 1
##        RunConfig('acl_exc_withoutstop_max100',rankthem,rougethem,ifshow =ifshow)
##        RunConfig('acl_inc_withoutstop_max100',rankthem,rougethem,ifshow =ifshow)
##        RunConfig('acl_exc_withstop_max100',rankthem,rougethem,ifshow =ifshow)
##        RunConfig('acl_inc_withstop_max100',rankthem,rougethem,ifshow =ifshow)
##        RunConfig('acl_exc_withoutstop_topk',rankthem,rougethem,ifshow =ifshow)
##        RunConfig('acl_inc_withoutstop_topk',rankthem,rougethem,ifshow =ifshow)
##        RunConfig('single_withoutstop',rankthem,rougethem,ifshow =ifshow)
##        MakeAllFileCSV('single_withoutstop')
##        print GetModSysFileNames('single_withoutstop','modeltopk')
##        RunConfig('single_withoutstop_steplen',rankthem,rougethem,ifshow =ifshow)
##        RunConfig('single_withoutstop_steplen_sim',rankthem,rougethem,ifshow =ifshow)
    if cmdstr == "keytree":
    #    MakeAllFileCSV('single_withoutstop')
      #  print GetModSysFileNames('single_withoutstop','keywordfile')[0]
        #TestBuildTree() #first build tree
       # TestRankNetwork() #sec rank nodes on the tree
       #TestGraphScore() # test evaluation, now they are all test ok
        CompareTopkWithKeyword('single_withoutstop',buildtree=False)