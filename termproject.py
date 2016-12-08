# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random

def rgbString(red, green, blue): 
# http://www.cs.cmu.edu/~112/notes/notes-graphics.html
    return "#%02x%02x%02x" % (red, green, blue)

class Platform(object):
    objList = []
    def __init__(self):
        # load data.xyz appropriate
        self.height = 450
        self.width = 400
        self.h = 60
        self.w = 60
        self.x0 = self.width//2 - self.w
        self.x1 = self.width//2 + self.w
        self.y0 = self.height//2 +self.h
        self.y1 = self.height
        self.color = "midnight blue"
        self.topx0 = self.x0 + 20
        self.topy0 = self.y0 - 20
        self.topx1 = self.x1 + 20
        self.topy1 = self.y0 - 20
        self.rx0 = self.topx1
        self.rx1 = self.topx1
        self.ry0 = self.topy1
        self.ry1 =  self.y1 - 20

    def mousePressed(self,event):
        # use event.x and event.y
        pass

    def keyPressed(self,event):
        # use event.char and event.keysym
        pass

    def timerFired(self):
        pass

    def draw(self,canvas):
        # draw in basic rect
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1,fill=self.color,width = 0)
        # draw top face
        canvas.create_polygon(self.x0,self.y0,self.x1,self.y0,self.topx1,self.topy1,self.topx0,self.topy0,fill=self.color)
        # draw right side face
        canvas.create_polygon(self.x1,self.y0,self.x1,self.y1,self.rx1,self.ry1,self.rx0,self.ry0,fill=self.color)
        # outline platform
        canvas.create_line(self.x0,self.y0,self.x1,self.y0)
        canvas.create_line(self.x1,self.y0,self.topx1,self.topy1)
        canvas.create_line(self.x1,self.y0,self.x1,self.y1)
        for obj in Platform.objList:
            canvas.create_rectangle(obj[1],obj[2],obj[3],obj[4],fill=obj[0],width=0)
            #top face
            canvas.create_polygon(obj[1],obj[2],obj[3],obj[2],obj[7],obj[8],obj[5],obj[6],fill=obj[0],width=0)
            # right face
            canvas.create_polygon(obj[3],obj[2],obj[3],obj[4],obj[7],obj[9],obj[7],obj[8],fill=obj[0],width=0)

