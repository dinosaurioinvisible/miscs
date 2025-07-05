import qrcode
import sys
import os

def make_qr(url=None,name=None):
    # check
    if not url:
        url = input('\nurl? ')
    # make
    qr = qrcode.make(url)
    # approx name
    if not name:
        fname = ''
        fname += fname.join(url.split('.')[1:])+'_qr.png'
    else:
        fname = name+'_qr.png'
    # try to save to desktop
    desktop = '/Users/f/Desktop'
    if os.path.isdir(desktop):
        qr.save(os.path.join(desktop,fname))
    else:
        print(f'\nsaved to {os.getcwd()}\n')
        qr.save(fname)

if __name__ == '__main__':
    args = sys.argv[1:]
    url = args[0] if args else None
    name = args[1] if len(args) == 2 else None
    make_qr(url,name)
