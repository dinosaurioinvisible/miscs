
import os
import sys
from pypdf import PdfWriter
from PIL import Image 
from pathlib import Path

pdfs = []

def check_n_input(n,optx=False):
    ok = False
    while not ok:
        x = input('\n_ ')
        if x == 'q':
            return x
        if optx:
            if x == 'x':
                return x
        try:
            x = int(x)
            if x <= n:
                return x
            print(f'\nno option {n}\n')
        except:
            print('\ninvalid input\n')

def search_desktop():
    cwd = os.getcwd()
    desktop_path_ok = False
    while not desktop_path_ok:
        if cwd.split('/')[-1] == 'Desktop':
            return cwd
        # go up
        else:
            cwd = os.path.abspath(os.path.join(cwd,'..'))
            if 'Desktop' in os.listdir(cwd):
                cwd = os.path.join(cwd,'Desktop')
                return cwd            
        # avoid inf loop going to far up (until /users/f)
        if len(cwd.split('/')) < 3:
            cwd = '/Users/'+os.listdir('/Users')[-1]+'/Desktop'
            if os.path.isdir(cwd):
                return cwd
            else:
                return

def select_dir(cwd):
    with os.scandir(cwd) as entries:
        dirs = [[e.name, e.path] for e in entries if e.is_dir()]
    print(f'\ndirs in {cwd}\n')
    for i,d in enumerate(dirs):
        print(f'{i+1} - {d[0]}')
    print('0 - to move up one dir')
    x = check_n_input(n=len(dirs),optx=True)
    if x == 0:
        cwd = os.path.abspath(os.path.join('/Users/f/Desktop','..'))
    else:
        cwd = dirs[x-1][1]
    return cwd

def select_pdf_dir(auto=False):
    pdfs_dir_ok = False
    cwd_ok = False
    while not pdfs_dir_ok:
        # menu 1 - move to working dir
        while not cwd_ok:
            print('\nmove to?\n')
            print('1 - Desktop')
            print(f'2 - cwd ({os.getcwd()})')
            print('3 - f')
            print('0 - manual input')
            print('q - quit')
            if auto:
                x = 1
            else:
                x = check_n_input(n=3)
            if x == 'q':
                return x
            if x == 1:
                cwd = search_desktop()
            elif x == 2:
                cwd = os.getcwd()
            elif x == 3:
                cwd = '/Users/f'
            elif x == 0:
                cwd = input('\n_ ')
            if not os.path.isdir(cwd):
                print(f'\ndidn\'t find {cwd}, moved to {os.getcwd()}\n')
                cwd = os.getcwd()
                print('1 - OK')
                print('0 - try again')
                xx = check_n_input(1)
                if xx == 1:
                    cwd_ok = True
            else:
                cwd_ok = True
        # menu 2 - inside working dir
        print(f'\ncurrent dir: {cwd}\n')
        print('1 - merge pdfs in current dir')
        print('2 - show entries in current dir')
        print('0 - select dir')
        print('q - quit')
        if auto:
            x2 = 0 
        else:
            x2 = check_n_input(2)
        if x2 == 'q':
            return x2
        if x2 == 0:
            cwd = select_dir(cwd)
        if x2 == 1:
            return cwd
        if x2 == 2:
            print()
            for entry in os.listdir(cwd):
                print(entry)
    
def ims_to_pdfs(ims_path):
    with os.scandir(ims_path) as entries:
        for e in entries:
            if '.jpg' in e.name.lower() or '.jpeg' in e.name.lower() or 'png' in e.name.lower():
                print(f'\nimg {e.name} to pdf')
                try:
                    imx = Image.open(e.path)
                    imx_name = e.name.split('.')[0]+'.pdf'
                    imx.save(os.path.join(ims_path,imx_name), 'pdf', resolution=100.0, save_all=True)
                    try_pdf = False
                except:
                    print(f'couldn\'t open {e.name} as image, check as .pdf')
                    try_pdf = True
                if try_pdf:
                    with open(e.path,'rb') as f:
                        header = f.read(5)
                        print(f'header: {header}')
                        if 'pdf' in str(header).lower():
                            print(f'{e.name} to pdf')
                            file = Path(e.path)
                            fname = e.path.split('.')[0]
                            file.rename(f'{fname}.pdf')
        
    
def merge_pdfs(auto=False):
    # get paths
    pdfs_path = select_pdf_dir(auto=auto)
    if pdfs_path == 'q':
        print('\n\n')
        return
    # search images files
    ims_to_pdfs(pdfs_path)
    # search pds files
    with os.scandir(pdfs_path) as entries:
        pdfs = []
        print()
        # check pdfs
        for e in entries:
            if '.pdf' in e.name.lower():
                pdfs.append([e.name,e.path])
                print(f'added {e.name}')
        pdfs = sorted(pdfs, key = lambda x:x[0])
    # just in case (it happened once)
    if len(pdfs) == 0:
        print('\nno valid image or pdf files')
        return
    # merge
    print()
    merger = PdfWriter()
    for i,(pdf_name,pdf_path) in enumerate(pdfs):
        print(f'{i+1} - {pdf_name}')
        merger.append(pdf_path)        
    print()
    try:
        desktop_path = search_desktop()
        os.chdir(desktop_path)
    except:
        print(f'\ncouldn\'t move to desktop, saving to {os.getcwd()}\n')
    filename = 'merged.pdf'
    if os.path.isfile(filename):
        from time import time as now
        filename = f'merged_{now()}.pdf'
    merger.write(filename)
    merger.close()
    print(f'\nsaved to {os.getcwd()}\n')


if __name__ == "__main__":
    args_auto = False
    if len(sys.argv) > 1:
        if 'auto' in sys.argv[1]:
            args_auto = True
            print('\nauto -> desktop = True\n')
    if not args_auto:
        print('\nauto -> desktop = False\n')
    merge_pdfs(auto=args_auto)

