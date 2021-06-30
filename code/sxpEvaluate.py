__author__ = 'a'
from sxpPackage import *
from numpy import *
from MyModel import *
from graph_base import *
from tf_idf import *
import os
from word_graph import WordGraph
import tjPaperIntroSentLabel

class sxpRankLabelResult:
    jdistance = []
    rdistance = []
    ddistance = []
    def __init__(self):
        jdistance = []
        rdistance = []
        ddistance = []

def sxp_display(idx_sentence, pickle_path):
    text = LoadSxptext(pickle_path)
    [nc,np] = text.c_p.shape
##    ranked_words = [words[idx_w[i, 0]] for i in range(len(words))]
    ranked_sentences = [text.sentenceset[idx_sentence[i, 0]] for i in range(len(text.sentenceset))]
##    ranked_paragraphs = [text.paraset[idx_p[i, 0]] for i in range(len(text.paraset))]
##    ranked_sections = [text.section_list[idx_c[i, 0]] for i in range(len(text.section_list))]

    ranked_sent_id = []
    ranked_sec_id = []
    for sentence in ranked_sentences:
        ranked_sent_id.append(sentence.id)
        ranked_sec_id.append(sentence.id_sec)
    ns = len(ranked_sec_id)
    important_per = []
##    zeroimport_topk = []
##    titlesent_topk = []
##    sectitle_topk = []
# for a top-k ranked set, we will count its features, like : howmany important sentence, how many section titles
# is it non important, does it have a documnet title?
    for i in range(ns / 5 + int((ns % 5) > 0)):
        topK = ranked_sec_id[:(i + 1) * 5]
        topKSent = ranked_sent_id[:(i + 1) * 5]
        sec_title_id = []
        sectitle_num = 0
        sec_import = 0
        for sid in topKSent:
            section_title = 0
            isimport = sxpIsAbsIntroConSentA(text.sentenceset[sid].sentence_text)
            if sid < nc:
                sectitle_num = sectitle_num + 1
                if isimport >= 1:
                    sec_import = sec_import + 1
        print('*****top :', len(topK))
        topsec,topsec_ct = sxpRankHist(topK)
        i = 0
        import_sent = 0
        zeroimport = 0
        titlesent = 0
        for sec_id in topsec:
            print(sec_id,topsec_ct[i],' : ', text.section_list[sec_id].title)
            isimport = sxpIsAbsIntroConSentA(text.section_list[sec_id].title)
##            if isimport == 0 and sec_id != 0 and zeroimport == 0:
##                zeroimport = zeroimport + 1 # we do not use topsec_ct[i] because we want this value to be an indicator variable with 0/1
            section_title = 0
            if sec_id == 0:
                titlesent = 1
                isimport = 1

            import_sent = import_sent + isimport*topsec_ct[i]
            i = i + 1
        print('important:',import_sent, ' in ranked top ',len(topK),'section title: ', sectitle_num, 'has title: ',titlesent, 'sec and imp: ',sec_import)
 #in a topk set, if one sec is not an important sec, then, all sent in this sec are counted as not important sent
        if import_sent == 0:
            zeroimport = 1
##        zeroimport_topk.append([len(topK),zeroimport])
##        titlesent_topk.append([len(topK),titlesent])
        important_per.append([len(topK),import_sent,zeroimport,titlesent,sectitle_num,sec_import])

        if len(topK)>=20:
            break
#so finally,zeroimport_topk will contains the number of non-important sentences in topk
    return important_per


