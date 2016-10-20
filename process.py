
from PIL import Image, ImageFilter
import numpy as np
from scipy.ndimage import imread
from scipy.ndimage.filters import generic_filter


class Process(object):
   
    def generate_watermark(self, img):
        """Generate watermark image

        Parameters
        ----------
        img : str | ndarray 
            Original image

        Returns
        ----------
        ws : ndarray
            Watermarked image
        """

        # read pixels of the image ( type : numpy.ndarray )
        pixels = imread(img)

        extra_keywords = dict()

        # the original image
        extra_keywords['original'] = pixels

        # get dimensions
        x, y, z = pixels.shape

        # stock the number of columns
        extra_keywords['sup'] = y

        # intialize the watershed image
        # It has the same dimension of the original image, but without colors
        ws = np.arange(x*y, dtype=np.float)
        ws = ws.reshape(x,y)

        # not display warnings
        with np.errstate(divide='ignore', invalid='ignore'):
            # create the overlopping blocks
            # for each block a function is called
            ws =  generic_filter(ws, function=self.__filter_fct, footprint=np.ones((3, 3)),
                                 mode='constant', cval=-1.0, origin=0.0, extra_keywords=extra_keywords)

        return ws
        

    def __filter_fct(self, x, sup, original):
        """Apply filter

        Parameters
        ----------
        x : np.ndarray
            Block of interest
        sup : int
            Number of columns of the original image
        original : array-like
            Original image

        Returns
        ---------
        w : float
            Weber differential descriptor for a specific block
        """  

        w = -1
        n = x[0]

        # if not an edge
        if (n != -1 and x[-1] != -1):

            # get indexes
            i = int(n // sup)
            j = int(n % sup)

            pix = original[i:i+3, j:j+3]

            # get center pixel
            Si = pix[1,1]

            # compute
            c = (pix-Si) / Si

            # the case of division by zero
            c[~ np.isfinite(c)] = 0

            w = np.arctan(c.sum())
        
        return w


if __name__ == '__main__':

    p = Process()
    ws = p.generate_watermark("save/test.jpg")

    print(ws[1])
        
        
        
