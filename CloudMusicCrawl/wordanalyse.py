# -*- coding:utf-8 -*-
import sys
import jieba
import jieba.analyse
import os
import re
from collections import Counter


# 获取路径下的所有txt并返回合并的字符串
def ReadTxt(filepath=None):
    txt = ''
    pathDir = os.listdir(filepath)  # 获取当前路径下的文件名，返回List
    for s in pathDir:
        if (filepath):
            newDir = os.path.join(filepath, s)  # 将文件命加入到当前文件路径后面
        else:
            newDir = os.path.join(s)
        if os.path.isfile(newDir):  # 如果是文件
            if os.path.splitext(newDir)[1] == ".txt":  # 判断是否是txt
                txt += Read_Txt(newDir)  # 读文件
    return txt


# 获取单个的txt返回字符串
def Read_Txt(txt):
    f = open(txt, encoding='utf-8')
    lines = f.readlines()
    str = ''
    for each in lines:
        str += each
   # print('read {} successfully'.format(txt))
    return str.lower()


# 将字符串写入txt
def Save_Txt(file, txt):
    fpath = os.path.join(file)
    f = open(fpath, 'w', encoding="utf-8")
    f.write(txt)


# 对指定txt进行分词，返回列表
def WordCut(file):
    tags = []
    for line in open(file, 'r', encoding='utf-8'):
        item = Standardize(line)
        tags += jieba.lcut(item)  # jieba分词
    print('wordcut successfully')
    return tags


#将分词后的列表写入txt
def SaveTags(tags,output):
    f = open(output, 'w', encoding='utf-8')
    for each in tags:
        if(each is not ','):
            f.write(str(each) + ',')
    f.close()


#将分词后的字符串去除空格、换行符和标点符号，均换成逗号
def Standardize(s):
    r = re.compile('[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\s]+')
    s = re.sub(r, ',', s)
    r = re.compile(',+')
    s = re.sub(r,',',s)
    return s

def Ignore(tag):
    ignored = Read_Txt(os.path.join('doc','ignorelist.txt')).split('\n')
    d = dict(Counter(tag))
    for each in ignored:
        if(each in d):
            d.pop(each)
    return d

#返回排序后能写入文件的字符串
def PrintMax(d,num = -1):
    txt = ''
    a = sorted(d.items(), key=lambda x: x[1], reverse=True)
    if num > len(d):
        num = len(d)
    for item in a[:num]:
        txt += item[0] + '\t' + str(item[1]) + '\n'
    return txt

def PrintMaxTag(d,num = 15):
    a = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return a[:num]


#读取源txt文本，生成分词txt后返回未排序的list
def OutputMax(filename,num = 15):
    if (filename.find('.txt') == -1):
        file = filename + '.txt'
      #  output = filename -'.txt' + 'WordCut.txt'
    else:
        file = filename
      #  output = filename + 'WordCut.txt'
    s = Read_Txt(file)
    taglist = WordCut(file)
   # SaveTags(taglist, output)
    maxcommon = Ignore(taglist)
    return maxcommon

#读取已经分好词的txt文本，返回未排序的list
def Output(filename,num = None):
    taglist = Read_Txt(filename).split(',')
    maxcommon = Ignore(taglist)
    return maxcommon
