from pytube import YouTube
import argparse
import re
import os
import platform
import sys

def getFolder(args):
    if args.path:
        # 有指定下載路徑
        if not os.path.isdir(args.path):
            print('{} 不是資料夾路徑'.format(args.path))
            sys.exit(2)
        return args.path
    else:
        if not os.path.isdir("Downloads_PyTube"): # 若沒有資料夾，則建立資料夾
            os.mkdir("Downloads_PyTube")
        return "Downloads_PyTube"


def show(yt):

    for i,e in enumerate(yt.streams.all()):
        print(i, ':', e)


    return 0

def findMaxResolutionFromAudio(audio_list):
    target = None
    pattern = re.compile(r'.*abr="(\d+)kbps"')
    audio_abr_dict = {}

    for audio in audio_list:
        # print(str(audio))
        abr_str = pattern.search(str(audio))
        if abr_str:
            # print(abr_str.group(1))
            audio_abr_dict[int(abr_str.group(1))] = audio
    return max(audio_abr_dict.items(), key=lambda x:x[0]) # return tuple
        

def onProgress(stream, chunk, file_handle, bytes_remaining):
    """
    https://python-pytube.readthedocs.io/en/latest/api.html
    """
    total = stream.filesize
    percent = (total - bytes_remaining) / total * 100
    print('downloading... {:05.2f}%'.format(percent), end='\r')

def get_video_res(yt):
    resolution_set = set()

    video_list = yt.streams.filter(type="video").all()
    for video in video_list:
        # print('res:', video.resolution)
        resolution_set.add(video.resolution)
    # print('available resolution:', resolution_set) # {'144p', '360p', '240p', '480p'}

    return sorted(resolution_set, key=lambda s:int(s[:-1]))

def download_video(yt, args):
    target = None
    res_dict = {
        'sd':'480p',
        'hd':'720p',
        'fhd':'1080p',
    }

    if args.sd:
        target = yt.streams.filter(file_extension="mp4", res=res_dict['sd']).all()
    elif args.hd:
        target = yt.streams.filter(file_extension="mp4", res=res_dict['hd']).first()
    elif args.fhd:
        target = yt.streams.filter(file_extension="mp4", res=res_dict['fhd']).first()
    elif args.a:
        target = yt.streams.filter(only_audio=True, file_extension='webm').all()
        target = findMaxResolutionFromAudio(target)[1]
    
    if not all( [args.sd, args.hd, args.fhd, args.a] ):
        # 使用者沒有指定想要下載的類型，預設下載影片，並請使用者輸入想要的解析度
        print('Please enter the video resolution, the available video as follows:')
        video_res_list = get_video_res(yt)
        # print(video_res_list)
        for i, res in enumerate(video_res_list):
            print('[{}]: {}'.format(i, res))
        input_res = input("> ")
        input_res = int(input_res)

        try:
            res = video_res_list[input_res]
        except:
            res = video_res_list[-1] # 使用者輸入錯誤，直接選擇最大的
        target = yt.streams.filter(type="video", res=res).first()

    if args.d: # show title and all info
        show(yt)
        print('target:', target)

    # 開始下載
    target.download(output_path=getFolder(args))

    return 0

def main():

    # 處理 cmd 介面
    parser = argparse.ArgumentParser() # 建立 argument parser 物件
    parser.add_argument('url', help="指定Youtube視訊網址")
    parser.add_argument('-sd', action="store_true", help="480p")
    parser.add_argument('-hd', action="store_true", help="720p")
    parser.add_argument('-fhd', action="store_true", help="1080p")
    parser.add_argument('-a', action="store_true", help="僅下載聲音")
    parser.add_argument('-p', '--path', action="store", help="指定下載路徑")
    parser.add_argument('-d', action="store_true", help="enter debug mode")

    args = parser.parse_args()

    print("download from {}".format(args.url))

    # 建立 YouTube 物件
    try:
        video_yt = YouTube(args.url, on_progress_callback=onProgress)
        # 下載影片函式
        download_video(video_yt, args)
    except Exception as e:
        print(f'下載影片時發生錯誤: {e}')

    return 0


if __name__=='__main__':
    main()
