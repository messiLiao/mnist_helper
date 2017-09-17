#/usr/bin/env python2.7
#coding:utf-8
import sys
import struct


def usage_merge():
    print "python mnist_helper merge image_file1 image_file2"
    print "python mnist_helper merge label_file1 label_file2"
    print ""
    pass

def mnist_merge(file1, file2):
    fd1 = open(file1, 'r')
    fd2 = open(file2, 'r')
    magic1, count1 = struct.unpack(">II", fd1.read(8))
    magic2, count2 = struct.unpack(">II", fd2.read(8))
    if magic1 not in [2049, 2051] or magic2 not in [2049, 2051]:
        raise Exception("Wrong file format!")
    if magic1 <> magic2:
        raise Exception("File format must be same!")

    magic = magic1
    count = count1 + count2

    if magic == 2051:
        rows1, cols1 = struct.unpack(">II", fd1.read(8))
        rows2, cols2 = struct.unpack(">II", fd2.read(8))
        if rows1 <> rows2 or cols1 <> cols2:
            raise Exception("Image rows and cols not same:({}, {}) != ({rows2}, {cols2})".\
                format(rows1, cols1, rows2, cols2))
        else:
            pass
    else:
        pass

    fn = './output_merge_file-ubyte'
    fd = open(fn, 'w')
    if magic == 2051:
        buf = fd.write(struct.pack(">IIII", magic, count, rows1, cols1))
        offset_base = 16
    else:
        buf = fd.write(struct.pack(">II", magic, count))
        offset_base = 8

    fd1.seek(offset_base)
    buf = fd1.read(2048)
    while len(buf) > 0:
        fd.write(buf)
        buf = fd1.read(2048)

    fd2.seek(offset_base)
    buf = fd2.read(2048)
    while len(buf) > 0:
        fd.write(buf)
        buf = fd2.read(2048)

    fd.close()
    fd1.close()
    fd2.close()

    print "file merge successfully!, output file is './output_merge_file-ubyte'"

