#-------------------------------------------------------------------------------
# Name:        模块1
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

#when using sypder, when upgrade it to pyqt5, it will not work, because pyqt5 works for python3 no.t for python 2.7o
#so you need to conda install pyqt=4.11.4 to down grade the pyqt to enable it work with python 2.7
##import sys
##sys.path.append('./context')
from context import sxpdorank
import context.sxpPackage
from context.sxpPackage import *

import sxpPyrougeEvaluate
import sxpParseRougeScore
import sxpRankingDoc
import sxpModelFileMan
from sxpLoadRankPara import MakeDemoRankPara, GetFName

def main():
    TestDemo()

def TestDemo():
    project_name = 'demo'
    test_case = 'test'
    idname ={'test':'01','graph':'02'}
    model_idname = idname#sxpRougeConfig.idname
    model_test =['test','graph']

     #this is to rank_parameter dict for this demo:
    rank_para= MakeDemoRankPara(project_name,test_case,model_idname,model_test)
    print('project ',project_name,'test_case', test_case,'***************')
    for k,v in rank_para.items():
        print(k, v)

    #this is to make model files for a set of inputting model files:
    print('make model files for ',project_name,'test_case', test_case,'***************')
    cmd = ['makemodel','rank','score']
   # cmd = ['score']
    if 'makemodel' in cmd:

        doc_model_sent_file_list = sxpModelFileMan.LoadDemo()#[[['hellow'],['good']],[['doc2','sent1'], ['doc2', 'sent2']]]
    #    print(doc_model_sent_file_list)
        DoMakeModel(project_name,test_case,doc_model_sent_file_list)

    if 'rank' in cmd:
    #this is to make a testing top-k sentences for the two test methods, they are the same
        print('make a test rank result top sentence files for ',project_name,'test_case', test_case,'***************')
        model_test_output_dict=ProduceTestRank(project_name,test_case,model_test)
    #    print(model_test_output_dict)
        WriteSystemOutput(rank_para,model_test_output_dict)

    if 'score' in cmd:
        print('do ROUGE score for the top sentence files in ',project_name,'test_case', test_case,'***************')
        #this is to make a testing top-k sentences for the two test methods, they are the same
        rankcmd = 'all'
        DoRougeScore(project_name,test_case,rankcmd)

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

    pk_sys_set = PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,
        pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)

    model_test_output_dict ={}
    for eachtest in testset:
        system_id= modelidname[eachtest]
        output_dict_list = []
        for eachdoc_dict in model_file_list:
            fid = eachdoc_dict['fid']
            system_name = eachdoc_dict['file_name']
            topksent_path = system_path + '\\' + system_name + '.html'+ '.'+system_id

            tops = sxpRankingDoc.RankDocDemo(eachtest,eachdoc_dict)
            st = ProduceSystem(tops,system_name,1)
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


def DoRougeScore(project_name,test_case, cmd='all'):
    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']
    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)
    if cmd == 'all':
        cmdlist = ['rouge','plot']
    else:
        cmdlist = [cmd]
    if 'rouge' in cmdlist:
        txtf,pkf =  DoPyrougeScoreByRankPara(rank_para)
        print(txtf,pkf)

    if 'plot' in cmdlist:
        PlotScore(project_name,test_case,ifshow =1)
def PlotScore(project_name,test_case,ifshow =0):
    fname_dict=GetFName(project_name,test_case)
    rankpara_fname = fname_dict['rankpara_fname']


    rank_para = sxpReadFileMan.LoadSxptext(rankpara_fname)
    scoreoutputdir = rank_para['outdir']#r'D:\pythonwork\code\tjrank_sentences\context\result\r3smax100'
    fhead = PrepareFilePrefix(rank_para)
    methodhead = rank_para['rougetxthead']#scoreoutputdir.split('\\')[-1]
    sxpReadFileMan.CheckMkDir(scoreoutputdir)
    para_file_name =methodhead + '_' +fhead +'_rankpara.pk'
    rankparafname = os.path.join(scoreoutputdir,para_file_name)
    sxpReadFileMan.StoreSxptext(rank_para, rankparafname)

    out_dir = rank_para['outdir']
    txtfilename = os.path.join(out_dir,fhead + '.txt')
    #sxpParseRougeScore.TestSxpPyrougeScoreTxtFile(txtfilename,scoreoutputdir,project_name+'_'+test_case,ifshow =0)
    modelid_dict = rank_para['idname']
    sxpParseRougeScore.ParseScoreTxt(txtfilename,scoreoutputdir,dict_conf_name=project_name+'_'+test_case,ifshow =ifshow,modelid_dict=modelid_dict)
