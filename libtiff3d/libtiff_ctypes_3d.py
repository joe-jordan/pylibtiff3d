import libtiff, numpy
from libtiff.libtiff_ctypes import debug

class TIFF3D(libtiff.TIFF):
    @classmethod
    def open(cls, filename, mode='r'):
        tiff = libtiff.TIFFOpen(filename, mode)
        if tiff.value is None:
            raise TypeError ('Failed to open file '+`filename`)
        return cls(tiff.value)
    
    @debug
    def read_image(self, verbose=False, as3d=False):
        """Read image from TIFF and return it as a numpy array.
           if as3d is passed True, will attempt to read multiple
           directories, and restore as slices in a 3D array.
        """
        if not as3d:
            return libtiff.TIFF.read_image(self, verbose)
        
        # Code is initially copy-paste from pylibtiff:
        width = self.GetField('ImageWidth')
        height = self.GetField('ImageLength')
        bits = self.GetField('BitsPerSample')
        sample_format = self.GetField('SampleFormat')
        compression = self.GetField('Compression')
        
        typ = self.get_numpy_type(bits, sample_format)
        
        if typ is None:
            if bits==1:
                typ = np.uint8
                itemsize = 1
            elif bits==4:
                typ = np.uint32
                itemsize = 4
            else:
                raise NotImplementedError (`bits`)
        else:
            itemsize = bits/8
        
        
        # in order to allocate the numpy array, we must count the directories:
        # code borrowed from libtiff.TIFF.iter_images():
        depth = 0
        while not self.LastDirectory():
            depth += 1
            self.ReadDirectory()
        self.SetDirectory(0)
        
        # we proceed assuming all directories have the same properties from above.
        layer_size = width * height * itemsize
        total_size = layer_size * depth
        arr = np.zeros((layers, height, width), typ)
        
        if compression==COMPRESSION_NONE:
            ReadStrip = self.ReadRawStrip
        else:
            ReadStrip = self.ReadEncodedStrip
        
        layer = 0
        first = True
        while first or not self.LastDirectory():
            first = False
            pos = 0
            elem = None
            for strip in range (self.NumberOfStrips()):
                if elem is None:
                    elem = ReadStrip(strip, arr.ctypes.data + layer * layer_size + pos, size)
                elif elem:
                    elem = ReadStrip(strip, arr.ctypes.data + layer * layer_size + pos, min(size - pos, elem))
                pos += elem
            self.ReadDirectory()
            layer += 1
        self.SetDirectory(0)
        return arr
            
