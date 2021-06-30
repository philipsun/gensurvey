#-------------------------------------------------------------------------------
# Name:        sxpParseRougeScore
# Purpose:
#
# Author:      sxp
#
# Created:     20-01-2017
# Copyright:   (c) sxp 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import sxpTimeManage
from pyrouge import Rouge155
from pyrouge import MyRouge155
import sxpPlotBar
import subprocess
from subprocess import check_output
import sxpReadFileMan
import xlrd
import xlsxwriter
import os
import re
import codecs
import sxpRougeConfig
def ParseMultiSysOutput(fname,system_id_set):
    txt = sxpReadFileMan.ReadTextUTF(fname)
  #  print txt
    recall_pattern = re.compile(r'(\d\d) (ROUGE-\S+) (Average_\w):\s+(\d.\d+)\s+' +   r"\(95%-conf.int. (\d.\d+) - (\d.\d+)\)")
    for line in txt.split("\n"):
        print(line)
        match = recall_pattern.match(line)
        if match:
            sys_id, rouge_type, metric, result, conf_begin, conf_end = \
                match.groups()
            print(sys_id,rouge_type, metric, result, conf_begin, conf_end)
            if rouge_type in system_id_set[sys_id]:
                a = system_id_set[sys_id][rouge_type]
                if a is None:
                    a = []
            else:
                a = []
            a.append([metric,result, conf_begin, conf_end])
            system_id_set[sys_id][rouge_type]=a
    return system_id_set

def ParseFileID(fname,modelid_dict=None):
    patstr = "_(\d\d)"
    pt = re.compile(patstr)
    id_set = pt.findall(fname)
    if modelid_dict is None:
        modelname = sxpRougeConfig.GetModelNameDict()
    else:
        modelname = sxpRougeConfig.GetModelName(modelid_dict)
    return id_set,modelname
metric_set = [
['ROUGE-1','Average_P','Average_R','Average_F'],
['ROUGE-2','Average_P','Average_R','Average_F'],
['ROUGE-3','Average_P','Average_R','Average_F'],
['ROUGE-4','Average_P','Average_R','Average_F'],
['ROUGE-L','Average_P','Average_R','Average_F'],
['ROUGE-SU4','Average_P','Average_R','Average_F']
]
def GetModelIDs(model_rouge_score):
    modelids = list(model_rouge_score.keys())
    modelids.sort()
    return modelids
def ProcessRougeScoreACLToExcel(pkname,outputdir,figtitlehead=""):
        print(pkname)
        model_rouge_score = sxpReadFileMan.LoadSxptext(pkname)
        print(model_rouge_score)
##        modelname = {'01':'Para','02':'TFIDF','03':'GS','04':'GW',
##        '05':'Context','06':'Section','07':'SecContext','08':'GW_Context','09':'sec_title','10':'word_sent'}
##        plotmodel = ['04','02','03','01','05','08','09','10']
##        modelname = {'01':'Para','02':'TFIDF','03':'GS','04':'GW',
##        '05':'Context','06':'Section','07':'SecContext','08':'GW_Context','09':'word_sent'}
##        plotmodel = ['04','02','03','01','05','08','09']
        dirname, rougefilename = sxpReadFileMan.GetFilePathName(pkname)
        plotmodel, modelname_dict=ParseFileID(pkname)
        plotmodel = GetModelIDs(model_rouge_score)
        print(plotmodel)
        modelname_dict = sxpRougeConfig.GetModelNameDict()
        nsection = 1
        nrow = nsection+1
        nc = 1
        coorname = ['precision','recall','f-score']
        xname = pkname + '.rouge_score.xls'
        fname = xname
        print(fname)
