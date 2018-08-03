# -*- coding:utf-8 -*-
from CloudMusicCrawl.mani import *


def generator():
    while True:
        print('当前代理地址为：', Read_Txt(proxypath))
        user_input = input('请输入想要进行的操作:\n1 - 爬取网易云音乐歌词并进行分词统计\n'
                           '2 - 仅爬取网易云音乐歌词\n3 - 仅对txt文本进行分词统计\n')
        if user_input:
            if (user_input == '1'):
                Crawl()
            if (user_input == '2'):
                Crawl(False)
            if (user_input == '3'):
                path = input('请输入文本的相对路径(如：dir/a.txt)')
                if (os.path.exists(path)):
                    print('已找到文件 {} ,开始词频统计')
                    Cut(path)


def Crawl(docut=True):
    path = ''
    user_input = input('请输入文件保存的相对路径(如：firstdir/secdir)，存放的文件夹会自动生成，不填则默认创建test文件夹：\n')
    if user_input:
        if (isAddress(user_input)):
            path = os.path.join(user_input)
        else:
            print('文件路径不合法，请重新输入')
            return
    else:
        path = os.path.join('test')

    location = input('请输入要爬的歌词所在的位置：1 - 歌单 2 - 专辑 3 - 歌曲 4 - 歌手:\n')

    if (location):
        if (location == '1'):
            IDs = input('请输入歌单ID，可一次性输入多个，用空格隔开:\n') #输入多个ID
            IDlist = IDs.split()
            for index,ID in enumerate(IDlist):
                songIDlist = GetListSongID(ID)
                Name = 'playlist_{}_{}'.format(ID,GetListName(ID))
                GetInfo(songIDlist, path, Name, docut)
                print('已完成歌单{}/{}'.format(index + 1, len(IDlist)))
        elif (location == '2'):
            IDs = input('请输入专辑ID，可一次性输入多个，用空格隔开:\n')
            IDlist = IDs.split()
            for index, ID in enumerate(IDs.split()):
                songIDlist = GetAlbumSongID(ID)
                Name = 'album_{}_{}'.format(ID,GetAlbumName(ID))
                GetInfo(songIDlist, path, Name, docut)
                print('已完成专辑{}/{}'.format(index + 1, len(IDlist)))
        elif (location == '3'):
            IDs = input('请输入歌曲ID，可一次性输入多个，用空格隔开:\n')
            songIDlist = IDs.split()
            for index, ID in enumerate(songIDlist):
                Name = 'song_{}_{}'.format(ID, GetSongName(ID))
                GetInfo(songIDlist, path, Name, docut)
                print('已完成专辑任务{}/{}'.format(index + 1, len(songIDlist)))
        elif (location == '4'):
            IDs = input('请输入歌手ID，可一次性输入多个，用空格隔开:\n')
            IDlist = IDs.split()
            for index, ID in enumerate(IDs.split()):
                songIDlist = []
                Albumlist = GetSingerAlbumID(ID)
                Name = 'singer_{}_{}'.format(ID,GetSingerName(ID))
                length = len(Albumlist)
                for _index, each in enumerate(Albumlist):
                    songIDlist.extend(GetAlbumSongID(each, ''))
                    print(' 已完成{}/{}'.format(_index + 1, length))
                GetInfo(songIDlist, path, Name, docut)
                print('已完成歌手{}/{}'.format(index + 1, len(IDlist)))
        else:
            return
    else:
        return


def GetInfo(songIDlist, path, Name,docut):
    Name = validateTitle(Name)
    path += '/' + Name
    makedir(path)
    print('保存地址为：.../', path)
    time.sleep(1)
    '''
    choose = input('请输入保存歌词是否删除标题、歌手（1/0 默认1删除）是否删除编曲、填词人信息（1/0 默认1删除）是否删除歌曲时间格式（1/0 默认1删除）\n')
    if (choose):
        try:
            one = int(choose[0])
            two = int(choose[1])
            three = int(choose[2])
        except:
            one = 1
            two = 1
            three = 1
    else:
        one = 1
        two = 1
        three = 1
    '''
    length = len(songIDlist)
    for index, each in enumerate(songIDlist):
        try:
            txt = GetLyric(each, 1, 1, 1, '')  # 使输出信息不换行
            print(' 已完成 {}/{}'.format(index + 1, length))
            if txt != '':
                name = GetSongName(each) + '.txt'
                Save(path + '/' + name, txt)
        except Exception as e:
            print(e)
            pass

    total = ReadTxt(path)
    name = 'Total_{}_songs_lyrics_'.format(length) + GetTime() + '.txt'
    Save(path + '/' + name, total)
    print('总歌词保存成功:{}'.format(path + '/' + name))
    if (docut):
        Cut(path + '/' + name, Name)


def Cut(file, name = ''):
    print('注：词频统计使用了部分停词表（如你、我、他、了、着、的 等），可在 doc/ignorelist.txt自行修改')
    tags = WordCut(file)
    wordcut = OutputMax(file)
    Max = PrintMax(wordcut)
    MaxTagEx = PrintMaxTag(wordcut)
    makedir('results')
    newname = 'results/' + GetTime() + '_{}_result.txt'.format(name)
    Save(newname, Max)
    print('词频统计保存成功：.../{}'.format(newname))
    print('前15个高频词示例：\n', MaxTagEx)


def isAddress(p):
    pa = re.compile(r'(([a-zA-Z0-9_]+.[a-zA-Z0-9_]{1,16}))+(/([a-zA-Z0-9_]+.[a-zA-Z0-9_]{1,16}))*')
    a = re.search(pa, p)
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