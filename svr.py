from mark import watermark, create_image, to_array, block_shaped
import numpy as np
from sklearn.svm import SVR

import os

#from numpy.random import randint
from PIL import Image





if __name__ == '__main__':

    name = "save/test.jpg"


    name = "save/"



    for file in os.listdir("learn"):
        if file.beginswith(".txt"):
            print(file)
    # name = "save/un.png"

    # RGB, L, ...
    mode = 'L'

    alpha = 0.98

    win_size = 3
    
    orig = Image.open(name)
    orig = orig.convert(mode)

    orig = to_array(orig)


    orig_w, w = watermark(orig, alpha, w=True)

    img = create_image(orig_w)

    alpha_learn = np.arange(0,1,0.1)

    alpha_learn = [0.98]

    X = []
    Y = []

    #23
    size =70

    coeff = -1

    for alpha in alpha_learn :

        dim = win_size * size
        
        #test = np.random.randint(256, size=(dim, dim))
        w_test = watermark(test, alpha, w=False)

        for t in (test, w_test):

            print(block_shaped(t, win_size, win_size)[0])
        
            X = np.append(X, block_shaped(t, win_size, win_size).flatten())
            Y = np.append(Y, np.ones(size*size) * coeff)
            coeff *= (-1)


    blocks = block_shaped(orig_w, win_size, win_size)[0]

    print(blocks)

    #X = np.append(X, blocks.flatten())
    #Y = np.append(Y, np.ones(1))
    
    X = X.reshape(-1,win_size*win_size)



    print(len(X))

    print(len(Y))


    

    svr = SVR(kernel='rbf', C=1e3, epsilon=0.2, gamma=0.2)

    fit = svr.fit(X,Y)

    x1 = np.array([2,3,6,8,9,7,3,6,5])
    x1 = x1.reshape(1,-1)

    orig_w = block_shaped(orig_w, win_size, win_size).flatten()
    orig_w = orig_w.reshape(-1,win_size*win_size)

    y = svr.predict([blocks.flatten()])

    print(y)

    
