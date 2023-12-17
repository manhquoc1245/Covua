import pygame, threading, random, time
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox
from pygame import mixer
from piece import *
from client import *

class EndGameScreen:
    def __init__(self, message, winPoint, pieceEatPoint, pointBonusTime, pointMinus, point):
        # point
        self.message = message
        self.winPoint = winPoint
        self.pieceEatPoint = pieceEatPoint
        self.pointBonusTime = pointBonusTime
        self.pointMinus = pointMinus
        self.point = point
        # screen
        self.screen = Tk()
        self.font = ("Arial", 14)
        self.bigFont = ("Arial", 40)
        w, h = 400, 400
        ws = self.screen.winfo_screenwidth()
        hs = self.screen.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2) - 50
        self.screen.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        self.screen.resizable(False, False)
        self.screen.configure(background = "#606060")
        self.screen.iconbitmap('image/UI/logo.ico')
        self.screen.title("Tổng điểm")

        self.bgColor1 = "#00FF2A"
        self.bgColor2 = "#4D88FF"

        self.frame1 = Frame(self.screen, bg=self.bgColor1, borderwidth=5)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.pack(padx=20, pady=10)

        self.gameOver = Label(self.frame1, bg=self.bgColor1, text="GAME OVER", font=self.bigFont)
        self.gameOver.grid(row=0, column=0)

        self.mess = Label(self.frame1, bg=self.bgColor1, text=self.message, font=self.font, fg="#B37700")
        self.mess.grid(row=1, column=0)

        self.frame2 = Frame(self.screen, bg=self.bgColor2, padx=50, borderwidth=5)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.frame2.pack(padx=20, pady=10)

        r = 1
        if self.winPoint != 0:
            self.txW = Label(self.frame2, bg=self.bgColor2, text=f"Điểm thắng", font=self.font)
            self.txW.grid(row=r, column=0, padx=(15, 0), sticky="W")
            self.vW = Label(self.frame2, bg=self.bgColor2, text=f"{self.winPoint}", font=self.font)
            self.vW.grid(row=r, column=1, padx=(0, 15), sticky="E")
            r += 1
        self.tx1 = Label(self.frame2, bg=self.bgColor2, text=f"Điểm ăn quân", font=self.font)
        self.tx1.grid(row=r, column=0, padx=(15, 0), sticky="W")
        self.v1 = Label(self.frame2, bg=self.bgColor2, text=f"{self.pieceEatPoint}", font=self.font)
        self.v1.grid(row=r, column=1, padx=(0, 15), sticky="E")
        r += 1
        self.tx2 = Label(self.frame2, bg=self.bgColor2,text="Điểm thời gian", font=self.font)
        self.tx2.grid(row=r, column=0, padx=(15, 0), sticky="W")
        self.v2 = Label(self.frame2, bg=self.bgColor2, text=f"{self.pointBonusTime}", font=self.font)
        self.v2.grid(row=r, column=1, padx=(0, 15), sticky="E")
        r += 1
        self.tx3 = Label(self.frame2, bg=self.bgColor2,text="Điểm trừ", font=self.font)
        self.tx3.grid(row=r, column=0, padx=(15, 0), sticky="W")
        self.v3 = Label(self.frame2, bg=self.bgColor2, text=f"-{self.pointMinus}", font=self.font)
        self.v3.grid(row=r, column=1, padx=(0, 15), sticky="E")
        r += 1
        self.tx4 = Label(self.frame2, bg=self.bgColor2, text="Tổng điểm thêm", font=self.font)
        self.tx4.grid(row=r, column=0, padx=(15, 0), sticky="W")
        x = self.winPoint+self.pieceEatPoint+self.pointBonusTime-self.pointMinus
        self.v4 = Label(self.frame2, bg=self.bgColor2, text=f"{x}", font=self.font)
        self.v4.grid(row=r, column=1, padx=(0, 15), sticky="E")
        r += 1
        self.tx5 = Label(self.frame2, bg=self.bgColor2, text="Điểm XP:", font=self.font)
        self.tx5.grid(row=r, column=0, padx=(15, 0), sticky="W")
        x += int(self.point)
        if x < 0: x = 0
        self.v5 = Label(self.frame2, bg=self.bgColor2, text=f"{x}", font=self.font)
        self.v5.grid(row=r, column=1, padx=(0, 15), sticky="E")
        r += 1

        self.btnClose = Button(self.frame2, text="Menu", command=self.goBackMenu, width=10, height=1, font=self.font)
        self.btnClose.grid(row=r, columnspan=2, rowspan=2, pady=(10, 10))
        self.frame2.pack(fill="both")
        self.screen.mainloop()
    
    def goBackMenu(self):
        self.screen.destroy()

