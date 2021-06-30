#coding: utf-8
from numpy import *
from sxpPackage import *
import os
from Weight import *
from Tree import *
import nltk
from rake import *
import sklearn
import tjPaperIntroSentLabel
#Version one is a very raw idea
# In this model, I did not consider the influence of neighborhood
# This model is strictly based on the tree structure of the document

'''
def save(f, content):
    out = dict(enumerate(content))
    cPickle.dump(out, f)


def rank(v, content):
    idx = argsort(array(-v), axis=0)
    ranked = [content[i] for i in idx[:, 0].tolist()]
    return ranked
'''

class sxpRankResult:
    idx_w =[]
    idx_s =[]
    idx_p =[]
    idx_c =[]
    def __init__(self):
        self.idx_w =[]
        self.idx_s =[]
        self.idx_p =[]
        self.idx_c =[]

class sxpRankLabelResult:
    jdistance = []
    rdistance = []
    ddistance = []
    def __init__(self):
        jdistance = []
        rdistance = []
        ddistance = []

def test_keys(pickle_path):
    text = LoadSxptext(pickle_path)
    paragraphs = text.paraset
    sec_keys = {}
    for sec in text.section_list:
        sec_keys[sec.id] = ""
    for para in paragraphs:
        sec_keys[para.id_sec] = sec_keys[para.id_sec] + para.para_text
    for sec_id in list(sec_keys.keys()):
        fd = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(sec_keys[sec_id]))


def test_bigram(path, file_name):
    f = open(path + '//' + file_name, 'r')
    text = f.read()
    sentences = nltk.sent_tokenize(text)
    #bi_count = {}
    #bigram = []
    gram = []
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        gram.extend(nltk.ngrams(words, 4))
    for elem in gram:
        print(elem)
'''
    for elem in bigram:
        ++bi_count[elem]
    for pair in bi_count.keys():
        print pair, bi_count[pair]
'''


def test_pivot(pickle_path):
    text = LoadSxptext(pickle_path)
    sentences = []
    for sent in text.sentenceset:
        sentences.append(sent.sentence_text)
    pivots = set(['however', 'but', 'while', 'although'])
    for sent in sentences:
        words = [word.lower() for word in nltk.word_tokenize(sent)]
        if len(pivots.intersection(set(words))) != 0:
            print(sent)


def get_parameters_with_stopwords(pickle_path):
    # use external function LoadSxptext to import data
    text = LoadSxptext(pickle_path)
    sentences = text.sentenceset
    words = text.sentence_tfidf.word
    # import relation matrix
    w_s = matrix(text.sentence_tfidf.tfidf.toarray()).T
    s_p = matrix(text.p_s.toarray()).T
    p_c = matrix(text.c_p.toarray()).T
    return words, w_s, s_p, p_c


def get_parameters_without_stopwords(pickle_path):
    words, w_s, s_p, p_c = get_parameters_with_stopwords(pickle_path)
    f = open('stopwords.txt', 'r')
    lines = f.readlines()
    f.close()
    stopwords = [line.strip() for line in lines]
    idx = [i for i in range(len(words)) if words[i] not in stopwords
           and re.match(r'^[a-zA-Z]+$', words[i]) is not None]
    new_w_s = []
    for i in idx:
        new_w_s.append(array(w_s[i, :]).tolist())
    new_w_s = matrix(array(new_w_s))
    new_words = [words[i] for i in idx]
    return new_words, new_w_s, s_p, p_c


def rank_weight(weight):
    idx_w = argsort(array(-weight.w), axis=0)
    idx_s = argsort(array(-weight.s), axis=0)
    idx_p = argsort(array(-weight.p), axis=0)
    idx_c = argsort(array(-weight.c),axis=0)
    return idx_w, idx_s, idx_p, idx_c


