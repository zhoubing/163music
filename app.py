from fsevents import Observer
from fsevents import Stream
import json

gdict = {}

def callback(fileevent):
    if (fileevent.name.endswith('music.163.log')):
        f = open("/Users/zhoubing/Library/Containers/com.netease.163music/Data/Documents/storage/Logs/music.163.log")
        last_song = list(filter(lambda line: '_$load' in line, f.readlines()))[-1]
        j = json.loads((last_song[last_song.find('{') : last_song.find('}') + 1]))
        if (not j['playId'] in gdict):
            gdict[j['playId']] = j 
            print(j['songName'])
            print(j['musicurl'])

if __name__ == "__main__":
    observer = Observer()
    stream = Stream(callback, 
    "/Users/zhoubing/Library/Containers/com.netease.163music/Data/Documents/storage/Logs", 
    file_events=True)
    observer.start()
    observer.schedule(stream)