##    try:
        workbook = xlsxwriter.Workbook(fname)
        worksheet = workbook.add_worksheet()
        for em in metric_set:# weplot one bar figure ROUGE1, R,P,F, ROUGE 2 R,P,F
            title = em[0]

            value = str(title)
            rown = nsection
            coln = 0
            for ic in range(len(em)):
                value = str(em[ic])
                worksheet.write(rown, coln+ic, value)
            dataset= []
            metric_name = em[1:]

            i = 0
            #for figure rouge-1, we need to get
            #input = [['v1',[0.8,0.9,0.85],['tfidf',[0.3,0.2,0.4]]]
            print(title)
            for eachmodel in plotmodel:#for 7 models, we extract each model's metric
            #for tfidf model
                #this is the name 'tfidf'
                if eachmodel not in list(model_rouge_score.keys()):
                    print("no such model data in pk",eachmodel)
                    continue

                modelresult = model_rouge_score[eachmodel]
                if len(modelresult)==0:
                     print("in this model, no data found in pk",eachmodel)
                     continue
                legendname  = modelname_dict[eachmodel]
                value = str(legendname)
                rown = rown + 1
                coln = 0
                print('1write',rown,coln,value)
                worksheet.write(rown, coln, value)
                if title not in model_rouge_score[eachmodel].keys():
                    continue
                datarow = []
                for eachm in metric_name:
                    rown = rown
                    coln = coln + 1

                    result_set =model_rouge_score[eachmodel][title]
                    for each_m in result_set:
                        if each_m[0]== eachm:
                            value =str(each_m[1]) #avergage score, not confidence value)
                            print('2write',rown,coln,value)
                            worksheet.write(rown, coln, value)
                            datarow.append(float(value))
                dataset.append([legendname, datarow])
                i = i + 1
            nsection = rown + 2
            print(dataset)
            figtitle =figtitlehead+' '+title
            sxpPlotBar.PlotBarFromCoordSet(figtitle,dataset,coorname,highratio=1.0)
            figname = os.path.join(outputdir,rougefilename+em[0])
            plt.savefig(figname+'.jpg')
        plt.show()
        workbook.close()
##    except Exception as e:
##        print 'error in writing excel',e
def ProcessRougeScoreToExcel(pkname,outputdir,dict_conf_name="",ifshow =0,modelid_dict=None):
        print(pkname)
        model_rouge_score = sxpReadFileMan.LoadSxptext(pkname)
        print(model_rouge_score)
##        modelname = {'01':'Para','02':'TFIDF','03':'GS','04':'GW',
##        '05':'Context','06':'Section','07':'SecContext','08':'GW_Context','09':'sec_title','10':'word_sent'}
##        plotmodel = ['04','02','03','01','05','08','09','10']
##        modelname = {'01':'Para','02':'TFIDF','03':'GS','04':'GW',
##        '05':'Context','06':'Section','07':'SecContext','08':'GW_Context','09':'word_sent'}
##        plotmodel = ['04','02','03','01','05','08','09']
        dirname, rougefilename = sxpReadFileMan.GetFilePathName(pkname)
        if modelid_dict is None:
            modelname = sxpRougeConfig.GetModelNameDict()
        else:
            modelname = sxpRougeConfig.GetModelName(modelid_dict)

        nsection = 1
        nrow = nsection+1
        nc = 1
        coorname = ['precision','recall','f-score']
        xname = pkname + dict_conf_name+'_rouge_score.xls'
        fname = xname
        print(fname)
##    try:
        workbook = xlsxwriter.Workbook(fname)
        worksheet = workbook.add_worksheet()
        for em in metric_set:# weplot one bar figure #recall, precision, f-score
            title = em[0]

            value = str(title)
            rown = nsection
            coln = 0
            for ic in range(len(em)):
                value = str(em[ic])
                worksheet.write(rown, coln+ic, value)
            dataset= []
            metric_name = em[1:]

            i = 0
            #for figure rouge-1, we need to get
            #input = [['v1',[0.8,0.9,0.85],['tfidf',[0.3,0.2,0.4]]]
            print(title)
            modellist = sorted(model_rouge_score.keys())

            for eachmodel in modellist:#for 7 models, we extract each model's metric
            #for tfidf model
                #this is the name 'tfidf'
                if eachmodel not in list(model_rouge_score.keys()):
                    print("no such model data in pk",eachmodel)
                    continue

                modelresult = model_rouge_score[eachmodel]
                if len(modelresult)==0:
                     print("in this model, no data found in pk",eachmodel)
                     continue
                model_legendname  = modelname[eachmodel]
                value = str(model_legendname)
                rown = rown + 1
                coln = 0
                print('1write',rown,coln,value)
                worksheet.write(rown, coln, value)
                if title not in model_rouge_score[eachmodel].keys():
                    continue
                datarow = []
                for eachm in metric_name:
                    rown = rown
                    coln = coln + 1
                    result_set =model_rouge_score[eachmodel][title]
                    for each_m in result_set:
                        if each_m[0]== eachm:
                            value =str(each_m[1]) #avergage score, not confidence value)
                            print('2write',rown,coln,value)
                            worksheet.write(rown, coln, value)
                            datarow.append(float(value))
                dataset.append([model_legendname, datarow])
                i = i + 1
            nsection = rown + 2
            print(dataset)
            if len(dataset)==0:
                continue
            figtitle =dict_conf_name+' '+title
            sxpPlotBar.PlotBarFromCoordSet(figtitle,dataset,coorname,highratio=1.5)
