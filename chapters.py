import os 
from mutagen.mp3 import MP3
from lxml import etree
import sys

def chapterize(path, title, parts):
    file = MP3(path+'/'+title+'-Part01.mp3')
    chapters = etree.fromstring(file['TXXX:OverDrive MediaMarkers'][0])
    if chapters:
        length = 0.0
        f = open(f"{path}/chapters.txt", "w")
        for i in range(parts):
                part = "{:02d}".format(i+1)

                file = MP3(path+'/'+title+'-Part'+part+'.mp3')
                chapters = etree.fromstring(file['TXXX:OverDrive MediaMarkers'][0])

                for chapter in chapters.getchildren():
                        name = chapter[0].text

                        time = chapter[1].text.split(":")
                        time = length+float(time[0])*60+float(time[1])

                        h = "{:02d}".format(int(time/3600))
                        m = "{:02d}".format(int((time%3600)/60))
                        s = "{:02d}".format(int(time%60))
                        ms = "{:03d}".format(int((time%1)*1000))

                        duration = h+":"+m+":"+s+"."+ms
                        f.write(duration+"    "+name+"\n")

                length += file.info.length

if __name__ == '__main__':
    try: 
        mode = sys.argv[1]
    except:
        print("chapters.py [-m Manual Mode, one directory at a time] [-a Automatic mode, all subdirectories]")
        exit()
    if mode == '-m':
        try: 
            chapter = sys.argv[2]
        except:
            print("chapters.py -m <Audiobook directory>")
            exit()
        parts = 0
        for file in os.listdir(folder):
            if os.path.splitext(file)[1] == '.mp3':
                parts += 1
                title = file.split('-')[0]
        chapterize(folder, title, parts)
    elif mode == '-a':
        for folder in os.listdir():
            if os.path.isdir(folder):
                parts = 0
                for file in os.listdir(folder):
                    if os.path.splitext(file)[1] == '.mp3':
                        parts += 1
                        title = file.split('-')[0]
                if parts > 0:
                    print('Extracting chapters from '+folder+'...')
                    try:
                        chapterize(folder, title, parts)
                    except:
                        print('Error!')
                else:
                    print('No mp3s, skipping...')