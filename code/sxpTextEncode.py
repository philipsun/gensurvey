#-------------------------------------------------------------------------------
# Name:        sxpTextEncode
# Purpose:
#
# Author:      sunxp
#
# Created:     22-03-2015
# Copyright:   (c) sunxp 2015
# Licence:     <MIT licence>
#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
#coding:utf-8
import codecs
import urllib.request, urllib.parse, urllib.error
import re
import sys
import chardet
import sys
import itertools
global_type = sys.getfilesystemencoding()
print(global_type)
def TransformListToUTFStr(sl):
    ns = []
    for s in sl:
       # s1=s.decode('mbcs').encode('utf-8')
        s1=GetPrintUTFStrA(s)
        ns.append(s1.encode('gbk'))
    return ns

def TransformListToUTF(sl):
#this version is currently work for my re.compile and re.search for chinese
#characters and engish digits
    ns = []
    for s in sl:
       # s1=s.decode('mbcs').encode('utf-8')
        s1=GetPrintUTFStrA(s)
        ns.append(s1)
    return ns
def PrintAsUnicode(s,fromcoding,tocoding):
    if isinstance(s,str):
        us = s.decode(fromcoding).encode(tocoding)
    if isinstance(s,str):
        us = str(s,fromcoding).encode(tocoding)
    print(us)
    return us
def GetReprUTFList(sl,fromcoding,tocoding):
    rslist=[]
    for s in sl:
        rslist.append(GetReprUTF(s,fromcoding,tocoding))
    return rslist
def GetReprUTFListStr(sl,fromcoding,tocoding):
    rslist=''
    for s in sl:
        rslist=rslist + s
    return GetReprUTFstr(rslist,fromcoding,tocoding)
def GetReprUTF(s,fromcoding,tocoding):
    if isinstance(s,str):
        rs =repr(s.encode(fromcoding).decode(tocoding));
    else:
        us = str(s,tocoding)
        rs = repr(us)
    return rs
def GetReprUTFstr(s,fromcoding,tocoding):
    if isinstance(s,str):
        rs =str(repr(s.encode(fromcoding).decode(tocoding)));
    else:
        us = str(s,tocoding)
        rs = str(repr(us))
    return rs
def PrintAsStr(s,encodeing='utf-8',tocoding='utf-8'):
    seg=TransformTo(s,encodeing,encodeing)
    print(seg)
    return seg
def TransformTo(s,fromcoding,tocodeing):
    if isinstance(s,str):
        us = s.encode(fromcoding)
    if isinstance(s,str):
        us = str(s,fromcoding).encode(tocodeing)

    return us
def TransformToUTF(s):
    tocodeing = 'utf-8'
    if isinstance(s,str):
        t = GetTestTypeCode(s)
        fromcoding = t[0][0] # it is ['utf-8', ok, 'word']
        us = s.encode(fromcoding).decode('utf-8')
    if isinstance(s,str):
        t=GetTestTypeCode(s)
        fromcoding = t[0][0]
        us = str(s,fromcoding).encode(fromcoding).decode('utf-8')
    return (us,fromcoding)
def utf(s):
    us = detutf(s)
    return us
def utf2str(s):
    if not isinstance(s,str):
       if not isinstance(s,str):
           print(('not a str',s))
           try:
              s = str(s)
           except Exception as e:
              return ""
    if not isinstance(s,str):
      if not isinstance(s,str):
        print(('not a str',s))
        try:
           s = str(s)
        except Exception as e:
           return ""

    us = detutf(s)
    uus,fromcoding,fromtype,totype =trytype(s)#when using unicode with fromcoding, it will be correctly print out.
    #when using 'mbcs', print will get a correct print of Beatriz Muńoz. But if using fromcoding, it will be a mess code
    #when using 'utf-8', print will be a mess out.
    ss= uus.encode('utf-8')
    return ss

