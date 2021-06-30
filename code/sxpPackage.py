__author__ = 'sxp'
import pickle

def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
class sxpResult:
    importance_sentset =[]

    def __init__(self):
        importance_sentset =[]

class sxpText:
    fname = ''
    title = ''
    abstract = ''
    relatedwork = ''
    conclusion = ''
    reference = ''
    section_id_dict ={}
    section_list = []
    paraset = []
    whole_sectitle = ''
    whole_text = ''
    keycount = None
    para_tfidf = None
    sentence_tfidf = None
    sentenceset = []
    context_set = []
    d_c = None
    c_p = None
    p_s = None
    s_k = None
    t_s = None #context - sentence
    p_t = None #paragraph - context
    c_c = None
    def __init__(self):
        self.fname = ''
        self.title = ''
        self.abstract = ''
        self.relatedwork = ''
        self.conclusion = ''
        self.reference = ''
        self.section_id_dict ={}
        self.section_list = []
        self.paraset = []
        self.whole_sectitle = ''
        self.whole_text = ''
        self.keycount = None
        self.para_tfidf = None
        self.sentence_tfidf = None
        self.sentenceset = []
        self.sentence_textset=[]
        self.d_c = None
        self.c_p = None
        self.p_s = None
        self.s_k = None
        self.context_set = []
        self.t_s = None
        self.p_t = None
        self.c_c = None

class sxpSectionTitle:
    title = ''
    id_str = ''
    id_set = ''
    level = 0
    id = 0
    t_type = ''
    def __init__(self):
        self.title = ''
        self.id_str = ''
        self.id_set = ''
        self.level = 0
        self.id = 0
        self.t_type = ''

class sxpPara:
    para_id = ''
    para_text = ''
    para_tuple = []
    para_tfidf =[]
    section_title=''
    sentenceset = []
    context_set = []

    id = 0
    id_sec = 0
    def __init__(self):
        self.para_id = ''
        self.para_text = ''
        self.para_tuple = []
        self.para_tfidf =[]
        self.section_title=''
        self.sentenceset = []
        self.context_set = []
        self.id = 0
        self.id_sec = 0
class sxpSent:
    sentence_text = ''
    id = 0
    id_para = 0
    id_sec = 0
    def __init__(self):
        self.sentence_text = ''
        self.id = 0
        self.id_para = 0
class sxpContext:
    context_txt = ''
    id = 0
    id_para = 0
    id_sec = 0
    context_sent = []
    def __init(self):
        self.id = 0
        self.id_para = 0
        self.id_sec = 0
        self.context_sent = 0
