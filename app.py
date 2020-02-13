from fsevents import Observer
from fsevents import Stream
import json
import requests
import os
import time
import urllib.parse

g_dict = {}
lasttime = int(time.time())

def callback(fileevent):
    global lasttime
    if (fileevent.name.endswith('music.163.log')):
        f = open("/Users/zhoubing/Library/Containers/com.netease.163music/Data/Documents/storage/Logs/music.163.log")
        last_song = list(filter(lambda line: '_$load' in line, f.readlines()))[-1]
        timestamp = (last_song[last_song.find('[') + 1 : last_song.find(']')])
        timestamp = int(time.mktime(time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')))
        if lasttime > timestamp:
            return

        lasttime = timestamp
        j = json.loads((last_song[last_song.find('{') : last_song.find('}') + 1]))
        if (not j['playId'] in g_dict):
            g_dict[j['playId']] = j 
            print(j['songName'])
            print(j['musicurl'])
            if os.path.exists("../mp3/" + j['artistName'].replace('/', "／") + "_" +j['albumName'].replace('/', "／") + "/" + j['songName'] + ".mp3"):
                print("file already exists")
                return
            if not os.path.exists("../mp3/" + j['artistName'].replace('/', "／") + "_" +j['albumName'].replace('/', "／")):
                os.makedirs("../mp3/" + j['artistName'].replace('/', "／") + "_" +j['albumName'].replace('/', "／")) 
            res = requests.get(j['musicurl'])
            f = open("../mp3/" + j['artistName'].replace('/', "／") + "_" +j['albumName'].replace('/', "／")+ "/" + j['songName'] + ".mp3", 'wb')
            for chunk in res.iter_content(100000):
                f.write(chunk)
            
            res = requests.get(j['url'])
            f = open("../mp3/" + j['artistName'].replace('/', "／") + "_" +j['albumName'].replace('/', "／")+ "/cover.jpg", 'wb')
            for chunk in res.iter_content(100000):
                f.write(chunk)
            f.close()


if __name__ == "__main__":
    observer = Observer()
    stream = Stream(callback, 
    "/Users/zhoubing/Library/Containers/com.netease.163music/Data/Documents/storage/Logs", 
    file_events=True)
    observer.start()
    observer.schedule(stream)