def trytype(us):

    if isinstance(us,str):
        if len(us)==0:
           return "","utf-8",'utf-8','str'
        codetype =['ISO-8859-2','mbcs','utf-8','gbk','gb2311']
        okcode= []
        for tocode in codetype:
            try:
                uus = us.encode(tocode).decode(tocode)#this will produce a unicode
                if isinstance(uus,str):
                    totype = 'str'
                if isinstance(uus,str):
                    totype = 'unicode'
                okcode.append([uus,tocode,totype])
            except Exception as e:
                 continue
        if len(okcode)>0:
            return okcode[0][0],okcode[0][1],'unicode',okcode[0][2]

        else:
            return repr(us).encode('utf-8'),'utf-8','str','repr'
    if isinstance(us,str):
        if len(us)==0:
           return "","utf-8",'str','str'
        d = chardet.detect(us)
        fromcoding = d['encoding']
        uus = us.decode(fromcoding) #convert str to unicode in type of fromcoding
        if isinstance(uus,str):
            tostr='unicode'
        else:
            tostr ='str'
        return uus,fromcoding,'str',tostr #so after this, us will be a unicode
    us = str(us)
    d = chardet.detect(us)
    fromcoding = d['encoding']
    uus = us.decode(fromcoding) #convert str to unicode in type of fromcoding
    if isinstance(uus,str):
        tostr='unicode'
    else:
        tostr ='str'
    return uus,fromcoding,'str',tostr #so after this, us will be a unicode
def makeunicode(s):
    if isinstance(s,str):
        return s
    trycode=['utf-8','mbcs','ISO-8859-2','gbk', 'gb2311']
    us=None
    for t in trycode:
        try:
            us = str(s,t)
            break
        except Exception as e:
            continue
    return us

def makeutf(s):
    us = makeunicode(s)
    if us is None:
        return None
    trycode=['utf-8','mbcs','ISO-8859-2','gbk', 'gb2311']
    uus=None
    for codepair in itertools.product(trycode,trycode):
        try:
            uus=us.encode(codepair[0]).decode(codepair[1])
        except Exception as e:
            continue
    return uus

def detutf(us,ignore=False):
    if len(us)==0:
       return ""
    if isinstance(us,str):
        codetype =['ISO-8859-2','mbcs','utf-8','gbk','gb2311']
        okcode= []
        if len(us)==0:
           return ""
        for tocode in codetype:
            try:
                uus = us.encode(tocode).decode(tocode) #this is to ensure that the uus is an unicode object, not a string object
                if isinstance(uus,str):
                    totype = 'str'
                if isinstance(uus,str):
                    totype = 'unicode'
                okcode.append([uus,tocode,totype])
            except Exception as e:
                 continue
        if len(okcode)>0:
            return okcode[0][0]

        else:
            return repr(us).endcode('utf-8') #repr will be a string and will be transformed to a unicode
    if isinstance(us,str):
        d = chardet.detect(us)
        fromcoding = d['encoding']
        print((us,d))
        if len(us)==0:
          uus=""
        else:
          uus = us.decode(fromcoding) #convert str to unicode in type of fromcoding.
        if isinstance(uus,str):
            tostr='unicode'
        else:
            tostr ='str'
        return uus #so after this, us will be a unicode
    us = str(us)
    d = chardet.detect(us)
    fromcoding = d['encoding']
    uus = us.decode(fromcoding) #convert str to unicode in type of fromcoding.
    if isinstance(uus,str):
        tostr='unicode'
    else:
        tostr ='str'
    return uus #so after this, us will be a unicode


def detutf2str(us,ignore=False):
    u,fromcode,fromtype, totype=trytype(us)
    ss =Transform2Str(u,fromcode)
    return ss
def tryutf(us,fromcoding,tocodeing='utf-8',ignore=False):
    if ignore:
        if isinstance(us,str):
          us = str(us,fromcoding,'ignore')
    else:
          us =str(us,fromcoding)
    rev = False;
    try:
         s = us.encode(fromcoding).decode(tocodeing)
    except Exception as e:
         s = us.encode(tocodeing).decode(fromcoding)
         rev = True
    return s,rev
