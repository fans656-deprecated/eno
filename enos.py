import os
import re

import config

def enos(path=config.enosPath, ignores=config.ignores):
    dirs = []
    files = []
    for t in os.listdir(path):
        if any((lambda r: re.match(r, t))(r) for r in ignores):
            print 'Ignore: {}'.format(t)
            continue
        abspath = os.path.join(path, t)
        if os.path.isdir(abspath):
            dirs.append(enos(abspath))
        else:
            files.append(abspath)
    return (path, dirs, files)

def show(a, depth=0):
    def indent(s, depth):
        print '    ' * depth + os.path.basename(s)

    path, dirs, files = a
    indent(path, depth)
    for di in dirs:
        show(di, depth + 1)
    for f in files:
        indent(f, depth + 1)

if __name__ == '__main__':
    enos = enos()
    show(enos)
