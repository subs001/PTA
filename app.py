from distutils.command.config import LANG_EXT
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
import os
import cv2
from numpy import pad
INITIAL_DIRECTORY = "/home/subramanian"
# VIDEO_DIRECTORY =  "/home/subramanian/Videos/Webcam"# change via some options menu
VIDEO_DIRECTORY = r"C:\Users\aadit\Videos\VA_vids"
# THUMBNAIL_DIRECTORY = "/home/subramanian/Pictures/thumbnails"
THUMBNAIL_DIRECTORY = r"C:\Users\aadit\OneDrive\Pictures\VA_Thumbs"
# height and width for image. set frame size based on this in MyAPP using geometry. else just let it auto adjust
IMG_HEIGHT = 120
IMG_WIDTH = 150

row_counter = 0
col_counter = 0                             
frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}
pokemon_info = [['Bulbasaur', 'Grass', '318'], ['Ivysaur', 'Grass', '405'], ['Venusaur', 'Grass', '525'], ['Charmander', 'Fire', '309'], ['Charmeleon', 'Fire', '405'], ['Charizard', 'Fire', '534'], ['Squirtle', 'Water', '314'], ['Wartortle', 'Water', '405'], ['Blastoise', 'Water', '530'], ['Caterpie', 'Bug', '195'], ['Metapod', 'Bug', '205'], ['Butterfree', 'Bug', '395'], ['Weedle', 'Bug', '195'], ['Kakuna', 'Bug', '205'], ['Beedrill', 'Bug', '395'], ['Pidgey', 'Normal', '251'], ['Pidgeotto', 'Normal', '349'], ['Pidgeot', 'Normal', '479'], ['Rattata', 'Normal', '253'], ['Raticate', 'Normal', '413'], ['Spearow', 'Normal', '262'], ['Fearow', 'Normal', '442'], ['Ekans', 'Poison', '288'], ['Arbok', 'Poison', '448'], ['Pikachu', 'Electric', '320'], ['Raichu', 'Electric', '485'], ['Sandshrew', 'Ground', '300'], ['Sandslash', 'Ground', '450'], ['Nidoran?', 'Poison', '275'], ['Nidorina', 'Poison', '365'], ['Nidoqueen', 'Poison', '505'], ['Nidoran?', 'Poison', '273'], ['Nidorino', 'Poison', '365'], ['Nidoking', 'Poison', '505'], ['Clefairy', 'Fairy', '323'], ['Clefable', 'Fairy', '483'], ['Vulpix', 'Fire', '299'], ['Ninetales', 'Fire', '505'], ['Jigglypuff', 'Normal', '270'], ['Wigglytuff', 'Normal', '435'], ['Zubat', 'Poison', '245'], ['Golbat', 'Poison', '455'], ['Oddish', 'Grass', '320'], ['Gloom', 'Grass', '395'], ['Vileplume', 'Grass', '490'], ['Paras', 'Bug', '285'], ['Parasect', 'Bug', '405'], ['Venonat', 'Bug', '305'], ['Venomoth', 'Bug', '450'], ['Diglett', 'Ground', '265'], ['Dugtrio', 'Ground', '425'], ['Meowth', 'Normal', '290'], ['Persian', 'Normal', '440'], ['Psyduck', 'Water', '320'], ['Golduck', 'Water', '500'], ['Mankey', 'Fighting', '305'], ['Primeape', 'Fighting', '455'], ['Growlithe', 'Fire', '350'], ['Arcanine', 'Fire', '555'], ['Poliwag', 'Water', '300'], ['Poliwhirl', 'Water', '385'], ['Poliwrath', 'Water', '510'], ['Abra', 'Psychic', '310'], ['Kadabra', 'Psychic', '400'], ['Alakazam', 'Psychic', '500'], ['Machop', 'Fighting', '305'], ['Machoke', 'Fighting', '405'], ['Machamp', 'Fighting', '505'], ['Bellsprout', 'Grass', '300'], ['Weepinbell', 'Grass', '390'], ['Victreebel', 'Grass', '490'], ['Tentacool', 'Water', '335'], ['Tentacruel', 'Water', '515'], ['Geodude', 'Rock', '300'], ['Graveler', 'Rock', '390'], ['Golem', 'Rock', '495'], ['Ponyta', 'Fire', '410'], ['Rapidash', 'Fire', '500'], ['Slowpoke', 'Water', '315'], ['Slowbro', 'Water', '490'], ['Magnemite', 'Electric', '325'], ['Magneton', 'Electric', '465'], ["Farfetch'd", 'Normal', '377'], ['Doduo', 'Normal', '310'], ['Dodrio', 'Normal', '470'], ['Seel', 'Water', '325'], ['Dewgong', 'Water', '475'], ['Grimer', 'Poison', '325'], ['Muk', 'Poison', '500'], ['Shellder', 'Water', '305'], ['Cloyster', 'Water', '525'], ['Gastly', 'Ghost', '310'], ['Haunter', 'Ghost', '405'], ['Gengar', 'Ghost', '500'], ['Onix', 'Rock', '385'], ['Drowzee', 'Psychic', '328'], ['Hypno', 'Psychic', '483'], ['Krabby', 'Water', '325'], ['Kingler', 'Water', '475'], ['Voltorb', 'Electric', '330'], ['Electrode', 'Electric', '490'], ['Exeggcute', 'Grass', '325'], ['Exeggutor', 'Grass', '530'], ['Cubone', 'Ground', '320'], ['Marowak', 'Ground', '425'], ['Hitmonlee', 'Fighting', '455'], ['Hitmonchan', 'Fighting', '455'], ['Lickitung', 'Normal', '385'], ['Koffing', 'Poison', '340'], ['Weezing', 'Poison', '490'], ['Rhyhorn', 'Ground', '345'], ['Rhydon', 'Ground', '485'], ['Chansey', 'Normal', '450'], ['Tangela', 'Grass', '435'], ['Kangaskhan', 'Normal', '490'], ['Horsea', 'Water', '295'], ['Seadra', 'Water', '440'], ['Goldeen', 'Water', '320'], ['Seaking', 'Water', '450'], ['Staryu', 'Water', '340'], ['Starmie', 'Water', '520'], ['Scyther', 'Bug', '500'], ['Jynx', 'Ice', '455'], ['Electabuzz', 'Electric', '490'], ['Magmar', 'Fire', '495'], ['Pinsir', 'Bug', '500'], ['Tauros', 'Normal', '490'], ['Magikarp', 'Water', '200'], ['Gyarados', 'Water', '540'], ['Lapras', 'Water', '535'], ['Ditto', 'Normal', '288'], ['Eevee', 'Normal', '325'], ['Vaporeon', 'Water', '525'], ['Jolteon', 'Electric', '525'], ['Flareon', 'Fire', '525'], ['Porygon', 'Normal', '395'], ['Omanyte', 'Rock', '355'], ['Omastar', 'Rock', '495'], ['Kabuto', 'Rock', '355'], ['Kabutops', 'Rock', '495'], ['Aerodactyl', 'Rock', '515'], ['Snorlax', 'Normal', '540'], ['Articuno', 'Ice', '580'], ['Zapdos', 'Electric', '580'], ['Moltres', 'Fire', '580'], ['Dratini', 'Dragon', '300'], ['Dragonair', 'Dragon', '420'], ['Dragonite', 'Dragon', '600'], ['Mewtwo', 'Psychic', '680'], ['Mew', 'Psychic', '600']]

