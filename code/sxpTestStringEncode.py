#-------------------------------------------------------------------------------
# Name:        sxpTestStringEncode
# Purpose:
#
# Author:      sunxp
#
# Created:     23-03-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def strdecode( string,charset=None ):
     if isinstance(string,str):
         return string
     if charset:
         try:
             return string.decode(charset)
         except UnicodeDecodeError:
             return _strdecode(string)
     else:
         return _strdecode(string)


def _strdecode(string):
     try:

         return string.decode('utf8')
     except UnicodeDecodeError:
         try:
             return string.decode('gb2312')
         except UnicodeDecodeError:
             try:

                 return string.decode('gbk')
             except UnicodeDecodeError:
                try:
                 return string.decode('gb18030')
                except:
                    try:
                        return string.decode('mbcs')
                    except:
                        return string.decode('ascii')

def strencode( string,charset=None ):
     if isinstance(string,str):
         return string
     if charset:
         try:
             return string.encode(charset)
         except UnicodeEncodeError:
             return _strencode(string)
     else:
         return _strencode(string)
def _strencode(string):

     try:
         return string.encode('utf8')
     except UnicodeEncodeError:
         try:
             return string.encode('gb2312')
         except UnicodeEncodeError:
             try:
                 return string.encode('gbk')
             except UnicodeEncodeError:
                try:
                    return string.encode('gb18030')
                except UnicodeEncodeError:
                    try:
                        return string.encode('mbcs')
                    except UnicodeEncodeError:
                        return string.encode('ascii')



def main():
    pass

if __name__ == '__main__':
    main()