def Test():
    s = 'Christian Urcuqui, Yor Casta駉, Jhoan Delgado, Andres Navarro, Javier Diaz, Beatriz Mu駉z and Jorge Orozco M.D.'
    print('makeunicode');print(( makeunicode(s)))
    print('raw');print(s)
    print('test of unicode')
    print((s.decode("ISO-8859-2").encode('utf-8')))
    print('------------')
    su = 'Christian Urcuqui, Yor Casta駉, Jhoan Delgado, Andres Navarro, Javier Diaz, Beatriz Mu駉z and Jorge Orozco M.D.'
    print('makeunicode');print((  makeunicode(su)))
    print((su.encode("gbk").decode('ISO-8859-2')))
    print((su.encode("utf-8").decode('mbcs')))
    print((su.encode("utf-8").decode('utf-8')))

    print('------string------')
    authors ="Christian Urcuqui, Yor Castaño, Jhoan Delgado, Andres Navarro, Javier Diaz, Beatriz Muñoz and Jorge Orozco M.D.', 'Exploring Machine Learning to Analyze Parkinson’s Disease Patients"
    print('raw');print(authors)
    print('test of unicode')
    print('makeunicode');print((  makeunicode(authors)))

    print((authors.decode("utf8").encode('mbcs')))
    print((authors.decode("utf8").encode('utf8')))
#    print(authors.decode("utf-8").encode('ISO-8859-2')) #failed

    print((authors.decode("mbcs").encode('utf8')))
    print((authors.decode("mbcs").encode('mbcs')))
#    print(authors.decode("mbcs").encode('ISO-8859-2'))#failed

    print((authors.decode("ISO-8859-2").encode('utf8')))
    print((authors.decode("ISO-8859-2").encode('mbcs')))
#    print(authors.decode("ISO-8859-2").encode('gb2312'))#failed

    print('------unicode------')
    uauthors ="Christian Urcuqui, Yor Castaño, Jhoan Delgado, Andres Navarro, Javier Diaz, Beatriz Muñoz and Jorge Orozco M.D.', 'Exploring Machine Learning to Analyze Parkinson’s Disease Patients"
    print('raw unicode');print(uauthors)  #ok
    print('test of unicode')
    print('makeunicode');print((  makeunicode(uauthors)))


    print((uauthors.encode("utf8").decode('mbcs')))
    print((uauthors.encode("utf8").decode('utf8')))#ok
#    print(uauthors.decode("utf-8").encode('ISO-8859-2')) #failed

#    print(uauthors.encode("mbcs").decode('utf8')) #failed
    print((uauthors.encode("mbcs").decode('mbcs')))
    print((uauthors.encode("mbcs").decode('ISO-8859-2')))

#    print(uauthors.encode("ISO-8859-2").decode('utf8'))#failed
#    print(uauthors.encode("ISO-8859-2").decode('mbcs'))#failed
#    print(uauthors.decode("ISO-8859-2").encode('gb2312'))#failed

    print('----str to--unicode------')
    authors3 ="Christian Urcuqui, Yor Castaño, Jhoan Delgado, Andres Navarro, Javier Diaz, Beatriz Muñoz and Jorge Orozco M.D.', 'Exploring Machine Learning to Analyze Parkinson’s Disease Patients"
    print('raw');print(authors3)
    print('test of unicode')

    print('makeunicode');print(( makeunicode(uauthors)))

    us3 = str(authors3,'utf-8')

    print("1:");print("unicode:");print(us3)#ok

    print("2:");print((us3.encode("utf8").decode('mbcs')))
    print("3:");print((us3.encode("utf8").decode('utf8')))#ok
#    print(uauthors.decode("utf-8").encode('ISO-8859-2')) #failed

#    print(uauthors.encode("mbcs").decode('utf8')) #failed
    print("4:");print((us3.encode("mbcs").decode('mbcs')))
    print("5:");print((us3.encode("mbcs").decode('ISO-8859-2')))

#    print(uauthors.encode("ISO-8859-2").decode('utf8'))#failed
#    print(uauthors.encode("ISO-8859-2").decode('mbcs'))#failed
#    print(uauthors.decode("ISO-8859-2").encode('gb2312'))#failed

    return
    us = detutf(s)
    print(us)
    print(('is str',isinstance(us,str)))
    print(('is unicode',isinstance(us,str)))

    ss = detutf2str(us)
    print(('detutf2str',ss))
    print(('is str',isinstance(ss,str)))
    print(('is unicode',isinstance(ss,str)))
    print(('GetPrintUTFStrA',GetPrintUTFStrA(s)))
    print(('GetPrintUTFStr',GetPrintUTFStr(s)))
    print('utf2str');print((utf2str(s)))
    print('utf');print((utf(s)))
    print('PrintAsStr');print((PrintAsStr(s)))
    print('two2oneUTF');print((two2oneUTF(s)))
 #   print(fromcoding)