def top10_sentence_id_set(idx_w, idx_s, idx_p, idx_c, words, pickle_path):
    text = LoadSxptext(pickle_path)
    ranked_words = [words[idx_w[i, 0]] for i in range(len(words))]
    ranked_sentences = [text.sentenceset[idx_s[i, 0]] for i in range(len(text.sentenceset))]
    ranked_paragraphs = [text.paraset[idx_p[i, 0]] for i in range(len(text.paraset))]
    ranked_sections = [text.section_list[idx_c[i, 0]] for i in range(len(text.section_list))]

    doc = {}
    for sec in text.section_list:
        doc[sec.title] = []
    for sentence in ranked_sentences:
        section_tag = text.paraset[sentence.id_para].section_title
        #section_id = text.paraset[sentence.id_para].id_sec
        if section_tag != '':
            doc[section_tag].append(sentence)
    intro_id_set = []
    for title in doc:
        print(title)
        print()
        if title.lower().find('introduction') > 0:
            for sentence in doc[title]:
                print(sentence.id_para, sentence.sentence_text)
                intro_id_set.append(sentence.id)
    return intro_id_set

def display(idx_w, idx_s, idx_p, idx_c, words, pickle_path):

    text = LoadSxptext(pickle_path)
    ranked_words = [words[idx_w[i, 0]] for i in range(len(words))]
    ranked_sentences = [text.sentenceset[idx_s[i, 0]] for i in range(len(text.sentenceset))]
    ranked_paragraphs = [text.paraset[idx_p[i, 0]] for i in range(len(text.paraset))]
    ranked_sections = [text.section_list[idx_c[i, 0]] for i in range(len(text.section_list))]

    doc = {}
    for sec in text.section_list:
        doc[sec.title] = []
    for sentence in ranked_sentences:
        section_tag = text.paraset[sentence.id_para].section_title
        #section_id = text.paraset[sentence.id_para].id_sec
        if section_tag != '':
            doc[section_tag].append(sentence)
    intro_id_set = []
    for title in doc:
        print(title)
        print()
        if title.lower().find('introduction') > 0:
            for sentence in doc[title]:
                print(sentence.id_sec,sentence.id_para, sentence.sentence_text)
                intro_id_set.append(sentence.id)


    '''
    out = {}
    for title in doc:
        min_size = amin([len(doc[title]), 3])
        out[title] = doc[title][0:min_size]
    # sort the sentence based on sentence id
    for title in out:
        out[title].sort(cmp=lambda x, y: cmp(x.id, y.id))
    for title in out:
        print title
        print
        for sentence in out[title]:
            print sentence.sentence_text


    print 'Ranked word list:\n'
    print ranked_words
    print
    print 'Ranked sentences list:\n'
    for id_num, sentence in enumerate(ranked_sentences):
        section_tag = text.paraset[sentence.id_para].section_title
        print id_num, len(sentence.sentence_text.split()), section_tag,\
            sentence.id_para, sentence.sentence_text
    print
    print 'Ranked paragraph list:\n'
    for para in ranked_paragraphs:
        print para.section_title, para.id_sec
    print
    print 'Ranked section list:\n'
    for section in ranked_sections:
        print section.title
'''


def test_with_stopwords(path, file_name):
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    words, w_s, s_p, p_c = get_parameters_with_stopwords(pickle_path)
    weight = Weight(w_s, s_p, p_c)
    w = matrix(random.rand(len(words))).T
    weight.iteration(w, 20)
    idx_w, idx_s, idx_p, idx_c = rank_weight(weight)
    display(idx_w, idx_s, idx_p, idx_c, words, pickle_path)


def calc_topK_distance(intro_id_set, intro_label_id_set):
    distance = []
    print(intro_id_set)
    print(intro_label_id_set)
    for i in range(len(intro_id_set) / 5 + int((len(intro_id_set) % 5) > 0)):
        topK = intro_id_set[:(i + 1) * 5]
        common_ids = set(topK).intersection(set(intro_label_id_set))
        total_ids = set(topK).union(set(intro_label_id_set))
        jaccard = float(len(common_ids)) / len(total_ids)
        distance.append(jaccard)
        print(jaccard)
    return distance


def precision(intro_id_set, intro_label_id_set):
    size = len(intro_label_id_set)
    topk = intro_id_set[:size]
    print("precision: ")
    common_ids = set(intro_label_id_set).intersection(set(topk))
    print(len(common_ids) / float(size))

