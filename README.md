pylibtiff3d
===========

a small extension to pylibtiff to enable the automatic parsing of 3D (multi-layered) TIFF files.

## About

`pylibtiff` is a great little ctypes wrapper for Sam Leffler/Silicon Graphics' open source `libtiff`, allowing you to trivially create a TIFF file from a numpy array:

    import libtiff, numpy
    t = libtiff.TIFF.open('myoutput.tiff', 'w') # (t is an instance of the libtiff.TIFF class)
    t.write(numpy.zeros((40, 200)))
    t.close()

(this will give you a black TIFF file 40px by 200px)

Additionally, it handles 3D numpy arrays out of the box:

    t.write(numpy.zeros((40, 200, 200)))

which are saved, as TIFF convention dictates, as 40 200x200 images.

However, if you read that same file back in with `pylibtiff`:

    import libtiff
    t = libtiff.TIFF.open('myoutput.tiff')
    arr = t.read_image()
    t.close()
    arr.shape # (200, 200)

This is reasonable behaviour, since you might not have meant to open someone else's multi-image tiff as one big 3D file, but quite counter-intuitive if you've just used the library to create a 3D tiff!

This is where `pylibtiff3d` comes in. It provides a single derived class - `TIFF3D` - which will open multi-image TIFF files as 3D numpy arrays by default:

    import libtiff3d
    t = libtiff3d.TIFF3D.open('myoutput.tiff') # (t is now an instance of pylibtiff3d.TIFF3D)
    arr = t.read_image()
    t.close()
    arr.shape # (40, 200, 200)

This may well crash if you have tiff files with different colour settings, bits-per-sample settings, and others - it assumes all images in the directory are configured identically (which they are, if you created them with `pylibtiff` from a 3D numpy array!)

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

##Installation of pylibtiff3d:

    git clone https://github.com/joe-jordan/pylibtiff3d.git
    cd pylibtiff3d
    python setup.py build
    sudo python setup.py install

## Thanks to:
stackoverflow user abarnert for [this answer](http://stackoverflow.com/questions/13866706/subclassing-ctypes-pointers-how-does-this-code-work-and-how-do-i-override-it/13866964#13866964), which actually makes this library work.


