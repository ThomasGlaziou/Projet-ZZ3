
from tkinter import *
from interface import Interface

class Mark(Interface):

    def __init__(self, root, obj):

        self.root = root

        self.obj = obj
        
        self.image_dict =self.create_icon(dict(text="image/text.jpg"))



    def create_text(self):

        try :
            self.text_fen = Tk()#creating window
            self.text_fen.focus()
            self.text_fen.title('insert a text --> click on enter')
            self.text_fen.geometry('400x200')
            self.main_frame_fen = Frame(self.text_fen)
            self.main_frame_fen.place(x=0, y=0, width=400, height=400)
            self.text_widget = Text(self.main_frame_fen)
            self.text_widget.place(x=0, y=0)
            self.text_widget.bind("<Return>",lambda x: self.insert_text(self.text_widget.get('1.0', END)))
            self.text_widget.bind("<Return>", lambda x : self.text_fen.destroy(), True)
            self.text_widget.grab_set()
            self.text_widget.focus_set()
            #self.text_fen.focus_force()
            #self.text_fen.grab_set_global()
            self.text_fen.mainloop()
        except TclError:
            self.text_fen.destroy()


    def insert_text(self, text):
        """ insert text in the picture """
        
        #delete the last line break
        text = text[:-1]

        

        
        


    def display_widget(self, master, color_style_1=None, color_style_2=None, active_color=None):

        self.mark_frame= Frame(master, bg=color_style_1)
        self.mark_frame.pack(side=LEFT)

        # button to create e new image
        self.text_button= Button(self.mark_frame, image=self.image_dict['text'], command=self.create_text,
                              bg= color_style_2, activebackground=active_color, cursor="hand2",
                              bd=0, width=20, height=20)
        self.text_button.pack(side=LEFT, padx=4)

    def display_menu(self, master):
        """ display the main menu """

        # create the file menu
        mark_menu = Menu(master)
        mark_menu.add_command(label="Text", command=self.create_text)
        mark_menu.add_separator()
        mark_menu.add_command(label="Other" , command="")

        return mark_menu


    
