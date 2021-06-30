#coding=utf-8
from bs4 import BeautifulSoup
import re
import sxpReadFileMan
import sxpTextEncode
import sxpMultiPaperData
from sxpMultiPaperData import sxpNode
import Levenshtein
import sxpMetricScore

output_dir = r'./test/multipaper/test/out/keywordquery'
sxpReadFileMan.CheckMkDir(output_dir)

def ProcessRefText():
 #   name_id_dict=ProcessHTML()
 #this is to find every refs that are in a para a section and build a dict
 # to map the para, the section to those refs in there text. refs are used as named id.
    fname = r'E:\pythonworknew\code\textsum\test\multipaper\citation_position.txt'
    txt = sxpReadFileMan.ReadTextUTF(fname)




    slines = txt.split('\n')
    pt = r'(\d+(\.\d+)*)\\t(([\w\W]+\s+)+)'
    fc = []
    para_list=[]
    ctpat= r'\(((\d+)[a-z]*)\)'
    ctpat = r'\(([A-Z][a-z]+\s)(and\s[A-Z][a-z]+\s|et\-al\.\s)*(\d+[a-z]*)\)'
    chapter_key_dict={}
    for i, st in enumerate(slines):
        if len(st.strip())==0:
            continue
        g = re.match(pt,st)
        if g:
            c = g.groups()
            print(i,st,c)
            titlekeys=c[2]

            if c[0]:
                chapter_key_dict[c[0]] = c[2]
                subs = c[0].split('.')
                fc = []
               # print(g)
                for k, each in enumerate(subs):
                    sc = '.'.join(subs[0:k+1])
                    fc.append(sc)

        else:
            para ={}
            para['content']=st;
            para['chapter']=fc

            ref=re.findall(ctpat,st)
            reftxt_list=[]
            for eachr in ref:
                reftxt_list.append(''.join(eachr))
            para['ref']=ref
            para['reftxt']=reftxt_list
            print(para['reftxt'],para['chapter'])
            para_list.append(para)
    chapter_ref_dict={}

    for chpter,keys in chapter_key_dict.items():
        chapter_dict={}
        chapter_dict['chapter']=chpter;
        chapter_dict['title']=keys;
        ref_list=[]
        txt = ""
        for eachpara in para_list:
            for ch in eachpara['chapter']:
                if ch == chpter:
                    txt = txt + '\n' + eachpara['content']
                    for ref in eachpara['reftxt']:
                        ref_list.append(ref)
        chapter_dict['ref']=ref_list
        chapter_dict['txt']=txt
        chapter_ref_dict[chpter]=chapter_dict
        print(chpter,keys,'-------has-----')
        print(ref_list)


    name_id_dict=ProcessHTML()


    refid_dict = FindAllRefWithFullTxt()

    print('--------map ref name to ref id-------')
    chapter_refid_dict={}
    for ch,chapter_dict in chapter_ref_dict.items():
        chapter_content_dict={}
        idlist=[]
        reflsit = chapter_dict['ref']
        chapter_content_dict['title']=chapter_dict['title']
        fulltxtidlist=[]
        for ref in reflsit:
            if ref in name_id_dict.keys():
                refid = name_id_dict[ref]
                idlist.append((refid['id'], ref))
                if refid['id'] in refid_dict.keys():
                   refidinfo= refid_dict[refid['id']]
                   print('fulltxt',refid['id'],refidinfo['fulltext_fid'])
                   if refidinfo['fulltext_fid']:
                      fulltxtidlist.append((refid['id'], ref,refidinfo['fulltext_fid']))
        chapter_content_dict['ref_idlist']=idlist#citation id in the text
        chapter_content_dict['content'] = chapter_dict['txt'] #the citation words in survey
        chapter_content_dict['fulltxt_fid']=fulltxtidlist #full text file id
        chapter_refid_dict[ch]=chapter_content_dict
    print('----------chapter_refid_dict----------')
    for ch,chapter_content_dict in chapter_refid_dict.items():
        print(ch,chapter_content_dict['ref_idlist'],chapter_content_dict['fulltxt_fid'])
    print('----------name_id_dict----------')

 # Sipos et-al. 2012 {'id': 'CR143', 'name': 'Sipos et-al. 2012', 'title': 'Large-margin learning of submodular summarization models', 'year': '2012', 'ref': 'Sipos R, Shivaswamy P, Joachims T (2012) Large-margin learning of submodular summarization models. In: Proceedings of the 13th conference of the European chapter of the association for computational linguistics, Association for Computational Linguistics, pp 224–233'}

    refname_dict = {}
    for ch,namedict in name_id_dict.items():
        print(ch,namedict)
        refidname_dict={}
        refidname_dict['refname']=ch
        refidname_dict['id']=namedict['id']
        refidname_dict['year']=namedict['year']
        refidname_dict['ref'] = namedict['ref']
        refidname_dict['title'] = namedict['title']
        refname_dict[namedict['id']]=refidname_dict
    print('----------refid_dict----------')
    fulltxtfid_dict={}
    for ch,refid in refid_dict.items():

        if refid['fulltext_fid'] not in fulltxtfid_dict.keys():
            refpaper ={}
            refpaper['refid']=ch
            if ch not in refname_dict.keys():
                print('not in refname_dict',ch,refid['title'])
                content = refid['content']
                s = re.split('\((\d+)\)',content)
                if len(s)>=3:
                    title= s[2]
                    year =s[1]
                    name = s[0] + year
                else:
                    title = refid['content']
                    name = refid['id']
                    year= 'none'
                refidname_dict = {}
                refidname_dict['year'] =year
                refidname_dict['title']=title
                refidname_dict['refname']=name
                refidname_dict['ref']=content
            else:
                refidname_dict = refname_dict[ch]
            refpaper['refcontent']=refid['content']
            refpaper['title']=refid['title']
            refpaper['year']=refidname_dict['year']
            refpaper['ref']=refidname_dict['ref']
            refpaper['refname']=refidname_dict['refname']
            refpaper['fulltext_fid']=refid['fulltext_fid']
            fulltxtfid_dict[refid['fulltext_fid']] =refpaper
            print(refid['fulltext_fid'], refpaper)
