import pygame
class SelectMenu:
    def __init__(self, side):
        self.run = True
        self.side = side
        self.screen = pygame.display.set_mode((750, 500))
        self.select = ""
        img_queen = pygame.image.load("image/upgrade/"+self.side+"_queen.png")
        img_knight = pygame.image.load("image/upgrade/"+self.side+"_knight.png")
        img_bishop = pygame.image.load("image/upgrade/"+self.side+"_bishop.png")
        img_rook = pygame.image.load("image/upgrade/"+self.side+"_rook.png")

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (0<=x<=375 and 0<=y<=250):
                        #chọn queen
                        self.select = "queen"
                        self.run = False
                    elif (376<=x<=750 and 0<=y<=250):
                        #chọn knight
                        self.select = "knight"
                        self.run = False
                    elif (0<=x<=375 and 251<=y<=500):
                        #chọn bishop
                        self.select = "bishop"
                        self.run = False
                    elif (376<=x<=750 and 251<=y<=500):
                        #chọn rook
                        self.select = "rook"
                        self.run = False
            self.screen.fill((96, 96, 96))
            #self.screen.blit(img_queen, (0, 0, 200, 200))
            pygame.draw.rect(self.screen, (191,0,230), (10, 10, 355, 230), 0, 20)
            pygame.draw.rect(self.screen, (191,0,230), (385, 10, 355, 230), 0, 20)
            pygame.draw.rect(self.screen, (191,0,230), (10, 260, 355, 230), 0, 20)
            pygame.draw.rect(self.screen, (191,0,230), (385, 260, 355, 230), 0, 20)
            self.screen.blit(img_queen, (73, 10))
            self.screen.blit(img_knight, (448, 10))
            self.screen.blit(img_bishop, (73, 260))
            self.screen.blit(img_rook, (448, 260))
            pygame.display.update()

class Piece:
    def __init__(self, side, locate):
        self.name = ""          # "pawn", "king", "queen", ...
        self.side = side        # "black" or "white"
        self.locate = locate    # [x, y]
        self.moveable = []      # [[x1, y1], [x2, y2], ...]
        self.movingStep = []    # 
        self.point = 0

    def predictMove(self):
        self.clearMove()

    def move(self, newLocate, table_matrix):
        self.movingStep.clear()
        self.movingStep.append(self.getName())  # 1
        if table_matrix[newLocate[0]][newLocate[1]] != 0:
            self.movingStep.append(table_matrix[newLocate[0]][newLocate[1]].getName())   # 2
            table_matrix[newLocate[0]][newLocate[1]].delete(table_matrix)
        else:
            self.movingStep.append("none")  # 2
        self.movingStep.append(self.locate) # 3
        self.movingStep.append(newLocate)   # 4
        table_matrix[newLocate[0]][newLocate[1]] = self
        table_matrix[self.locate[0]][self.locate[1]] = 0
        self.locate = newLocate
        self.clearMove()

    def moving(self, newLocate, table_matrix):
        self.move(newLocate, table_matrix)
        # [pieceName, pieceBeenEat, oldLocate, newLocate]
        # movingStep has 4 items: 4 basic
        return self.movingStep

    def clearMove(self):
        self.moveable.clear()

    def getLocate(self):
        return self.locate
    
    def getOnlyName(self):
        return self.name
    
    def getName(self):
        return self.side + "_" + self.name
    
    def getSide(self):
        return self.side
    
    def delete(self, table_matrix):
        table_matrix[self.locate[0]][self.locate[1]] = 0

