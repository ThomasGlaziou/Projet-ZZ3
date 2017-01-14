
from tkinter import *
from interface import Interface
from image_canvas import CanvasSelection
class Attack(Interface):

    def __init__(self, root, obj):

        self.root = root

        self.obj = obj
        
        self.image_dict =self.create_icon(dict(text='image/text.jpg',
                                               selection='image/selection.jpg',
                                               selection_active='image/selection_active.jpg',
                                               zoom_up = 'image/zoom_up.jpg',
                                               zoom_down = 'image/zoom_down.jpg',
                                               watermarking="image/watermarking.jpg"))

        self.selection = None

        self.select_active = True

    def create_selection(self, widget):
        if self.select_active:
            self.selection = CanvasSelection(self.obj)
            self.selection.start_event()
            widget['image'] = self.image_dict['selection_active']
            self.select_active = False
            
        else:
            if self.selection is not None:
                self.selection.end_event()
            widget['image'] = self.image_dict['selection']
            self.select_active = True

    def create_text(self):

        try :
            self.text_fen = self.create_fen() #creating window
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
            self.destroy_fen()


    def insert_text(self, text):
        """ insert text in the picture """
        
        #delete the last line break
        text = text[:-1]

##            self.frame_w.place(x=0, y=0)
##            self.label_w = Label(self.frame_w, text='alpha')
##            self.label_w.pack(x=20, y=10)
##            self.text_w = Text(self.frame_w)
##            self.text_w.place(x=100, y=10)

    def parameters_watermark(self):
        try :
            self.fen_w = self.create_fen()
            self.fen_w.title('Give parameters for watermarking')
            #self.fen_w.geometry('200x200')
            self.frame_w = Frame(self.fen_w, bg='white')
            self.frame_w.pack(side=TOP)
            self.label_w = Label(self.frame_w, text='alpha', width=10 , height=5, bg='white')
            self.label_w.grid(row=0, column=0)
            self.entry_w = Text(self.frame_w, width=8 , height=1)
            self.entry_w.grid(row=0, column=1)
            self.entry_w.bind("<Return>", lambda x : self.valid())
            self.entry_w.grab_set()
            self.entry_w.focus_set()
            self.btn_valid = Button(self.frame_w, text='Valid', cursor="hand2", bg='white',
                                    command= self.valid, width=6)
            self.btn_valid.grid(row=1, column=2, padx=(6,6), pady=(4,4))
        except TclError:
            self.destroy_fen()

    def valid(self):
        text = self.entry_w.get('1.0', END)
        text = text[:-1]
        self.apply_watermark(text)
        self.destroy_fen()
                                    

    def apply_watermark(self, alpha):
        
        if alpha == '':
            alpha = 0.98
        
            alpha = float(alpha)

            self.obj.mark.set_alpha(alpha)
            img = self.obj.mark.watermark()
            self.obj.update(img)

            self.frame_w_position.pack(side=RIGHT, expand=NO, fill=Y)
            

    def quit_watermark_mode(self):
        self.frame_w_position.pack_forget()
        self.obj.display(self.mark.get_img())
        
        

    def display_widget(self, master, image_frame, color_style_1=None, color_style_2=None, active_color=None):

        self.attack_frame= Frame(master, bg=color_style_1)
        self.attack_frame.pack(side=LEFT)

        self.text_button= Button(self.attack_frame, image=self.image_dict['text'], command=self.create_text,
                                 bg=color_style_2, activebackground=active_color, cursor="hand2",
                                 bd=0, width=20, height=20)
        self.text_button.pack(side=LEFT, padx=4)

        self.selection_button= Button(self.attack_frame, image=self.image_dict['selection'],
                                 bg=color_style_2, activebackground=active_color, cursor="hand2",
                                 bd=0, width=20, height=20)
        self.selection_button['command'] = lambda : self.create_selection(self.selection_button)

        self.selection_button.pack(side=LEFT, padx=4)

        self.zoom_up_button= Button(self.attack_frame, image=self.image_dict['zoom_up'], command= lambda : self.obj.set_zoom(1.1),
                                 bg=color_style_2, activebackground=active_color, cursor="hand2",
                                 bd=0, width=20, height=20)
        
        self.zoom_up_button.pack(side=LEFT, padx=4)

        self.zoom_down_button= Button(self.attack_frame, image=self.image_dict['zoom_down'], command= lambda: self.obj.set_zoom(0.9),
                                 bg=color_style_2, activebackground=active_color, cursor="hand2",
                                 bd=0, width=20, height=20)
        
        self.zoom_down_button.pack(side=LEFT, padx=4)

        self.text_button= Button(self.attack_frame, image=self.image_dict['watermarking'], command=self.parameters_watermark,
                                 bg=color_style_2, activebackground=active_color, cursor="hand2",
                                 bd=0, height=20)
        self.text_button.pack(side=LEFT, padx=4)

        # ====== image frame ========

        self.frame_w_position = Frame(image_frame, padx=4, pady=5)
        self.frame_w_position.pack(side=RIGHT, expand=NO, fill=Y)

        self.quit_button_w = Button(self.frame_w_position, text='Quit', command=self.quit_watermark_mode)
        self.quit_button_w.pack(side=TOP)
        

    def display_menu(self, master):
        """ display the main menu """

        # create the file menu
        attack_menu = Menu(master)
        attack_menu.add_command(label="Text", command=self.create_text)
        attack_menu.add_command(label="Selection", command=lambda : self.create_selection(self.selection_button))
        attack_menu.add_command(label="Zoom +", command= lambda : self.obj.set_zoom(1.1))
        attack_menu.add_command(label="Zoom -", command= lambda: self.obj.set_zoom(0.9))
        attack_menu.add_separator()
        attack_menu.add_command(label="Watermarking" , command=self.parameters_watermark)

        return attack_menu


    