def test_without_stopwords(path, file_name):
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    words, w_s, s_p, p_c = get_parameters_without_stopwords(pickle_path)
    weight = Weight(w_s, s_p, p_c)
    w = matrix(random.rand(len(words))).T
    weight.iteration(w, 20)
    idx_w, idx_s, idx_p, idx_c = rank_weight(weight)
    #display(idx_w, idx_s, idx_p, idx_c, words, pickle_path)
    intro_id_set = top10_sentence_id_set(idx_w, idx_s, idx_p, idx_c, words, pickle_path)
    fname = path + '\\pickle\\' + 'intro_sent_dict_id.pickle'
    intro_label_id_set = LoadSxptext(fname)
    #for file_name in intro_label_id_set:
     #   print file_name
    paper_intro_id_set = intro_label_id_set[file_name.lower()]
    #calc_topK_distance(intro_id_set, paper_intro_id_set)
    if paper_intro_id_set[0] == -1:
        print("no this paper")
    precision(intro_id_set, paper_intro_id_set)

##    intro_id_set = top10_sentence_id_set(idx_w, idx_s, idx_p, idx_c, words, pickle_path)
##    fname = path + '\\pickle\\' + 'intro_sent_dict_id.pickle'
##    intro_label_id_set = LoadSxptext(fname)
##    #for file_name in intro_label_id_set:
##     #   print file_name
##    paper_intro_id_set = intro_label_id_set[file_name.lower()]
##    #calc_topK_distance(intro_id_set, paper_intro_id_set)
##    if paper_intro_id_set[0] == -1:
##        print "no this paper"
##    precision(intro_id_set, paper_intro_id_set)


def visit(root):
    if len(root.children) == 0:
        print(root.root, root.tag)
    for child in root.children:
        visit(child)


def test_tree(path, file_name):
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    text = LoadSxptext(pickle_path)

    #print len(text.paraset)
    #print len(text.section_list)
    #print len(text.sentenceset)
    words, w_s, s_p, p_c = get_parameters_without_stopwords(pickle_path)
    weight = Weight(w_s, s_p, p_c)
    w = matrix(random.rand(len(words))).T
    weight.iteration(w, 20)
    s = weight.s.T
    p = weight.p.T
    c = weight.c.T
    #print s.shape
    #print p.shape
    #print c.shape

    root = create_section_trees(text, array(s)[0].tolist(), array(p)[0].tolist(), array(c)[0].tolist())
    visit(root)
    '''
    for section in root.children:
        for para in section.children:
            para.children = sorted(para.children, cmp=lambda x, y: cmp(x.weight, y.weight),reverse= True)

    for section in root.children:
        print section.tag
        sent_sum = 0
        total = 0.0
        for para in section.children:
            sent_sum += len(para.children)
            total += para.weight
        if sent_sum == 0 or total == 0.0:
            continue
        for para in section.children:
            print para.root
            for i in range(int(math.ceil((para.weight / total) * sent_sum * (6.0 / sent_sum)))):
                if i < len(para.children):
                    print para.children[i].tag
    '''

def Process():
    #TestSimple()
    #TestsxpLoadPickle()
  #  path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
    path = r'D:\pythonwork\code\paperparse\paper\papers'
    file_name = 'P14-1019.xhtml'
    #path = r"C:\Users\a\Desktop\graduate paper related\code"
    #file_name = 'test.txt'
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    #test_with_stopwords(path, file_name)
    test_without_stopwords(path, file_name)
    #sxptest_without_stopwords(path, file_name)
    #test_tree(path, file_name)
    #test_bigram(path, file_name)
    #test_pivot(pickle_path)
    #test_keys(pickle_path)

def sxpTestLabelSentence():
    path = r'D:\pythonwork\code\paperparse\paper\papers'
    LabelSet = tjPaperIntroSentLabel.intro_sent
    fname = path + '\\pickle\\' + 'intro_sent_id.pickle'
    intro_label_id_set = LoadSxptext(fname)
    fname = path + '\\pickle\\' + 'intro_sent_dict_id.pickle'
    intro_label_id_dict = LoadSxptext(fname)
    #for file_name in intro_label_id_set:
     #   print file_name
    for file_name,paper_intro_id_set in list(intro_label_id_dict.items()):
        sxpfilename = path + '\\pickle\\' +file_name+ '_1.pickle'
        print('******************')
        print(file_name)
        if os.path.exists(sxpfilename) == False:
            print('no such file')
            continue;
        sxptxt = LoadSxptext(sxpfilename)
        sentenceset = sxptxt.sentenceset
        list_id = paper_intro_id_set[0]
        sent_id = paper_intro_id_set[1:]
        LabelSetSent = LabelSet[list_id][1:]
        i = 0
        for sid in sent_id:
            papersent = sentenceset[sid]
            labelsent = LabelSetSent[i]
            i = i + 1
            print(sid)
            print('origin: ', papersent.sentence_text)
            print('label: ', labelsent)

