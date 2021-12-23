import cv2
import numpy as np
import os
from ffpyplayer.player import MediaPlayer
from config import Config

_Config = Config()
VIDEO_SAVE_PATH = _Config.SavePath()['VIDEO_SAVE_PATH']

def PlayVideo(video_path):
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    i=0
    while True:
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
        #print(audio_frame)
        if audio_frame==None and i>=10:
            break
        else:
            i+=1
        if not grabbed:
            break
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

        cv2.imshow("PaddleNews", frame)
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
    video.release()
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    LAST_TIMESTAMP = 0 #上一个视频的时间戳

    while True:
        VideoList = os.listdir(VIDEO_SAVE_PATH)
        VideoPlayList = []
        for video in VideoList:
            if video.endswith(".mp4"):
                VideoPlayList.append(int(video.replace(".mp4", "")))
        VideoPlayList = np.array(VideoPlayList)
        Newest_Video = VideoPlayList.max()

        #如果有新的视频，播放最新视频；否则，循环随机播放文件夹里的视频
        if Newest_Video != LAST_TIMESTAMP:
            PlayVideo(VIDEO_SAVE_PATH + str(Newest_Video) + ".mp4")
            LAST_TIMESTAMP = Newest_Video
        else:
            Random_Video = np.random.choice(VideoPlayList,replace=False)
            PlayVideo(VIDEO_SAVE_PATH + str(Random_Video) + ".mp4")        
