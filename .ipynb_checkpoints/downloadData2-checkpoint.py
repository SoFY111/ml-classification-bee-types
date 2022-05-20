from youtube_dl import YoutubeDL
import json
from pydub import AudioSegment
import os

YoutubeDL()._ies = [YoutubeDL().get_info_extractor('Youtube')]

def downloadAudio(link, folderName, counter):
    video_url = link
    video_info = YoutubeDL().extract_info(url = video_url,download=False)
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    'outtmpl': './data2/' + folderName + '/' + folderName + str(counter) + '.%(ext)s'
    }
    filename = './data2/' + folderName + '/' + folderName + str(counter) + ".mp3"
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_info['webpage_url']])
    print("Download complete... {}".format(filename))
    
def convertMP3toWAV(folderName, counter):
    song = AudioSegment.from_mp3('./data2/' + folderName + '/' + folderName + str(counter) + '.mp3')
    song.export('./data2/' + folderName + '/converted/' + folderName + str(counter) + '.wav', format='wav')
    print('Converted complete... {}'.format('./data2/' + folderName + '/converted/' + folderName + str(counter) + '.wav'))
    
#downloadAudio('https://www.youtube.com/watch?v=XLWI9AXERTE', 'deneme', '1')

f = open('audioData.json')
data = json.load(f)
counter = 1
for i in data:
    print(i)
    try:
        os.mkdir('./data2/' + str(i))
        os.mkdir('./data2/' + str(i) + '/converted')
        os.mkdir('./data2/' + str(i) + '/converted/splitted')
        
        print('Dizin olusturuldu: /' + str(i) + '/converted/splitted')
    except:
        print('Dizin olusturulmadi: /' + str(i) + '/converted/splitted')
    counter = 1
    for j in data[i]:
        try:
            print('\n\n ------------------------ \n')
            print(i)
            print(j['link'], str(counter))
            downloadAudio(j['link'], i, counter)
            print('\n INDIRME ISLEMI BITTI \n')
            print('CEVIRME ISLEMI BASLIYOR \n')
            convertMP3toWAV(i, counter)
            print('\n ------------------------ \n\n')
        except:
            print('HATA!!:' ,j['link'].split('=')[1], 'indirilemedi ', counter)
        counter= counter + 1 
# Closing file
f.close()