#********************** compare ranked sentence with the label sentence set

def sxpTestLabelSentenceRank(path):

    #path = r'D:\pythonwork\code\paperparse\paper\papers'
    LabelSet = tjPaperIntroSentLabel.intro_sent
    fname = path + '\\pickle\\' + 'intro_sent_id.pickle'
    intro_label_id_set = LoadSxptext(fname)
    fname = path + '\\pickle\\' + 'intro_sent_dict_id.pickle'
    intro_label_id_dict = LoadSxptext(fname)
    fname = path + '\\pickle\\importance_sentset.pickle'
    rankresult = LoadSxptext(fname)
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
        rankedsent_set,rankedsent_secid = sxpGetRankedSentIDSet(path,file_name)
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
    fname = path + '\\pickle\\' + 'rank_label_distance.pickle'
    StoreSxptext(sxpre,fname)
    #now begin to calculate the average distance of topk, top
def sxpShowLableRankDistance(path):
    fname = path + '\\pickle\\' + 'rank_label_distance.pickle'
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
#*********************************************
#**************Ranking sentence in global range
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
def sxpGetRankedSentIDSet(path,file_name):
    rankfname = path + '\\pickle\\' + file_name + '_rankresult.pickle'
    rankresult = LoadSxptext(rankfname)
    sxptxtfname = path + '\\pickle\\' + file_name + '_1.pickle'
    text = LoadSxptext(sxptxtfname)
    words, w_s, s_p, p_c = get_parameters_without_stopwords(sxptxtfname)
    ranked_words = [words[rankresult.idx_w[i, 0]] for i in range(len(words))]
    ranked_sentences = [text.sentenceset[rankresult.idx_s[i, 0]] for i in range(len(text.sentenceset))]
    ranked_paragraphs = [text.paraset[rankresult.idx_p[i, 0]] for i in range(len(text.paraset))]
    ranked_sections = [text.section_list[rankresult.idx_c[i, 0]] for i in range(len(text.section_list))]

    ranked_sent_id = []
    ranked_sent_secid = []
    for sentence in ranked_sentences:
        ranked_sent_id.append(sentence.id)
        ranked_sent_secid.append(sentence.id_sec)
    return ranked_sent_id, ranked_sent_secid

def sxpdisplay(idx_w, idx_s, idx_p, idx_c, words, pickle_path):
    text = LoadSxptext(pickle_path)
    [nc,np] = text.c_p.shape
    ranked_words = [words[idx_w[i, 0]] for i in range(len(words))]
    ranked_sentences = [text.sentenceset[idx_s[i, 0]] for i in range(len(text.sentenceset))]
    ranked_paragraphs = [text.paraset[idx_p[i, 0]] for i in range(len(text.paraset))]
    ranked_sections = [text.section_list[idx_c[i, 0]] for i in range(len(text.section_list))]

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
def sxpProcessFile(path, file_name):
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    words, w_s, s_p, p_c = get_parameters_without_stopwords(pickle_path)
    weight = Weight(w_s, s_p, p_c)
    w = matrix(random.rand(len(words))).T
    weight.iteration(w, 20)
    idx_w, idx_s, idx_p, idx_c = rank_weight(weight)
    rankresult = sxpRankResult()
    rankresult.idx_w = idx_w
    rankresult.idx_s = idx_s
    rankresult.idx_p = idx_p
    rankresult.idx_c = idx_c
    rankfname = path + '\\pickle\\' + file_name + '_rankresult.pickle'
    StoreSxptext(rankresult,rankfname)
    return sxpdisplay(idx_w, idx_s, idx_p, idx_c, words, pickle_path)
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
    #TestRankHist()
    #Process()
    #sxpTestsxpIsAbsIntroConSentA()
    #sxpTestLabelSentence()
    sxpBeginProcessFileInDir()
    sxpBeginProcessRankLabelTest()
if __name__ == '__main__':
    main()