def sxpGetDirFileList(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
    filelist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      if os.path.isdir(os.path.join(filedir, f)):
         pass
      else:
         filelist.append(f)
    return filelist


def sxpProcessFile(path, file_name):
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    #using correspond model to get the idx_sentence
    model = MyModel(pickle_path)
    #model = TfIdf(pickle_path)
    #model = GraphBased(pickle_path)
    #model = WordGraph(pickle_path)
    idx_sentence = model.idx_s


    return sxp_display(idx_sentence, pickle_path)
#def sxpProcessFile(path, file_name):
##    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
##    words, w_s, s_p, p_c = get_parameters_without_stopwords(pickle_path)
##    weight = Weight(w_s, s_p, p_c)
##    w = matrix(random.rand(len(words))).T
##    weight.iteration(w, 20)
##    idx_w, idx_s, idx_p, idx_c = rank_weight(weight)
##    rankresult = sxpRankResult()
##    rankresult.idx_w = idx_w
##    rankresult.idx_s = idx_s
##    rankresult.idx_p = idx_p
##    rankresult.idx_c = idx_c
##    rankfname = path + '\\pickle\\' + file_name + '_rankresult.pickle'
##    StoreSxptext(rankresult,rankfname)
##    return sxpdisplay(idx_w, idx_s, idx_p, idx_c, words, pickle_path)

def sxpProcessFilesInDir(paperpath):
    flist = sxpGetDirFileList(paperpath)
    importance_sentset = []
    i = 0
    for fn in flist:
        fset = fn.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'xhtml':
                print(fn)
                important_sent_per =sxpProcessFile(paperpath, fn)
                importance_sentset.append(important_sent_per )
                i = i + 1
##                if i > 10:
##                    break
    result= sxpResult()
    result.importance_sentset =importance_sentset
    fname = paperpath + '\\pickle\\importance_sentset.pickle'
    StoreSxptext(result,fname)

def sxpProcessImportentSent(paperpath):
    fname = paperpath + '\\pickle\\importance_sentset.pickle'
    result = LoadSxptext(fname)

    top_st = zeros((100,1),dtype = float)
    top_zero =zeros((100,1),dtype = float)
    top_title =zeros((100,1),dtype = float)
    top_sec =zeros((100,1),dtype = float)
    top_sec_imp =zeros((100,1),dtype = float)
    maxi = 0
    n  = 0
    for pap in result.importance_sentset:
        i = 0

#        important_per.append([len(topK),import_sent,zeroimport,titlesent,sectitle_num,sec_import])
        for topk in pap:
            topkzero = topk[2]
            titlesent = topk[3]
            top_st[i] = top_st[i] + float(topk[1])
            top_zero[i] = top_zero[i] + float(topk[2])
            top_title[i] = top_title[i] + float(topk[3])
            top_sec[i] = top_sec[i] + float(topk[4])
            top_sec_imp[i] = top_sec_imp[i] + float(topk[5])

            i = i + 1
            if i > maxi:
                maxi = i
        n = n + 1

    print('zero', top_zero[0:maxi]/float(n))
    print('import', top_st[0:maxi]/float(n))
    print('title', top_title[0:maxi]/float(n))
    print('sec_title', top_sec[0:maxi]/float(n))
    print('sec_imp', top_sec_imp[0:maxi]/float(n))

def sxpRankHist(data):
    #print data
    y = bincount(data)
    #print y
    x = nonzero(y)[0]
    #print x
    #print y[x]
    rankedvalue = argsort(-y[x], axis=0)
    return x[rankedvalue],y[x][rankedvalue]
def sxpTestRankHist():
    a=[1, 1, 3, 4, 5, 5, 2, 2, 2]
    print(sxpRankHist(a))
##    y = y[x]
##    argsort(array(-w), axis=0)
def sxpIsAbsIntroConSentA(sec_title):
    tag = ['result','introduction','conclusion','abstract','discussion','method','motivation']
    total_ct  = 0
    lstr = sec_title.lower()
    for tstr in tag:
        rstr = lstr.find(tstr)
        if rstr >= 0:
            rstr = 1
        else:
            rstr = 0
        total_ct  = total_ct  + rstr
    if total_ct>0:
        total_ct = 1
    return total_ct
def sxpTestsxpIsAbsIntroConSentA():
    str = '1  1Abstract introduction'
    print(sxpIsAbsIntroConSentA(str))
def sxpIsAbsIntroConSent(sec_title):
    lstr = sec_title.lower()
    rstr = lstr.find('result')
    total_ct  = 0
    if rstr >= 0:
        rstr = 1
    else:
        rstr = 0
    istr = lstr.find('introduction')
    if istr >= 0:
        istr = 1
    else:
        istr = 0
    cstr = lstr.find('conclusion')
    if cstr >= 0:
        cstr = 1
    else:
        cstr = 0
    astr = lstr.find('abstract')
    if astr >= 0:
        astr = 1
    else:
        astr = 0
    total_ct = rstr + istr + cstr + astr

    return total_ct


def sxpBeginProcessFileInDir():
    path = r'D:\pythonwork\code\paperparse\paper\papers'
    #path = r"C:\Users\a\Desktop\graduate paper related\code"
    print(" are you want to recompute the data  (r) or just load them for process (l)")
    ys = input("c, l ")
    if ys == 'c':
        sxpProcessFilesInDir(path)
        sxpProcessImportentSent(path)
    if ys == 'l':
        sxpProcessImportentSent(path)

def sxpGetRankedSentIDSet(path,file_name):
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    #using correspond model to get the idx_sentence
#    model = MyModel(pickle_path)
    model = TfIdf(pickle_path)
    #model = GraphBased(pickle_path)
    #model = WordGraph(pickle_path)
    text = model.text
    idx_sentence = model.idx_s
    ranked_sentences = [text.sentenceset[idx_sentence[i, 0]] for i in range(len(text.sentenceset))]
##    ranked_paragraphs = [text.paraset[idx_p[i, 0]] for i in range(len(text.paraset))]
##    ranked_sections = [text.section_list[idx_c[i, 0]] for i in range(len(text.section_list))]

    rankedsent_set = []
    ranked_sec_id = []
    for sentence in ranked_sentences:
        rankedsent_set.append(sentence.id)
        ranked_sec_id.append(sentence.id_sec)
    return rankedsent_set, ranked_sec_id
def sxpCalculateTopK(rankset,dataset,topk):
    ns = len(rankset)
    distanceset = []
    k = 0
    for i in range(ns / 5 + int((ns % 5) > 0)):
        topkids = rankset[:(i + 1) * 5]
        distances = sxpCompareTopk(topkids,dataset)
        distanceset.append(distances)
        n = len(topkids)
        k = k + 1
        if k >= topk:
            break;
##        if n >= topk:
##            break;
    return distanceset
def sxpCompareTopk(topkids,dataset):
# I want to find how many items of topk are in the dataset
    common_ids = set(topkids).intersection(set(dataset))
    total_ids = set(topkids).union(set(dataset))
    jaccard = float(len(common_ids)) / len(total_ids)
    distance = []
    topindataset = float(len(common_ids)) / len(dataset)
    topintop = float(len(common_ids)) / len(topkids)
    distance.append(jaccard)        #jaccard
    distance.append(topindataset) # /label data
    distance.append(topintop)    # /ranked data
    return distance
def sxpTestLabelSentenceRank(path):

    #path = r'D:\pythonwork\code\paperparse\paper\papers'
    LabelSet = tjPaperIntroSentLabel.intro_sent
    fname = path + '\\pickle\\' + 'intro_sent_id.pickle'
    intro_label_id_set = LoadSxptext(fname)
    fname = path + '\\pickle\\' + 'intro_sent_dict_id.pickle'
    intro_label_id_dict = LoadSxptext(fname)
    fname = path + '\\pickle\\importance_sentset.pickle'

    #for file_name in intro_label_id_set:
     #   print file_name
    top5 = 4
    npaper = len(intro_label_id_dict)
    paper_distance = []
    jdistance = zeros((npaper,top5),dtype=float) # jaccard dist = (topk intersect data)/(topk + data)
    rdistance =zeros((npaper,top5),dtype=float) # ranked dist = (topk intersect data)/(topk )
    ddistance = zeros((npaper,top5),dtype=float) # data dist = (topk intersect data)/(data )
    papidset = []#this is to store the index of paper in the list of intro_label_id_set
    papid = 0
    for file_name,paper_intro_id_set in list(intro_label_id_dict.items()):
        sxpfilename = path + '\\pickle\\' +file_name+ '_1.pickle'
        print('******************')
        print(file_name)
        if os.path.exists(sxpfilename) == False:
            print('no such file')
            continue;
        rankedsent_set,ranked_sec_id = sxpGetRankedSentIDSet(path,file_name)
        sxptxt = LoadSxptext(sxpfilename)
        sentenceset = sxptxt.sentenceset
        list_id = paper_intro_id_set[0]#this is the list index of label sentence of a paper
        sent_id = paper_intro_id_set[1:]#this is the label sentence
        LabelSetSent = LabelSet[list_id][1:]
        i = 0
        for sid in sent_id:
            papersent = sentenceset[sid]
            labelsent = LabelSetSent[i]
            i = i + 1
            print(sid)
            print('origin: ', papersent.sentence_text)
            print('label: ', labelsent)
        topk_distance = sxpCalculateTopK(rankedsent_set,sent_id,top5)
        i = 0
        #print topk_distance
        for topk_dist in topk_distance:
##    distance.append(jaccard)        #jaccard
##    distance.append(topindataset) # /label data
##    distance.append(topintop)    # /ranked data
            jdistance[papid,i] = topk_dist[0] #jacard
            ddistance[papid,i] = topk_dist[1] #over label data
            rdistance[papid,i] = topk_dist[2] # over ranked topk
            i = i + 1
        papid = papid + 1
        papidset.append(list_id)

        paper_distance.append(topk_distance)
    sxpre = sxpRankLabelResult()
    sxpre.ddistance = ddistance
    sxpre.rdistance = rdistance
    sxpre.jdistance = jdistance
    sxpre.papidset = papidset
    fname = path + '\\pickle\\' + 'rank_label_distance_tfidf.pickle'
    StoreSxptext(sxpre,fname)
    #now begin to calculate the average distance of topk, top
def sxpShowLableRankDistance(path):
    fname = path + '\\pickle\\' + 'rank_label_distance_tfidf.pickle'
    sxpre = LoadSxptext(fname)
    r,topkn = sxpre.ddistance.shape
    print(r,topkn)
    for i in range(topkn):
        print('topk', (i+1)*5, end=' ')
    print('======================')
    print('intersect/label data:')
    print(mean(sxpre.ddistance,axis = 0))
    print('intersect/ranked data:')
    print(mean(sxpre.rdistance,axis = 0))
    print('intersect/(data + lable):')
    print(mean(sxpre.jdistance,axis = 0))
def sxpBeginProcessRankLabelTest():
    print(" are you want to recompute the data  (c) or just load them for process (l)")
    ys = input("c, l ")
    path = r'D:\pythonwork\code\paperparse\paper\papers'
    if ys == 'c':
        sxpTestLabelSentenceRank(path)
        sxpShowLableRankDistance(path)
    if ys == 'l':
        sxpShowLableRankDistance(path)
def main():
    #sxpBeginProcessFileInDir()
    sxpBeginProcessRankLabelTest()

if __name__ == '__main__':
    main()