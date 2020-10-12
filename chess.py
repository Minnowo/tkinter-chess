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
        self.PIECE_NAME = {}
        CELL_WIDTH = 64
        CELL_HEIGHT = 64
        self.SCALE = 64
        switch = 0      
        self.startpos = (None, None)
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
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#B58863", tag = ["square", (row, column)])#0xB58863, 0xF0D9B5, 
                else:
                    item = self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#F0D9B5", tag = ["square", (row, column)])

                    
        self.create_pieces()
        self.place_pieces()
        print(self.PIECE_NAME)

    def create_pieces(self):
        for piece in self.PIECES:
            img = ImageTk.PhotoImage(file = "pieces\\{}.png".format(piece))
            
            for i in range(self.PIECES[piece]):
                image = self.canvas.create_image(0, 0, image = img, anchor = NW, tag = ["piece", piece]) 
                self.canvas.image = img                     # Keep img in memory # VERY IMPORTANT
                self.images[image] = img
                self.PIECE_NAME[image] = piece
                root.update()
                self.canvas.tag_raise("piece")

    def place_pieces(self):
        row = 1
        column = 0
        for i in self.canvas.find_withtag("pblack"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 1

        column = 0
        row = 6
        for i in self.canvas.find_withtag("pwhite"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 1

        column = 1
        row = 0
        for i in self.canvas.find_withtag("nblack"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column *= 6

        column = 1
        row = 7
        for i in self.canvas.find_withtag("nwhite"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column *= 6

        column = 4
        row = 0
        for i in self.canvas.find_withtag("kblack"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

        column = 4
        row = 7
        for i in self.canvas.find_withtag("kwhite"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

        column = 0
        row = 0
        for i in self.canvas.find_withtag("rblack"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 7

        column = 0
        row = 7
        for i in self.canvas.find_withtag("rwhite"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 7

        column = 2
        row = 0
        for i in self.canvas.find_withtag("bblack"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 3

        column = 2
        row = 7
        for i in self.canvas.find_withtag("bwhite"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 3

        column = 3
        row = 0
        for i in self.canvas.find_withtag("qblack"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

        column = 3
        row = 7
        for i in self.canvas.find_withtag("qwhite"):
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

            
        #x = 0
        #while True:
        #    x += 1
        #    coords = [int(i) for i in self.canvas.coords(x)]
        #    print(coords)

        #    if x-1 <= len(self.images)-1 :
        #        keys = list(self.images.keys())
        #        self.canvas.coords(keys[x-1], coords[0], coords[1])
        #    else:break

    def reset(self, event):  
        if self.item:
            try:
                square = [i for i in self.canvas.find_overlapping(event.x, event.y, event.x, event.y) if (i,) != self.item]
                lockin = [int(i) for i in self.canvas.coords(square[0])]
                print(lockin)
                self.canvas.coords(self.item, lockin[0], lockin[1])
                

                for i in self.canvas.find_overlapping(lockin[0]+1, lockin[1]+1, lockin[2]-1, lockin[3]-1):
                    print(i)
                    if "square" not in self.canvas.itemcget(i, "tags") and (i,) != self.item:
                        self.canvas.delete(i)
                self.item = None
            except: # if there is an error put the piece back where it started
                square = [i for i in self.canvas.find_overlapping(self.startpos[0], self.startpos[1], self.startpos[0], self.startpos[1]) if (i,) != self.item]
                lockin = [int(i) for i in self.canvas.coords(square[0])]
                self.canvas.coords(self.item, lockin[0], lockin[1])
                self.item = None
            print(square)

    def click(self, event):
        print(event)
        self.startpos = (event.x , event.y)
        self.item = self.canvas.find_closest(event.x, event.y)
        self.canvas.tkraise(self.item)
        tags = [i for i in self.canvas.itemcget(self.item, "tags").split(" ") if i in self.PIECES]
        piece = tags[0]

        if piece[0] == "p":   # pawn
            pass
        elif piece[0] == "n": # knight
            pass
        elif piece[0] == "q": # queen
            pass
        elif piece[0] == "b": # bishop
            pass 
        elif piece[0] == "r": # rook
            pass
        elif piece[0] == "k": # king
            pass


        print(tags)
        
        #print(self.item)
        #print(self.canvas.itemcget(self.item, "tags"))
        


    def drag(self, event):
        if "piece" in self.canvas.itemcget(self.item, "tags"):
            self.canvas.coords(self.item, event.x - self.SCALE//2, event.y - self.SCALE//2)

if __name__ == "__main__":
    a = Board(root)
    #a.create_pieces()
    root.mainloop()