#8.2 [('CR126', 'Pitler and Nenkova 2008'), ('CR16', 'Barzilay and Lapata 2005'), ('CR51', 'Grosz et-al. 1995'), ('CR155', 'Vadlapudi and Katragadda 2010')] [('CR16', 'Barzilay and Lapata 2005', '0061'), ('CR51', 'Grosz et-al. 1995', '0022')]
    sxpReadFileMan.SaveObject(chapter_refid_dict,'survey_ref_chapter_refid_dict.dict',output_dir)
#Sipos et-al. 2012 {'id': 'CR143', 'name': 'Sipos et-al. 2012', 'title': 'Large-margin learning of submodular summarization models', 'year': '2012', 'ref': 'Sipos R, Shivaswamy P, Joachims T (2012) Large-margin learning of submodular summarization models. In: Proceedings of the 13th conference of the European chapter of the association for computational linguistics, Association for Computational Linguistics, pp 224–233'}
    sxpReadFileMan.SaveObject(name_id_dict, 'survey_ref_name_id_dict.dict',output_dir)
#CR1 {'id': 'CR1', 'content': 'Abuobieda A, Salim N, Albaham AT, Osman AH, Kumar YJ (2012) Text summarization features selection method using pseudo genetic-based model. In: International conference on information retrieval knowledge management, pp 193–197', 'year': '2012', 'title': 'Text summarization features selection method using pseudo genetic-based model', 'fulltext_fid': False}
    sxpReadFileMan.SaveObject(refid_dict, 'survey_ref_refid_dict.dict',output_dir)
#0050 {'refid': 'CR140', 'refcontent': 'Shen C, Li T, Ding CH (2011) Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis PLSA with sentence bases. In: AAAI', 'title': 'Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis PLSA with sentence bases', 'year': '2011', 'ref': 'Shen C, Li T, Ding CH (2011) Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis PLSA with sentence bases. In: AAAI', 'refname': 'Shen et-al. 2011', 'fulltext_fid': '0050'}
    sxpReadFileMan.SaveObject(fulltxtfid_dict, 'survey_ref_fulltxtfid_dict.dict', output_dir)

    return  chapter_refid_dict,para_list,chapter_key_dict
def GetRefFid():
    chapter_refid_dict=sxpReadFileMan.LoadObject('survey_ref_fulltxtfid_dict.dict',output_dir);
    return chapter_refid_dict
def GetRefFidText():
    chapter_refid_dict=sxpReadFileMan.LoadObject('survey_ref_fulltxtfid_dict.dict',output_dir);
    sentxt=[]
    for fid,refpaper in chapter_refid_dict.items():

        sentxt.append(str(fid) +' '+ refpaper['refname'] +' '+refpaper['ref'])
    return sentxt
