pylibtiff3d
===========

a small extension to pylibtiff to enable the automatic parsing of 3D (multi-layered) TIFF files.

##Installation Prerequisites

libtiff: http://www.libtiff.org/

    curl http://dl.maptools.org/dl/libtiff/tiff-3.8.2.tar.gz > tiff-3.8.2.tar.gz
    tar -xzf tiff-3.8.2.tar.gz
    cd tiff-3.8.2
    ./configure && make
    sudo make install

pylibtiff: http://code.google.com/p/pylibtiff/

    svn checkout http://pylibtiff.googlecode.com/svn/trunk/ pylibtiff-read-only
    cd pylibtiff-read-only
    python setup.py build
    sudo python setup.py install

## Thanks to:
stackoverflow user abarnert for [this answer](http://stackoverflow.com/questions/13866706/subclassing-ctypes-pointers-how-does-this-code-work-and-how-do-i-override-it/13866964#13866964), which actually makes this library work.