class MovingSlab(Platform):

    def __init__(self, speed = 5,i=0,difficulty="easy", starty0 = 270, starty1 = 285,bottomx0 = 140,bottomx1=260,width = 120,score = 0):
        super().__init__()
        self.bottomPlatx0 = bottomx0
        self.bottomPlatx1 = bottomx1
        self.bottomPlaty0 = self.y0
        self.bottomPlaty1 = self.y1
        self.height = 15
        self.width = width
        self.startx0 = 5
        self.starty0 = starty0
        self.startx1 = self.startx0 + self.width
        self.starty1 = starty1
        self.dx = speed
        self.topx1 = self.startx1 + 10
        self.topy1 = self.starty0 - 10
        self.topx0 = self.startx0 + 10
        self.topy0 = self.topy1
        self.ry1 = self.starty1 - 10
        self.score = score
        self.makeNewBlock = False
        self.colorListEasy = [ "Medium Blue","Royal Blue", "Blue", "Dodger Blue","Deep Sky Blue", "Sky Blue","Light Sky Blue","Steel Blue"]
        self.colorListMedium = [ "pink","Light pink","Pale Violet Red","Maroon","Medium Violet Red","Violet Red" ]
        self.colorListHard = ["Dim Gray","Slate Gray","Light Slate Gray","gray","Light gray"]
        if difficulty =="easy":
            self.colorList = self.colorListEasy
        elif difficulty =="medium":
            self.colorList = self.colorListMedium
        elif difficulty =="hard":
            self.colorList = self.colorListHard
        self.i = i
        self.color = self.colorList[self.i%len(self.colorList)]

        

    def checkOffPlatform(self):
        # checks if left side is not on platform
        if self.startx0 <= self.bottomPlatx0 and (self.startx1 >= self.bottomPlatx0 and self.startx1<= self.bottomPlatx1):
            self.startx0 = self.bottomPlatx0
            self.topx0 = self.startx0 + 10
            self.width = self.startx1 - self.startx0

            self.bottomPlatx0,self.bottomPlatx1 = self.startx0,self.startx1
            self.bottomPlaty0,self.bottomPlaty1 = self.starty0,self.starty1
            self.makeNewBlock = True
            
            
        # checks if right side is not on platform
        if self.startx1 >= self.bottomPlatx1 and (self.startx0 <= self.bottomPlatx1 and self.startx0 >= self.bottomPlatx0):
            self.startx1 = self.bottomPlatx1
            self.topx1 = self.startx1 + 10
            self.width = self.startx1 - self.startx0

            self.bottomPlatx0,self.bottomPlatx1 = self.startx0,self.startx1
            self.bottomPlaty0,self.bottomPlaty1 = self.starty0,self.starty1
            self.makeNewBlock = True


        # checks if block doesn't land on the platform
        elif (self.startx0 < self.bottomPlatx0 and (self.startx1 < self.bottomPlatx0)) or(self.startx1 > self.bottomPlatx1 and (self.startx0 > self.bottomPlatx1)):
            self.width = 0
            self.startx0 = 0
            self.startx1 = 0
            self.topx1 = 0
            self.topy1 = 0
            self.topx0 = 0
            self.topy0 = 0
            self.ry1 = 0

    def getNewBottomCords(self):
        return (self.bottomPlatx0,self.bottomPlatx1)

    def getWidth(self):
        return self.width

    def getScore(self):
        return self.score

        


    def mousePressed(self,event):
        # use event.x and event.y
        pass

    def keyPressed(self,event):
        # use event.char and event.keysym
        if event.keysym == "space":
            self.checkOffPlatform()
            self.dx =0
            Platform.objList.append([self.color,self.startx0,self.starty0,self.startx1,self.starty1,self.topx0,self.topy0,self.topx1,self.topy1,self.ry1])

            if self.makeNewBlock:
                self.score +=1



        if event.keysym == "Return":
            Platform.objList = []
            self.__init__();
            return

    def timerFired(self):
        self.startx0 += self.dx
        self.startx1 += self.dx
        self.topx0 += self.dx
        self.topx1 += self.dx
        if self.startx0 < 5:
            self.dx = -1*self.dx
        if self.topx1 > 400:
            self.dx = -1*self.dx


    def drawAll(self,canvas):
        # main rectangle
        canvas.create_rectangle(self.startx0,self.starty0,self.startx1,self.starty1,fill=self.color)

        # top face
        canvas.create_polygon(self.startx0,self.starty0,self.startx1,self.starty0,self.topx1,self.topy1,self.topx0,self.topy0,fill=self.color)

        # right face
        canvas.create_polygon(self.startx1,self.starty0,self.startx1,self.starty1,self.topx1,self.ry1,self.topx1,self.topy1,fill=self.color)

        #outline shape
        canvas.create_line(self.startx0,self.starty0,self.startx1,self.starty0,fill= "black")
        canvas.create_line(self.startx1,self.starty0,self.topx1,self.topy1,fill= "black")
        canvas.create_line(self.startx1,self.starty0,self.startx1,self.starty1,fill= "black")

        #draw score
        canvas.create_text(200,40,text=str(self.score),font=("Apple Chancery", 30, "bold"))

        

    






####################################
# customize these functions
####################################