def GetChapterRefList(chapter='4.1'):
    chapter_refid_dict=sxpReadFileMan.LoadObject('survey_ref_chapter_refid_dict.dict',output_dir);
    if chapter in chapter_refid_dict.keys():
        return chapter_refid_dict[chapter]
def GetAllChapterDict():
    chapter_refid_dict = sxpReadFileMan.LoadObject('survey_ref_chapter_refid_dict.dict',output_dir)

    return chapter_refid_dict

def ComputeRankFidResult(chapter,rank_fid):
    chapter_refid_dict=sxpReadFileMan.LoadObject('survey_ref_chapter_refid_dict.dict',output_dir);
    if chapter in chapter_refid_dict.keys():
        chapter_content_dict= chapter_refid_dict[chapter]
        fulltxt_fid = chapter_content_dict['fulltxt_fid']
        if len(fulltxt_fid)==0:
            print('fulltxt_fid is empty')
        result=sxpMetricScore.jaccardscore(rank_fid,fulltxt_fid)
        return result
    return None
def ProcessRefList():
    #this is to get the info of each ref from reference list including
    #named id, id, title and year return refid_dict
    fname = r'E:\pythonworknew\code\textsum\test\multipaper\reference.html'
    f = open(fname,encoding='utf-8')
    soup = BeautifulSoup(f)
    ctlist=soup.findAll(name="div", attrs={"class" :"CitationContent"})
    i = 1
    refid_dict={}
    pt = r'\((\d{4}[a-z]*)\)\s+([A-Za-z\:\?\s\-\,0-9\/\']+)\.'
    for ct in ctlist:
        #print(i, ct)
        refid = {}
        refid['id']=ct['id']
        ps = str(ct.contents[0].string)
        refid['content']= ps

        i = i + 1

        ctitle=re.findall(pt,ps)
        refid['year']=ctitle[0][0]
        refid['title'] = ctitle[0][1]
#        if len(ctitle)==0:
#            print(i,ct['id'],ct.contents[0],ctitle)
       # print(i,ct['id'],ct.contents[0],ctitle)
        refid['fulltext_fid']=False
      #  print(i,ct['id'],ctitle[0][0],ctitle[0][1])
        if ct['id'] not in refid_dict.keys():
            refid_dict[ct['id']] = refid
        else:
            print('duplate ref id',ct)
    f.close()
    return refid_dict

def BuildAlreadyInData():
    refid_dict=ProcessRefList()
    filenamelist=sxpMultiPaperData.LoadDocFileName()
    for doc_dict in filenamelist:
        print(doc_dict['title'], doc_dict['fid'])
    fname = r'./test/multipaper/allpaper.list'
    sxpReadFileMan.SaveObject(filenamelist,fname)
def FindAllRefWithFullTxt():
    refid_dict=ProcessRefList()
    print('----refid_dict-----')
    for rf,di in refid_dict.items():
        print(rf,di)
    fname = r'./test/multipaper/allpaper.list'
    alltxtlist= sxpReadFileMan.LoadObject(fname)
    i = 1
    print('----alltxtlist-----')
    for doc_dict in alltxtlist:
        print(i,doc_dict['title'],doc_dict['fid'])
        i = i + 1
    i = 1
    for doc_dict in alltxtlist:


        for refid,ref in refid_dict.items():
            d = Levenshtein.distance(ref['title'].lower(),doc_dict['title'].lower())
            if d<=10:
             #   print(d,ref['title'].lower(),doc_dict['title'].lower())
                ref['fulltext_fid']=doc_dict['fid'];
                print(i,doc_dict['title'], doc_dict['fid'],refid)
              #  print(i,'has full text')
                i = i + 1;

            # if ref['title'].lower()==doc_dict['title'].lower():
            #     ref['fulltxt']=doc_dict['fid'];
            #     print(i,'has full text')
            #     i = i + 1;
    return refid_dict
def ProcessHTML():
    #this is to parse out all refs in the html format full raw text
    #but now we have not yet to produce it out this is to map
    #from name id(Liu 2004) to cit id(CR100) so that we can have
    refid_dict = ProcessRefList()
    print('---ProcessHTML-refid_dict-----')
    for k,ct in refid_dict.items():
        print(k,ct)
    fname = r'E:\pythonworknew\code\textsum\test\multipaper\Recent automatic text summarization techniques_ a survey _ SpringerLink.html'
   # soup = BeautifulSoup(open(fname))
    txt = sxpReadFileMan.ReadTextUTF(fname)

    utxt = sxpTextEncode.utf2str(txt)
  #  print(txt)
    ctinfo_list=[]
