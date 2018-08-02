# -*- coding:utf-8 -*-
import requests
import os
import json
import re
import time
from proxy import *
from wordanalyse import *

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

cookies = {'appver': '2.0.2'}


def ShowList(list):
    for each in list:
        print(each)


#返回作品名称的字符串
def GetSongName(songID):
    url = 'http://music.163.com/api/song/detail/?id={}&ids=%5B{}%5D.'.format(songID,songID)
    detail = GetResponse(url,headers,cookies)
    detail_json = json.loads(detail.text)
    name = detail_json['songs'][0]['name']
    return name

#返回作品作者的字符串
def GetSongAuthor(songID):
    url = 'http://music.163.com/api/song/detail/?id={}&ids=%5B{}%5D.'.format(songID, songID)
    detail = GetResponse(url, headers, cookies)
    detail_json = json.loads(detail.text)
    artistlist = detail_json['songs'][0]['artists']
    artist = ''
    for each in artistlist:
        artist += each['name'] + ' '
    return artist.strip()


#从songID返回歌词字符串，API不稳定有可能会返回NULL
def GetLyric(songID, titledel = True, artistdel=True, timedel=True):
    songname = GetSongName(songID)
    songartist = GetSongAuthor(songID)
    title = ''
    lyric_url = 'http://music.163.com/api/song/lyric?id=' + str(songID) + '&lv=1&kv=1&tv=-1'  # 歌词的api
    lyr = GetResponse(lyric_url,headers,cookies)
    lyric = json.loads(lyr.text)['lrc']['lyric']  # 导入歌词文本
    if(not titledel):
        title = songname + '\n' + '歌手：' + GetSongAuthor(songID) + '\n'
    if (timedel):
        pattern = re.compile(r'\[\S*\]')  # 去除[]的时间标识
        lyric = re.sub(pattern, '', lyric)
    if (artistdel):
        pattern = re.compile(r'.+[:：].+')  # 去除艺术家
        lyric = re.sub(pattern, '', lyric)
    print('get lyric from songID:{} {} artist: {} successfully'.format(songID,songname,songartist))
    return title + lyric.strip()


#从albumID返回songID列表
def GetAlbumSongID(albumID):
    album_url = 'http://music.163.com/api/album/' + str(albumID)
    album = GetResponse(album_url, headers, cookies)
   # print('Response done')
    s = str(album.content, encoding='utf-8')
    album_json = json.loads(s)
    songIDlist = []
    for each in album_json['album']['songs']:
        songIDlist.append(each['id'])
    print('get songID from albumID:{} successfully'.format(albumID))
    return songIDlist


#从歌单ID返回songID列表
def GetListSongID(ListID):
    url = 'http://music.163.com/api/playlist/detail?id=' + str(ListID)
    songlist = GetResponse(url,headers,cookies)
    s = songlist.text
    list_json = json.loads(s)
    songIDlist = []
    listname = list_json['result']['name']
    for each in list_json['result']['tracks']:
        songIDlist.append(each['id'])
    print('get songID from songlistID:{} {} successfully'.format(ListID,listname))
    return songIDlist

def AddLyric(file,text):
    fpath = os.path.join(file+'.txt')
    f = open(fpath,'a', encoding="utf-8")
    f.write(text)
    f.close()