##            figname = os.path.join(outputdir,rougefilename+em[0])
            figname = os.path.join(outputdir,dict_conf_name+'_'+rougefilename+em[0])
            print(figname+'.jpg')
            plt.savefig(figname+'.jpg')
        if ifshow==1:
            plt.show()
        workbook.close()
##    except Exception as e:
##        print 'error in writing excel',e

def ParseScoreTxt(txtfilename,outputdir,dict_conf_name="",ifshow =0,modelid_dict = None):
    print('to process txt file ',txtfilename, outputdir,modelid_dict)
    plotmodel, modelname=ParseFileID(txtfilename,modelid_dict)
    print(plotmodel,modelname)
#    system_id_set={'01':{},'02':{},'03':{},'04':{},'05':{},'08':{},'09':{}}
    system_id_set={}
    for eachid in plotmodel:
        system_id_set[eachid]={}
        print(system_id_set[eachid])
    system_id_set_result =ParseMultiSysOutput(txtfilename,system_id_set)
    td,fname=sxpReadFileMan.GetFilePathName(txtfilename)
    print(td, fname)
    pkname = os.path.join(outputdir, fname+'.pk')
    print('store pk name for dict parsed out from txt',pkname)
    sxpReadFileMan.StoreSxptext(system_id_set_result,pkname)
    print('now begin to store it in excel and plot it')

    #ProcessRougeScoreACLToExcel(pkname,outputdir,dict_conf_name)
    ProcessRougeScoreToExcel(pkname,outputdir,dict_conf_name,ifshow =0,modelid_dict = modelid_dict)
def ParseMultiSysOutput(fname,system_id_set):
    txt = sxpReadFileMan.ReadTextUTF(fname)
  #  print txt
    print(system_id_set)
    recall_pattern = re.compile(r'(\d\d) (ROUGE-\S+) (Average_\w):\s+(\d.\d+)\s+' +   r"\(95%-conf.int. (\d.\d+) - (\d.\d+)\)")
    for line in txt.split("\n"):
        print(line)
        match = recall_pattern.match(line)
        if match:
            sys_id, rouge_type, metric, result, conf_begin, conf_end = \
                match.groups()
            print(sys_id,rouge_type, metric, result, conf_begin, conf_end)
            if sys_id in system_id_set:
                if rouge_type in system_id_set[sys_id]:
                    a = system_id_set[sys_id][rouge_type]
                    if a is None:
                        a = []
                else:
                    a = []
                a.append([metric,result, conf_begin, conf_end])
                system_id_set[sys_id][rouge_type]=a
            else:
                print('system id in txt is not in file name, we add it:',sys_id)
                system_id_set[sys_id] = {}
                if rouge_type in system_id_set[sys_id]:
                    a = system_id_set[sys_id][rouge_type]
                    if a is None:
                        a = []
                else:
                    a = []
                a.append([metric,result, conf_begin, conf_end])
                system_id_set[sys_id][rouge_type]=a


    return system_id_set