#    pt = r'\<span class="CitationRef"\>\<a href\="\#(CR\d+)">(\w+)\<\/a\>\<\/span\>'
    pt = r'(([A-Z][a-z]+)\s+\<span class="CitationRef"\>\<a href\="\#(CR\d+)">(\w+)\<\/a\>\<\/span\>)'
    ct = re.findall(pt,txt)
    for c in ct:
        cinfo ={}
        cinfo['name']=c[1]
        cinfo['id']=c[2]
        cinfo['year']=c[3]
        ctinfo_list.append(cinfo)
   #     print(c)
    pt = r'(([A-Z][a-z]+\s+and\s+[A-Z][a-z]+)\s+\<span class="CitationRef"\>\<a href\="\#(CR\d+)">(\w+)\<\/a\>\<\/span\>)'
    ct = re.findall(pt,txt)
    for c in ct:
        cinfo ={}
        cinfo['name']=c[1]
        cinfo['id']=c[2]
        cinfo['year']=c[3]
        ctinfo_list.append(cinfo)
 #       print(c)
 #   pt = r'([A-Z][a-z]+\s+et\s+al\.)\s+\<span class="CitationRef"\>\<a href\="\#(CR\d+)">(\w+)\<\/a\>\<\/span\>'
 #   pt = r'([A-Z][a-z]+\s+et\s+al\.)\s+\(*\<span class="CitationRef"\>\<a href\="\#(CR\d+)">(\w+)\<\/a\>\<\/span\>'
 #   pt = r'([A-Z][a-z]+\s*et\s*al)'
    pt = r'(([A-Z][a-z]+\s*et\-al\.)\s+\(*\<span class="CitationRef"\>\<a href\="\#(CR\d+)">(\w+)\<\/a\>\<\/span\>)'
    ct = re.findall(pt,txt)
    for c in ct:
        cinfo ={}
        cinfo['name']=c[1]
        cinfo['id']=c[2]
        cinfo['year']=c[3]
        ctinfo_list.append(cinfo)
  #      print(c)
    print('--ProcessHTML--ctinfo_list-----')
    i = 1
    name_id_dict={}
    for c in ctinfo_list:
        print(i,c)
        i = i + 1
        name = c['name'] + ' '+ c['year']
        if name in name_id_dict.keys():
            #print('conflicted',c,name_id_dict[name])
            continue
        else:
            namedict ={}
            namedict['id']=c['id']
            namedict['name']=name
            #namedict=ing et-al. 2015 {'id': 'CR17', 'name': 'Bing et-al. 2015', 'title': 'Abstractive multi-document summarization v
            name_id_dict[name]=namedict

    print('--ProcessHTML--name_id_dict-----')
    for name,namedict in name_id_dict.items():
        id= namedict['id']
        if id in refid_dict.keys():
            print(refid_dict[id])
        else:
            print('no in ref')
        namedict['title']=refid_dict[id]['title']
        namedict['year'] = refid_dict[id]['year']
        namedict['ref'] = refid_dict[id]['content']
    print('--ProcessHTML--name_id_dict-----')
    for name,namedict in name_id_dict.items():
        print(name,namedict)
      #  print(name,id,refid_dict[id])
    # poslist = searchallpos(txt,pt)
    # i = 1;
    # for ct,et,p in poslist:
    #     print(ct)
    #     print(i,txt[ct:et],p.groups())
    #     i = i + 1
    return name_id_dict
def searchallpos(s,pt):
    n = len(s)
    pos=[]
    substr = s[0:n]
    p = re.search(pt,substr)
    currentpos = 0
    while(p):
        print(p,'--------------------')
        ps = p.span()
        st = currentpos + ps[0]

        et = currentpos + ps[1]
        pos.append((st,et,p))
        substr = s[et:]
        currentpos = et
        p = re.search(pt,substr)
    return pos
def main(maincmd =""):
    #BuildAlreadyInData()
 #   FindAllRefWithFullTxt()
    if maincmd:
        cmd = maincmd
    else:
        cmd ='ProcessRefText'
    if cmd =='ProcessRefText':
        print('run ProcessRefText-----')
        ProcessRefText()
    #ProcessRefList()
    #ProcessRefText()
    #refid_list = ProcessRefList()

    #ProcessHTML()
if __name__ == '__main__':
    main()

