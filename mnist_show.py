#/usr/bin/env python2.7
#coding:utf-8
import sys
import cv2
import struct
import numpy


def usage_show():
    print "python mnist_helper  show image_file image_index"
    print "\t display image from image_file"
    print ""
    pass

def mnist_show(image_file, image_index):
    try:        
        fd = open(image_file, 'rb')
        try:
            magic, image_count = struct.unpack(">II", fd.read(8))
            if magic not in [2049, 2051]:
                raise Exception("Wrong file format!")
            if (image_index < 0) or (image_index >= image_count):
                raise Exception("index must between 0 and {0}".format(image_count-1))


            if magic == 2051:
                rows, cols = struct.unpack(">II", fd.read(8)) 
                print "this file is image file, image count is {0}, rows={1}, cols={1}".\
                format(image_count, rows, cols)
                offset = image_index*rows*cols + 16
                fd.seek(offset)
                data = fd.read(cols*rows)
                image = numpy.fromstring(data, dtype=numpy.uint8).reshape(cols, rows)
                cv2.imshow("image", image)
                cv2.waitKey(0)
            else:
                print ""
                print "this file is label file, label count is {0}".format(image_count)
                print ""
                offset = image_index + 8
                fd.seek(offset)
                data = fd.read(1)
                print "the {0}th label is {1}".format(image_index, ord(data))
                print ""

        except Exception, ex:
            print "error:", ex.message
        fd.close()
    except Exception, err:
        print "error:", err.message
        usage_show()
    pass