def TestFname():
    outputdir = r'D:\pythonwork\code\tjrank_sentences\context\result\r2'
    if os.path.exists(outputdir)==False:
        os.path.os.mkdir(outputdir)
    plotwho = 'duc'
    doall = True
    if plotwho=='inc' or doall:
        incacl_txtname = r'D:\pythonwork\code\paperparse\paper\papers\system_html5\inc_abs01_02_03_04_05_06_07_08_09_10.pk.txt'
        ParseScoreTxt(incacl_txtname,outputdir,figtitlehead='acl_inc')
    if plotwho=='exc' or doall:
        excacl_txtname = r'D:\pythonwork\code\paperparse\paper\papers\system_html4\exc_abs01_02_03_04_05_06_07_08_09_10.pk.txt'
        ParseScoreTxt(excacl_txtname,outputdir,figtitlehead='acl_exc')
    if plotwho == 'duc' or doall:
        duc_txtname = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html1\duc_maxword_01_02_03_04_05_08_10.pk.txt'
        ParseScoreTxt(duc_txtname,outputdir,figtitlehead='duc')
##    pkname = r'D:\pythonwork\code\paperparse\paper\papers\system_html5\inc01_02_03_04_05_06_07_08_09_10.pk.txt.pk'
##    print ProcessRougeScoreACLToExcel(pkname)
def TestSxpPyrougeScore(model_set,plotwho = 'all',outputdir='',methodhead="",fhead=""):
    if len(outputdir)==0:
        outputdir = r'D:\pythonwork\code\tjrank_sentences\context\result\r2'
    if os.path.exists(outputdir)==False:
        os.path.os.mkdir(outputdir)

    doall = True
    if len(methodhead)>0:
        methodhead = methodhead+'_'
    if plotwho=='inc' or plotwho == 'all':
        incacl_txtname = sxpDoPyrougeScoreTest.test_inc.MakePkFileName(model_set,fhead)#full_output_fname_pk_txt#r'D:\pythonwork\code\paperparse\paper\papers\system_html5\inc_abs01_02_03_04_05_06_07_08_09_10.pk.txt'
        print(incacl_txtname)
        ParseScoreTxt(incacl_txtname,outputdir,figtitlehead=methodhead+'acl_inc')
    if plotwho=='exc' or  plotwho == 'all':
        excacl_txtname =  sxpDoPyrougeScoreTest.test_exc.MakePkFileName(model_set)#full_output_fname_pk_txt #r'D:\pythonwork\code\paperparse\paper\papers\system_html4\exc_abs01_02_03_04_05_06_07_08_09_10.pk.txt'
        print(excacl_txtname)
        ParseScoreTxt(excacl_txtname,outputdir,figtitlehead =methodhead+'acl_exc')
    if plotwho == 'duc' or  plotwho == 'all':
        duc_txtname =     sxpDoPyrougeScoreTest.test_duc.MakePkFileName(model_set,fhead)#full_output_fname_pk_txt
        print(duc_txtname)
        #r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html1\duc_maxword_01_02_03_04_05_08_10.pk.txt'
        ParseScoreTxt(duc_txtname,outputdir,figtitlehead = methodhead+'duc')
def TestSxpPyrougeScoreTxtFile(txtfilename,outputdir='',dict_conf_name="",ifshow =0):
    if len(outputdir)==0:
        outputdir = r'D:\pythonwork\code\tjrank_sentences\context\result\r2'
    if os.path.exists(outputdir)==False:
        os.path.os.mkdir(outputdir)
    ParseScoreTxt(txtfilename,outputdir,dict_conf_name=dict_conf_name,ifshow =0)

def TestParseFileName():
    incacl_txtname = r'D:\pythonwork\code\paperparse\paper\papers\system_html5\inc_abs01_02_03_04_05_06_07_08_09_10.pk.txt'
    outputdir = r'D:\pythonwork\code\tjrank_sentences\context\result'
    td,fname=sxpReadFileMan.GetFilePathName(incacl_txtname)
    pkname = os.path.join(outputdir, fname+'.pk')
    print(pkname)
def main():
    pkname = r'E:\pythonworknew\code\tjrank_sentences\context\result\r3smax100\duc_maxword_01_02_03_04_05_08_10.txt.pk'
    outputdir = r'E:\pythonworknew\code\tjrank_sentences\context\result\r3smax100'
    figtitlehead='duc_withoutstop_max100'
    ProcessRougeScoreToExcel(pkname,outputdir,figtitlehead)

if __name__ == '__main__':
    main()