#buttons and their assocated commands in the menu bar
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Application", menu=menu_file)
        # menu_file.add_command(label="All Widgets", command=lambda: parent.show_frame(Some_Widgets))
        # menu_file.add_separator()
        menu_file.add_command(label="Exit Application", command=lambda: parent.Quit_application())

        menu_orders = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Excercise", menu=menu_orders)
        menu_orders.add_command(label="Video Select", command=lambda: parent.show_frame(PageOne))


        # menu_pricing = tk.Menu(self, tearoff=0)
        # self.add_cascade(label="Menu3", menu=menu_pricing)
        # menu_pricing.add_command(label="Page One", command=lambda: parent.show_frame(PageOne))

        menu_operations = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Menu3", menu=menu_operations)
        # menu_operations.add_command(label="Page Two", command=lambda: parent.show_frame(PageTwo))
        menu_positions = tk.Menu(menu_operations, tearoff=0)
        menu_operations.add_cascade(label="Folder Select", menu=menu_positions)
        menu_positions.add_command(label="Change Video Directory", command=set_dir)
        menu_positions.add_command(label="Change Initital Directory", command=lambda: parent.show_frame(PageOne))

        menu_help = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Menu4", menu=menu_help)
        menu_help.add_command(label="Open New Window", command=lambda: parent.OpenNewWindow())


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=600)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) prevents the app from being resized
        self.geometry(str( IMG_WIDTH*4 + 40) + "x" + str(IMG_HEIGHT*4)) #fixes the applications size
        self.frames = {}
        pages = PageOne
        # For multiple frames
        # for F in pages:
        #     frame = F(main_frame, self)
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")
        # self.show_frame(Some_Widgets)
        frame = PageOne(main_frame, self)
        self.frames[PageOne] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PageOne)
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def OpenNewWindow(self):
        OpenNewWindow()

    def Quit_application(self):
        self.destroy()

    # def remakeFrame(self):
    #     # self.frames[PageOne].destroy()
    #     # main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=600)
    #     # main_frame.pack_propagate(0)
    #     # main_frame.pack(fill="both", expand="true")
    #     # main_frame.grid_rowconfigure(0, weight=1)
    #     # main_frame.grid_columnconfigure(0, weight=1)
    #     # self.frames[PageOne] = PageOne(self, main_frame)
    #     # # self.frames[PageOne].tkraise()
    #     # self.show_frame(PageOne)
    #     self.__init__()