def getAllEnemyMove(matrix, mySide):
    allEnemyMoveable = []
    for row in matrix:
        for piece in row:
            if piece != 0:
                if piece.getSide() != mySide:
                    if piece.getOnlyName() == "pawn":
                        piece.predictMoveEat(matrix)
                        allEnemyMoveable += piece.moveable
                        piece.clearMove()
                    else:
                        piece.predictMove(matrix)
                        allEnemyMoveable += piece.moveable
                        piece.clearMove()
    return allEnemyMoveable

def getAllMyMove(matrix, mySide):
    allMyMoveable = []
    for row in matrix:
        for piece in row:
            if piece != 0:
                if piece.getSide() == mySide:
                    piece.predictMove(matrix)
                    allMyMoveable += piece.moveable
                    piece.clearMove()
    return allMyMoveable

def cloneMatrix(matrix):
    m = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(0, 8):
        for j in range(0, 8):
            if matrix[i][j] != 0:
                m[i][j] = matrix[i][j].clone()
    return m

def hander_server_gameControl(game):
    while game.running:
        order = game.conn.recv(5).decode(FORMAT)
        if order == "ENDGM":
            # you win
            time.sleep(1)
            game.endgameMsg = "Bạn thắng"
            game.running = False
            break
        elif order == "DRAW1":
            # draw in the first condition
            time.sleep(1)
            game.endgameMsg = "Hòa, đối thủ không còn nước đi nào hợp lệ"
            game.running = False
            break
        elif order == "DRAW2":
            # draw in in the second condition
            time.sleep(1)
            game.endgameMsg = "Hòa, một thế cờ lặp lại 3 lần"
            game.running = False
            break
        elif order == "SURDE":
            # enemy surrender, you win 
            time.sleep(1)
            game.running = False
            game.endgameMsg = "Đối thủ đầu hàng, bạn thắng"
            break
        elif order == "MOVIN":
            mess = recv_message(game.conn, [12, 12, 1, 1, 1, 1])
            mess = removeSpace(mess)
            game.table_matrix[int(mess[2])][int(mess[3])].move([int(mess[4]), int(mess[5])], game.table_matrix)
            f, t = [int(mess[2]), int(mess[3])], [int(mess[4]), int(mess[5])]
            game.animationPiece(f, t, game.image_dict[mess[0]])
            game.enemyMove.append(f)
            game.enemyMove.append(t)
        elif order == "UPGRA":
            mess = recv_message(game.conn, [12, 12, 1, 1, 1, 1, 12])
            mess = removeSpace(mess)
            side = game.table_matrix[int(mess[2])][int(mess[3])].getSide()
            game.table_matrix[int(mess[2])][int(mess[3])].move([int(mess[4]), int(mess[5])], game.table_matrix)
            f, t = [int(mess[2]), int(mess[3])], [int(mess[4]), int(mess[5])]
            game.animationPiece(f, t, game.image_dict[mess[0]])
            game.enemyMove.append(f)
            game.enemyMove.append(t)
            # sleep in animation time
            time.sleep(0.3)
            if mess[6] == "queen":
                game.table_matrix[int(mess[4])][int(mess[5])] = Queen(side, [int(mess[4]), int(mess[5])])
            elif mess[6] == "rook":
                game.table_matrix[int(mess[4])][int(mess[5])] = Rook(side, [int(mess[4]), int(mess[5])])
            elif mess[6] == "bishop":
                game.table_matrix[int(mess[4])][int(mess[5])] = Bishop(side, [int(mess[4]), int(mess[5])])
            elif mess[6] == "knight":
                game.table_matrix[int(mess[4])][int(mess[5])] = Knight(side, [int(mess[4]), int(mess[5])])
        elif order == "ROOKI":
            mess = recv_message(game.conn, [12, 12, 1, 1, 1, 1, 12, 1, 1, 1, 1])
            mess = removeSpace(mess)
            game.table_matrix[int(mess[2])][int(mess[3])].move([int(mess[4]), int(mess[5])], game.table_matrix)
            game.table_matrix[int(mess[7])][int(mess[8])].move([int(mess[9]), int(mess[10])], game.table_matrix)
            f, t = [int(mess[2]), int(mess[3])], [int(mess[4]), int(mess[5])]
            game.animationPiece(f, t, game.image_dict[mess[0]])
            game.animationPiece([int(mess[7]), int(mess[8])], [int(mess[9]), int(mess[10])], game.image_dict[mess[6]])
            game.enemyMove.append(f)
            game.enemyMove.append(t)
        game.turn = True
        game.beginTime = round(time.time())
        game.MSG = "Your turn"
        if game.checkEnd():
            # you lose or draw
            time.sleep(3) # wait to end the animation
            game.running = False

