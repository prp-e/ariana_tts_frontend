from datetime import datetime
import os
import pyaudio 
import requests
import ssl
import urllib.parse
import wave

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

class ArianaFrontend:
    def __init__(self):
        pass 

    def play_sound(self, wave_file):
        wave_file = wave.open(wave_file, 'rb')
        chunk = 1024
        player = pyaudio.PyAudio() 

        stream = player.open(
            format = player.get_format_from_width(wave_file.getsampwidth()),
            channels = wave_file.getnchannels(), 
            rate = wave_file.getframerate(),
            output = True
        )

        data = wave_file.readframes(chunk) 

        while data != b'':
            stream.write(data)
            data = wave_file.readframes(chunk)
        
        stream.close()
        player.terminate()
    
    def say(self, input_text, file_name='tts.wav', keep_file=False):
        input_text = urllib.parse.quote(input_text)
        url = f'https://api.farsireader.com/ArianaCloudService/ReadTextGET?APIKey={os.getenv("ARIANA_KEY")}&Text={input_text}&Speaker=female&Format=wav16&Quality=normal&ToneLevel=8&SpeechSpeedLevel=4'
        res = requests.get(url)
        tts = open('tts.wav', 'wb').write(res.content)
        if keep_file:
            pass
        else:
            self.play_sound('tts.wav')
            os.remove('tts.wav')

if __name__ == '__main__':
    a = ArianaFrontend()
    a.say('سلام. این یک متن آزمایشی نِسبَتَن بلند است.')