#/usr/bin/env python2.7
#coding:utf-8
import gzip
import os
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets
read_data_sets("./MNIST_data", one_hot=True)
print "download successfully!"
file_list = ['t10k-images-idx3-ubyte.gz', 't10k-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz', 'train-labels-idx1-ubyte.gz']
for fn in file_list:
    basename, _ = os.path.splitext(fn)
    fullname = os.path.join('./MNIST_data', fn)
    gz_file = gzip.GzipFile(fullname)
    ungz_filename = os.path.join('./MNIST_data', basename)
    open(ungz_filename, "w+").write(gz_file.read())
    gz_file.close()

print "ungz successfully!"