class Pawn(Piece):
    def __init__(self, side, locate):
        super().__init__(side, locate)
        self.name = "pawn"
        self.firstMove = True
        self.point = 1
    
    def clone(self):
        x = Pawn(self.side, self.locate)
        x.firstMove = self.firstMove
        return x

    def predictMoveEat(self, matrix):
        self.clearMove()
        if self.side == "white":
            x = self.locate[0]-1
            y = self.locate[1]+1
            if (0<=x<=7 and 0<=y<=7): 
                self.moveable.append([x,y])
            x = self.locate[0]-1
            y = self.locate[1]-1
            if (0<=x<=7 and 0<=y<=7):
                self.moveable.append([x,y])
        elif self.side == "black":
            x = self.locate[0]+1
            y = self.locate[1]+1
            if (0<=x<=7 and 0<=y<=7):
                self.moveable.append([x,y])
            x = self.locate[0]+1
            y = self.locate[1]-1
            if (0<=x<=7 and 0<=y<=7):
                self.moveable.append([x,y])
    
    def predictMove(self, matrix):
        self.clearMove()
        if self.side == "white":
            x = self.locate[0]-1
            y = self.locate[1]+1
            if (0<=x<=7 and 0<=y<=7): 
                if matrix[x][y] != 0:
                    if matrix[x][y].getSide() == "black":
                        self.moveable.append([x,y])
            x = self.locate[0]-1
            y = self.locate[1]-1
            if (0<=x<=7 and 0<=y<=7):
                if matrix[x][y] != 0:
                    if matrix[x][y].getSide() == "black":
                        self.moveable.append([x,y])
            x = self.locate[0]-1
            y = self.locate[1]
            if 0<=x<=7:
                if matrix[x][y] == 0:
                    self.moveable.append([x,y])
            if self.firstMove:
                x = self.locate[0]-2
                y = self.locate[1]
                if 0<=x<=7:
                    if matrix[x][y] == 0 and matrix[x+1][y] == 0:
                        self.moveable.append([x,y])
        elif self.side == "black":
            x = self.locate[0]+1
            y = self.locate[1]+1
            if (0<=x<=7 and 0<=y<=7): 
                if matrix[x][y] != 0:
                    if matrix[x][y].getSide() == "white":
                        self.moveable.append([x,y])
            x = self.locate[0]+1
            y = self.locate[1]-1
            if (0<=x<=7 and 0<=y<=7):
                if matrix[x][y] != 0:
                    if matrix[x][y].getSide() == "white":
                        self.moveable.append([x,y])
            x = self.locate[0]+1
            y = self.locate[1]
            if 0<=x<=7:
                if matrix[x][y] == 0:
                    self.moveable.append([x,y])
            if self.firstMove:
                x = self.locate[0]+2
                y = self.locate[1]
                if 0<=x<=7:
                    if matrix[x][y] == 0 and matrix[x-1][y] == 0:
                        self.moveable.append([x,y])

    def move(self, newLocate, table_matrix):
        self.firstMove = False
        super().move(newLocate, table_matrix)
    
    def moving(self, newLocate, table_matrix):
        self.move(newLocate, table_matrix)
        if self.locate[0] == 0 or self.locate[0] == 7:
            # phong hậu
            select = SelectMenu(self.side).select
            if select == "queen":
                table_matrix[self.locate[0]][self.locate[1]] = Queen(self.side, self.locate)
                self.movingStep.append(table_matrix[self.locate[0]][self.locate[1]].getOnlyName())
            elif select == "knight":
                table_matrix[self.locate[0]][self.locate[1]] = Knight(self.side, self.locate)
                self.movingStep.append(table_matrix[self.locate[0]][self.locate[1]].getOnlyName())
            elif select == "bishop":
                table_matrix[self.locate[0]][self.locate[1]] = Bishop(self.side, self.locate)
                self.movingStep.append(table_matrix[self.locate[0]][self.locate[1]].getOnlyName())
            elif select == "rook":
                table_matrix[self.locate[0]][self.locate[1]] = Rook(self.side, self.locate)
                self.movingStep.append(table_matrix[self.locate[0]][self.locate[1]].getName())
        # movingStep has 5 items: 4 basic and name of the piece that the pawn upgrade to
        return self.movingStep

