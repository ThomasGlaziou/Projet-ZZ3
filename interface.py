
from PIL import Image, ImageTk

from abc import ABCMeta
from abc import abstractmethod

class Interface(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def display_widgets(self, master, color_style_1=None,
                        color_style_2=None, active_color=None):
        
        raise NotImplementedError

    @abstractmethod
    def display_menu(self, master):

        raise NotImplementedError

    def create_icon(self, image_dict):
        
        for key, value in image_dict.items():
            img = Image.open(value)
            image_dict[key] = ImageTk.PhotoImage(img)

        return image_dict