def init(data):
    data.mode = "menu"
    data.platform = Platform()
    data.x = data.width//2
    data.y = 10
    data.playX = data.width//2 + 5
    data.playY = 100
    data.difficulty = "easy"
    data.backgroundColor = "white"
    data.easyWidth = 4
    data.medWidth = 0
    data.hardWidth = 0
    data.scrollUp = 20
    data.speed = 5
    data.gameOver = False
    data.baseColorEasy = "midnight blue"
    data.colorListEasy = [ "Medium Blue","Blue","Steel Blue","Royal Blue","Dodger blue","Light Sky Blue","Sky Blue"]
    data.baseColorMedium = "Hot Pink"
    data.colorListMedium = [ "pink","Light pink","Pale Violet Red","Maroon","Medium Violet Red","Violet Red" ]
    data.baseColorHard = "Dark Slate Gray"
    data.colorListHard = ["Dim Gray","Slate Gray","Light Slate Gray","gray","Light gray"]
    data.colorList = data.colorListEasy
    data.easyBackground = None
    data.mediumBackground = None
    data.hardBackground = None
    data.easyBackground = PhotoImage(file='easy.gif')
    data.mediumBackground = PhotoImage(file='medBackground.gif')
    data.hardBackground = PhotoImage(file='hardBackground.gif')
    data.Image = data.easyBackground
    data.i = 0
    data.slab = MovingSlab(data.speed,data.i,data.difficulty)
    data.highScoreEasy = 0
    data.highScoreMedium = 0
    data.highScoreHard = 0



def mousePressed(event, data):
    # use event.x and event.y
    checkMouseClick(data,event.x,event.y)

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.mode == "game":
        data.slab.keyPressed(event)
        if event.keysym == "space":
            if data.slab.starty0 < 200:
                data.platform.y0 += data.scrollUp
                data.platform.y1 += data.scrollUp
                data.platform.topy0 += data.scrollUp
                data.platform.topy1 += data.scrollUp
                data.platform.ry0 += data.scrollUp
                data.platform.ry1 += data.scrollUp

                for obj in data.platform.objList:
                    obj[2] = obj[2] + data.scrollUp
                    obj[4] = obj[4] + data.scrollUp
                    obj[6] = obj[6] + data.scrollUp
                    obj[8] = obj[8] + data.scrollUp
                    obj[9] = obj[9] + data.scrollUp

        if(data.slab.makeNewBlock):
            if data.slab.starty0 < 200:
                bottomx0,bottomx1 = data.slab.getNewBottomCords()
                width = data.slab.getWidth()
                score = data.slab.getScore()
                speed = data.speed

                data.slab = MovingSlab(speed,data.i,data.difficulty,data.slab.starty0 - 15+data.scrollUp,data.slab.starty1-15+data.scrollUp,bottomx0,bottomx1,width,score)
            else:
                bottomx0,bottomx1 = data.slab.getNewBottomCords()
                width = data.slab.getWidth()
                score = data.slab.getScore()
                speed = data.speed
                data.slab = MovingSlab(speed,data.i,data.difficulty,data.slab.starty0 - 15,data.slab.starty1-15,bottomx0,bottomx1,width,score)

        else:
            data.gameOver = True
        if event.keysym == "Return":
            data.gameOver = False
            data.i = 0
            data.platform = Platform()
            if data.difficulty =="easy":
                data.platform.color = data.baseColorEasy
            elif data.difficulty =="medium":
                data.platform.color = data.baseColorMedium
            elif data.difficulty =="hard":
                data.platform.color = data.baseColorHard
            data.slab= MovingSlab(data.speed,data.i,data.difficulty)
        