#    print(rev)
def Transform2Str(us,fromcoding='utf-8'):
    if isinstance(us,str):
        return us
    s =str(us.encode(fromcoding))
    return s
def TestTransformUTF():
    print(('get default coding',sys.getdefaultencoding()))
    print('**********unicode test******')
    s = '哈哈'
    print(('is str', isinstance(s, str)))
    print(('is unicode', isinstance(s, str)))

    us,fromcoding = TransformToUTF(s)
    print(us)
    print(fromcoding)
    print(('is str', isinstance(us, str)))
    print(('is unicode', isinstance(us, str)))
    print('*********agina**************')
    uus,ufromcoding =  TransformToUTF(us)
    print(uus)
    print(ufromcoding)
    print('**********back to string test******')
    ts = Transform2Str(us,fromcoding)
    print(ts)
    print(('is str', isinstance(ts, str)))
    print(('is unicode', isinstance(ts, str)))

    print('**********string test******')
    s = '哈哈'
    print(('is str', isinstance(s, str)))
    print(('is unicode', isinstance(s, str)))
    us,fromcoding = TransformToUTF(s)
    print(us)
    print(fromcoding)
    print(('is str', isinstance(us, str)))
    print(('is unicode', isinstance(us, str)))
    print('*********agina**************')
    uus,ufromcoding =  TransformToUTF(us)
    print(uus)
    print(ufromcoding)
    print('**********back to string test******')
    ts = Transform2Str(us,fromcoding)
    print(ts)
    print(('is str', isinstance(ts, str)))
    print(('is unicode', isinstance(ts, str)))

def PrintList(restr_list):
    for t,s in restr_list:
        print((s,t))
        print((s.encode(t).decode('utf-8')))
def Compose(sent_list):
    sent =''
    for ch in sent_list:
        sent=sent+ch
    return sent
def two2oneUTF(two_bytes):
    #('ch', '\xa3\xa9', u'\uff09')
    t,seg = GetPrintUTFStr(two_bytes)
    seg =  seg.encode('utf-8').decode('utf-8')
    return seg
def DetermineCode(s):
    typeset = GetTestTypeCode(s)
    for t in typeset:
        if t[1] == 'ok':
            return t[0]
    ignore = True;
    itypeset = GetTestTypeCode(s,ignore)
    for t in typeset:
        if t[1] == 'ok':
            return t[0]
    return 'ascii';
def GetTestTypeCode(s,ignore = False):
    typeset =[]
    if isinstance(s,str) == True:
       d = ('utf-8','ok',s)
       typeset.append(d)
       return typeset
    else:
        codetype =['ISO-8859-2','mbcs','utf-8','gbk','gb2311']
        for ctype in codetype:
            try:
                if ignore == False:
                    us = str(s,ctype)
                else:
                    us = str(s,ctype,'ignore')
                d = (ctype,1,us)
                typeset.append(d)
    #            print d;
            except Exception as e:
                d = (ctype,0,s)
                typeset.append(d)
    return typeset;
def GetGBKStr(s):
    us = GetUnicode(s);
    if us[0]=='utf-8':
        gs = us[1].encode('gbk');
    else:
        return s;
    return gs
def GetURLEncode(urlstr):
    gs = GetUnicode(urlstr)
    gss = gs.encode('gbk')
    return urllib.parse.quote(gss,':./=?%!&$')
def GetTypeUnicode(s,coding='utf'):
    if isinstance(s,str):
        return s;
    return str(s,coding)
def GetUnicode(s):
    if isinstance(s,str):
        return s;
    typeset = GetTestTypeCode(s)
    restr = None
    for t in typeset:
        if t[1] == 1 and t[0] == 'utf-8':
            restr = t[2];
            break;
        elif t[1] == 1:
            restr = t[2];
    return restr;
def GetUnicodePair(s):
    if isinstance(s,str):
        restr = ['utf-8',s];
        return restr;
    typeset = GetTestTypeCode(s)
    restr = ['', s]
    for t in typeset:
        if t[1] == 1 and t[0] == 'utf-8':
            restr = ['utf-8',t[2]];
            break;
        elif t[1] == 1:
            restr = [t[0],t[2]];
    return restr;

