
import os 
# import pyigor     # only if you have igor installed
from igor2 import binarywave, packed
import io
import numpy as np

def load_file(fpath=None, demo=True):
    igor_dir = os.chdir('../igor_files')
    file_ok = False
    while not file_ok:
        if not fpath:
            # files in dir
            print()
            files = os.listdir(igor_dir)
            for ei,efile in enumerate(files):
                print(ei+1,efile)
            # auto load
            if demo:
                file_n = 2
            else:
                file_n = input('\n\nfile?: ')
                # to quit
                if file_n == 'q':
                    return
        try:
            # check path
            file_path = os.path.abspath(files[int(file_n)-1]) if not fpath else fpath
            # load
            if os.path.isfile(file_path) == True:
                with open(file_path, "rb") as f:
                    pxp = packed.load(f)
                print(f'\n{file_path}\n')
                file_ok = True
            else:
                print(f'\ninvalid file {file_path}\n')
                fpath = None
        except:
            # deactivate demo to avoid loop
            print(f'\ninvalid input/file, path: {file_path}\n')
            demo = False
    return pxp

# pxp is tuple of records + structure
pxp = load_file()
structure = pxp[1]
exps = {}
# look for wave data
for key,val in structure['root'].items():
    if val != 0:
        key_str = key.decode if isinstance(key, bytes) else key
        exps[key_str] = val

# ex: check wave 
wave_key,wave_obj = list(exps.items())[0]
# print(wave_obj)
# decode from bytes
# wave_file = io.BytesIO(wave_obj.data)
# wave = binarywave.load(wave_file)
# this seems to be the same that wave_obj.data, but already decoded into a dict
wave_data = wave_obj.wave
# np array
wave = wave_data['wave']['wData']



