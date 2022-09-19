#小白量化汉字模块
import pandas as pd

global  pys
pys={}

def loadhzk(file='pinyin.csv'):
    global  pys
    df=pd.read_csv(file , encoding= 'utf-8')
    pys={}
    for i in range(len(df)):
        pys[df.hz[i]]=df.py[i]
    
    for i  in range(1,255):
        pys[chr(i)]=chr(i).lower()
    pys['Ａ']='a'
    pys['Ｂ']='b'
    return pys

def loadhzk2(file='pinyin.csv'):
    global  pys
    df=pd.read_csv(file , encoding= 'utf-8')
    pys={}
    for i in range(len(df)):
        pys[df.hz[i]]=str(df.py[i]).upper()
    
    for i  in range(1,255):
        pys[chr(i)]=chr(i).upper()
    i=0
    for s in 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ':
        pys[s]=chr(65+i)
        i+=1
    for s in 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ':
        pys[s]=chr(65+i)
        i+=1
    return pys

#汉字转首拼
def hz2sp(hz=''):
    global  pys
    r=''
    for i in range(len(hz)):
        r=r+pys[hz[i:i+1]][0:1]
    return r

import pypinyin
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=(pypinyin.NORMAL)):
        s += ''.join(i)
    return s

def firstpinyin(word):
    if word=='':
        return word
    s1=''
    for s in pypinyin.pinyin(word, style=(pypinyin.NORMAL)):
        s2=''.join(s)
        if s2[0] !=' ':
            s1=s1+s2[0].upper()
    return s1


#测试
if __name__ == '__main__':
    loadhzk2()
    print(hz2sp('广发证券'))


