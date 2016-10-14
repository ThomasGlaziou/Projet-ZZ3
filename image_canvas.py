
from tkinter import Canvas, NW
from PIL import Image, ImageTk

from history import History

class MImage(object):
    def __init__(self, img=None, size=(800,500)):
        self.__img = img
        self.size = size


    def __copy__(self, obj):
        self.__img = obj.get_img()

        
    def get_img(self):
        return self.__img
        
    def set_img(self, img):
        self.__img = img

  

class ImageCanvas(Canvas):

    def __init__(self, *arg1, **arg2):

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

        Canvas.__init__(self, *arg1, **arg2)

        self.img = MImage()

        self.img_on_canvas = self.create_image(0, 0, anchor=NW, image = None)

        self.tkpi = None

        self.hist = History()    

    def undo(self):
        elem = self.hist.undo()
        if elem is not None:
            self.display(elem.get_img())


    def redo(self):
        elem = self.hist.redo()
        if elem is not None:
            self.display(elem.get_img())


    def initialize(self, size=(800, 500)):

        img = Image.new('RGB', size,'#FFFFFF')
        self.display(img, size=size)
        self.new()

    def new(self, img=None):
        if img is None:
            img = self.img
        self.hist.empty()
        self.hist.add(img)

    def display(self, img, size=(800,500)):

        self.img.set_img(img)

        img.thumbnail(size, Image.ANTIALIAS)
            
        self.tkpi = ImageTk.PhotoImage(img)

        self.configure(width=self.tkpi.width())
        self.configure(height=self.tkpi.height())

        self.itemconfig(self.img_on_canvas, image=self.tkpi)

        

    def update(self, img, size=(800,500)):
        self.display(img, size)
        self.hist.add(self.img)
        

    def save(self, filename):
        self.img.get_img().save(filename)


class ImageProcessing(object):

    def __init__(self):
        pass
    

    