class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=600, width=600)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        #set column spaces
        self.main_frame.grid_rowconfigure(0,weight = 1)
        self.main_frame.grid_rowconfigure(1, uniform="rowgroup", weight=2)
        self.main_frame.grid_rowconfigure(2, uniform="rowgroup", weight=2)
        self.main_frame.grid_columnconfigure(0, uniform="colgroup")
        self.main_frame.grid_columnconfigure(1, uniform="colgroup")
        self.main_frame.grid_columnconfigure(2, uniform="colgroup")
        self.main_frame.grid_columnconfigure(3, uniform="colgroup")

# A bunch of random working widgets in tkinter
# class Some_Widgets(GUI):  # inherits from the GUI class
#     def __init__(self, parent, controller):
#         GUI.__init__(self, parent)

#         frame1 = tk.LabelFrame(self, frame_styles, text="This is a LabelFrame containing a Treeview")
#         frame1.place(rely=0.05, relx=0.02, height=400, width=400)

#         frame2 = tk.LabelFrame(self, frame_styles, text="Some widgets")
#         frame2.place(rely=0.05, relx=0.45, height=500, width=500)

#         button1 = tk.Button(frame2, text="tk button", command=lambda: Refresh_data())
#         button1.pack()
#         button2 = ttk.Button(frame2, text="ttk button", command=lambda: Refresh_data())
#         button2.pack()

#         Var1 = tk.IntVar()
#         Var2 = tk.IntVar()
#         Cbutton1 = tk.Checkbutton(frame2, text="tk CheckButton1", variable=Var1, onvalue=1, offvalue=0)
#         Cbutton1.pack()
#         Cbutton2 = tk.Checkbutton(frame2, text="tk CheckButton2", variable=Var2, onvalue=1, offvalue=0)
#         Cbutton2.pack()

#         Cbutton3 = ttk.Checkbutton(frame2, text="ttk CheckButton1", variable=Var1, onvalue=1, offvalue=0)
#         Cbutton3.pack()
#         Cbutton3 = ttk.Checkbutton(frame2, text="ttk CheckButton2", variable=Var2, onvalue=1, offvalue=0)
#         Cbutton3.pack()

#         Lbox1 = tk.Listbox(frame2, selectmode="multiple")
#         Lbox1.insert(1, "This is a tk ListBox")
#         Lbox1.insert(2, "Github")
#         Lbox1.insert(3, "Python")
#         Lbox1.insert(3, "StackOverflow")
#         Lbox1.pack(side="left")

#         Var3 = tk.IntVar()
#         R1 = tk.Radiobutton(frame2, text="tk Radiobutton1", variable=Var3, value=1)
#         R1.pack()
#         R2 = tk.Radiobutton(frame2, text="tk Radiobutton2", variable=Var3, value=2)
#         R2.pack()
#         R3 = tk.Radiobutton(frame2, text="tk Radiobutton3", variable=Var3, value=3)
#         R3.pack()

