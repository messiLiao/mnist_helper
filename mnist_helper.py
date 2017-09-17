#/usr/bin/env python2.7
#coding:utf-8
import sys
import struct

from mnist_show import usage_show, mnist_show
from mnist_merge import usage_merge, mnist_merge
from mnist_generate import usage_generate, mnist_generate
from mnist_extract import usage_extract, mnist_extract


def usage():
    print "python mnist_helper -h | --help"
    print ""
    usage_generate()
    usage_merge()
    usage_show()
    print ""
    pass

def main(argv):
    if len(argv) < 1:
        usage()
        sys.exit(2)
    cmd = argv[0]

    if cmd == 'generate':
        image_dir = argv[1]
        mnist_generate(image_dir)
        pass
    elif cmd == 'merge':
        image_file1, image_file2 = argv[1], argv[2]
        mnist_merge(image_file1, image_file2)
        pass
    elif cmd == 'show':
        image_file, image_index = argv[1], int(argv[2])
        mnist_show(image_file, image_index)
        pass
    elif cmd == 'extract':
        image_file = argv[1]
        if len(argv) > 2 and int(argv[2]) >= 0:
            image_index = int(argv[2])
        else:
            image_index = -1
        mnist_extract(image_file, image_index)
        pass
    else:
        try:
            usage()
            sys.exit(2)
        except Exception, ex:
            usage()
    pass


if __name__ == '__main__':
    main(sys.argv[1:])