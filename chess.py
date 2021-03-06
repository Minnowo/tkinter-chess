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
        self.piece_position = {}
        self.move_position = []
        switch = 0      
        self.startpos = (None, None)
        self.item = None
        self.last_move = {"move" : [(None, None), (None, None)], "piece" : None, "type" : None}
        self.piece_type = None
        self.en_passant = {"piece" : None, "canhappen" : False, "coords" : None}
        self.white_king_pos = (4, 0)
        self.black_king_pos = (4, 7)
        self.attacked_white = []
        self.attacked_black = []
        self.attached_squares = []

        master.geometry(f"{CELL_WIDTH*8}x{CELL_HEIGHT*8}")
        #master.resizable(0, 0)

        self.canvas = Canvas(master, bg = "black", highlightthickness = 0)
        self.canvas.pack(fill = BOTH, expand = True)
        #self.canvas.bind('<B1-Motion>')
        #self.canvas.bind("<Button-1>", self.click)
        self.canvas.tag_bind("piece","<Button-1>", self.click)
        self.canvas.tag_bind("piece",'<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.reset)


        for row in range(8):
            switch = 1 - switch
            for column in range(8):
                x1 = column * CELL_WIDTH
                y1 = row * CELL_HEIGHT
                x2 = x1 + CELL_WIDTH
                y2 = y1 + CELL_HEIGHT
                switch = 1 - switch


                if switch:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#B58863", tag = ["square", (column, row)])#0xB58863, 0xF0D9B5, 
                else:
                    item = self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#F0D9B5", tag = ["square", (column, row)])

                    
        self.create_pieces()
        self.place_pieces()
        
        print(self.PIECE_NAME)
        self.attacked()
        print(self.attached_squares)

    def horizontal_move(self, spaces, attack_color, coords, pos, create_circles=0, isking=0):
        for x in [(coords[0], coords[1], "+y"), (coords[0], coords[1], "-y"), (coords[0], coords[1], "+x"), (coords[0], coords[1], "-x")]:
            for i in range(spaces):
                i += 1 
                if x[2] == "+y":cord = (x[0], x[1]+i)
                elif x[2] == "-y":cord = (x[0], x[1]-i)
                elif x[2] == "+x":cord = (x[0]+i, x[1])
                elif x[2] == "-x":cord = (x[0]-i, x[1])
                if cord[0] < 0 or cord[1] < 0 or cord[0] > 7 or cord[1] > 7:break
                
                if not create_circles:
                    self.attached_squares.append(cord)
                    break

                #if isking and cord in self.attached_squares:break

                if cord not in pos:
                    self.create_cirle((cord[0])*self.SCALE+self.SCALE//2, (cord[1])*self.SCALE+self.SCALE//2, 16, cord)
                elif any(i.find(attack_color) != -1 for i in self.canvas.itemcget(list(self.piece_position.keys())[list(pos).index(cord)], "tags").split(" ")):
                    self.create_cirle((cord[0])*self.SCALE+self.SCALE//2, (cord[1])*self.SCALE+self.SCALE//2, 16, cord)
                    break
                else:break

    def diagonal_move(self, spaces, attack_color, coords, pos, create_circles=0, isking=0):
        for x in [(coords[0], coords[1], "+y+x"), (coords[0], coords[1], "-y+x"), (coords[0], coords[1], "+y-x"), (coords[0], coords[1], "-y-x")]:
            for i in range(spaces):
                i += 1 
                if x[2] == "+y+x":cord = (x[0]+i, x[1]+i)
                elif x[2] == "-y+x":cord = (x[0]+i, x[1]-i)
                elif x[2] == "+y-x":cord = (x[0]-i, x[1]+i)
                elif x[2] == "-y-x":cord = (x[0]-i, x[1]-i)
                if cord[0] < 0 or cord[1] < 0 or cord[0] > 7 or cord[1] > 7:break
                
                if not create_circles:
                    self.attached_squares.append(cord)
                    break

                #if isking and cord in self.attached_squares:break

                if cord not in pos:
                    self.create_cirle((cord[0])*self.SCALE+self.SCALE//2, (cord[1])*self.SCALE+self.SCALE//2, 16, cord)
                elif any(i.find(attack_color) != -1 for i in self.canvas.itemcget(list(self.piece_position.keys())[list(pos).index(cord)], "tags").split(" ")):
                    self.create_cirle((cord[0])*self.SCALE+self.SCALE//2, (cord[1])*self.SCALE+self.SCALE//2, 16, cord)
                    break
                else:break

    def pawn_move(self, attack_color, coords, pos, direction, first_move_row, create_circles=0):
        for cord in [(coords[0]-(1*direction), coords[1]-(1*direction)), (coords[0]+(1*direction), coords[1]-(1*direction))]:
            if not create_circles:
                self.attached_squares.append(cord)
                break
            if cord in pos:
                if any(i.find(attack_color) != -1 for i in self.canvas.itemcget(list(self.piece_position.keys())[list(pos).index(cord)], "tags").split(" ")):
                    self.create_cirle((cord[0])*self.SCALE+self.SCALE//2, (cord[1])*self.SCALE+self.SCALE//2, 16, cord) 
                    
            if (coords[0], coords[1]-(1*direction)) not in pos:
                self.create_cirle(coords[0]*self.SCALE+self.SCALE//2, (coords[1]-(1*direction))*self.SCALE+self.SCALE//2, 16, (coords[0], coords[1]-(1*direction))) 
                if coords[1] == first_move_row and (coords[0], coords[1]-(2*direction)) not in pos:                   
                    self.create_cirle(coords[0]*self.SCALE+self.SCALE//2, (coords[1]-(2*direction))*self.SCALE+self.SCALE//2, 16, (coords[0], coords[1]-(2*direction)))            
                                      
            if self.last_move["type"] == f"p{attack_color}" and self.last_move["move"][1][1] - (2*direction) == self.last_move["move"][0][1] and self.last_move["move"][1][1] == coords[1]:
                self.en_passant["piece"] = self.last_move["piece"]
                self.en_passant["canhappen"] = True
                print("en_passent")
                if self.last_move["move"][1][0] + (1*direction) == coords[0]: 
                    self.create_cirle((coords[0]-(1*direction))*self.SCALE+self.SCALE//2, (coords[1]-(1*direction))*self.SCALE+self.SCALE//2, 16, (coords[0]-(1*direction), coords[1]-(1*direction)), 1) 
                    self.en_passant["coords"] = (coords[0]-(1*direction), coords[1]-(1*direction))
                if self.last_move["move"][1][0] - (1*direction) == coords[0]: 
                    self.create_cirle((coords[0]+(1*direction))*self.SCALE+self.SCALE//2, (coords[1]-(1*direction))*self.SCALE+self.SCALE//2, 16, (coords[0]+(1*direction), coords[1]-(1*direction)), 1) 
                    self.en_passant["coords"] = (coords[0]+(1*direction), coords[1]-(1*direction))

    def knight_move(self, attack_color, coords, pos, create_circles=0):
        for cord in [(coords[0]-2, coords[1]-1), (coords[0]+2, coords[1]-1), (coords[0]+2, coords[1]+1), (coords[0]-2, coords[1]+1), (coords[0]-1, coords[1]-2), (coords[0]+1, coords[1]-2), (coords[0]+1, coords[1]+2), (coords[0]-1, coords[1]+2)]:
            if not create_circles:
                self.attached_squares.append(cord)
                break
            if cord in pos:
                if any(i.find(attack_color) != -1 for i in self.canvas.itemcget(list(self.piece_position.keys())[list(pos).index(cord)], "tags").split(" ")):                          
                    self.create_cirle((cord[0])*self.SCALE+self.SCALE//2, (cord[1])*self.SCALE+self.SCALE//2, 16, cord)
            elif cord[0] >= 0 and cord[1] >= 0 and cord[0] <= 7 and cord[1] <= 7:
                self.create_cirle((cord[0])*self.SCALE+self.SCALE//2, (cord[1])*self.SCALE+self.SCALE//2, 16, (cord[0], cord[1])) 

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
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 1

        column = 0
        row = 6
        for i in self.canvas.find_withtag("pwhite"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 1

        column = 1
        row = 0
        for i in self.canvas.find_withtag("nblack"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column *= 6

        column = 1
        row = 7
        for i in self.canvas.find_withtag("nwhite"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column *= 6

        column = 4
        row = 0
        for i in self.canvas.find_withtag("kblack"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

        column = 4
        row = 7
        for i in self.canvas.find_withtag("kwhite"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

        column = 0
        row = 0
        for i in self.canvas.find_withtag("rblack"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 7

        column = 0
        row = 7
        for i in self.canvas.find_withtag("rwhite"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 7

        column = 2
        row = 0
        for i in self.canvas.find_withtag("bblack"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 3

        column = 2
        row = 7
        for i in self.canvas.find_withtag("bwhite"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)
            column += 3

        column = 3
        row = 0
        for i in self.canvas.find_withtag("qblack"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

        column = 3
        row = 7
        for i in self.canvas.find_withtag("qwhite"):
            self.piece_position[i] = (column, row)
            self.canvas.coords(i, column * self.SCALE, row * self.SCALE)

    def attacked(self, move_piece = None):
        self.attached_squares.clear()
        for i in self.canvas.find_withtag("piece"):
            print(i)
            tags = [i for i in self.canvas.itemcget(i, "tags").split(" ") if i in self.PIECES]
            piece = tags[0]
            self.piece_type = piece
            coords = self.piece_position[i]
            print(coords)
            print(piece, "\n")
            #print(self.piece_position)
            pos = self.piece_position.values()
            if piece[0] == "p":   # pawn
                if piece[1] == "w":
                    self.pawn_move("black", coords, pos, 1, 6)
                else:
                    self.pawn_move("white", coords, pos, -1, 1)
            elif piece[0] == "n": # knight            
                if piece[1] == "w": 
                    self.knight_move("black", coords, pos)                  
                else:
                    self.knight_move("white", coords, pos)
            elif piece[0] == "q": # queen
                if piece[1] == "w":
                    self.diagonal_move(7, "black", coords, pos)
                    self.horizontal_move(7, "black", coords, pos)
                else:
                    self.diagonal_move(7, "white", coords, pos)
                    self.horizontal_move(7, "white", coords, pos)
            elif piece[0] == "b": # bishop
                if piece[1] == "w":
                    self.diagonal_move(7, "black", coords, pos)
                else:
                    self.diagonal_move(7, "white", coords, pos)

            elif piece[0] == "r": # rook
                if piece[1] == "w":
                    self.horizontal_move(7, "black", coords, pos)
                else:
                    self.horizontal_move(7, "white", coords, pos)
            elif piece[0] == "k": # king
                if piece[1] == "w":
                    self.diagonal_move(1, "black", coords, pos)
                    self.horizontal_move(1, "black", coords, pos)
                else:
                    self.diagonal_move(1, "white", coords, pos)
                    self.horizontal_move(1, "white", coords, pos)

    def checkKing(self):
        king_pos = [self.white_king_pos, self.black_king_pos]
        pieces = {"white":[], "black":[]}
        for king in king_pos:
            for square in [(king[0]-1, king[1]-1), (king[0]+1, king[1]-1), (king[0]-1, king[1]+1), (king[0]+1, king[1]+1), (king[0]-1, king[1]), (king[0], king[1]-1), (king[0]+1, king[1]), (king[0], king[1]+1)]:
                if square in self.piece_position.values():
                   piece = list(self.piece_position.keys())[list(self.piece_position.values()).index(square)]
                   tags = [i for i in self.canvas.itemcget(piece, "tags").split(" ") if i in self.PIECES]
                   print(tags, piece)
                   print(f"{square} : {list(self.piece_position.keys())[list(self.piece_position.values()).index(square)]}")
                    

    def reset(self, event): 
        self.checkKing()
        if self.item:
            try:
                square = [i for i in self.canvas.find_overlapping(event.x, event.y, event.x, event.y) if (i,) != self.item]
                lockin = [int(i) for i in self.canvas.coords(square[0])]
                #print(lockin)
                coords = (lockin[0]//self.SCALE, lockin[1]//self.SCALE)
                print(coords)
                print(self.piece_type)
                if coords in self.move_position:        
                    self.last_move["move"] = (self.piece_position[self.item[0]], coords)
                    self.last_move["piece"] = self.item
                    self.last_move["type"] = self.piece_type

                    if self.piece_type in ("kwhite", "kblack"):
                        if self.piece_type == "kwhite":
                            self.white_king_pos = coords
                        else:
                            self.black_king_pos = coords

                    if coords in self.piece_position.values():
                        delete = list(self.piece_position.keys())[list(self.piece_position.values()).index(coords)]
                        self.canvas.delete(delete)
                        del self.piece_position[delete]

                    if self.en_passant["canhappen"]:
                        print("en_passant")
                        if self.en_passant["coords"] == coords:
                            self.canvas.delete(self.en_passant["piece"])
                            del self.piece_position[self.en_passant["piece"][0]]
                            self.en_passant["canhappen"] = False
                            self.en_passant["piece"] = None
                            self.en_passant["coords"] = None

                    self.canvas.coords(self.item, coords[0]*self.SCALE, coords[1]*self.SCALE)
                    self.piece_position[self.item[0]] = coords
                    self.move_position.clear()
                    self.canvas.delete("move_view")
                else:
                    raise Exception

                self.item = None
            except Exception as e: # if there is an error put the piece back where it started
                print(e)
                square = [i for i in self.canvas.find_overlapping(self.startpos[0], self.startpos[1], self.startpos[0], self.startpos[1]) if (i,) != self.item]
                lockin = [int(i) for i in self.canvas.coords(square[0])]
                self.canvas.coords(self.item, lockin[0], lockin[1])
                self.item = None
            #root.update()
            #self.attacked()
            

    def click(self, event):
        self.move_position.clear()
        self.canvas.delete("move_view")
        self.startpos = (event.x , event.y)
        self.item = self.canvas.find_closest(event.x, event.y)
        
        tags = [i for i in self.canvas.itemcget(self.item, "tags").split(" ") if i in self.PIECES]
        piece = tags[0]
        self.piece_type = piece
        coords = self.piece_position[self.item[0]]
        #print(self.piece_position)
        pos = self.piece_position.values()
        #self.attacked(self.item)
        if piece[0] == "p":   # pawn
            if piece[1] == "w":
                self.pawn_move("black", coords, pos, 1, 6, 1)
            else:
                self.pawn_move("white", coords, pos, -1, 1, 1)
        elif piece[0] == "n": # knight            
            if piece[1] == "w": 
                self.knight_move("black", coords, pos, 1)                  
            else:
                self.knight_move("white", coords, pos, 1)
        elif piece[0] == "q": # queen
            if piece[1] == "w":
                self.diagonal_move(7, "black", coords, pos, 1)
                self.horizontal_move(7, "black", coords, pos, 1)
            else:
                self.diagonal_move(7, "white", coords, pos, 1)
                self.horizontal_move(7, "white", coords, pos, 1)
        elif piece[0] == "b": # bishop
            if piece[1] == "w":
                self.diagonal_move(7, "black", coords, pos, 1)
            else:
                self.diagonal_move(7, "white", coords, pos, 1)

        elif piece[0] == "r": # rook
            if piece[1] == "w":
                self.horizontal_move(7, "black", coords, pos, 1)
            else:
                self.horizontal_move(7, "white", coords, pos, 1)
        elif piece[0] == "k": # king
            if piece[1] == "w":
                print("white king")
                self.diagonal_move(1, "black", coords, pos, 1, 1)
                self.horizontal_move(1, "black", coords, pos, 1, 1)
            else:
                self.diagonal_move(1, "white", coords, pos, 1, 1)
                self.horizontal_move(1, "white", coords, pos, 1, 1)


        print(tags)
        self.canvas.tag_raise("piece")
        self.canvas.tkraise(self.item)

        


    def drag(self, event):
        if "piece" in self.canvas.itemcget(self.item, "tags"):
            self.canvas.coords(self.item, event.x - self.SCALE//2, event.y - self.SCALE//2)

    def create_cirle(self, x, y, radius, coords, redsquare = 0):
        if coords in self.piece_position.values() or redsquare:
            x1 = x-radius*2 + 5
            y1 = y-radius*2 + 5
            x2 = x+radius*2 - 5
            y2 = y+radius*2 - 5
            self.canvas.create_rectangle(x1, y1, x2, y2, tag = "move_view", outline='red', width = 5)
        else:
            x1 = x-radius 
            y1 = y-radius
            x2 = x+radius
            y2 = y+radius
            self.canvas.create_oval(x1, y1, x2, y2,fill = "green", tag = "move_view")
        self.move_position.append(coords)

        

if __name__ == "__main__":
    a = Board(root)
    #a.create_pieces()
    root.mainloop()