def checkMouseClick(data,x,y):
    # clicks play button
    if (x >= data.playX- 100) and (x <= data.playX+100) and (y >= data.playY - 30) and (y <= data.playY + 30):
        if data.mode != "settings":
            data.mode = "game"
        else:
            data.difficulty = "easy"
            data.easyWidth = 4
            data.medWidth = 0
            data.hardWidth = 0
            data.Image = data.easyBackground

    # clicks instructions button
    if (x >= data.playX- 100) and (x <= data.playX+100) and (y >= data.playY - 30+100) and (y <= data.playY + 30+100):
        if data.mode != "settings":
            data.mode = "help"
        else:
            data.difficulty = "medium"
            data.easyWidth = 0
            data.medWidth = 4
            data.hardWidth = 0
            data.Image = data.mediumBackground


    # clicks back
    if (x >= 5 and x <= 25) and (y >=10 and y<= 40):
        data.mode = "menu"
        data.platform = Platform()
        Platform.objList = []
        data.i = 0
        if data.difficulty == "easy":
            data.colorList = data.colorListEasy
        if data.difficulty == "medium":
            data.colorList = data.colorListMedium
        else:
            data.colorList = data.colorListHard
        data.slab = MovingSlab(data.speed,data.i,data.difficulty)

        return


    # clicks settings button
    if (x >= data.playX- 200) and (x <= data.playX+200) and (y >= data.playY - 30+200) and (y <= data.playY + 30+200):
        if data.mode != "settings":
            data.mode = "settings"
        else:
            data.difficulty = "hard"
            data.easyWidth = 0
            data.medWidth = 0
            data.hardWidth = 4
            data.Image = data.hardBackground

def changeDifficulty(data):
    if data.difficulty == "easy":
        data.slab.__init__()
        data.slab.dx = 5
        data.speed = 5
        data.colorList = data.colorListEasy
        data.platform.color = data.baseColorEasy
        return
    if data.difficulty == "medium":
        data.slab.dx = 10
        data.speed = 10
        data.colorList = data.colorListMedium
        data.platform.color = data.baseColorMedium
        data.slab.__init__(data.speed,0,data.difficulty)
        return
    if data.difficulty == "hard":
        data.slab.dx = 25
        data.speed = 25
        data.colorList = data.colorListHard
        data.platform.color = data.baseColorHard
        data.slab.__init__(data.speed,0,data.difficulty)
        return

def highScore(data):
    currScore = data.slab.getScore()
    if data.difficulty == "easy" and currScore > data.highScoreEasy:
        data.highScoreEasy = currScore
    if data.difficulty == "medium" and currScore > data.highScoreMedium:
        data.highScoreMedium = currScore
    if data.difficulty == "hard" and currScore > data.highScoreHard:
        data.highScoreHard = currScore

def timerFired(data):
    if data.mode == "game":
        data.slab.timerFired()
        highScore(data)

def drawHighScore(canvas,data):
    if data.difficulty =="easy":
        canvas.create_text(200,60,text="High Score= " + str(data.highScoreEasy),font=("Apple Chancery", 12, "bold"))
    if data.difficulty =="medium":
        canvas.create_text(200,60,text="High Score= " + str(data.highScoreMedium),font=("Apple Chancery", 12, "bold"))
    if data.difficulty =="hard":
        canvas.create_text(200,60,text="High Score= " + str(data.highScoreHard),font=("Apple Chancery", 12, "bold"))


def redrawAll(canvas, data):
    # draw in canvas
    if data.mode == "menu":
        canvas.create_image(0,0,image=data.Image,anchor=NW)
        #drawButtons(canvas,data)
        drawAll(canvas,data)
        changeDifficulty(data)
    if data.mode == "game":
        canvas.create_image(0,0,image=data.Image,anchor=NW)
        data.platform.draw(canvas)
        for obj in data.platform.objList:
            #color = data.colorList[data.i%len(data.colorList)]
            canvas.create_rectangle(obj[1],obj[2],obj[3],obj[4],fill=obj[0],width=0)
            #top face
            canvas.create_polygon(obj[1],obj[2],obj[3],obj[2],obj[7],obj[8],obj[5],obj[6],fill=obj[0],width=0)
            # right face
            canvas.create_polygon(obj[3],obj[2],obj[3],obj[4],obj[7],obj[9],obj[7],obj[8],fill=obj[0],width=0)
            #outline shape
            canvas.create_line(obj[1],obj[2],obj[3],obj[2],fill= "black")
            canvas.create_line(obj[3],obj[2],obj[7],obj[8],fill= "black")
            canvas.create_line(obj[3],obj[2],obj[3],obj[4],fill= "black")

        data.i += 1
        data.slab.drawAll(canvas)
        # draw highScore
        drawHighScore(canvas,data)
        drawBack(canvas,data)
        if data.gameOver == True:
            canvas.create_image(0,0,image=data.Image,anchor=NW)
            canvas.create_text(200,100, text="Game Over", font= "arial 25 bold",fill="red")
            canvas.create_text(220,150, text="Your Score was " + str(data.slab.score)+"!\nPress Enter to Play Again", font= "arial 12 bold")
    if data.mode == "help":
        canvas.create_image(0,0,image=data.Image,anchor=NW)
        drawBack(canvas,data)
        drawHelp(canvas,data)
    if data.mode == "settings":
        canvas.create_image(0,0,image=data.Image,anchor=NW)
        drawSettingsButtons(canvas,data)
        drawSettings(canvas,data)
        drawBack(canvas,data)
        

