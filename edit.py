# -*- coding: utf-8 -*-



# -*- coding: utf-8 -*-


from tkinter import *
from tkinter.messagebox import showerror

from PIL import Image, ImageTk

import os

from interface import Interface



class Edit(Interface):
    
    def __init__(self, root, obj):
        """ initialize """

        self.filename = None

        # initialize the path to save picture
        self.filepath=os.getcwd()+'/save'

        self.root = root

        # object of the interest
        self.obj = obj
        

        self.image_dict = self.create_icon(dict(undo="image/undo.jpg", redo="image/redo.jpg"))
        

    def display_menu(self, master):
        """ display the main menu """

        # create the file menu
        edit_menu = Menu(master)
        edit_menu.add_command(label="Undo", command=self.obj.undo)
        edit_menu.add_command(label="Redo", command=self.obj.redo)
        edit_menu.add_separator()

        return edit_menu


    def display_widget(self, master, color_style_1=None, color_style_2=None, active_color=None):
        """ display the file widgets """

        self.edit_frame= Frame(master, bg=color_style_1)
        self.edit_frame.pack(side=LEFT)

        # button to create e new image
        self.undo_button= Button(self.edit_frame, image=self.image_dict['undo'], command=self.obj.undo,
                                  bg= color_style_2, activebackground=active_color, cursor="hand2",
                                  bd=0, width=20, height=20)
        self.undo_button.pack(side=LEFT, padx=4)

        # button to open new image
        self.redo_button= Button(self.edit_frame, image=self.image_dict['redo'], command=self.obj.redo,
                                  bg=color_style_2, activebackground=active_color, cursor="hand2",
                                  bd=0, width=20, height=20)
        self.redo_button.pack(side=LEFT, padx=4)

        

if __name__ == '__main__':
    pass
