
from tkinter import Label
from PIL import Image, ImageTk

from history import History

class MImage(object):
    def __init__(self, img):
        self.__img = img

    def __copy__(self, obj):
        self.__img = obj.get_img()
        
    def get_img(self):
        return self.__img
        
    def set_img(self, img):
        self.__img = img

        

class ImageLabel(Label):

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

        
        Label.__init__(self, *arg1, **arg2)

        img = arg2.get('image', None)

        self.img = MImage(img)

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


    def initialize(self, L=800, H=500):

        img = Image.new('RGB',(L,H),'#FFFFFF')
        self.display(img, size=(L, H))
        self.new()

    def new(self, img=None):
        if img is None:
            img = self.img
        self.hist.empty()
        self.hist.add(img)

    def display(self, img, size=(800,800)):
        self.img.set_img(img)
        img.thumbnail(size, Image.ANTIALIAS)
        self.tkpi = ImageTk.PhotoImage(img)
        self.configure(image=self.tkpi)

    def update(self, img, size=(800,800)):
        self.display(img, size)
        self.hist.add(self.img)

    def save(self, filename):
        self.img.get_img().save(filename)

    
