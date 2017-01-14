
from tkinter import Canvas, NW
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from decimal import Decimal
import math

from history import History

class MImage(object):
    def __init__(self, img=None, size=(800,500)):
        self.__img = img
        self.size = size
        self.mode = 'RGB'


    def __copy__(self, obj):
        self.__img = obj.get_img()

    def get_img(self):
        return self.__img
        
    def set_img(self, img):
        self.__img = img.copy()
            

class CanvasSelection(object):
    
    def __init__(self, canvas):

        self.canvas = canvas
        self.move = False
        self.select = False

        self.__rectangle = None

        self.__x = None
        self.__y = None
        self.__width = None
        self.__height = None

        self.orig = None

        self.first_move = True

        self.tkpi = None
        self.box = None

        self.id = 0


    def start_event(self):
        self.canvas.bind('<Button-1>', self.press)
        self.canvas.bind('<B1-Motion>', self.motion)
        self.canvas.bind('<ButtonRelease-1>', self.release)

    def end_event(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.delete()

    def delete(self):
        if self.__rectangle is not None:
            [self.canvas.delete(rect) for rect in self.__rectangle]
            self.__rectangle = None

    def press(self, event):
        x, y = self.canvas.get_offset(event.x, event.y)
        init = True
    
        if self.__rectangle is not None:
            if x > self.__x[0] and x < self.__y[0]\
               and y > self.__x[1] and y < self.__y[1]:
                if self.move:
                    self.coords = np.array([x, y])
                else:
                    self.select = False
                    self.move = True
                init = False
        if init:
            if self.move:
                if self.box is not None:

                    if self.id == self.canvas.id:

                        x = tuple(self.coord_from_img(self.__x))
                        
                        self.canvas.get_img().paste(self.orig, x)

                        self.tkpi = self.canvas.update()
                        
                        self.canvas.delete(self.box)
                        self.canvas.delete(self.create_empty)
                        self.box = None
                        self.create_empty = None
                self.first_move = True
            
            self.move = False
            self.select = True
            self.initialize(event)
            
    def initialize(self, event):
        self.delete()
        self.__x = self.canvas.get_offset(event.x, event.y)
        self.__y = None

    def release(self, event=None):
        if self.select and self.__y is not None:
            
            x1, x2 = self.__x
            y1, y2 = self.__y
            self.__x = [min(x1, y1), min(x2, y2)]
            self.__y = [max(x1, y1), max(x2, y2)]
            self.__width = self.__y[0] - self.__x[0]
            self.__height = self.__y[1] - self.__x[1]
        if self.move:
            self.select_update()
            
    def motion(self, event):
        if self.select:
            self.draw(event)
        elif self.move:

            x, y = self.canvas.get_offset(event.x, event.y)

            coords = np.array([x, y])
            if self.first_move:

                xi, yi = self.coord_from_img(self.__x, self.__y)
                box_coords = xi + yi
                cour_coords = [self.__x[0], self.__x[1]] + [self.__y[0]+1,self.__y[1]+1]
                orig_coords = [xi[0], xi[1]] + [yi[0]+1, yi[1]+1]

                winx, winy = self.canvas.size_win()
                
                self.orig = self.canvas.get_img().crop(orig_coords).copy()

                self.create_empty = self.canvas.create_rectangle(self.__x, self.__y, fill='white', outline='white')
                
                x1, x2 = self.__x

##                print(self.orig.width)
##                print(self.orig.height)
##                print(self.orig.width/self.canvas.get_coeff())
##                print(self.orig.height/self.canvas.get_coeff())
##                print(self.__width)
##                print(self.__height)

                # self.canvas.display()

                box = self.canvas.get_img().copy()
                box.thumbnail(self.canvas.size_win())
                box = box.crop(cour_coords)

                self.tkpi = ImageTk.PhotoImage(box)
                
                self.box = self.canvas.create_image(x1, x2, anchor=NW, image = self.tkpi)

                draw = ImageDraw.Draw(self.canvas.get_img())

                draw.rectangle(box_coords, fill='white', outline='white')

                self.first_move = False

                self.id = self.canvas.id
                

            else:
                diff = coords - self.coords
                
                self.__x = (np.array(self.__x) + diff).tolist()
                x1, x2 = self.__x

                self.__y = [x1 +self.__width, x2 + self.__height]
                self.canvas.coords(self.box, x1, x2)
                self.delete()
                
            self.coords = coords.copy()

            
        
    def draw(self, event=None):
        size = np.array(self.canvas.size_win())-1
        X, Y = list(map(int, size))

        x, y = self.canvas.get_offset(event.x, event.y)
        if not (x<0 or x>X or y<0 or y>Y):
            self.__y = [x, y]
            
        else:
            xi, yi = x, y
            if x<0:
                xi = 0
            elif x>X:
                xi = X
            if y<0:
                yi = 0
            elif y>Y:
                yi = Y
            self.__y = [xi, yi]
        self.select_update()

    def select_update(self):
        points = self.__x + self.__y
        param = [dict(outline='white', dash=None), dict(outline='black', dash=(4,2))]
        if self.__rectangle is None:
            self.__rectangle = [self.canvas.create_rectangle(*points, **kw) for kw in param]
                                    
        else:
            [self.canvas.coords(rect, *points) for rect in self.__rectangle]
        

    def get_pos(self):
        return self.__base, self.__cour

    def coord_from_img(self, x, y=None):
        coeff = self.canvas.get_coeff()
        width = round(self.__width * coeff)
        height = round(self.__height * coeff)
        x = np.round(np.array(x) * coeff).astype(np.int).tolist()
        output = x

        if y is not None:
            y = [x[0] + width , x[1] + height]
            output = [x, y]
        
        return output


  

class ImageCanvas(Canvas):

    def __init__(self, *args, **kw):

        """
        Initialize the object

        Parameters
        ----------
        arg1 : list
        arg2 : dict

        Returns
        ----------
        None
        ----------

        """     

        Canvas.__init__(self, *args, **kw)

        self.img = MImage()

        # self.img_on_canvas = self.create_image(0, 0, anchor=NW, image = None)

        self.tkpi = None

        self.__size = None

        self.__win_coords=[]

        self.hist = History()

        self.__zoom = False

        self.__offset = [0,0]

        self.id = 0

    def undo(self):
        elem = self.hist.undo()
        if elem is not None:
            self.display(elem.get_img())


    def redo(self):
        elem = self.hist.redo()
        if elem is not None:
            self.display(elem.get_img())


    def initialize(self):

        img = Image.open('save/test_dim.jpg')
        self.new(img)
        self.display(img)

    def new(self, img=None):
        if img is None:
            img = self.img
        self.hist.empty()
        self.hist.add(img)
        self.__set_size([img.width, img.height])


    def display(self, img=None):

        if img is None:
            img = self.get_img()
        
        self.img.set_img(img)

        print(self.__size)
        img.thumbnail(self.__size)

        self.id += 1

        self.__size = img.width, img.height

        self.delete('all')
            
        self.tkpi = ImageTk.PhotoImage(img, Image.LINEAR)

        self.create_image(0, 0, anchor=NW, image = self.tkpi)

        

    def __set_size(self, size):

        self.__size = size
        width = min(self.__size[0], self.winfo_screenwidth()-100)
        height = min(self.__size[1], self.winfo_screenheight()-200)
        self.config(width=width, height=height)
        self.configure(scrollregion=(0,0,self.__size[0],self.__size[1]))
        


    def update(self, img=None):
        if img is None:
            img = self.get_img()
        self.display(img)
        self.hist.add(self.img)

    def save(self, filename):
        self.img.get_img().save(filename)

    def size_win(self):
        return self.__size

    def size_img(self, coord):

        s = [self.img.get_img().width(), self.img.get_img().height()]
        return s

    def get_img(self):
        img = self.img.get_img()
        return img

    def get_coeff(self):
        coeff = self.img.get_img().width/self.__size[0]
        return coeff

    def set_Xscroll(self, pos, x, y):
        self.xview(x, y)
        self.__offset[0] = round(pos[0] * self.__size[0])

    def set_Yscroll(self, pos, x, y):
        self.yview(x,y)
        self.__offset[1] = round(pos[0] * self.__size[1])

    def get_offset(self, x, y=None):
        x = x + self.__offset[0]
        if y is not None:
            y = y + self.__offset[1]
            output = [x, y]
        else:
            output = x

        return output

    def set_zoom(self, offset=None, pct=None):
        x, y = self.__size
        if offset is None or pct is None:
            if offset is not None:
                x+=offset
                y+=offset
            elif pct is not None:
                x*=pct
                y*=pct

        if x*y < 8e7:
            self.__set_size([x,y])
            self.display()
            


class ImageProcessing(object):

    def __init__(self, image_canvas):
        self.image_canvas = image_canvas
        self.selection = None

    def set_selection(self, active):
        if active:
            if self.selection is None:
                pass
        pass
    

    
