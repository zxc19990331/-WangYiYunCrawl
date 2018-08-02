# -*- coding:utf-8 -*-
from mani import *

def generator():
    while True:
        print('当前代理地址为：',Read_Txt(proxypath))
        user_input = input('请输入想要进行的操作:\n1 - 爬取网易云音乐歌词并进行分词统计\n2 - 仅爬取网易云音乐歌词\n3 - 仅对txt文本进行分词统计\n')
        if user_input:
            if(user_input == '1'):
                Crawl()
            if(user_input == '2'):
                Crawl(False)
            if(user_input == '3'):
                path = input('请输入文本的相对路径(如：dir/a.txt)')
                if(os.path.exists(path)):
                    print('已找到文件 {} ,开始词频统计')
                    Cut(path)



def Crawl(docut = True):
    path = ''
    user_input = input('请输入文件保存的相对路径(如：firstdir/secdir)并确保为空，不填则在根目录下：\n')
    if user_input:
        if (isAddress(user_input)):
            path = os.path.join(user_input)
        else:
            print('文件路径不合法，请重新输入')
    else:
        path = os.path.join('')
    print('保存地址为：.../', path)
    makedir(path)
    location = input('请输入要爬的歌词所在的位置：1 - 歌单 2 - 专辑 3 - 歌曲  :\n')
    if (location):
        if (location == '1'):
            ID = input('请输入歌单ID:\n')
            songIDlist = GetListSongID(ID)
        elif (location == '2'):
            ID = input('请输入专辑ID:\n')
            songIDlist = GetAlbumSongID(ID)
        elif (location == '3'):
            ID = input('请输入歌曲ID:\n')
            songIDlist = [ID]
        else:
            return
    else:
        return

    choose = input('请输入保存歌词是否删除标题、歌手（1/0 默认1不包含） 是否删除编曲、填词人信息（1/0 默认1删除）是否删除歌曲时间格式（1/0 默认1删除）\n')
    if (choose):
        one = int(choose[0])
        two = int(choose[1])
        three = int(choose[2])
    else:
        one = 1
        two = 1
        three = 1
    for each in songIDlist:
        txt = GetLyric(each, one, two, three)
        name = str(each) + '_' + GetSongName(each) + '.txt'
        Save(path + '/' + name, txt)
    total = ReadTxt(path)
    name = 'Total_{}_songs_lyrics_'.format(len(songIDlist))+GetTime() + '.txt'
    Save(path + '/' + name,total)
    print('总歌词保存成功:{}'.format(path + '/' +name))
    if(docut):
        Cut(path + '/' + name)


def Cut(file):
    print('注：词频统计使用了部分停词表（如你、我、他、了、着、的 等），可在 doc/ignorelist.txt自行修改')
    tags = WordCut(file)
    wordcut = OutputMax(file)
    Max = PrintMax(wordcut)
    MaxTagEx = PrintMaxTag(wordcut)
    newname = GetTime() + '_result.txt'
    Save(newname,Max)
    print('词频统计保存成功：.../{}'.format(newname))
    print('前15个高频词示例：\n',MaxTagEx)


def isAddress(p):
    pa = re.compile(r'(([a-zA-Z0-9_]+.[a-zA-Z0-9_]{1,16}))+(/([a-zA-Z0-9_]+.[a-zA-Z0-9_]{1,16}))*')
    a = re.search(pa,p)
    if a:
        return True
    else:
        return False

def Save(path, txt):
    f = open(path, 'w', encoding='utf-8')
    f.write(txt)
    f.close()


def makedir(path):
    if (not os.path.exists(path)):
        os.makedirs(path)


def GetTime():
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())