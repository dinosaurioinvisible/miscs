# import igor
import os

import igor.igorpy as igor

igor_dir = os.chdir('../igor_files')
file_ok = False
while not file_ok:
    print()
    files = os.listdir(igor_dir)
    for ei,efile in enumerate(files):
        print(ei+1,efile)
    # file_n = input('\n\nfile?: ')
    file_n = 2
    try:
        file_path = os.path.abspath(files[int(file_n)-1])
        if os.path.isfile(file_path) == True:
            file = igor.load(file_path)
            print(f'\n{file_path}\n')
            file_ok = True
    except:
        print(f'\ninvalid input\n')




