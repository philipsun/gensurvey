#-------------------------------------------------------------------------------
# Name:        sxpKeywordEvaluate
# Purpose:
#
# Author:      sunxp
#
# Created:     15/11/2017
# Copyright:   (c) sunxp 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import sxpReadFileMan
import xlrd
import xlsxwriter
import os
import re
import codecs
import sxpPyrougeEvaluate
import sxpRougeConfig
import pandas as pd

from graphengine import sxpGraphEngine
from graphengine.sxpGraphEngine import *
from graphengine import sxpParseMyNet

dir_net_db = r'./sln'

def BuildTree(dbstore,keytreefname,fid):
    print('----build and rank keytree db-----:',fid,keytreefname,dbstore)
    sxpParseMyNet.ParseNetFile(keytreefname,dbstore,fid)
    sxpgraph = sxpGraphEngine.sxpNetwork(dbstore,fid,dbinit=False)
    id = sxpgraph.GetMaxNodeID()
    pr = sxpgraph.PagerankScore(id)
    print('--------------------------:')
def TestBuildTree():
##    fname = r'./sln/testdimension_2.txt2.net'
    dbstore = r'./sln'
    dbname = r'dbsum_keytree'
    fname = r'E:\pythonworknew\code\paperparse\paper\single\papertxt\testdimension_2.txt.keytree'
    sxpParseMyNet.ParseNetFile(fname,dbstore,dbname)
def TestRankNetwork():
    sxpgraph = sxpGraphEngine.sxpNetwork(r'./sln','dimsum_keytree',dbinit=False)
    id = sxpgraph.GetMaxNodeID()
    pr = sxpgraph.PagerankScore(id)
    print(pr)

def ComputeDistance(doc_sent_list,dbstore,fid):
    sxpgraph = sxpGraphEngine.sxpNetwork(dbstore,fid,dbinit=False)

    doc_dist,doc_general_dist,doc_score_list=sxpgraph.ComputeSimilarityOfDocSentList(doc_sent_list,doc_dist_type="sel",doc_dist_pos=[0,0])
    return doc_dist,doc_general_dist,doc_score_list
def ComputeOneDistance(doc_sent_list,dbstore,fid):
    sxpgraph = sxpGraphEngine.sxpNetwork(dbstore,fid,dbinit=False)

    doc_dist,doc_general_dist,doc_score_list=sxpgraph.ComputeSimilarityOfDocSentList(doc_sent_list,doc_dist_type="sel",doc_dist_pos=[0,0])
    return doc_score_list[0]
def PlotSaveScore(dict_conf_name):
    rankpara = sxpRougeConfig.GetRankPara(dict_conf_name)
    out_dir = rankpara['outdir']
    fname = os.path.join(out_dir,dict_conf_name+'.keyscore.csv')
    df=pd.read_csv(fname)
    print(df)
    npd = pd.DataFrame()

    grp1 = df.groupby(['model_id'])
    for n,group in grp1:
        print('----')
        print(n)
    renamed=df.rename(columns={"pkfnameid":"filetype"})
    nd= renamed.pivot(index='model_id',columns="filetype",values='score' )
    nff= nd.rename(columns={"testdimension_3.txt.pk":"no_abs","testdimension_4.txt.pk":"yes_abs"})
    nff.to_csv('pivot.csv')
    print(nff)
    nd['id']=nd.index
#    plt.figure();
    xtickname = []

    for each in nd['id']:
        xtickname.append(sxpRougeConfig.modename_dict["{:0>2}".format(str(each))])
    print(xtickname)
#    print nff
    ax=nff.plot.bar();
    ax.set_xticklabels(xtickname)
    plt.xticks(rotation=30)
    fname = os.path.join(out_dir,dict_conf_name+'_keytreescore.jpg')
    plt.tight_layout()
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(fname)
    plt.show()
def PlotSaveModelScore(dict_conf_name):
    rankpara = sxpRougeConfig.GetRankPara(dict_conf_name)
    out_dir = rankpara['outdir']
    fname = os.path.join(out_dir,dict_conf_name+'.keyscore.csv')
    df=pd.read_csv(fname)
    print(df)
    npd = pd.DataFrame()

    grp1 = df.groupby(['model_id'])['score'].sum()
    print(grp1)
    grp2 = df.groupby(['model_id'])['score'].mean()
    print(grp2)
    mdf = pd.DataFrame(grp1)
    print()
    grp3=df.groupby(['model_id'])
    gdf = grp3['score'].agg([np.sum,np.mean,np.std])
    print(gdf)
    fname = os.path.join(out_dir,dict_conf_name+'keymodelagg.csv')
    gdf.to_csv(fname)
    xtickname = []
    model_id=gdf.index
    for each in model_id:
        xtickname.append(sxpRougeConfig.modename_dict["{:0>2}".format(str(each))])
##    for n,group in grp1:
##        print '----'
##        print n
##    renamed=df.rename(columns={"pkfnameid":"filetype"})
##    nd= renamed.pivot(index='model_id',columns="filetype",values='score' )
##    nff= nd.rename(columns={"testdimension_3.txt.pk":"no_abs","testdimension_4.txt.pk":"yes_abs"})
##    nff.to_csv('pivot.csv')
##    print nff
##    nd['id']=nd.index
###    plt.figure();
##    xtickname = []
##
##    for each in nd['id']:
##        xtickname.append(sxpRougeConfig.modename_dict["{:0>2}".format(str(each))])
    print(xtickname)
###    print nff
    ax=gdf.plot.bar();
    ax.set_xticklabels(xtickname)
    plt.xticks(rotation=30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    fname = os.path.join(out_dir,dict_conf_name+'_keytreemodelavgscore.jpg')
    plt.tight_layout()
    plt.savefig(fname)
    plt.show()

def TestGraphScore():
    docsent=[["dimension",'semantic link'],['summarization','citation']]
    sxpgraph = sxpGraphEngine.sxpNetwork(r'./sln','dimsum_keytree',dbinit=False)

    doc_dist,doc_general_dist,doc_score_list=sxpgraph.ComputeSimilarityOfDocSentList(docsent,doc_dist_type="sel",doc_dist_pos=[0,0])
    print(doc_dist.shape)
    print(doc_general_dist)
    print(doc_score_list)

def main():
    PlotSaveScore('single_withoutstop')
    PlotSaveModelScore('single_withoutstop')

if __name__ == '__main__':
    main()