#         R4 = tk.Radiobutton(frame2, text="ttk Radiobutton1", variable=Var3, value=1)
#         R4.pack()
#         R5 = tk.Radiobutton(frame2, text="ttk Radiobutton2", variable=Var3, value=2)
#         R5.pack()
#         R6 = tk.Radiobutton(frame2, text="ttk Radiobutton3", variable=Var3, value=3)
#         R6.pack()

#         # This is a treeview.
#         tv1 = ttk.Treeview(frame1)
#         column_list_account = ["Name", "Type", "Base Stat Total"]
#         tv1['columns'] = column_list_account
#         tv1["show"] = "headings"  # removes empty column
#         for column in column_list_account:
#             tv1.heading(column, text=column)
#             tv1.column(column, width=50)
#         tv1.place(relheight=1, relwidth=0.995)
#         treescroll = tk.Scrollbar(frame1)
#         treescroll.configure(command=tv1.yview)
#         tv1.configure(yscrollcommand=treescroll.set)
#         treescroll.pack(side="right", fill="y")

#         def Load_data():
#             for row in pokemon_info:
#                 tv1.insert("", "end", values=row)

#         def Refresh_data():
#             # Deletes the data in the current treeview and reinserts it.
#             tv1.delete(*tv1.get_children())  # *=splat operator
#             Load_data()

#         Load_data()


