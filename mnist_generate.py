#/usr/bin/env python2.7
#coding:utf-8
import os
import cv2
import numpy
import sys
import struct

DEFAULT_WIDTH = 28
DEFAULT_HEIGHT = 28
DEFAULT_IMAGE_MAGIC = 2051
DEFAULT_LBAEL_MAGIC = 2049
IMAGE_BASE_OFFSET = 16
LABEL_BASE_OFFSET = 8

def usage_generate():
    print "python mnist_helper generate path_to_image_dir"
    print "\t path_to_image_dir/subdir, subdir is the label"
    print ""
    pass

def create_image_file(image_file):
    fd = open(image_file, 'w+b')
    buf = struct.pack(">IIII", DEFAULT_IMAGE_MAGIC, 0, DEFAULT_WIDTH, DEFAULT_HEIGHT)
    fd.write(buf)
    fd.close()
    pass

def create_label_file(label_file):
    fd = open(label_file, 'w+b')
    buf = struct.pack(">II", DEFAULT_LBAEL_MAGIC, 0)
    fd.write(buf)
    fd.close()
    pass

def update_file(image_file, label_file, image_list, label_list):
    ifd = open(image_file, 'r+')
    ifd.seek(0)
    image_magic, image_count, rows, cols = struct.unpack(">IIII", ifd.read(IMAGE_BASE_OFFSET))
    image_len = rows * cols
    image_offset = image_count * rows * cols + IMAGE_BASE_OFFSET
    ifd.seek(image_offset)
    for image in image_list:
        ifd.write(image.astype('uint8').reshape(image_len).tostring())
    image_count += len(image_list)
    ifd.seek(0, 0)
    buf = struct.pack(">II", image_magic, image_count)
    ifd.write(buf)
    ifd.close()

    lfd = open(label_file, 'r+')
    lfd.seek(0)
    label_magic, label_count = struct.unpack(">II", lfd.read(LABEL_BASE_OFFSET))
    buf = ''.join(label_list)
    label_offset = label_count + LABEL_BASE_OFFSET
    lfd.seek(label_offset)
    lfd.write(buf)

    lfd.seek(0)
    label_count += len(label_list)
    buf = struct.pack(">II", label_magic, label_count)
    lfd.write(buf)
    lfd.close()


def mnist_generate(image_dir):
    if not os.path.isdir(image_dir):
        raise Exception("{0} is not exists!".format(image_dir))

    image_file = os.path.join(image_dir, "user-images-ubyte")
    label_file = os.path.join(image_dir, "user-labels-ubyte")
    create_image_file(image_file)
    create_label_file(label_file)

    for i in range(10):
        path = os.path.join(image_dir, "{0}".format(i))
        if not os.path.isdir(path):
            continue
        image_list = []
        label_list = []
        for f in os.listdir(path):
            fn = os.path.join(path, f)
            image = cv2.imread(fn, 0)
            w, h = image.shape
            if w and h and (w <> 28) or (h <> 28):
                simg = cv2.resize(image, (28, 28))
                image_list.append(simg)
                label_list.append(chr(i))
        update_file(image_file, label_file, image_list, label_list)
    print "user data generate successfully"
    print "output files: \n\t {0}\n\t {1}".format(image_file, label_file)
    pass