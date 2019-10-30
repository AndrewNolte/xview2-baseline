

import argparse
import inspect

import os
import pathlib
from shutil import copy2
from glob import glob


def parseargs(f):
    argspec = inspect.getfullargspec(f)
    argnames = argspec[0]
    defaults = list() if argspec[3] is None else argspec[3]
    reqlen = len(argnames)-len(defaults)

    parser = argparse.ArgumentParser(description=('signature = ' + str(inspect.signature(f))))
    parser.add_argument('arglist', nargs=reqlen)
    for option, default in zip(argnames[reqlen:], defaults):
        parser.add_argument('--' + option, required=False, default=default)
    args = parser.parse_args()

    d = vars(args).copy()
    del d['arglist']
    f(*(args.arglist), **d)



def restructure(DATA_PATH, NEW_PATH):
    images = sorted(glob(DATA_PATH+'/images/*.png'))
    labels = sorted(glob(DATA_PATH+'/labels/*.json'))
    assert len(images) == len(labels)
    seen = set()

    for impath, lbpath in zip(images, labels):
        imsplit = impath.split('_')
        lbsplit = lbpath.split('_')        
        disaster = imsplit[0][impath.rindex('/')+1:]
        if disaster not in seen:
            print('copying ', disaster)
            imdir = os.path.join(NEW_PATH, disaster, 'images')
            lbdir = os.path.join(NEW_PATH, disaster, 'labels')
            
            if not os.path.isdir(os.path.join(NEW_PATH, disaster)):
                pathlib.Path(imdir).mkdir(parents=True, exist_ok=True)
                pathlib.Path(lbdir).mkdir(parents=True, exist_ok=True)
            for file in glob(imsplit[0] + '*'):
                copy2(file, imdir)
            for file in glob(lbsplit[0] + '*'):
                copy2(file, lbdir)
            seen.add(disaster)
            
    print('done')


if __name__ == '__main__':
    parseargs(restructure)