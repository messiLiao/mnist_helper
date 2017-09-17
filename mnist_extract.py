#/usr/bin/env python2.7
#coding:utf-8
import os
import sys
import cv2
import struct
import numpy


def usage_extract():
    print "python mnist_helper  extract image_file [image_index]"
    print "\t extract images from image_file"
    print ""

def mnist_extract(image_file, image_index):
    try:        
        fd = open(image_file, 'rb')
        try:
            magic, image_count = struct.unpack(">II", fd.read(8))
            if magic not in [2051]:
                raise Exception("Wrong file format!")
            if image_index >= image_count:
                raise Exception("index must be between 0 and {0}".format(image_count-1))


            rows, cols = struct.unpack(">II", fd.read(8)) 
            if image_index >= 0:
                index_min = image_index
                index_max = image_index + 1
                offset = image_index*rows*cols + 16                
            else:
                index_min = 0
                index_max = image_count
                offset = 16
            print index_min, index_max, image_index, offset
            fd.seek(offset)
            for i in xrange(index_min, index_max, 1):
                data = fd.read(cols*rows)
                image = numpy.fromstring(data, dtype=numpy.uint8).reshape(cols, rows)
                fn = os.path.join("output_extract", "%05d.bmp"%i)
                cv2.imwrite(fn, image)
            print "extract {0} images successfully".format(index_max - index_min)
            print "output directory is ./output_extract/"

        except Exception, ex:
            print ex.message
        fd.close()
    except Exception, err:
        print err.message
        usage_extract()
    pass