def movingAnimation(game, froM, to, imgPiece):
        game.isAnimation.append(to)
        try:
            t = 0.3
            frames = 100
            t_sleep = t / frames
            step_x, step_y = (to[0] - froM[0]) / frames, (to[1] - froM[1]) / frames
            x, y = froM
            while x != float(to[0]) or y != float(to[1]):
                if game.draw_reverse:
                    game.screen.blit(imgPiece, (-1 * (y - 7) * 60 + game.t_x, -1 * (x - 7) * 60 + game.t_y, 60, 60))
                else:
                    game.screen.blit(imgPiece, (y * 60 + game.t_x, x * 60 + game.t_y, 60, 60))
                x += step_x
                y += step_y
                x = round(x, 2)
                y = round(y, 2)
                time.sleep(t_sleep)
        except:
            pass
        if not game.master.pauseS:
            pygame.mixer.Sound.play(game.sounds[random.randint(0, len(game.sounds)-1)])
        game.isAnimation.remove(to)

class ButtonText:
    def __init__(self, surface, position, action, imgs, text="", textFont=None, textColor=(255, 0, 0), size=(90, 50)):
        self.suface = surface
        self.position = position
        self.action = action
        self.imgs = imgs
        self.img = self.imgs[0]
        self.text = text
        self.textColor = textColor
        self.textFont = pygame.font.SysFont('arial', 20)
        self.size = size

    def draw(self):
        self.suface.blit(self.img, self.position)
        t = self.textFont.render(self.text, True, self.textColor)
        hw, hh = int(t.get_width() / 2), int(t.get_height() / 2)
        self.suface.blit(t, (self.position[0]+int(self.size[0]/2)-hw, self.position[1]+int(self.size[1]/2)-hh))

    def mouseOn(self, x, y):
        if self.position[0] <= x <= self.position[0] + self.size[0] and self.position[1] <= y <= self.position[1] + self.size[1]:
            self.img = self.imgs[1]
        else:
            self.img = self.imgs[0]
    
    def onClick(self, x, y):
        if self.position[0] <= x <= self.position[0] + self.size[0] and self.position[1] <= y <= self.position[1] + self.size[1]:
            self.action()

class ButtonOffOn(ButtonText):
    def __init__(self, surface, position, action, imgs, state, text="", textFont=None, textColor=(255, 0, 0), size=(90, 50)):
        super().__init__(surface, position, action, imgs, text=text, textFont=textFont, textColor=textColor, size=size)
        self.state = state
        if not self.state:
            x = self.imgs[0]
            self.imgs[0] = self.imgs[2]
            self.imgs[2] = x

    def onClick(self, x, y):
        if self.position[0] <= x <= self.position[0] + self.size[0] and self.position[1] <= y <= self.position[1] + self.size[1]:
            x = self.imgs[0]
            self.imgs[0] = self.imgs[2]
            self.imgs[2] = x
            self.state = not self.state
            self.action()