def PlotScoreRankPara(rank_para,project_name,test_case,ifshow =0):
    scoreoutputdir = rank_para['outdir']#r'D:\pythonwork\code\tjrank_sentences\context\result\r3smax100'
    fhead = PrepareFilePrefix(rank_para)
    methodhead = rank_para['rougetxthead']#scoreoutputdir.split('\\')[-1]
    sxpReadFileMan.CheckMkDir(scoreoutputdir)
    para_file_name =methodhead + '_' +fhead +'_rankpara.pk'
    rankparafname = os.path.join(scoreoutputdir,para_file_name)
    sxpReadFileMan.StoreSxptext(rank_para, rankparafname)

    out_dir = rank_para['outdir']
    txtfilename = os.path.join(out_dir,fhead + '.txt')
    #sxpParseRougeScore.TestSxpPyrougeScoreTxtFile(txtfilename,scoreoutputdir,project_name+'_'+test_case,ifshow =0)
    modelid_dict = rank_para['idname']
    sxpParseRougeScore.ParseScoreTxt(txtfilename,scoreoutputdir,dict_conf_name=project_name+'_'+test_case,ifshow =ifshow,modelid_dict=modelid_dict)
def DoPyrougeScoreByRankPara(rank_para,onlyid=[]):
    fhead=PrepareFilePrefix(rank_para)

    system_model_id = GetSystemID(rank_para['model_test'], rank_para['idname'])
    out_dir = rank_para['outdir']
    system_path =rank_para['system_path']
    model_path = rank_para['model_path']
    modelpattern =rank_para['modelpattern']
    systempattern =rank_para['systempattern']
    rouge_dir = rank_para['rouge_dir']
    perl_path = rank_para['perl_path']
    if 'rouge_args' in rank_para.keys():
        rouge_args = rank_para['rouge_args']
    else:
        rouge_args = None
    sxpReadFileMan.CheckMkDir(system_path)
    sxpReadFileMan.CheckMkDir(out_dir)
    if 'conf_path' not in rank_para.keys(): #has_key('conf_path'):
        conf_path = r'.\rouge_conf.xml'
    else:
        conf_path =rank_para['conf_path']
    print('conf_path',conf_path)
    full_rouge_set_txtfile_name, full_rouge_set_pkfile_name = sxpPyrougeEvaluate.CallMyPyrougeOut(system_path,
        model_path,modelpattern,systempattern,out_dir,fhead,system_model_id,conf_path,rouge_dir=rouge_dir, perl_path = perl_path,rouge_args=rouge_args,onlyid=onlyid)
    return  full_rouge_set_txtfile_name, full_rouge_set_pkfile_name
 #   print scipy.spatial.distance.jaccard(str1,str2)

def PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,pickle_file_pattern_id,system_filename_pattern_id):
    flist, sublist = sxpReadFileMan.sxpGetDirFileSubList(model_path)
    model_filenames_pattern_id = re.compile(model_filenames_pattern_id)
    model_set_id = {}
    i = 0
    for eachf in flist:
        match = model_filenames_pattern_id.match(eachf)
        if match:
            id = match.groups(0)[0]
            model_set_id[id] = (i,eachf)
            i = i + 1

    pk_sys_set = []
    for eachid,(i,eachf) in model_set_id.items():
        pk_sys_set.append([pickle_file_pattern_id.replace('#ID#', eachid),system_filename_pattern_id.replace('#ID#', eachid)])

    return pk_sys_set


