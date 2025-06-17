# import igor
import os

# import igor.igorpy as igor
# import igor
from igor.igorpy import load as load_pxp
from igor.binarywave import load as load_ibx

def load_file(fpath=None, demo=True):
    igor_dir = os.chdir('../igor_files')
    file_ok = False
    while not file_ok:
        if not fpath:
            print()
            files = os.listdir(igor_dir)
            for ei,efile in enumerate(files):
                print(ei+1,efile)
            if demo:
                file_n = 2
            else:
                file_n = input('\n\nfile?: ')
        try:
            if not fpath:
                file_path = os.path.abspath(files[int(file_n)-1])
            else:
                file_path = fpath
            if os.path.isfile(file_path) == True:
                extension = file_path.split('.')[-1]
                if extension == 'pxp':
                    file = load_pxp(file_path)
                    print(f'\n{file_path}\n')
                    file_ok = True
                elif extension == 'ibw':
                    file = load_ibx(file_path)
                    print(f'\n{file_path}\n')
                    file_ok = True
                else:
                    print('\nnot an igor file\n')
            else:
                print(f'\nno file {file_path}\n')
                fpath = None
        except:
            print(f'\ninvalid input\n')

# python igor_demo fpath --demo on/off
if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if args:
        fpath = args[0] if '--' not in args[0] else None
    for ei in range(len(args)):
        if args[ei] == '--demo':
            if args[ei+1] == 'on':
                demo = True
            elif args[ei+1] == 'off':
                demo = False
            else:
                print('\ndemo can be on/off\n')
    load_file(fpath=fpath, demo=demo)




