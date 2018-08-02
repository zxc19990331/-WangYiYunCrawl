# WangYiCloudMusicCrawl
通过网易云API获取专辑/歌单下的歌曲信息，顺便附带了分词词频统计

请输入想要进行的操作:
1 - 爬取网易云音乐歌词并进行分词统计
2 - 仅爬取网易云音乐歌词
3 - 仅对txt文本进行分词统计
 
代理 Ip 用的是 proxypool
require ：
requests 爬取网易云API,感谢大佬整理的API
jieba 分词统计
json 
 
目前可以通过专辑、歌单、歌曲、歌手的ID爬取所有的歌词信息，并进行分词词频统计