def drawAll(canvas,data):
    canvas.create_text(data.x,data.y,text = "3-D Stacker", font = "arial 35 bold",anchor = N,fill ="honeydew")
    canvas.create_text(data.playX,data.playY,text = "Play", font = "arial 25",fill="honeydew")
    canvas.create_text(data.playX,data.playY+100,text = "Instructions", font = "arial 25",fill="honeydew")
    canvas.create_text(data.playX,data.playY+200,text = "Settings", font = "arial 25",fill="honeydew")

def drawButtons(canvas,data):
    canvas.create_rectangle(data.playX - 100,data.playY - 30, data.playX + 100, data.playY + 30, fill= "light blue")
    canvas.create_rectangle(data.playX - 100,data.playY - 30+100, data.playX + 100, data.playY + 30+100, fill= "light blue")
    canvas.create_rectangle(data.playX - 100,data.playY - 30+200, data.playX + 100, data.playY + 30+200, fill= "light blue")

def drawBack(canvas,data):
    canvas.create_polygon(25,10,25,40,5,25,fill="black")

def drawHelp(canvas,data):
    canvas.create_text(data.x,data.y+50,text = "Instructions", font = "arial 25 bold",anchor = N,fill="honeydew")
    canvas.create_text(data.playX,data.playY+50,text = "The Goal of 3D Stacker is to stack\n the blocks as high as possible", font = "arial 17",fill="honeydew")
    canvas.create_text(data.playX+25,data.playY+100,text = "* To place a block, press Space", font = "arial 15",anchor=E,fill="honeydew")
    canvas.create_text(data.playX,data.playY+150,text = "* You earn one point for every block added to the stack\n  Your Score is displayed at the top", font = "arial 15",fill="honeydew")
    canvas.create_text(data.playX-45,data.playY+200,text = "* You can change the difficulty in Settings", font = "arial 15",fill="honeydew")

def drawSettingsButtons(canvas,data):
    canvas.create_rectangle(data.playX - 100,data.playY - 30, data.playX + 100, data.playY + 30, fill= "sky blue",width= data.easyWidth)
    canvas.create_rectangle(data.playX - 100,data.playY - 30+100, data.playX + 100, data.playY + 30+100, fill= "pink",width=data.medWidth)
    canvas.create_rectangle(data.playX - 100,data.playY - 30+200, data.playX + 100, data.playY + 30+200, fill= "grey",width = data.hardWidth)

def drawSettings(canvas,data):
    canvas.create_text(data.playX,data.playY,text = "Easy", font = "arial 25")
    canvas.create_text(data.playX,data.playY+100,text = "Medium", font = "arial 25")
    canvas.create_text(data.playX,data.playY+200,text = "Hard", font = "arial 25")


####################################
# use the run function as-is
####################################
# run function taken from
# http://www.cs.cmu.edu/~112/notes/notes-animations.html

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill="white", width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 30 # milliseconds
    #init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    init(data)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 400)