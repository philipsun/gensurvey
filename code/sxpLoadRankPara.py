#-------------------------------------------------------------------------------
# Name:        sxpLoadRankPara.py
# Purpose:
#
# Author:      sunxp
#
# Created:     22/11/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sxpReadFileMan

basedir = os.path.abspath(os.path.dirname(__file__))
#this is to replace the host url

perl_path = 'D:\\Perl\\bin\\perl'
rouge_path= '\\ROUGE-1.5.5\\RELEASE-1.5.5'
def MakeDemoRankPara(project_name,test_case_name,idname,model_test):
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
    rouge_dir =basedir+r'\\ROUGE-1.5.5\\RELEASE-1.5.5'
    rank_para={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': out_dir, # this is to store rouge score out puts and figures #os.path.join(system_dir,'duc_withstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':test_case_name,#'duc_withstop_topk',
        u'model_test':model_test,#['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':test_case_name,#'duc',
        u'conf_path':conf_path,
        u'dataroot':main_dir,
        u"pickle_path" : pk_dir,
        u"model_path": model_dir,
        u'perl_path':perl_path,
        u"rouge_dir" : rouge_dir,
        u"system_path" : system_dir, #this is to store each system file produced by ranking models
       # u'modelpattern':  r'{0}_#ID#.[A-Z].html'.format(test_case_name),
        u'modelpattern': r'{0}_#ID#.[A-Z].html'.format(project_name),
        u'systempattern': r'{0}_(\d+).html'.format(test_case_name),
      #  u'model_filenames_pattern_id' : r'{0}_(\d+).[A-Z].html'.format(test_case_name),
        u'model_filenames_pattern_id': r'{0}_(\d+).[A-Z].html'.format(project_name),
        u'system_filename_pattern_id' : r'{0}_#ID#.html'.format(test_case_name),
        u'pickle_file_pattern_id' :r'{0}_#ID#.pk'.format(test_case_name), # inc_test
        u'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    rankpara_fname = test_dir +'\\rank_para.pk'
    sxpReadFileMan.StoreSxptext(rank_para,rankpara_fname)
    return rank_para
def MakeMultiPaperPara(project_name,test_case_name,idname,model_test,model_file_case,system_file_case,rouge_args=None):
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
    rouge_dir =basedir+'\\ROUGE-1.5.5\\RELEASE-1.5.5'
    rank_para={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': out_dir, # this is to store rouge score out puts and figures #os.path.join(system_dir,'duc_withstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':test_case_name,#'duc_withstop_topk',
        u'model_test':model_test,#['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':test_case_name,#'duc',
        u'conf_path':conf_path,
        u'dataroot':main_dir,
        u"pickle_path" : pk_dir,
        u"model_path": model_dir,
        u"rouge_dir" : rouge_dir,
        u'perl_path': perl_path,
        u"system_path" : system_dir, #this is to store each system file produced by ranking models
        u'modelpattern':  r'{0}_#ID#.[A-Z].html'.format(model_file_case),
        u'systempattern': r'{0}_(\d+).pk.html'.format(system_file_case),
        u'model_filenames_pattern_id' : r'{0}_(\d+).[A-Z].html'.format(model_file_case),
        u'system_filename_pattern_id' : r'{0}_#ID#.pk.html'.format(system_file_case),
        u'pickle_file_pattern_id' :r'{0}_#ID#.pk'.format(test_case_name), # inc_test
        u'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    if rouge_args is not None:
        rank_para['rouge_args']=rouge_args
    rankpara_fname = test_dir +'\\rank_para.pk'
    sxpReadFileMan.StoreSxptext(rank_para,rankpara_fname)
    return rank_para
def MakeACL2014Para(project_name,test_case_name,idname,model_test):
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
    rouge_dir =basedir+'\\ROUGE-1.5.5\\RELEASE-1.5.5'
    rank_para={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': out_dir, # this is to store rouge score out puts and figures #os.path.join(system_dir,'duc_withstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':test_case_name,#'duc_withstop_topk',
        u'model_test':model_test,#['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':test_case_name,#'duc',
        u'conf_path':conf_path,
        u'dataroot':main_dir,
        u"pickle_path" : pk_dir,
        u"model_path": model_dir,
        u"rouge_dir" : rouge_dir,
        u"system_path" : system_dir, #this is to store each system file produced by ranking models
        u'modelpattern':  r'{0}_#ID#.[A-Z].html'.format(test_case_name),
        u'systempattern': r'{0}_(\d+).html'.format(test_case_name),
        u'model_filenames_pattern_id' : r'{0}_(\d+).[A-Z].html'.format(test_case_name),
        u'system_filename_pattern_id' : r'{0}_#ID#.html'.format(test_case_name),
        u'pickle_file_pattern_id' :r'{0}_#ID#.pk'.format(test_case_name), # inc_test
        u'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    rankpara_fname = test_dir +'\\rank_para.pk'
    sxpReadFileMan.StoreSxptext(rank_para,rankpara_fname)
    return rank_para
def MakeSurveyPara(project_name,test_case_name,idname,model_test):
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
    rouge_dir =basedir+'\\ROUGE-1.5.5\\RELEASE-1.5.5'
    rank_para={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': out_dir, # this is to store rouge score out puts and figures #os.path.join(system_dir,'duc_withstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':test_case_name,#'duc_withstop_topk',
        u'model_test':model_test,#['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':test_case_name,#'duc',
        u'conf_path':conf_path,
        u'dataroot':main_dir,
        u"pickle_path" : pk_dir,
        u"model_path": model_dir,
        u"rouge_dir" : rouge_dir,
        u"system_path" : system_dir, #this is to store each system file produced by ranking models
        u'modelpattern':  r'{0}_#ID#.[A-Z].html'.format(test_case_name),
        u'systempattern': r'{0}_(\d+).html'.format(test_case_name),
        u'model_filenames_pattern_id' : r'{0}_(\d+).[A-Z].html'.format(test_case_name),
        u'system_filename_pattern_id' : r'{0}_#ID#.html'.format(test_case_name),
        u'pickle_file_pattern_id' :r'{0}_#ID#.pk'.format(test_case_name), # inc_test
        u'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    rankpara_fname = test_dir +'/rank_para.pk'
    sxpReadFileMan.StoreSxptext(rank_para,rankpara_fname)
    return rank_para
def GetFName(project_name,test_case_name):
    main_dir = basedir+'\\test\\{0}'.format(project_name)
    test_dir =   main_dir+'\\' + test_case_name
    rankpara_fname = test_dir +'\\rank_para.pk'
    model_dir = main_dir + '\\model'
    system_dir = test_dir + '\\system'
    pk_dir =  main_dir + '\\pk'
    out_dir=  test_dir + '\\out'
    conf_path = os.path.join(out_dir,'rouge_conf.xml')
    fname_dict = {}
    fname_dict['main_dir']=main_dir
    fname_dict['test_dir']=test_dir
    fname_dict['out_dir']=out_dir
    fname_dict['rankpara_fname']=rankpara_fname
    fname_dict['model_dir']=model_dir
    fname_dict['pk_dir']=pk_dir
    fname_dict['conf_path']=conf_path
    fname_dict['system_dir']=system_dir
    fname_dict['model_test_output_dict']= os.path.join(fname_dict['out_dir'],'model_test_output_dict.dict')
    fname = os.path.join(fname_dict['pk_dir'],'model_file_list.list')
    fname_dict['model_file_list']= fname

    fname = os.path.join(fname_dict['pk_dir'],'doc_model_sent_file_list.list')
    fname_dict['doc_model_sent_file_list']= fname
    fname_dict['model_doc_list']=os.path.join(fname_dict['pk_dir'],'model_doc_list.list')
    return fname_dict
def main():
    pass

if __name__ == '__main__':
    main()
