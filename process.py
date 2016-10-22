
from PIL import Image, ImageFilter
import numpy as np
from scipy.ndimage import imread
from scipy.ndimage.filters import generic_filter


def to_array(elem):
    """ conversion in array """
    
    if isinstance(elem, str):
        elem = imread(elem)
    elif isinstance(elem, Image.Image):
        # width, height = elem.size
        # elem = np.array(list(elem.getdata()))
        # elem = elem.reshape(height, width, elem.shape[-1])

        elem.save('tmp/tmp.jpg')
        elem = imread('tmp/tmp.jpg')
        
    else:
        try:
            elem = np.array(elem)
        except ValueError:
            raise ValueError('elem has an incorrect type')

    return elem


def block_shaped(array, row, col):
    """Return an array divided in blocks

    Parameters
    ----------
    array : np.ndarray
        Array of interest
    row : int
        Number of rows in blocks
    col : int
        Number of cols in blocks

    Returns
    ---------
    blocks : np.ndarray(n * nrows * ncol)
    """

    l, c = array.shape

    blocks = array.copy()

    # delete pixels wich cannot go in blocks
    maxX = l%row
    if maxX != 0:
        blocks = blocks[:-maxX]
    maxY = c%col
    if maxY != 0:
        blocks = blocks[:,:-maxY]

    # reshape the array to divide it in blocks
    blocks = np.reshape(blocks, (l//row, row, -1, col))
    blocks = blocks.swapaxes(1,2)
    blocks = blocks.reshape(-1, row, col)
    
    return blocks

def generate_watermark(orig):
    """Generate watermark image

    Parameters
    ----------
    img : str | like-array
        Original image

    Returns
    ----------
    ws : ndarray
        Watermarked image
    """

    orig = to_array(orig)

    # if pixel is just one color --> that the case for grayscale
    if orig.ndim == 2:
        # add one dimension
        orig = orig[...,None]

    x, y, z = orig.shape

    # get positions of each pixel
    pos = np.arange(x*y, dtype=np.int)
    pos = pos.reshape(x,y)

    # create blocks
    blocks = block_shaped(pos, 3, 3)

    # align the blocks in the same dimension
    blocks = blocks.flatten()
    orig = orig.reshape(-1, z)

    # replace position by its color in each block 
    blocks = np.take(orig, blocks, axis=0)
    blocks = blocks.reshape(-1,3,3,z)

    center = blocks[:,1,1]

    center = center[:, None, None]

    # compute
    with np.errstate(divide='ignore', invalid='ignore'):
        ws = (blocks-center)/center

    # the case of division by zero
    ws[~ np.isfinite(ws)] = 0

    x = ws.shape[0]

    ws = ws.reshape((x,-1,z))

    ws = np.arctan(ws.sum(1))

    return ws


def embedding_process(orig, ws, alpha=0.5):
    """The watershed generation based on Weber differential
    descriptor process

    Paramaters
    ----------
    orig : str | like-array
        Original image
    ws : like-array
        Watermark image
    alpha : float
        Alpha of image

    Returns
    ----------
    iw : np.ndarray
        Watermarked image
    """

    orig = to_array(orig)
    ws = to_array(ws)

    if orig.ndim == 2:
        orig = orig[...,None]

    x, y, z = orig.shape

    # create the output
    iw = np.zeros_like(orig)

    # get center points of the original image
    orig = orig[2::3,2::3]

    # reshape in order to have the same matrix dimensions for computing
    ws = ws.reshape(x//3,y//3,z)

    # compute
    iw[2::3,2::3] = (1-alpha)*ws+alpha*orig

    # delete dimensions with one element
    iw = iw.squeeze()


    return iw

def extraction_process(iwa, w, alpha=0.5):
    """Verify the watermark

    Parameters
    ----------
    iwa : np.ndarray
        Attacked watermarked image
    w : np.ndarray
        Original watermark
    alpha : float
        Alpha of image

    Returns
    --------
    wa : np.ndarray
        Attacked watermark
    """

    iwa = to_array(iwa)
    w = to_array(w)

    if iwa.ndim == 2:
        iwa = iwa[...,None]
    
    z = iwa.shape[-1]

    # keep color of the center pixels in the same dimension
    iwa = iwa[2::3,2::3].reshape(-1,z)

    wa = np.zeros_like(w)

    # compute
    wa = (1/alpha)*w*((1-alpha)/alpha)*iwa

    # delete dimensions with one element
    wa = wa.squeeze()

    return wa



if __name__ == '__main__':


    name = "save/test.jpg"

    # RGB, L, ...
    mode = 'L'

    # we use three cases to show the impercibility
    #alpha = 0.01 / 0.5 / 0.98
    alpha = 0.98

    orig = Image.open(name)
    
    orig = orig.convert(mode)
    
    orig = to_array(orig)


    ws = generate_watermark(orig)

    iw = embedding_process(orig, ws, alpha)

    wa = extraction_process(orig, ws, alpha)

    img = orig - iw


    img1 = Image.fromarray(orig, mode)
    img2 = Image.fromarray(img, mode)

    img1.show()
    img2.show()
        
        
        
