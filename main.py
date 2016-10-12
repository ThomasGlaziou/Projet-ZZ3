# -*- coding: utf-8 -*-


from tkinter import *
from tkinter.messagebox import showerror

from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw

from math import *
from random import randrange as rr
import os
import time

from history import History
from image_label import ImageLabel
from file import File
from edit import Edit
from mark import Mark



class WaterMark(Tk):
    
    def __init__(self):
        """ initialize """

        # define the root
        self.root = Tk()

        self.fen= Frame(self.root)
        self.fen.pack(side=TOP, fill=BOTH, expand=YES)

        # colors for widgets
        self.color_style_1 = '#1630A3'
        self.color_style_2 = 'white'
        self.active_color ='#0070F9'

        # font style
        # self.fontLegende ='Arial 10 bold'

        self.img = None

        # initialize the picures dict used in widgets
        self.image_dict= None


        # pictures's name
        self.filename = None

        # size of the window
        self.L=self.fen.winfo_screenwidth()
        self.H=self.fen.winfo_screenheight()

        self.display()

        # loop
        self.root.mainloop()




    def display_menu(self):
        """ display the main menu """

        main_menu = Menu(self.root)

        # create the file menu
        file_menu = self.file.display_menu(main_menu)

        # create the edition
        edit_menu = self.edit.display_menu(main_menu)

        # create the mark menu
        mark_menu = self.mark.display_menu(main_menu)

        # create the help menu
        help_menu = Menu(main_menu)
        help_menu.add_command(label="Help" , command="")
        help_menu.add_separator()
        help_menu.add_command(label="About" , command="")

        # pack menus on the main menu
        main_menu.add_cascade(label = "File", menu=file_menu)
        main_menu.add_cascade(label = "Edit", menu=edit_menu)
        main_menu.add_cascade(label = "Mark", menu=mark_menu)
        main_menu.add_cascade(label = "Help", menu=help_menu)

        

        # display the main menu
        self.root.config(menu=main_menu)



    def display_widget(self):
        """create widgets"""

        self.image_dict = dict(new="new.jpg", open="open.jpg", save="save_1.jpg", save_2="save_2.jpg")
        
        for key, value in self.image_dict.items():
            img = Image.open("image/"+value)
            self.image_dict[key] = ImageTk.PhotoImage(img)
        
        self.option_frame=Frame(self.fen, bg= self.color_style_1, relief="raised", bd=4,
                               padx=4, pady=5)
        self.option_frame.pack(side=TOP, fill=BOTH)
        
        self.tab_frame=Frame(self.fen, bg= self.color_style_1, relief="raised", bd=4,
                               padx=4, pady=5)
        self.tab_frame.pack(side=TOP, fill=BOTH)
        
        
        #===================================================IMAGE==========================================================

        self.picture_frame= Frame(self.fen, bg='grey')
        self.picture_frame.pack(side=TOP, fill= BOTH , expand=YES)

        self.edge_image= Frame(self.picture_frame, bg='#A39F9F', padx=2, pady=2)
        self.edge_image.pack(side=TOP, padx=2, pady=2)

        self.image_label = ImageLabel(self.edge_image, cursor='pencil', bd=0)
        self.image_label.pack(side=TOP)

        self.image_label.initialize()

        #=====================================================================================================================
        

        self.file = File(self.root, self.image_label)
        self.file.display_widget(self.option_frame, self.color_style_1, self.color_style_2, self.active_color)

        self.edit = Edit(self.root, self.image_label)
        self.edit.display_widget(self.option_frame, self.color_style_1, self.color_style_2, self.active_color)

        self.mark = Mark(self.root, self.image_label)
        self.mark.display_widget(self.option_frame, self.color_style_1, self.color_style_2, self.active_color)


    def display(self):
        
        # display graphic elements
        self.display_widget()
        self.display_menu()



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    WaterMark()

    
# ========================================================================
