from tkinter import *
import ctypes 
from PIL import Image, ImageTk
ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(ctypes.c_int()))
ctypes.windll.shcore.SetProcessDpiAwareness(2)
ctypes.windll.user32.SetProcessDPIAware()

root = Tk()

class Board:

    def __init__(self, master):
        self.white = []
        self.black = []
        self.images = {}
        self.PIECES = {"pwhite" : 8, "pblack" : 8, "nwhite" : 2, "nblack" : 2, "kwhite" : 1, "kblack" : 1, "rwhite" : 2, "rblack" : 2, "bwhite" : 2, "bblack" : 2, "qwhite" : 1, "qblack" : 1}
        CELL_WIDTH = 64
        CELL_HEIGHT = 64
        switch = 0      
        self.item = None

        master.geometry(f"{CELL_WIDTH*8}x{CELL_HEIGHT*8}")
        #master.resizable(0, 0)

        self.canvas = Canvas(master, bg = "black", highlightthickness = 0)
        self.canvas.pack(fill = BOTH, expand = True)
        #self.canvas.bind('<B1-Motion>')
        #self.canvas.bind("<Button-1>", self.click)
        self.canvas.tag_bind("piece","<Button-1>", self.click)
        self.canvas.tag_bind("piece",'<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        #self.c.bind('<B1-Motion>', self.paint)
        #self.c.bind('<ButtonRelease-1>', self.reset)
        #self.c.bind('<B3-Motion>', self.eraseItem)
        #self.c.bind("<Motion>", self.circle_follow)

        for row in range(8):
            switch = 1 - switch
            for column in range(8):
                x1 = column * CELL_WIDTH
                y1 = row * CELL_HEIGHT
                x2 = x1 + CELL_WIDTH
                y2 = y1 + CELL_HEIGHT
                switch = 1 - switch


                if switch:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#B58863", tag = f"{row} {column} square")#0xB58863, 0xF0D9B5, 
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#F0D9B5", tag = f"{row} {column} square")
        self.create_pieces()
        self.place_pieces()
        #print(self.images)

    def create_pieces(self):
        for piece in self.PIECES:
            img = ImageTk.PhotoImage(file = "pieces\\{}.png".format(piece))
            
            for i in range(self.PIECES[piece]):
                image = self.canvas.create_image(0, 0, image = img, anchor = NW, tag = "piece") 
                self.canvas.image = img                     # Keep img in memory # VERY IMPORTANT
                self.images[image] = img
                root.update()
                self.canvas.tag_raise("piece")

    def place_pieces(self):
        x = 0
        while True:
            x += 1
            coords = [int(i) for i in self.canvas.coords(x)]
            print(coords)

            if x-1 <= len(self.images)-1 :
                keys = list(self.images.keys())
                self.canvas.coords(keys[x-1], coords[0], coords[1])
            else:break

    def reset(self, event):
        self.item = None

    def click(self, event):
        print(event)
        self.item = self.canvas.find_closest(event.x, event.y)
        print(self.item)


    def drag(self, event):
        if self.item:
            self.canvas.coords(self.item, event.x - 32, event.y -32)

if __name__ == "__main__":
    a = Board(root)
    #a.create_pieces()
    root.mainloop()