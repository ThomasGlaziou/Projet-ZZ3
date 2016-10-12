# -*- coding: utf-8 -*-


from tkinter import *
from tkinter.messagebox import showerror

from PIL import Image, ImageTk

import os

from interface import Interface



class File(Interface):
    
    def __init__(self, root, obj):
        """ initialize """

        self.filename = None

        # initialize the path to save picture
        self.filepath=os.getcwd()+'/save'

        self.root = root

        # object of the interest
        self.obj = obj

        self.image_dict = self.create_icon(dict(new="image/new.jpg", open="image/open.jpg",
                                           save="image/save_1.jpg", save_2="image/save_2.jpg"))


    def search_file(self):
        """ Open a window to select a picture """

        err = False
        filename = filedialog.askopenfilename(title="Open a picture", initialdir=self.filepath,\
                                              filetypes=[('JPEG','*.jpg;*.jpeg;*.jpe;*.jfif'),('all files','.*')])


        # if user has not selected file
        if filename :
            try:
                img=Image.open(filename)
                self.obj.update(img)

            except:
                err = True
                showerror("Error", "The file cannot be open")

        return err, filename
        
        
    def open_file(self):
        """ Open a window to select a picture """
        
        err, filename= self.search_file()
        if not err:
            self.filepath = os.path.split(filename)[0]
            self.filename = filename

        self.obj.new()
            


    def paste_from(self):
        self.search_file()
                

    def save_as_file(self):
        """ save the picture in gaving its name """
        
        filename = filedialog.asksaveasfilename(filetypes=[('all files','.*')],initialdir=self.filepath, title="Save")
        filepath = None
        
        if filename:
            try:
                self.obj.save(filename)
                
                #store the file's path  
                self.filepath = os.path.split(filename)[0]
                self.filename = filename

            except:
                showerror("Error", "Name or extension of the filename is wrong")



    def save_file(self):
        """ save the picture """

        # if the picture is not saved yet
        if self.filename is None:
            self.save_as_file()
        else:
            self.obj.save(self.filename)

    def new(self):
        self.obj.initialize()
        self.filename = None


    def display_menu(self, master):
        """ display the main menu """

        # create the file menu
        file_menu = Menu(master)
        file_menu.add_command(label="New", command=self.new)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save" , command=self.save_file)
        file_menu.add_command(label="Save as" , command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Paste From .." , command=self.paste_from)
        file_menu.add_separator()
        file_menu.add_command(label="Quit" , command=self.root.destroy)

        return file_menu

    def display_widget(self, master, color_style_1=None, color_style_2=None, active_color=None):
        """ display the file widgets """

        self.file_frame= Frame(master, bg=color_style_1)
        self.file_frame.pack(side=LEFT)

        # button to create e new image
        self.new_button= Button(self.file_frame, image=self.image_dict['new'], command=self.new,
                                  bg= color_style_2, activebackground=active_color, cursor="hand2",
                                  bd=0, width=20, height=20)
        self.new_button.pack(side=LEFT, padx=4)

        # button to open new image
        self.open_button= Button(self.file_frame, image=self.image_dict['open'], command=self.open_file,
                                  bg=color_style_2, activebackground=active_color, cursor="hand2",
                                  bd=0, width=20, height=20)
        self.open_button.pack(side=LEFT, padx=4)

        # button to save the image
        self.save_button= Button(self.file_frame, image=self.image_dict['save'], command=self.save_file, bg=color_style_2,
                                  activebackground=active_color, cursor="hand2", bd=0)
        self.save_button.pack(side=LEFT, padx=4)

        

if __name__ == '__main__':
    pass
