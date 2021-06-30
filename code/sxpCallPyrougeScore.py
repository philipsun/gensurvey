#coding=utf-8
#-------------------------------------------------------------------------------
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

import subprocess
from subprocess import check_output
import sxpReadFileMan
import xlrd
import xlsxwriter
import os
import re
import codecs
import sxpDoPyrougeEvaluate

idname = {'mymodel':'01',
    'tfidf':'02',
    'graphb':'03',
    'graphw':'04',
    'context1':'05',
    'mysecmodel':'06',
    'myseccontextmodel':'07',
    'hybrid':'08',
    'sectitle':'09',
    'mywordgraph':'10'
    }
def GetSystemID(testset):
    test_id =[]
    for eachtest in testset:
        test_id.append(idname[eachtest])
    return test_id
systemdir = r'D:\pythonwork\code\paperparse\paper\papers\system'
dataroot = r'D:\pythonwork\code\paperparse\paper'
sxpDoPyrougeEvaluate.conf_path = r'D:\pythonwork\code\paperparse\paper\rouge_conf.xml'
sxpDoPyrougeEvaluate.perlpathname=r'D:\Perl\bin\perl'

def TestDUC():

    pickle_path = os.path.join(dataroot,r'papers\duc\txt\pickle')
    model_path =  os.path.join(dataroot,r'papers\duc\txt\model_html')
    system_path = os.path.join(dataroot,r'papers\duc\txt\system_html1')
    print(pickle_path)
    print(model_path)
    print(system_path)

    modelpattern = r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html'
    systempattern = r'^(\w+-\w+).html'
#    system_id =['01','02','03','04','05','06','07']
##    system_id =['01','02','03','04','05','08','09']
    testset = ['mymodel','tfidf','graphb','graphw','context1','hybrid','mywordgraph']
    system_id = GetSystemID(testset)
    system_name = 'duc_lw'+'_'.join(system_id)+'.pk'
    output_fname = system_name#"output_set_model1_inc.pk"
    sxpDoPyrougeEvaluate.CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id)
def TestExcAB():
##    pickle_path = r'E:\pythonworknew\code\paperparse\paper\papers\pickle'
##    model_path =  r'E:\pythonworknew\code\paperparse\paper\papers\model_html' #a,b
##    system_path = r'E:\pythonworknew\code\paperparse\paper\papers\system_html4'
    pickle_path = os.path.join(dataroot,r'papers\pickle')
    model_path =  os.path.join(dataroot,r'papers\model_html')
    system_path = os.path.join(dataroot,r'papers\system_html4')
    print(pickle_path)
    print(model_path)
    print(system_path)
    modelpattern = r'P14-#ID#.xhtml.[A-Z].html'
    systempattern = r'^P14-(\d+).xhtml.html'
    system_id =['01','02','03','04','05','06','07','08','09','10']
    testset = ['mymodel','tfidf','graphb','graphw','context1','mysecmodel','myseccontextmodel','hybrid','sectitle','mywordgraph']
    system_id = GetSystemID(testset)
##    system_id =['06','09']
    system_name = 'exc'+'_'.join(system_id)+'.pk'
    output_fname = system_name#"output_set_model1_inc.pk"
    sxpDoPyrougeEvaluate.CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id)

def TestIncAB():
##    pickle_path = r'E:\pythonworknew\code\paperparse\paper\papers\pickle'
##    model_path =  r'E:\pythonworknew\code\paperparse\paper\papers\model_html' #a,b
##    system_path = r'E:\pythonworknew\code\paperparse\paper\papers\system_html5'
    pickle_path = os.path.join(dataroot,r'papers\pickle')
    model_path =  os.path.join(dataroot,r'papers\model_html')
    system_path = os.path.join(dataroot,r'papers\system_html5')
    print(pickle_path)
    print(model_path)
    print(system_path)

    modelpattern = r'P14-#ID#.xhtml.[A-Z].html'
    systempattern = r'^P14-(\d+).xhtml.html' #note that in real dir, .0[1-7] is appended to the systempattern for the model id
##    system_id =['03','04','08']
##    system_id =['01','02','03','04','05','06','07','08','09','10']
#    system_id =['01','02','03','04','05','06','07','08']
    testset = ['mymodel','tfidf','graphb','graphw','context1','mysecmodel','myseccontextmodel','hybrid','sectitle','mywordgraph']
    system_id = GetSystemID(testset)
    system_name = 'inc'+'_'.join(system_id)+'.pk'
    output_fname = system_name#"output_set_model1_inc.pk"
    sxpDoPyrougeEvaluate.CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id)
def RunPyrougeTest():
##    TestExcAB()
##    TestIncAB()
    TestDUC()
if __name__ == '__main__':
    RunPyrougeTest()
