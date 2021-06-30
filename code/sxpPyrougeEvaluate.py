#coding=utf-8
#-------------------------------------------------------------------------------
# Name:        sxpDoPyrougeEvaluate
# Purpose:
#
# Author:      sunxp
#
# Created:     17/01/2017
# Copyright:   (c) sunxp 2017
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

global  conf_path
#global perlpathname

conf_path = r'E:\pythonworknew\code\paperparse\paper\rouge_conf.xml'


def Test():
    r = Rouge155()
    #SL.P.10.R.11.SL062003-01.html
    #SL.P.10.R.11.SL062003-(\d+).html
    r.system_dir = r'D:\Python27\Lib\site-packages\pyrouge\tests\data\systems'
    #SL.P.10.R.A.SL062003-01.html,
    #SL.P.10.R.[A-Z].SL062003-#ID#.html
    r.model_dir = r'D:\Python27\Lib\site-packages\pyrouge\tests\data\models'
    r.system_filename_pattern = 'SL.P.10.R.11.SL062003-(\d+).html'
    r.model_filename_pattern = 'SL.P.10.R.[A-Z].SL062003-#ID#.html'

    output = r.evaluate()
    print(output)
    output_dict = r.output_to_dict(output)


def CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id,rouge_dir=None,rouge_args=None,onlyid=[]):
    global  conf_path
    perlpathname=r'D:\Perl\bin\perl'
##    conf_path = r'E:\pythonworknew\code\paperparse\paper\rouge_conf.xml'
##    perlpathname=r'D:\Perl\bin\perl'
    print(system_path, systempattern,modelpattern)
    output_set = []
    output = RunPaperMyRougeHtml(system_path,model_path,modelpattern,systempattern,conf_path,perlpath = perlpathname,system_idstr=system_id,rouge_args=rouge_args,onlyid=onlyid)
    output_set.append(output)
    output_set_pkfname = os.path.join(system_path,output_fname)
    sxpReadFileMan.StoreSxptext(output_set,output_set_pkfname)
    output_txt_fname = output_fname + '.txt'
    sxpReadFileMan.WriteStrFile(output_txt_fname,output,'utf-8')
    return output_txt_fname,output_set_pkfname
def CallMyPyrougeOut(system_path,model_path,modelpattern,systempattern,out_dir,output_fname_head,system_id,conf_path,rouge_dir=None,perl_path = None,rouge_args=None,onlyid=[]):
#    global conf_path
    if perl_path is None:
        perlpathname=r'D:\Perl\bin\perl'
    else:
        perlpathname = perl_path
    print('perlpathname',perlpathname)
##    conf_path = r'E:\pythonworknew\code\paperparse\paper\rouge_conf.xml'
##    perlpathname=r'D:\Perl\bin\perl'
    print(system_path, systempattern, modelpattern)
    output_set = []
    output = RunPaperMyRougeHtml(system_path,model_path,modelpattern,systempattern,conf_path,perlpath = perlpathname,system_idstr=system_id,rouge_dir=rouge_dir,rouge_args=rouge_args,onlyid=onlyid)
    output_set.append(output)
    output_set_pkfname = os.path.join(out_dir,output_fname_head+'.pk')
    sxpReadFileMan.StoreSxptext(output_set,output_set_pkfname)
    output_txt_fname = os.path.join(out_dir,output_fname_head + '.txt')
    sxpReadFileMan.WriteStrFile(output_txt_fname,output,'utf-8')
    return output_txt_fname,output_set_pkfname
def RunPaperMyRougeHtml(system_path,model_path,modelpattern,systempattern,config_file_path = None,perlpath='d:\\Perl\\bin\\perl',system_idstr=['None'],rouge_dir=None,rouge_args=None,onlyid=[]):
    r = MyRouge155(rouge_dir=rouge_dir)
    #SL.P.10.R.11.SL062003-01.html
    #SL.P.10.R.11.SL062003-(\d+).html
    r.system_dir =system_path # r'D:\Python27\Lib\site-packages\pyrouge\tests\data\systems'
    #SL.P.10.R.A.SL062003-01.html,
    #SL.P.10.R.[A-Z].SL062003-#ID#.html
    #P14-1007.xhtml.A.html
    #P14-1007.xhtml.01.html
    r.config_file = config_file_path
    r.model_dir =  model_path #r'D:\Python27\Lib\site-packages\pyrouge\tests\data\models'
    r.system_filename_pattern = systempattern#'SL.P.10.R.11.SL062003-(\d+).html'
    r.model_filename_pattern = modelpattern # 'SL.P.10.R.[A-Z].SL062003-#ID#.html'
#    evaluate(self, system_id=1,conf_path = None, PerlPath =r'D:\Perl\bin\perl', rouge_args=None )
#    output= r.evaluate(system_id=system_idstr,conf_path = config_file_path, PerlPath =perlpath)
    print('perpath:********',perlpath)
    output= r.evaluatecmd(system_id=system_idstr,conf_path = config_file_path, PerlPath =perlpath,rouge_args=rouge_args ,onlyid=onlyid)

    print(output)
    output_dict = r.output_to_dict(output)
    return output
def ProduceSysModPair(system_dir,model_dir,system_idset,model_filenames_pattern,system_filename_pattern):
    return MyRouge155.ProduceSysModPair(system_dir,model_dir,system_idset,model_filenames_pattern,system_filename_pattern)
def main():
    Test()

if __name__ == '__main__':
    main()
