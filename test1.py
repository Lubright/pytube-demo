"""
Reference:
1. Jimmy's Code: https://tech.r567tw.tw/pytube-%E7%B0%A1%E5%96%AE%E6%95%99%E5%AD%B8/
2. 超圖解 Python 程式設計入門
"""
from pytube import YouTube

url = r"https://www.youtube.com/watch?v=zoSqVpFoB7o&list=RDzoSqVpFoB7o&start_radio=1"
print("download from {}".format(url))

# 建立 YouTube 物件
video = YouTube(url)

# print(dir(video))

# 顯示影片的 title， pytube==9.5.2 須修正不能顯示 title 的 bug
# https://github.com/nficano/pytube/commit/54bef712036ab0d3afc865211af4a690d0a2155c
print("Video title: {}".format(video.title))

# 查看視訊的全部檔案格式
print('video format: {}'.format(video.streams.all())