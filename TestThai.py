#!/usr/bin/env python
# -- coding: utf-8 --

def arrUnicode(myArr):
    #uniStr = [unicode(i, encoding='UTF-8') if isinstance(i, basestring) else i for i in myArr]
    uniStr = [str(i, encoding='UTF-8') if isinstance(i, str) else i for i in myArr]
    s = repr(uniStr).decode('unicode_escape').encode('utf-8')
    if s.startswith("[u'"):
        s2 = s.replace("u'", "'")
    elif s.startswith('[u"'):
        s2 = s.replace('u"', '"')
    else:
        return s
    return s2

myArr = ['นี่', 'ไทย', 'นะ']
#print arrUnicode(myArr=myArr)
arrUnicode(myArr=myArr)