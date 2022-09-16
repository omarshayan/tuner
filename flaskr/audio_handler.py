import numpy as np
import sounddevice as sd
import queue
import time
from . import pitch_detection

A4 = 440
notes = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#']



def closestNote(f):
    semitones = int(12 * np.log2(abs(f)/A4))
    note = notes[semitones%12]
    return str(note)

def queryInputDevices():
    #query audio devices and interfaces
    all_audio_devices = sd.query_devices()
    host_apis = sd.query_hostapis()

    #only list device if it has input channels
    all_input_devices = [ad for ad in all_audio_devices if ad['max_input_channels'] > 0]

    return host_apis, all_input_devices
    

def audioSetup(config):
    #choose driver and input device
    apis, devices = queryInputDevices()
    device = config[1]
    api = config[0]

    api_idx = 0
    for a in apis:
        if api in a:
            api_idx = apis.index(a)



    input_device = list(filter(lambda dev: dev['name'] == device
                               and dev['hostapi'] == api_idx, devices))

    #set up stream and queue for recording
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())



    #get sample rate from input device
    fs = input_device[0]['default_samplerate']

    #make stream
    dev_str = device + ", " + api
    stream = sd.InputStream(samplerate= fs,\
                            device=dev_str,\
                            channels=1,\
                            callback=callback)

    #print out driver and device to be streamed

    return q, callback, stream, fs




def start_stream(config):
    #start stream with given config
    q, callback, stream, fs = audioSetup(config)
    count = 1
    prevblock = np.array([])
    block = np.array([])

    with stream:
        while True:
            #get an audio block and yield its pitch
            block = q.get()
            f = pitch_detection.fastautoc(block, fs)
            count += 1
            prevblock = block
            yield "{}\n".format(str(round(f)) + '\t\t' + closestNote(f))
            


