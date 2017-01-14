
from PIL import Image, ImageFilter
import numpy as np
from scipy.ndimage import imread
from scipy.ndimage.filters import generic_filter
from textwrap import dedent


from sympy import *


import os
import sys

import pymzn

import subprocess

from subprocess import call

def to_array(elem):
    """ conversion in array """
    
    if isinstance(elem, str):
        elem = imread(elem).astype(np.float)
    elif isinstance(elem, Image.Image):
        # width, height = elem.size
        # elem = np.array(list(elem.getdata()))
        # elem = elem.reshape(height, width, elem.shape[-1])

        elem = np.array(elem).copy()

        #elem.save('tmp/tmp.jpg')
        #elem = imread('tmp/tmp.jpg').astype(np.float)
        
    else:
        try:
            elem = np.array(elem).copy()
        except ValueError:
            raise ValueError('elem has an incorrect type')

    elem = elem.astype(np.float)

    return elem

def create_image(elem, modif=True):
    elem = np.where(elem<0, 0, elem)

    if modif :
        elem = np.round(elem.copy()).astype(np.uint8)

    img = Image.fromarray(elem)
    
    return img

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

    blocks = blocks.astype(np.float)

    center = blocks[:,1,1]

    # print(center)

    center = center[:, None, None]

    
    
    # compute
    with np.errstate(divide='ignore', invalid='ignore'):
        ws = (blocks-center)/center
        

##    print(blocks[0])
##    print(center[0])
##
##    print((blocks[0]-center[0]))
##    print(((blocks-center)/center)[0])

    

    # the case of division by zero
    ws[~ np.isfinite(ws)] = 0

    x = ws.shape[0]

    ws = ws.reshape((x,-1,z))

    ws = np.arctan(ws.sum(1))


    #ws = ws.flatten()


    return ws