def PrepareFilePrefix(rank_para):
    mid = []
    idname =rank_para['idname']
    for eachmod in rank_para['model_test']:
        mid.append( idname[eachmod])
    smid = '_'.join(mid)
    shead = rank_para['rougetxthead']
    fileprefix = shead+'_'+smid
    return fileprefix

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
    pk_dir =  fname_dict['pk_dir'] #not used yet for current test_case because
    out_dir = fname_dict['out_dir']
    sxpReadFileMan.CheckMkDir(model_dir)
    model_id = ['A','B','C','D','E','F','G','H']
  #  doc_sent_list = sxpReadFileMan.GetDirFile(raw_doc_dir,'pk')
    i = 0
    model_file_list = []
    for i, eachdoc in enumerate( doc_model_sent_file_list):
       # fid = '{0:0>4}'.format(i)
        fid = eachdoc['fid']
       # file_name = '{0}_{1}'.format(test_case_name,fid)
        file_name = '{0}_{1}'.format(project_name, fid) #here the latest version of model file naming schema
        models ={}
        sent_list =[]
        for i, eachmodel in enumerate( eachdoc['model']):
            model_file_name = file_name +'.'+ model_id[i] +'.html'
            models[model_file_name]=eachmodel
            for eachsent in eachmodel:
                sent_list.append(eachsent)
        model_fname_dict = {}
        model_fname_dict['fid']=fid
        model_fname_dict['file_name']=file_name
        model_fname_dict['sent_list']=sent_list
        model_fname_dict['models']=models
        model_file_list.append(model_fname_dict)

    sxpReadFileMan.StoreSxptext(model_file_list,fname_dict['model_file_list'])
    WriteModelFile(model_file_list,model_dir)
    return model_file_list
def DoMakeModelFID(project_name,test_case_name,doc_model_sent_file_list):
    fname_dict=GetFName(project_name,test_case_name)
    rankpara_fname = fname_dict['rankpara_fname']
    model_dir = fname_dict['model_dir']# r'./test/demo/model'

    sxpReadFileMan.StoreSxptext(doc_model_sent_file_list,fname_dict['doc_model_sent_file_list'])

    PrepareModelForRawSentencePkModelFID(project_name,test_case_name,doc_model_sent_file_list,model_dir)
def PrepareModelForRawSentencePkModelFID(project_name,test_case_name,doc_model_sent_file_list,model_dir):
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
    for i, eachdoc in enumerate( doc_model_sent_file_list):
        fid = eachdoc['fid']#{0:0>4}'.format(i)
        file_name = '{0}_{1}'.format(test_case_name,fid)
        models ={}
        sent_list =[]
        for i, eachmodel in enumerate( eachdoc['model']):
            model_file_name = file_name +'.'+ model_id[i] +'.html'
            models[model_file_name]=eachmodel
            for eachsent in eachmodel:
                sent_list.append(eachsent)
        model_fname_dict = {}
        model_fname_dict['fid']=fid
        model_fname_dict['file_name']=file_name
        model_fname_dict['sent_list']=sent_list
        model_fname_dict['models']=models
        model_file_list.append(model_fname_dict)

    sxpReadFileMan.StoreSxptext(model_file_list,fname_dict['model_file_list'])
    WriteModelFile(model_file_list,model_dir)
    return model_file_list

def PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,pickle_file_pattern_id,system_filename_pattern_id):
    flist, sublist = sxpReadFileMan.sxpGetDirFileSubList(model_path)
    model_filenames_pattern_id = re.compile(model_filenames_pattern_id)
    model_set_id = {}
    i = 0
    for eachf in flist:
        match = model_filenames_pattern_id.match(eachf)
        if match:
            id = match.groups(0)[0]
            model_set_id[id] = (i,eachf)
            i = i + 1

    pk_sys_set = []
    for eachid,(i,eachf) in model_set_id.items():
        pk_sys_set.append([pickle_file_pattern_id.replace('#ID#', eachid),system_filename_pattern_id.replace('#ID#', eachid)])

    return pk_sys_set