class Rook(Piece):
    def __init__(self, side, locate):
        super().__init__(side, locate)
        self.name = "rook"
        self.firstMove = True
        self.point = 5
        self.save = False
    
    def clone(self):
        x = Rook(self.side, self.locate)
        x.firstMove = self.firstMove
        return x

    def predictMove(self, matrix):
        if not self.save:
            self.clearMove()
        for x in range(self.locate[0]+1, 8):
            if matrix[x][self.locate[1]] == 0:
                self.moveable.append([x, self.locate[1]])
            elif matrix[x][self.locate[1]] != 0:
                if matrix[x][self.locate[1]].getSide() !=self.side:
                    self.moveable.append([x, self.locate[1]])
                break
        for x in range(self.locate[0]-1, -1, -1):
            if matrix[x][self.locate[1]] == 0:
                self.moveable.append([x, self.locate[1]])
            elif matrix[x][self.locate[1]] != 0:
                if matrix[x][self.locate[1]].getSide() !=self.side:
                    self.moveable.append([x, self.locate[1]])
                break
        for y in range(self.locate[1]+1, 8):
            if matrix[self.locate[0]][y] == 0:
                self.moveable.append([self.locate[0], y])
            elif matrix[self.locate[0]][y] != 0:
                if matrix[self.locate[0]][y].getSide() !=self.side:
                    self.moveable.append([self.locate[0], y])
                break
        for y in range(self.locate[1]-1, -1, -1):
            if matrix[self.locate[0]][y] == 0:
                self.moveable.append([self.locate[0], y])
            elif matrix[self.locate[0]][y] != 0:
                if matrix[self.locate[0]][y].getSide() !=self.side:
                    self.moveable.append([self.locate[0], y])
                break

    def moving(self, newLocate, table_matrix):
        self.firstMove = False
        return super().moving(newLocate, table_matrix)

class Knight(Piece):
    def __init__(self, side, locate):
        super().__init__(side, locate)
        self.name = "knight"
        self.point = 4

    def clone(self):
        x = Knight(self.side, self.locate)
        return x

    def predictMove(self, matrix):
        self.clearMove()
        x = self.locate[0] - 1
        y = self.locate[1] + 2
        self.checkMove(x, y, matrix)
        x = self.locate[0] - 2
        y = self.locate[1] + 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] - 2
        y = self.locate[1] - 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] - 1
        y = self.locate[1] - 2
        self.checkMove(x, y, matrix)
        x = self.locate[0] + 1
        y = self.locate[1] - 2
        self.checkMove(x, y, matrix)
        x = self.locate[0] + 2
        y = self.locate[1] - 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] + 2
        y = self.locate[1] + 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] + 1
        y = self.locate[1] + 2
        self.checkMove(x, y, matrix)
    
    def checkMove(self, x, y, matrix):
        if (0<=x<=7 and 0<=y<=7):
            if matrix[x][y] == 0:
                self.moveable.append([x, y])
            else:
                if (matrix[x][y].getSide() != self.side):
                    self.moveable.append([x, y])

class Bishop(Piece):
    def __init__(self, side, locate):
        super().__init__(side, locate)
        self.name = "bishop"
        self.point = 3
        self.save = False
    
    def clone(self):
        x = Bishop(self.side, self.locate)
        return x

    def predictMove(self, matrix):
        if not self.save:
            self.clearMove()
        for x, y in zip(range(self.locate[0]+1, 8), range(self.locate[1]+1, 8)):
            answer = self.checkMove(x, y, matrix)
            if answer == "break":
                break
        for x, y in zip(range(self.locate[0]-1, -1, -1), range(self.locate[1]+1, 8)):
            answer = self.checkMove(x, y, matrix)
            if answer == "break":
                break
        for x, y in zip(range(self.locate[0]+1, 8), range(self.locate[1]-1, -1, -1)):
            answer = self.checkMove(x, y, matrix)
            if answer == "break":
                break
        for x, y in zip(range(self.locate[0]-1, -1, -1), range(self.locate[1]-1, -1, -1)):
            answer = self.checkMove(x, y, matrix)
            if answer == "break":
                break

    def checkMove(self, x, y, matrix):
        if matrix[x][y] == 0:
            self.moveable.append([x, y])
            return "continue"
        else:
            if (matrix[x][y].getSide() != self.side):
                self.moveable.append([x, y])
            return "break"