class PageOne(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        # label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Video Select")
        # label1.pack(side="top")
        # dir_btn = tk.Button(self.main_frame, text = "Get Videos" ,command=lambda: makeVidButtons(self.main_frame))
        # dir_btn.pack(padx=10, pady=30, side='top')  
        # self.main_frame.grid_columnconfigure(0, weight=1)
        # self.main_frame.grid_rowconfigure(0, weight=1)
        self.craftFrame(parent,controller)
    
    def craftFrame(self, parent, controller):
        print(VIDEO_DIRECTORY)
        # count num of files for placement
        vidCount = 0
        for _, _, files in os.walk(VIDEO_DIRECTORY):
            for file in files:    
                if file.endswith(('.mp4', '.avi', '.webm')) and file.startswith('.') == False:
                    vidCount += 1

        global row_counter, col_counter
        frame_label = ttk.LabelFrame(self.main_frame, text="VIDEO SELECT",labelanchor="ns")
        frame_label.grid(row=row_counter, column=0, columnspan=3, sticky="nsew")
        #make reset buttn
        reset_btn = ttk.Button(self.main_frame, text="Reset", command=lambda: resetPage())
        reset_btn.grid(row=row_counter, column=3, sticky="nsew")

        row_counter += 1 # start from 1 row down
        
        for item in os.listdir(VIDEO_DIRECTORY):
            print(item)
            if item.endswith(('.mp4', '.avi', '.webm')):
                # get_thumbnail(root,vid_dir + "/" + item, item)
                
                # print(item,col_counter)
                cap = cv2.VideoCapture(VIDEO_DIRECTORY + "/" + item)
                cap.set(cv2.CAP_PROP_POS_FRAMES, 10-1)
                res, img = cap.read()
                # print(res)
                cv2.imwrite(THUMBNAIL_DIRECTORY + "/thumbnail" + str(col_counter) + ".png", img)
                print(THUMBNAIL_DIRECTORY + "/thumbnail" + str(col_counter) + ".png")
                # create_button(root,vid_name)\
                # print(col_counter)
                img = tk.PhotoImage(file = THUMBNAIL_DIRECTORY + "/thumbnail" + str(col_counter) + ".png")
                img = img.subsample(4, 4)
                print("creating buttons")
                btn = tk.Button(self.main_frame,height=IMG_HEIGHT, width=IMG_WIDTH, text = item, image = img, compound = 'top', command = lambda: launch_video(col_counter))
                btn.image = img
                btn.vid_path = col_counter
                btn.grid(column=col_counter%4, row=row_counter, sticky="ew",padx=2, pady=2)
                col_counter += 1
                print(col_counter,row_counter)
                if col_counter%4 == 0:
                    row_counter += 1

def resetPage():
    print("resetting page")
    global row_counter, col_counter,root
    row_counter = 0
    col_counter = 0
    # for widget in self.winfo_children():
    #     widget.destroy()
    # self.craftFrame(parent,controller)
    # # self.__init__(parent, controller)
    root.destroy()
    root = MyApp()




# class PageThree(GUI):
#     def __init__(self, parent, controller):
#         GUI.__init__(self, parent)

#         label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Page Three")
#         label1.pack(side="top")


# class PageFour(GUI):
#     def __init__(self, parent, controller):
#         GUI.__init__(self, parent)

#         label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Page Four")
#         label1.pack(side="top")


class OpenNewWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.title("Here is the Title of the Window")
        self.geometry("500x500")
        self.resizable(0, 0)

        frame1 = ttk.LabelFrame(main_frame, text="This is a ttk LabelFrame")
        frame1.pack(expand=True, fill="both")

        label1 = tk.Label(frame1, font=("Verdana", 20), text="OpenNewWindow Page")
        label1.pack(side="top")

def launch_video(vid_path):
    print(vid_path)
    OpenNewWindow()

# def create_button(root,vid_name):
#     global row_counter, col_counter
#     img = tk.PhotoImage(file = "/home/subramanian/Pictures/thumbnails/thumbnail" + str(col_counter) + ".png")
#     img = img.subsample(5, 5)
#     print("creating byuttons")
#     btn = tk.Button(root, text = vid_name, image = img, compound = 'top', command = (launch_video, col_counter))
#     btn.image = img
#     btn.vid_path = col_counter
#     # btn.grid(column=col_counter%4, row=row_counter, padx=10, pady=5)
#     col_counter += 1
#     if col_counter%4 == 0:
#         row_counter += 1

# def get_thumbnail(root,vid_dir, vid_name) :
#     cap = cv2.VideoCapture(vid_dir)
#     cap.set(cv2.CAP_PROP_POS_FRAMES, 10-1)
#     res, frame = cap.read()
#     cv2.imwrite("/home/subramanian/Pictures/thumbnails/thumbnail" + str(col_counter) + ".png", frame)
#     create_button(root,vid_name)

# def get_videos(root,vid_dir):
#     for item in os.listdir(vid_dir):
#         if item.endswith(('.mp3', '.avi', 'webm')):
#             get_thumbnail(root,vid_dir + "/" + item, item)
# def makeVidButtons(rootObj):
#     for item in os.listdir(VIDEO_DIRECTORY):
#         if item.endswith(('.mp3', '.avi', 'webm')):
#             # get_thumbnail(root,vid_dir + "/" + item, item)
#             global row_counter, col_counter
#             cap = cv2.VideoCapture(VIDEO_DIRECTORY)
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 10-1)
#             res, frame = cap.read()
#             cv2.imwrite("/home/subramanian/Pictures/thumbnails/thumbnail" + str(col_counter) + ".png", frame)
#             # create_button(root,vid_name)\
#             img = tk.PhotoImage(file = "/home/subramanian/Pictures/thumbnails/thumbnail" + str(col_counter) + ".png")
#             img = img.subsample(5, 5)
#             print("creating buttons")
#             btn = tk.Button(rootObj, text = item, image = img, compound = 'top', command = lambda: launch_video(col_counter))
#             btn.image = img
#             btn.vid_path = col_counter
#             # btn.grid(column=col_counter%4, row=row_counter, padx=10, pady=5)
#             col_counter += 1
#             if col_counter%4 == 0:
#                 row_counter += 1


# function to open the directory menu and chose a directory            
# def get_dir(root):
#     root.directory = tkFileDialog.askdirectory(initialdir="/home/subramanian")
#     get_videos(root,root.directory)
def set_dir():
    global VIDEO_DIRECTORY
    VIDEO_DIRECTORY = tkFileDialog.askdirectory(initialdir= INITIAL_DIRECTORY)
    print(VIDEO_DIRECTORY)

# root = tk.Tk()
# root.title("Physiotherapy Assistant")
# root.geometry("960x540")

# dir_btn = tk.Button(root, text = "Get Videos" ,command=(get_dir)).grid(columnspan=3, rowspan=2)
# # dir_btn.pack(padx=10, pady=30, side='top')

# root.mainloop() 
# # if__name__ == "__main__":

root = MyApp()
root.mainloop() 