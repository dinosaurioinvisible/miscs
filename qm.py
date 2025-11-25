
import os
import sys
import wave
from mido import MidiFile
import pandas as pd
from collections import defaultdict

datadir = '/Users/f/Desktop/data'

# data_dir is the directory with all the data
def indexing(data_dir=datadir):
    # simple check
    while os.path.isdir(data_dir) == False:
        print('\ninvalid directory, enter dir: (\'q\' to quit)\n')
        data_dir = input('_ ')
        if data_dir == 'q':
            return
        print()
    # individual dir names in main data directory - may be irregular(?)
    dirs = [d.name.split('_') for d in os.scandir(data_dir) if d.is_dir()]
    dirs.sort(key=lambda x: (int(x[0][1:]), int(x[2])))
    # make dict to store data
    dx = {}
    participants = list(set([x[0] for x in dirs]))
    for participant in participants:
        dx[participant] = {}
    for (participant,activity,version) in dirs:
        if activity not in dx[participant].keys():
            dx[participant][activity] = {}
        if version not in dx[participant][activity].keys():
            dx[participant][activity][version] = defaultdict(dict)  # for other/new things
    # inspect folders to get data
    for (participant,activity,version) in dirs:
        dirpath = os.path.join(data_dir,f'{participant}_{activity}_{version}')
        # wav files
        wavs = [[f.name, f.path] for f in os.scandir(dirpath) if f.name.lower().endswith('.wav')]
        for wav in wavs:
            # example: "P3_performance_1_micamp.wav"
            participant,activity,version,modality = wav[0].split('.')[0].split('_')
            # get frames & frequency
            with wave.open(wav[1],'r') as wav_file:
                print(wav[1])
                frames = wav_file.getnframes()
                duration = wav_file.getnframes() / wav_file.getframerate()
                dx[participant][activity][version][modality]['audioframes'] = frames
                dx[participant][activity][version][modality]['duration'] = duration
                wav_file.close()
        # ego/exo videoframes
        vf_dirs = [[d.name, d.path] for d in os.scandir(dirpath) if d.is_dir()]
        for vf_dir in vf_dirs:
            # example: "P3_performance_1_ego_frames_455x256"
            participant,activity,version,modality = vf_dir[0].split('.')[0].split('_')[:4]
            modality += '-vf'
            dx[participant][activity][version][modality]['frames'] = len(os.listdir(vf_dir[1]))
        # get midi data
        midi_name, midi_path = [[f.name, f.path] for f in os.scandir(dirpath) if f.name.endswith('.mid')][0]
        mid = MidiFile(midi_path, clip=True)
        # modality: 'midi'
        dx[participant][activity][version]['midi']['frames'] = len(os.listdir(vf_dir[1]))
        import pdb; pdb.set_trace()
        
        print(os.listdir(dirpath))

    
        



    
    

x = indexing(datadir)