class Queen(Bishop, Rook):
    def __init__(self, side, locate):
        super().__init__(side, locate)
        self.name = "queen"
        self.point = 9
        self.save = True

    def clone(self):
        x = Queen(self.side, self.locate)
        return x

    def predictMove(self, matrix):
        self.clearMove()
        Bishop.predictMove(self, matrix)
        Rook.predictMove(self, matrix)

class King(Piece):
    def __init__(self, side, locate):
        super().__init__(side, locate)
        self.name = "king"
        self.point = 10
        self.firstMove = True
    
    def clone(self):
        x = King(self.side, self.locate)
        x.firstMove = self.firstMove
        return x

    def predictMove(self, matrix):
        self.clearMove()
        x = self.locate[0] + 1
        y = self.locate[1]
        self.checkMove(x, y, matrix)
        x = self.locate[0] - 1
        y = self.locate[1]
        self.checkMove(x, y, matrix)
        x = self.locate[0] 
        y = self.locate[1] + 1
        self.checkMove(x, y, matrix)
        x = self.locate[0]
        y = self.locate[1] - 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] + 1
        y = self.locate[1] + 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] + 1
        y = self.locate[1] - 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] - 1
        y = self.locate[1] + 1
        self.checkMove(x, y, matrix)
        x = self.locate[0] - 1
        y = self.locate[1] - 1
        self.checkMove(x, y, matrix)
        if self.side == "white" and self.firstMove:
            if matrix[7][0] != 0:
                if matrix[7][0].getOnlyName() == "rook":
                    if matrix[7][0].firstMove and (matrix[7][1] == 0 and matrix[7][2] == 0 and matrix[7][3] == 0):
                        self.moveable.append([7,2,7,0,7,3])
            if matrix[7][7] != 0:
                if matrix[7][7].getOnlyName() == "rook":
                    if matrix[7][7].firstMove and (matrix[7][5] == 0 and matrix[7][6] == 0):
                        self.moveable.append([7,6,7,7,7,5])
        if self.side == "black" and self.firstMove:
            if matrix[0][0] != 0:
                if matrix[0][0].getOnlyName() == "rook":
                    if matrix[0][0].firstMove and (matrix[0][1] == 0 and matrix[0][2] == 0 and matrix[0][3] == 0):
                        self.moveable.append([0,2,0,0,0,3])
            if matrix[0][7] != 0:
                if matrix[0][7].getOnlyName() == "rook":
                    if matrix[0][7].firstMove and (matrix[0][5] == 0 and matrix[0][6] == 0):
                        self.moveable.append([0,6,0,7,0,5])

    def checkMove(self, x, y, matrix):
        if (0<=x<=7 and 0<=y<=7):
            if matrix[x][y] == 0:
                self.moveable.append([x, y])
            else:
                if (matrix[x][y].getSide() != self.side):
                    self.moveable.append([x, y])

    def moving(self, newLocate, table_matrix):
        self.firstMove = False
        if len(newLocate) == 2:
            return super().moving(newLocate, table_matrix)
        else:
            super().move([newLocate[0],newLocate[1]], table_matrix)
            self.movingStep.append(table_matrix[newLocate[2]][newLocate[3]].getName())
            table_matrix[newLocate[2]][newLocate[3]].move([newLocate[4], newLocate[5]], table_matrix)
            self.movingStep.append(newLocate[2:4])
            self.movingStep.append(newLocate[4:6])
            # movingStep has 7 items: 4 basic and name of the piece that the pawn upgrade to
            return self.movingStep

if __name__ == "__main__":
    x = [[Queen("white", [0, 0]), 0, 0, 0, 0, 0, Pawn("white", [0, 6]), 0], 
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, Pawn("black", [4, 6]), 0],
        [0, 0, 0, 0, Knight("white", [5, 4]), 0, 0, 0],
        [0, 0, 0, 0, 0, 0, Pawn("white", [6, 6]), 0],
        [Rook("white",[7,0]), 0, 0, 0, King("white",[7,4]), 0, 0, Rook("white",[7,7])]]
    print(x[0][0].moveable)
    x[7][0].predictMove(x)
    print(x[7][0].moveable)