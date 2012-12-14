#from libtiff.libtiff_ctypes import * << doesn't do anything useful with attributes.
# for some reason, debug/np seem to be missing?!
from libtiff.libtiff_ctypes import TIFF, libtiff, debug, np, COMPRESSION_NONE

class TIFF3D(TIFF):
    @classmethod
    def open(cls, filename, mode='r'):
        # monkey-patch the restype:
        old_restype = libtiff.TIFFOpen.restype
        libtiff.TIFFOpen.restype = TIFF3D
        
        # actually call the library function:
        tiff = libtiff.TIFFOpen(filename, mode)
        
        # restore the old restype:
        libtiff.TIFFOpen.restype = old_restype
        if tiff.value is None:
            raise TypeError ('Failed to open file '+`filename`)
        return tiff
    
    @debug
    def read_image(self, verbose=False, as3d=True):
        """Read image from TIFF and return it as a numpy array.
           if as3d is passed True (default), will attempt to read 
           multiple directories, and restore as slices in a 3D array.
        """
        if not as3d:
            return TIFF.read_image(self, verbose)
        
        # Code is initially copy-paste from TIFF:
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
        # code borrowed from TIFF.iter_images():
        depth = 0
        while True:
            depth += 1
            if self.LastDirectory():
                break
            self.ReadDirectory()
        self.SetDirectory(0)
        
        # we proceed assuming all directories have the same properties from above.
        layer_size = width * height * itemsize
        total_size = layer_size * depth
        arr = np.zeros((depth, height, width), typ)
        
        if compression == COMPRESSION_NONE:
            ReadStrip = self.ReadRawStrip
        else:
            ReadStrip = self.ReadEncodedStrip
        
        layer = 0
        while True:
            pos = 0
            elem = None
            for strip in range (self.NumberOfStrips()):
                if elem is None:
                    elem = ReadStrip(strip, arr.ctypes.data + layer * layer_size + pos, layer_size)
                elif elem:
                    elem = ReadStrip(strip, arr.ctypes.data + layer * layer_size + pos, min(layer_size - pos, elem))
                pos += elem
            if self.LastDirectory():
                break
            self.ReadDirectory()
            layer += 1
        self.SetDirectory(0)
        return arr