def WriteModelFile(model_file_list,model_dir):
    for model_fname_dict in model_file_list:
        for fname,sentenceset in model_fname_dict['models'].items():
           model_txt= MakeModel(sentenceset,fname, formatsent = 1)
           fullname = os.path.join(model_dir,fname)
           sxpReadFileMan.WriteStrFile(fullname,model_txt, 'utf-8')

def  ProduceSystem(tops, systemfilename, formatsent = 0):
        modeltxt  = '''<html>\n<head>\n<title>%s</title>\n</head>\n'''%(systemfilename)
        sentenceset = tops
        i = 0
        abstract_str = ''
        for sent in sentenceset:
            rsent = RemoveUStrSpace(sent)

            if len(rsent)<=0:
                rsent = 'test sentence is empty'
            i = i + 1
            if formatsent == 1:
                sentr ='''<a name="%d">[%d]</a> <a href="#%d" id=%d>%s.</a>\n'''%(i,i,i,i,rsent)
            if formatsent == 0:
                sentr = rsent + '\n'
            abstract_str = abstract_str +sentr
        if formatsent == 1:
            bodytxt = '''<body bgcolor="white">\n%s</body>\n</html>'''%(abstract_str)
        if formatsent == 0:
            bodytxt = abstract_str

        if formatsent== 0:
            abstract_str = bodytxt
        if formatsent == 1:
            abstract_str = modeltxt + bodytxt
        return abstract_str


def GetSystemID(testset,idname_dict):
    test_id =[]
    for eachtest in testset:
        test_id.append(idname_dict[eachtest])
    return test_id

def RemoveUStr(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
##    patstr = "\s"
##    pattern = re.compile(patstr)
##    nstr = pattern.sub(' ',nstr)
    return nstr

def RemoveUStrSpace(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
    patstr = "\s+"
    pattern = re.compile(patstr)
    nstr = pattern.sub(' ',nstr)
    return nstr

def MakeModel(sentenceset,fn, formatsent = 1):
        modeltxt  = '<html>\n<head>\n<title>%s</title>\n</head>\n'%(fn)
        i = 0
        abstract_str = ''
        for s in sentenceset:
            if isinstance(s,tuple) or isinstance(s,list):
                if len(s)==2:
                    sent = s[1]
                if len(s)==1:
                    sent = s[0]
            else:
                sent = s
            rsent = RemoveUStrSpace(sent)
            if len(rsent)<=1:
                continue
            i = i + 1
            if formatsent == 1:
                sentr ='''<a name="%d">[%d]</a> <a href="#%d" id=%d>%s.</a>\n'''%(i,i,i,i,rsent)
                abstract_str = abstract_str +sentr
            if formatsent == 0:
                abstract_str = abstract_str +rsent + '\n'
        if formatsent == 1:
            bodytxt ='<body bgcolor="white">\n%s</body>\n</html>'%(abstract_str)
        if formatsent == 0:
            bodytxt = abstract_str
        if formatsent == 1:
            abstract_str = modeltxt + bodytxt
        if formatsent== 0:
            abstract_str = bodytxt

        return abstract_str


def WriteSystemOutput(rank_para,model_test_output_dict):
    for test, outputlist in model_test_output_dict.items():
        for output_dict in outputlist:
            topksent_path = output_dict['topksent_path']
            sxpReadFileMan.WriteStrFile(topksent_path, output_dict['st'], 'utf-8')

            topsent_pk_file=topksent_path + '.topsent.pk'
            sxpReadFileMan.StoreSxptext( output_dict['tops'], topsent_pk_file)

            pkfname = topksent_path + '.allsent.pk'
            sxpReadFileMan.StoreSxptext(output_dict['allsent'], pkfname)
##            output_dict ={}
##            output_dict['topksent_path']=topksent_path
##            output_dict['tops']=tops
##            output_dict['st']=st
##            output_dict['allsent']=allsent
##            output_dict_list.append(output_dict)
            #save text abstact text and conclusion text

if __name__ == '__main__':
    main()