def GetPrintUTFStr(s):
    if isinstance(s,str):
        restr = ['utf-8',s];
        return restr;
    typeset = GetTestTypeCode(s)
    restr = ['utf-8',s];
    for i in range(len(typeset)):
            t = typeset[i]
            if t[1] == 1 and t[0] == 'utf-8':
                u = t[2]
                if isinstance(u,str)==False:
                    restr = ['utf-8',str(u,t[0])]
                else:
                    restr =['utf-8',u]
                break;
            elif t[1] == 1:
                u = t[2]
                if isinstance(u,str)==False:
                    restr = (t[0],str(u,t[0]))
                else:
                    restr = [t[0],u]
    return restr
def GetPrintUTFStrList(s):
    if isinstance(s,str):
        restr = ['utf-8',s];
        return [restr];
    typeset = GetTestTypeCode(s)
    restrlist = [];
    for i in range(len(typeset)):
            t = typeset[i]
            if t[1] == 1 and t[0] == 'utf-8':
                u = t[2]
                if isinstance(u,str)==False:
                    restr = ['utf-8',str(u,t[0])]
                else:
                    restr =['utf-8',u]
                restrlist.append(restr)
            elif t[1] == 1:
                u = t[2]
                if isinstance(u,str)==False:
                    restr = (t[0],str(u,t[0]))
                else:
                    restr = [t[0],u]
                restrlist.append(restr)
    return restrlist
def GetPrintUTFStrA(s):
    if isinstance(s,str):
        return s;
    typeset = GetTestTypeCode(s)
    restr = s;
    for i in range(len(typeset)):
            t = typeset[i]
            if t[1] == 1 and t[0] == 'utf-8':
                restr = t[2]
                if isinstance(restr,str)==False:
                    restr = str(restr,t[0])
    return restr

def TestTypeA():
    s = '哈哈'
    us = GetPrintUTFStr(s)
    print(us[0],us[1], isinstance(us[1],str))
    uss = GetUnicodePair(s)
    print(uss[0], uss[1], isinstance(uss[1],str))
    print(GetGBKStr(s))
    print('*****')
    s= r'雷军vs周鸿祎，20年的&quot;天地对决&quot;'
    us = GetPrintUTFStr(s)
    print(us[0],us[1], isinstance(us[1],str))
    uss = GetUnicodePair(s)
    print(uss[0], uss[1], isinstance(uss[1],str))
    gs = GetGBKStr(s)
    print(gs);
    ugs = GetUnicodePair(gs)
    print(ugs[1])
    ug = GetUnicode(gs)
    print(ug)

def _strdecode(txtstr):
     try:
         return txtstr.decode('utf8')
     except UnicodeDecodeError:
         try:
             return txtstr.decode('gb2312')
         except UnicodeDecodeError:
             try:

                 return txtstr.decode('gbk')
             except UnicodeDecodeError:
                 return txtstr.decode('gb18030')
def _strencode(txtstr):
     try:
         return txtstr.encode('utf8')
     except UnicodeEncodeError:
         try:
             return txtstr.encode('gb2312')
         except UnicodeEncodeError:
             try:
                 return txtstr.encode('gbk')
             except UnicodeEncodeError:
                 return txtstr.encode('gb18030')

def TransformToGBK(txtstr):
    gbtxt = GetPrintUTFStr(txtstr)
    return GetGBKStr(gbtxt[1])
def TestTransform():
    s = '哈哈'
    us = TransformToGBK(s)
    print(us)
 #   print us[0],us[1], isinstance(us[1],unicode)
    uss = GetUnicodePair(s)
    print((uss[0], uss[1], isinstance(uss[1],str)))
    print((GetGBKStr(s)))
    print('*****')
    s= r'雷军vs周鸿祎，20年的&quot;天地对决&quot;'
    us = GetPrintUTFStr(s)

    print(us)
    uus = makeutf(s)
    print('makeutf(s)')
    print(uus)
    hanzi=FindAllChineseCharacter(uus)
    for han in hanzi:
        print(han)
def FindAllChineseCharacter(txtstr):
    p=re.compile('(^\s+|\s+$)');
    phanzigbk=re.compile('[\\x20-\\x7f]');
    phanzi=re.compile('[\u4e00-\u9fa5]');#这里要加u
    hanzi=phanzi.findall(txtstr)
    return hanzi
def main():
    #TestTransform()
    #TestTypeA()
    #TestTransformUTF()
    Test()
    TestTransform()
if __name__ == '__main__':
    main()