class Game:
    def __init__(self, master, player1, player2, side, client, clWhite, clBlack):
        pygame.init()
        self.master = master
        self.player1 = player1
        self.player2 = player2
        self.myTime = 0
        self.enemyMove = []
        self.dangerLocation = []
        self.MSG = ""
        self.endgameMsg = ""
        self.isAnimation = []
        self.conn = client.conn
        self.colorWhite = clWhite
        self.colorBlack = clBlack
        self.side = side
        self.gameStates = []
        self.timeLimit = int(master.setTimeLimit.get())
        self.image_names = ("white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_pawn",
                        "black_pawn", "black_rook", "black_knight", "black_bishop", "black_queen", "black_king")
        self.image_dict = {}
        self.t_x, self.t_y = 135, 135
        self.screen_size = (750, 750)
        pygame.display.set_icon(pygame.image.load("image/UI/logo.ico"))
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Cờ vua")
        self.serverListenThread = threading.Thread(target=hander_server_gameControl, args=(self,))

        if side == "white":
            self.beginTime = round(time.time())
            self.draw_reverse = False
            self.turn = True
            self.MSG = "Your turn"
        else:
            self.beginTime = None
            self.draw_reverse = True
            self.turn = False

        self.running = True

        self.select_location = []
        self.font1 = pygame.font.SysFont('arial', 50)
        self.font2 = pygame.font.SysFont('arial', 25)
        self.name1 = self.font1.render("Name: "+self.player1, True, (0, 255, 0))
        self.name2 = self.font1.render("Name: "+self.player2, True, (0, 255, 0))

        self.setup_image()
        self.setup_sound()
        self.table_matrix = [[Rook("black",[0,0]), Knight("black",[0,1]), Bishop("black",[0,2]), Queen("black",[0,3]), King("black",[0,4]), Bishop("black",[0,5]), Knight("black",[0,6]), Rook("black",[0,7])],
                        [Pawn("black",[1,0]), Pawn("black",[1,1]), Pawn("black",[1,2]), Pawn("black",[1,3]), Pawn("black",[1,4]), Pawn("black",[1,5]), Pawn("black",[1,6]), Pawn("black",[1,7])],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [Pawn("white",[6,0]), Pawn("white",[6,1]), Pawn("white",[6,2]), Pawn("white",[6,3]), Pawn("white",[6,4]), Pawn("white",[6,5]), Pawn("white",[6,6]), Pawn("white",[6,7])],
                        [Rook("white",[7,0]), Knight("white",[7,1]), Bishop("white",[7,2]), Queen("white",[7,3]), King("white",[7,4]), Bishop("white",[7,5]), Knight("white",[7,6]), Rook("white",[7,7])]]

    def animationPiece(self, froM, to, imgPiece):
        animationThread = threading.Thread(target=movingAnimation, args=(self, froM, to, imgPiece,))
        animationThread.start()

    def getState(self):
        state = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(0, 8):
            for j in range(0, 8):
                if self.table_matrix[i][j] != 0:
                    if self.table_matrix[i][j].getSide() == "white":
                        state[i][j] = self.table_matrix[i][j].point
                    else:
                        state[i][j] = self.table_matrix[i][j].point * -1
        return state

    def checkEnd(self):
        # you lose return true else return false
        # king been eaten
        kingName = self.side+"_king"
        not_find_king = True
        for row in self.table_matrix:
            for piece in row:
                if piece != 0:
                    if piece.getName() == kingName:
                        not_find_king = False
                        x, y = piece.locate
        if not_find_king:
            self.endgameMsg = "Bạn thua, mất vua"
            self.conn.send("ENDGM".encode(FORMAT))
            return True
        # checkmate
        allEnemyMoveable = getAllEnemyMove(self.table_matrix, self.side)
        if [x, y] in allEnemyMoveable:
            # you are being checkmated right now
            self.dangerLocation.append([x, y])
            for row in self.table_matrix:
                for piece in row:
                    if piece != 0:
                        if piece.getOnlyName() == "king" and piece.side != self.side:
                            enemyKingPos = piece.getLocate()
                            break
            allMyMoveable = getAllMyMove(self.table_matrix, self.side)
            # enemy king not being checkmated by you?
            if enemyKingPos not in allMyMoveable:
                kingBeEat = []
                # can use other piece to block the checkmate?
                for row in self.table_matrix:
                    for myPiece in row:
                        if myPiece != 0:
                            if myPiece.getSide() == self.side and myPiece.getOnlyName() != 'king':
                                myPiece.predictMove(self.table_matrix)
                                myPieceMoves = myPiece.moveable
                                for myPieceMove in myPieceMoves:
                                    matrix_copy = cloneMatrix(self.table_matrix)
                                    locPiece = myPiece.getLocate()
                                    matrix_copy[locPiece[0]][locPiece[1]].move(myPieceMove, matrix_copy)
                                    allEnemyMoveable = getAllEnemyMove(matrix_copy, self.side)
                                    if [x, y] in allEnemyMoveable:
                                        kingBeEat.append(True)
                                    else:
                                        kingBeEat.append(False)
                # can move king to other pos to not be checkmate
                allEnemyMoveable = getAllEnemyMove(self.table_matrix, self.side)
                self.table_matrix[x][y].predictMove(self.table_matrix)
                kingMove = self.table_matrix[x][y].moveable
                for l in kingMove:
                    if l in allEnemyMoveable:
                        kingBeEat.append(True)
                        self.dangerLocation.append(l)
                    else:
                        kingBeEat.append(False)
                if False not in kingBeEat:
                    self.clear_moveable_step()
                    self.endgameMsg = "Bạn thua, bị chiếu hết"
                    self.conn.send("ENDGM".encode(FORMAT))
                    return True
        else:
            myPiece = 0
            for row in self.table_matrix:
                for piece in row:
                    if piece != 0:
                        if piece.getSide() == self.side:
                            myPiece += 1
            if myPiece == 0:
                c = 0
                allEnemyMoveable = getAllEnemyMove(self.table_matrix, self.side)
                self.table_matrix[x][y].predictMove(self.table_matrix)
                kingMove = self.table_matrix[x][y].moveable
                for l in kingMove:
                    if l in allEnemyMoveable:
                        c += 1
                        self.dangerLocation.append(l)
                if c == len(kingMove):
                    self.endgameMsg = "Hòa, bạn không còn nước đi nào hợp lệ"
                    self.conn.send("DRAW1".encode(FORMAT))
                    return True
        self.clear_moveable_step()
        # Threefold repetition
        state = self.getState()
        c = 0
        for s in self.gameStates:
            if s == state:
                c += 1
            if c == 2:
                # a state repeat 3 times => draw
                self.endgameMsg = "Hòa, một thế cờ lặp lại 3 lần"
                self.conn.send("DRAW2".encode(FORMAT))
                return True
        self.gameStates.append(state)
        
        return False

    def surrender(self):
        if (self.turn):
            t = round(time.time()) - self.beginTime
            self.conn.send("SURDE".encode(FORMAT))
            self.endgameMsg = "Bạn đã đầu hàng"
            send_message(self.conn, encode_message([str(t)], [3]))
            self.running = False
        else:
            self.MSG = "You can only surender in your turn"
    
    def clickSurrender(self):
        answer = tkinter.messagebox.askquestion("Thoát", "Bạn có chắc muốn đầu hàng?")
        if answer == "yes":
            self.surrender()

    def endGame(self):
        while True:
            if self.isAnimation == []:
                mess = removeSpace(recv_message(self.conn, [2, 2, 4, 2]))
                EndGameScreen(self.endgameMsg, int(mess[0]), int(mess[1]), int(mess[2]), int(mess[3]), self.master.point)
                pygame.quit()
                break

    def setup_image(self):
        self.btnImgs = [pygame.image.load("image/UI/button.png"), pygame.image.load("image/UI/button2.png")]
        self.btnImgs2 = [pygame.image.load("image/UI/button.png"), pygame.image.load("image/UI/button2.png"), pygame.image.load("image/UI/button3.png")]
        self.image_dict.clear()
        for image_name in self.image_names:
            self.image_dict.update({image_name: pygame.image.load("image/piece/"+self.master.setFileImage+"/"+image_name+".png")})

    def setup_sound(self):
        self.sounds = []
        self.sounds.append(pygame.mixer.Sound("music/sound1.wav"))
        self.sounds.append(pygame.mixer.Sound("music/sound2.wav"))
        self.sounds.append(pygame.mixer.Sound("music/sound3.wav"))
        self.sounds.append(pygame.mixer.Sound("music/sound4.wav"))
        self.sounds[0].set_volume(float(self.master.soundVol/100))
        self.sounds[1].set_volume(float(self.master.soundVol/100))
        self.sounds[2].set_volume(float(self.master.soundVol/100))
        self.sounds[3].set_volume(float(self.master.soundVol/100))

    def clear_moveable_step(self):
        for row in self.table_matrix:
            for pie in row:
                if pie != 0:
                    pie.clearMove()

    def draw_piece(self):
        for i in range (0, 8):
            for j in range (0, 8):
                if self.table_matrix[i][j] != 0 and [i, j] not in self.isAnimation:
                    if self.draw_reverse:
                        self.screen.blit(self.image_dict[self.table_matrix[i][j].getName()], (-1 * (j - 7) * 60 + self.t_x, -1 * (i - 7) * 60 + self.t_y, 60, 60))
                    else:
                        self.screen.blit(self.image_dict[self.table_matrix[i][j].getName()], (j * 60 + self.t_x, i * 60 + self.t_y, 60, 60))

    def draw_table(self):
        # full size (480, 480)
        # draw table square
        for i in range(0, 8):
            for j in range(0, 8):
                if ((i%2==0 and j%2==0) or (i%2!=0 and j%2!=0)): 
                    cl = self.colorWhite#(255, 204, 153)
                else:
                    cl = self.colorBlack#(0, 255, 0)
                pygame.draw.rect(self.screen, cl, (i * 60 + self.t_x, j * 60 + self.t_y, 60, 60))
        # draw moving step square
        for x in range(0, 8):
            for y in range(0, 8):
                if self.table_matrix[x][y] != 0:
                    if self.table_matrix[x][y].moveable != []:
                        if self.draw_reverse:
                            for step_ma in self.table_matrix[x][y].moveable:
                                if len(step_ma) == 2:
                                    pygame.draw.rect(self.screen, (102,204,255), ( -1 * (step_ma[1] - 7) * 60 + self.t_x + 5, -1 * (step_ma[0] - 7) * 60 + self.t_y + 5, 50, 50))
                                else:
                                    pygame.draw.rect(self.screen, (102,204,255), ( -1 * (step_ma[1] - 7) * 60 + self.t_x + 5, -1 * (step_ma[0] - 7) * 60 + self.t_y + 5, 50, 50))
                                    pygame.draw.rect(self.screen, (204,136,0), ( -1 * (step_ma[3] - 7) * 60 + self.t_x + 5, -1 * (step_ma[2] - 7) * 60 + self.t_y + 5, 50, 50))
                                    pygame.draw.rect(self.screen, (204,136,0), ( -1 * (step_ma[5] - 7) * 60 + self.t_x + 5, -1 * (step_ma[4] - 7) * 60 + self.t_y + 5, 50, 50))
                        else:
                            for step_ma in self.table_matrix[x][y].moveable:
                                if len(step_ma) == 2:
                                    pygame.draw.rect(self.screen, (102,204,255), (step_ma[1] * 60 + self.t_x + 5, step_ma[0] * 60 + self.t_y + 5, 50, 50))
                                else:
                                    pygame.draw.rect(self.screen, (102,204,255), (step_ma[1] * 60 + self.t_x + 5, step_ma[0] * 60 + self.t_y + 5, 50, 50))
                                    pygame.draw.rect(self.screen, (204,136,0), (step_ma[3] * 60 + self.t_x + 5, step_ma[2] * 60 + self.t_y + 5, 50, 50))
                                    pygame.draw.rect(self.screen, (204,136,0), (step_ma[5] * 60 + self.t_x + 5, step_ma[4] * 60 + self.t_y + 5, 50, 50))
        # draw enemy move
        if self.enemyMove != []:
            for step in self.enemyMove:
                if self.draw_reverse:
                    pygame.draw.rect(self.screen, (0,48,143), ( -1 * (step[1] - 7) * 60 + self.t_x + 8, -1 * (step[0] - 7) * 60 + self.t_y + 8, 44, 44))
                else:
                    pygame.draw.rect(self.screen, (0,48,143), (step[1] * 60 + self.t_x + 8, step[0] * 60 + self.t_y + 8, 44, 44))
        # draw danger location for king
        if self.dangerLocation != []:
            for location in self.dangerLocation:
                if self.draw_reverse:
                    pygame.draw.rect(self.screen, (255,51,51), ( -1 * (location[1] - 7) * 60 + self.t_x + 5, -1 * (location[0] - 7) * 60 + self.t_y + 5, 50, 50))
                else:
                    pygame.draw.rect(self.screen, (255,51,51), (location[1] * 60 + self.t_x + 5, location[0] * 60 + self.t_y + 5, 50, 50))

    def run(self):
        self.serverListenThread.start()
        self.btnSur = ButtonText(self.screen, (640, 400), self.clickSurrender, self.btnImgs, text="Surrender", textColor=(204,230,255))
        self.btnVol = ButtonOffOn(self.screen, (640, 540), self.master.pauseMusic, self.btnImgs2, self.master.pause, text="Music", textColor=(204,230,255))
        while self.running:
            M_x, M_y = pygame.mouse.get_pos()
            self.btnSur.mouseOn(M_x, M_y)
            self.btnVol.mouseOn(M_x, M_y)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.btnSur.onClick(M_x, M_y)
                    self.btnVol.onClick(M_x, M_y)
                if event.type == pygame.MOUSEBUTTONDOWN and self.select_location == [] and self.turn:
                    x, y = event.pos
                    x -= self.t_x
                    y -= self.t_y
                    x //= 60
                    y //= 60
                    if self.draw_reverse:
                        x = -1 * (x - 7)
                        y = -1 * (y - 7)
                    try:
                        x, y = y, x
                        if self.table_matrix[x][y] != 0:
                            if self.table_matrix[x][y].side == self.side:
                                self.clear_moveable_step()
                                self.table_matrix[x][y].predictMove(self.table_matrix)
                                self.select_location = [x, y]
                            else:
                                self.clear_moveable_step()
                        else:
                            self.clear_moveable_step()
                    except:
                        pass
                elif event.type == pygame.MOUSEBUTTONDOWN and self.select_location != [] and self.turn:
                    x, y = event.pos
                    x -= self.t_x
                    y -= self.t_y
                    x //= 60
                    y //= 60
                    if self.draw_reverse:
                        x = -1 * (x - 7)
                        y = -1 * (y - 7)
                    x, y = y, x
                    for step in self.table_matrix[self.select_location[0]][self.select_location[1]].moveable:
                        if x == step[0] and y == step[1]:
                            t = round(time.time()) - self.beginTime
                            self.beginTime = None
                            imgPiece = self.image_dict[self.table_matrix[self.select_location[0]][self.select_location[1]].getName()]
                            move = self.table_matrix[self.select_location[0]][self.select_location[1]].moving(step, self.table_matrix)
                            # send message to server about the move "MOVIN" "UPGRA" "ROOKI"
                            #mess = encode_message(["MOVIN", ], [])
                            if len(move) == 4:
                                # nomal move
                                self.animationPiece(move[2], move[3], imgPiece)
                                mess = ["MOVIN"] + move[0:2] + move[2] + move[3]
                                mess = encode_message(mess, [5, 12, 12, 1, 1, 1, 1])
                            elif len(move) == 5:
                                # upgrade move
                                self.animationPiece(move[2], move[3], imgPiece)
                                mess = ["UPGRA"] + move[0:2] + move[2] + move[3] + [move[4]]
                                mess = encode_message(mess, [5, 12, 12, 1, 1, 1, 1, 12])
                            elif len(move) == 7:
                                # rooking move
                                imgPieceRook = self.image_dict[move[4]]
                                self.animationPiece(move[2], move[3], imgPiece)
                                self.animationPiece(move[5], move[6], imgPieceRook)
                                mess = ["ROOKI"] + move[0:2] + move[2] + move[3] + [move[4]] + move[5] + move[6]
                                mess = encode_message(mess, [5, 12, 12, 1, 1, 1, 1, 12, 1, 1, 1, 1])
                            send_message(self.conn, mess)
                            send_message(self.conn, encode_message([str(t)], [3]))
                            self.MSG = ""
                            self.turn = False
                            self.screen = pygame.display.set_mode(self.screen_size)
                            self.enemyMove.clear()
                            self.dangerLocation.clear()
                    self.select_location.clear()
                elif event.type == pygame.QUIT:
                    answer = tkinter.messagebox.askquestion("Thoát", "Bạn có chắc muốn rời đi? Việc rời đi sẽ coi như bạn đầu hàng")
                    if answer == "yes":
                        self.surrender()
            self.screen.fill((96, 96, 96))
            self.draw_table()
            self.draw_piece()
            self.btnSur.draw()
            self.btnVol.draw()
            if self.beginTime != None:
                self.time = round(time.time()) - self.beginTime
                self.screen.blit(self.font1.render(" Time: "+str(self.time), True, (0, 255, 0)), (0, 0))
                if self.time >= self.timeLimit:
                    # surrender if time out of time limit
                    self.surrender()
            self.screen.blit(self.name1, (350, 680))
            self.screen.blit(self.name2, (350, 20))
            self.msg = self.font2.render(self.MSG, True, (0, 255, 0))
            self.screen.blit(self.msg, (375-int(self.msg.get_width() / 2), 615))
            pygame.display.update()
        self.endGame()

if __name__ == "__main__":
    EndGameScreen("sdfghjjgfdfghjjhgedfgbnh\nnjteerfvbgnhjmnhgtrde", 10, 10, 10, 10, 100)