def embedding_process(orig, ws, alpha):
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
    iw = np.zeros_like(orig).astype(np.float)

    # get center points of the original image
    orig = orig[1:-1:3,1:-1:3]

    # reshape in order to have the same matrix dimensions for computing
    ws = ws.reshape(x//3,y//3,z)
    
    # compute
    iw[1:-1:3,1:-1:3] = (1-alpha)*ws+alpha*orig

    # delete dimensions with one element
    #iw = iw.squeeze()

    return iw

def extraction_process(iwa, w, alpha):
    """Extraction

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
    iwa = iwa[1:-1:3,1:-1:3].reshape(-1,z)


    # compute
    wa = np.round((1/alpha)*iwa-((1-alpha)/alpha)*w, decimals=13)


    # delete dimensions with one element
    #wa = wa.squeeze()

    return wa


def watermark(orig, alpha, w=False):

    """ Generate watermark and compute it

    Parameters
    ----------
    orig : str | like-array
        Original image
    alpha : float
        Alpha of image

    Returns
    --------
    output : ndarray | ( watermark )
        Watermarked image
    """

    # np.uint8
    orig = to_array(orig)

    ws = generate_watermark(orig)

    iw = embedding_process(orig, ws, alpha).squeeze()

    img = orig.copy()

    img[1:-1:3,1:-1:3] = iw[1:-1:3,1:-1:3]

    
    if w:
        output = [img, ws]
    else:
        output = img

    return output


def MSE(i, iw):
    
    i = to_array(i)
    iw = to_array(iw)

    N, M = iw.shape[0], iw.shape[1]   

    
    s = (i - iw)

    mse = s*s

    mse = np.sum(mse)/ (M*N)

    if (i.ndim==3):
        mse/=i.shape[-1]


    return mse

def PSNR(i , iw):

    i = to_array(i)
    iw = to_array(iw)

    if i.ndim == 2:
        P = 8
    else :
        P = 8 * i.shape[-1]
    

    mse = MSE(i, iw)
    psnr = 10 * np.log((2**P - 1)**2/mse)

    return psnr

def verif(iwa, w, alpha, get=False):
    # to array : convert 
    iwa = to_array(iwa)

    # Algo3 : detection of any modifications
    wa = extraction_process(iwa, w, alpha)

    # x,y coordonates of the attacked image
    x = iwa.shape[0]
    y = iwa.shape[1]

    # Transform the value list into an appopriate matrix
    wa = wa.reshape(x//3, y//3, -1)

    # If no 3th dimension (grey) -> adding of a dimension
    if iwa.ndim == 2:
        iwa = iwa[...,None]

    # Replace
    iwa[1:-1:3,1:-1:3] = wa

    ws = generate_watermark(iwa)

    #diff = np.abs(np.round(w-ws, decimals=23)

    diff = np.abs(w-ws)

    print(diff[0])
    
    modif = False
    if np.any(diff!=0):
        modif = True

    print('error : %s'%str(int(diff[diff>0].shape[0]/ws.shape[-1])))

    if get:
        

        img = np.zeros_like(iwa)
        
        diff = diff.reshape(x//3, y//3, -1)

        z = iwa.shape[-1]

        diff = np.where(diff>0, np.ones(z)*255, np.zeros(z))
        
        img[1:-1:3,1:-1:3] = diff

        img = img.squeeze()
        
        img = create_image(img)

        struct = np.ones((3,3))

        shape = struct.shape

        struct = struct.flatten()


        kernel_f = ImageFilter.Kernel(shape,
                                      struct,
                                      scale=1/(shape[0]))

        img = img.filter(kernel_f)

        output=[modif, img]
    else:
        output = modif

    return output



def mzn(iwa, win, pos, val):
    
    # read the mzn file
    data = open("test.mzn", "r").read()

    sol = None

    win = win.reshape(-1).tolist()

    print(win)

    #win_c = np.delete(win, 4)

    #win =[128,128,128,128,128,128,128,128,128]


    #win = [94, 96, 96, 95, 93, 96, 95, 95, 96]

    #win = [8, 16, 8, 8, 2, 8, 32, 16, 64]


    size = len(win)

    data1 = "s = "+str(win)+";"
    data1 += "\npos = "+str(pos)+";"
    data1 += "\nval = "+str(val)+";"
    data1 += "\nsize = "+str(size)+";"


    data1_name = 'WatermarkNonOverlapping.dzn'

    with open(data1_name, 'w') as f:
        f.write(data1)

    os.environ["PATH"]+= ";C:\Program Files\MiniZinc IDE (bundled)\;"

    msg_unsat ="unsatisfiable"
    

    file = "WatermarkNonOverlapping.mzn"

    arg = "mzn-gecode --no-output-comments --unsat-msg "+msg_unsat + " " + file

    # mzn-gecode WatermarkNonOverlapping_2.mzn WatermarkNonOverlapping.dzn


    #arg = "mzn-gecode test.mzn"

    proc = subprocess.Popen(arg, shell=True, bufsize=1,
                            universal_newlines=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    print("sortie")
    
    print(out)

    # delete spaces
    #out = out.strip()

    print(err)

    if out != msg_unsat:
        
        sol = out.split("\n")[0] # get the first line

        # indices
        lb = sol.index("[")
        ub = sol.index("]")

        # get the solution
        sol = eval(sol[lb:ub+1])

        sol = np.array(sol, dtype = np.float)

        # print(sol)

        sol = win+sol

        sol = sol.reshape(3,3)

        # print(sol)


        # print(tab)

        #sol = np.sum((sol-sol[4])/sol[4])

    else:
        print("impossible")

    return sol



def attack(image,  w, x, y, val, size=3):


    image = image.copy()
    
    posx = x - x % size
    posy = y - y % size

    print("pos")
    print(posx)
    print(posy)
    
    win = image[posx:posx+size, posy:posy+size]

    pos =  size * (x % size) + y % size

    print(win)

    print(pos)

    print(val)


    win = mzn(image, win, pos, val)

    print(image[0:4,0:4])
    image[posx:posx+size, posy:posy+size] = win
    print(image[0:4,0:4])

    return image


def get_alpha(I, size=3):

    blocks = block_shaped(I, size, size)
    x_blocks = blocks.reshape(-1, size*size)

    x_blocks = x_blocks[x_blocks[:,(size*size)//2]!=0]

    # print(x_blocks[x_blocks[:,(size*size)//2]==0])



    #delete doublons
    b = np.ascontiguousarray(x_blocks).view(np.dtype((np.void, x_blocks.dtype.itemsize * x_blocks.shape[1])))
    _, idx = np.unique(b, return_index=True)



    length_c = 20
    X = x_blocks[idx][:length_c]

    #print(X)

    X = X.reshape(-1, size, size)

    c = 0

    find = False

    x = symbols('x')

    ind = 0

    y = X[ind,1,1]
    w = X[ind].copy()

    print(w)

    X = np.delete(X, ind, axis=0)[:length_c].reshape(-1,3)
    

    # print(X)


    while not find and c < 256:

        #print(generate_watermark(X[0])[0,0])

        # print('test')

        w_search = w.copy()
        w_search[1,1] = c

        # print(c)
        w_search = generate_watermark(w_search)[0,0]

        # print(w_search)

        # print('find')
        

        if c - w_search != 0:

            alpha = np.round((y - w_search)/(c - w_search), 15)

            # print(alpha)

            #alpha = 0.98

            # print(alpha)

            # for i in range(1,len(X)):

                # calcul de w
                # ...
                #o = extraction_process(X[i], w, alpha)[0,0]
                #o = np.round(o, decimals=20)


                # b = np.delete(X[i].flatten(),(size*size-1)/2)
                
                

                #o = solve((1 - alpha) * atan((np.sum(b)-(size*size-1)*x)/x) + alpha*x - X[i,size//2,size//2], x)


            orig = np.zeros(len(X)//3)


            t_X = X.copy()

            res = 0

            for l in range(256):


                t_X[1:-1:3,1] = l
                o = watermark(t_X, alpha)

                res += np.sum(o[1:-1:3,1] == X[1:-1:3,1])

                # print(o)


                orig = np.where(o[1:-1:3,1] == X[1:-1:3,1], l, orig)
            

            #print(X)

                    
            #print(o)

            #print(orig)

            #print(stop)

            if res == length_c - 1:
                find = True


        

            if alpha>0.2 and alpha < 0.3:

                print('extraction')
                # print(np.round(extraction_process(X[i], w, alpha)[0,0], decimals=1))
                print(alpha)
                print(orig)
                pass

        c+=1

    print(orig)


    return alpha



def delete_watermark(iw, alpha):

    
    
    iw = to_array(iw)

    width, height = iw.shape[:2]

    nb_block = (width//3)*(height//3)

    T = np.zeros(nb_block)

    iw_copy = iw.copy()

    block_iw = block_shaped(iw_copy, 3, 3)

    A = np.ones((width//3, height//3))

    for x in range(256):
        
        iw_copy[1:-1:3,1:-1:3] = A*x
        w = watermark(iw_copy, alpha, False)

        block_w = block_shaped(w, 3, 3)

        # print(block_iw.shape)

        # print(block_w.shape)


        c = np.all(np.all(block_iw == block_w, axis=1), axis=1)
        

        T = np.where(c, x, T)

    iw_copy[1:-1:3,1:-1:3] = T.reshape(width//3, height//3)

    print(iw_copy[1:-1:3,1:-1:3])

    return iw_copy


    

    

    



class Mark(object):

    def __init__(self, img, alpha=0.98):
        self.__img = img
        self.__watermark = None
        self.__key = None
        self.__active = False
        
    def watermark(self):
        self.__watermark, self.__key = watermark(self.__img, self.__alpha, True)
        img = create_image(self.__watermark, True)
        return img

    def set_active(val):
        self.__acive = bool(val)  

    def get_img(self):
        return create_image(self.__img)

    def set_alpha(self, alpha):
        self.__alpha = alpha
        
    def get_alpha(self):
        return self.__alpha


if __name__ == '__main__':



    name = "save/test.jpg"

    # name = "save/un.png"

    # RGB, L, ...
    mode = 'L'
    
    orig = Image.open(name)

    try :
        orig = orig.convert(mode)
    except:
        pass

    orig2 = orig.copy()

    # we use three cases to show the impercibility
    #alpha = 0.01 / 0.5 / 0.98
    alpha = 0.98

    orig = to_array(orig)
    

    print(orig[:-1:3,1:-1:3])


    orig_w, w = watermark(orig, alpha, w=True)

    alpha = get_alpha(orig_w)

    print(alpha)

    #delete_watermark(orig_w, alpha)
    


    

    #print(stop)

    img = create_image(orig_w)

    # psnr = PSNR(orig2, orig)

    # img.show()
    
    img.save("save/test256.tiff")



    #iwa = Image.open("save/test_alpha_0.5.png")

    iwa = Image.open("save/test256.tiff")
    # iwa.show()

    #iwa = Image.open("save/test5.png")

    iwa = iwa.convert(mode)

    # iwa = to_array(iwa)


    iwa = to_array(orig_w) 

    # iwa[2,4]=(5,3,6)  

    # iwa[4,42]=(2,56,83)

    
    # iwa = attack(orig,w, 1, 2, 95)

    # iwa = attack(orig, 4, 46, 23)

    # Test suppression WM

    modif, img = verif(iwa, w, alpha, get=True)

    print(modif)

    #img.show()

    

    

    

    
        
