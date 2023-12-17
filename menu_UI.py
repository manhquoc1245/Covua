from tkinter import *
import tkinter.messagebox, random, threading, os
from tkinter import ttk
from PIL import ImageTk, Image
from game import *
from pygame import mixer
# test
from client import *

theFont = ("Arial", 12)

def rgb_to_hex(rgb):
    r = str(hex(rgb[0])[2:])
    if len(r) == 1: r = '0'+r
    g = str(hex(rgb[1])[2:])
    if len(g) == 1: g = '0'+g
    b = str(hex(rgb[2])[2:])
    if len(b) == 1: b = '0'+b
    return "#"+r+g+b

class Menu:
    def __init__(self, client, name, id, point, setting):
        self.client = client
        self.save = setting
        # user info
        self.name = name
        self.id = id
        self.point = point
        # music
        pygame.mixer.init()
        self.musics = []
        self.music = mixer.music
        self.pause = True
        self.pauseS = True
        self.musicVol = int(self.save["musicVol"])
        self.soundVol = int(self.save["soundVol"])
        self.soundBtn = mixer.Sound("music/buttonSound.mp3")
        self.music.set_volume(self.musicVol/100)
        self.soundBtn.set_volume(self.soundVol/100)
        # UI
        self.root = Tk()
        self.setting = Toplevel()
        img = Image.open("image/UI/logo.png")
        #btnImg = PhotoImage("image/UI/menu_button.png")
        photo = ImageTk.PhotoImage(image=img)
        # game setting
        self.setTimeLimit = StringVar()
        self.setTimeLimit.set(self.save["timeLimit"])
        if self.save["music"] == "on":
            self.pause = False
        if self.save["sound"] == "on":
            self.pauseS = False
        self.listFolderImage = os.listdir('image/piece')
        self.setFileImage = self.save["imgFolder"]
        self.locateFolder = self.listFolderImage.index(self.setFileImage)
        self.imgPawns = []
        self.loadImgPawn()
        # self.loadImgBtn()
        self.W_R = int(self.save["W_R"])
        self.W_G = int(self.save["W_G"])
        self.W_B = int(self.save["W_B"])
        self.B_R = int(self.save["B_R"])
        self.B_G = int(self.save["B_G"])
        self.B_B = int(self.save["B_B"])

        self.setupSetting()
        w, h = 500, 400
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2) - 50
        self.root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        self.root.resizable(False, False)
        self.root.title("Cờ vua")
        self.root.iconbitmap('image/UI/logo.ico')
        self.root.configure(background = "#606060")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        # menu
        self.imgLogo = Label(self.root, image=photo)
        self.imgLogo.pack(padx=10, pady=(10, 30))
        self.btnPlay = Button(self.root, text="Chơi", font=theFont, command=self.beginGame, width=10, bg="#60a80d")
        self.btnPlay.pack(padx=10, pady=10)
        self.btnSetting = Button(self.root, text="Cài đặt", font=theFont, command=self.openSetting, width=10, bg="#60a80d")
        self.btnSetting.pack(padx=10, pady=10)
        self.btnExit = Button(self.root, text="Thoát", font=theFont, command=self.close, width=10, bg="#60a80d")
        self.btnExit.pack(padx=10, pady=10)

        self.finding = False
        self.loadMusic()
        if self.pause:
            self.music.pause()
    
        self.root.mainloop()

    def beginGame(self):
        if not self.pauseS:
            self.soundBtn.play()
        if not self.finding:
            send_message(self.client.conn, encode_message(["GAMEB", self.setTimeLimit.get()], [5, 3]))
            self.btnStop = Button(self.root, text="Dừng tìm", font=theFont, command=self.stopSearch)
            self.btnStop.pack(padx=10, pady=10)
            startGameThread = threading.Thread(target=self.startGame)
            if self.finding == False:
                startGameThread.start()
                self.finding = True

    def startGame(self):
        mess = self.client.conn.recv(5).decode(FORMAT)
        if mess == "GAMES":
            self.finding = False
            self.btnStop.destroy()
            mess = recv_message(self.client.conn, [15, 15, 5])
            removeSpace(mess)
            self.root.withdraw()
            Game(self, mess[0], mess[1], mess[2], client=self.client, clWhite=(self.W_R, self.W_G, self.W_B), clBlack=(self.B_R, self.B_G, self.B_B)).run()
            pygame.mixer.init()
            self.soundBtn = mixer.Sound("music/buttonSound.mp3")
            self.soundBtn.set_volume(self.soundVol/100)
            if not self.pause:
                self.playMusic()
            self.root.deiconify()
        else:
            self.finding = False
            self.btnStop.destroy()

    def stopSearch(self):
        if not self.pauseS:
            self.soundBtn.play()
        newClient = Client(self.client.SERVER, self.client.PORT)
        send_message(newClient.conn, encode_message(["USEAR", self.id, self.setTimeLimit.get()], [5, 10, 3]))
        newClient.conn.close()

    def openSetting(self):
        if not self.pause: 
            self.playMusic()
        if not self.pauseS:
            self.soundBtn.play()
        if self.finding:
            self.stopSearch()
        self.setting.deiconify()
        self.root.withdraw()

    def closeSetting(self):
        if not self.pause: 
            self.playMusic()
        if not self.pauseS:
            self.soundBtn.play()
        self.root.deiconify()
        self.setting.withdraw()

    def setupSetting(self):
        w, h = 500, 400
        ws = self.setting.winfo_screenwidth()
        hs = self.setting.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2) - 50
        self.setting.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        self.setting.resizable(False, False)
        self.setting.title("Cờ vua")
        self.setting.configure(background = "#606060")
        self.setting.protocol("WM_DELETE_WINDOW", self.exit)
        self.setting.iconbitmap('image/UI/logo.ico')
        self.setting.withdraw()

        self.settingButtonFrame = Frame(self.setting, bg="#425465")
        self.settingButtonFrame.pack(side='left')
        self.settingButtonFrame.pack_propagate(False)
        self.settingButtonFrame.configure(width=190, height=400)
        self.btnInfo = Button(self.settingButtonFrame, text="Thông tin người chơi", font=theFont, width=20, bg="#f7a51d", command=lambda: self.showSetting(self.setupSettingInfoFrame))
        self.btnInfo.pack(padx=3, pady=3)
        self.btnImg = Button(self.settingButtonFrame, text="Hình ảnh", font=theFont, width=20, bg="#f7a51d", command=lambda: self.showSetting(self.setupSettingImageFrame))
        self.btnImg.pack(padx=3, pady=3)
        self.btnMusic = Button(self.settingButtonFrame, text="Âm thanh", font=theFont, width=20, bg="#f7a51d", command=lambda: self.showSetting(self.setupSettingMusicFrame))
        self.btnMusic.pack(padx=3, pady=3)
        self.btnClose = Button(self.settingButtonFrame, text="Đóng", font=theFont, width=20, bg="#f7a51d", command=self.closeSetting)
        self.btnClose.pack(padx=3, pady=3)

        self.mainFrame = Frame(self.setting, bg="#421A65")
        self.mainFrame.pack(side='top')
        self.mainFrame.pack_propagate(False)
        self.mainFrame.configure(width=500, height=400)

    def showSetting(self, page):
        if not self.pauseS:
            self.soundBtn.play()
        for frame in self.mainFrame.winfo_children():
            frame.destroy()
        page()
    # setting player info
    def setupSettingInfoFrame(self):
        self.client.conn.send("SINFO".encode(FORMAT))
        mess = removeSpace(recv_message(self.client.conn, [10, 10]))
        rank = mess[0]
        self.point = mess[1]
        self.settingInfo = Frame(self.mainFrame, bg="#421A65")
        self.settingInfo.pack(padx=10, pady=10)

        self.imgPInfo = PhotoImage(file="image/UI/pInfo.png")
        self.playerInfo = Label(self.settingInfo, image=self.imgPInfo, bg="#421A65", width=240, height=192)
        self.playerInfo.columnconfigure(0, weight=1)
        self.playerInfo.columnconfigure(1, weight=1)
        self.playerInfo.pack(side=TOP, pady=(20, 0))
        self.nameLabel = Label(self.playerInfo, text="Name: "+self.name, font=theFont, bg="#9bacbf", fg="#2c88d6")
        self.nameLabel.grid(row=0, column=0, padx=30, pady=(50, 10))
        self.idLabel = Label(self.playerInfo, text="ID: "+self.id, font=theFont, bg="#9bacbf", fg="#2c88d6")
        self.idLabel.grid(row=0, column=1, padx=30, pady=(50, 10))
        self.pointLabel = Label(self.playerInfo, text="Điểm XP: "+self.point, font=theFont, bg="#9bacbf", fg="#2c88d6")
        self.pointLabel.grid(row=1, column=0, padx=10, pady=10)
        self.rankLabel = Label(self.playerInfo, text="Rank: "+rank, font=theFont, bg="#9bacbf", fg="#2c88d6")
        self.rankLabel.grid(row=1, column=1, padx=10, pady=10)
        level = "Người mới"
        if 2000 <= int(self.point) < 4000:
            level = "Nghiệp dư" 
        elif 4000 <= int(self.point) < 6000:
            level = "Trung cấp" 
        elif 6000 <= int(self.point) < 8000:
            level = "Chuyên gia"
        elif int(self.point) > 8000:
            level = "Bậc thầy"
        self.levelLabel = Label(self.playerInfo, text="Cấp độ: "+level, font=theFont, bg="#9bacbf", fg="#2c88d6")
        self.levelLabel.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 35))
        self.selectTimeLabel = Label(self.settingInfo, text="Giới hạn thời gian", font=theFont)
        self.selectTimeLabel.pack(padx=10, pady=10)
        self.selectTimeLimit = ttk.Combobox(self.settingInfo, textvariable=self.setTimeLimit)
        l = ["30", "60", "90", "120"]
        self.selectTimeLimit["values"] = l
        self.selectTimeLimit["state"] = "readonly"
        self.selectTimeLimit.current(l.index(self.setTimeLimit.get()))
        self.selectTimeLimit.pack(padx=10, pady=10)
    # setting image frame    
    def setupSettingImageFrame(self):
        self.settingImage = Frame(self.mainFrame, bg="#421A65")
        self.settingImage.columnconfigure(0, weight=1)
        self.settingImage.columnconfigure(1, weight=1)
        self.settingImage.columnconfigure(2, weight=1)
        self.settingImage.pack(padx=5, pady=(2, 0))
        # piece image
        self.setImgLabel = Label(self.settingImage, text="Quân cờ", font=theFont)
        self.setImgLabel.grid(row=0, column=0, columnspan=3, pady=(0,2))

        self.btnImgSelectFrame = Frame(self.settingImage, bg="#421A65")
        self.btnImgSelectFrame.grid(row=1, column=0, pady=(1,1))
        self.btnUpImgSelect = Button(self.btnImgSelectFrame, text="/\\", command=lambda: self.editImgPawn(1))
        self.btnUpImgSelect.pack(padx=(10, 70), pady=(1, 1))
        self.btnDownImgSelect = Button(self.btnImgSelectFrame, text="\\/", command=lambda: self.editImgPawn(-1))
        self.btnDownImgSelect.pack(padx=(10, 70), pady=(1, 1))

        self.imgPawn = Label(self.settingImage, image=self.imgPawns[self.locateFolder])
        self.imgPawn.grid(row=1, column=2)
        # broad white panel
        self.setImgLabel = Label(self.settingImage, text="Màu ô trắng", font=theFont)
        self.setImgLabel.grid(row=2, column=0, columnspan=2, pady=(1, 1))
        self.RGB_whitePanelFrame = Frame(self.settingImage, bg="#421A65")
        self.RGB_whitePanelFrame.grid(row=3, column=0, pady=2, columnspan=2, sticky=W+N)
        self.scaleRed_whitePanel = Scale(self.RGB_whitePanelFrame, length=220, width=8, from_=0, to=255, orient="horizontal", bg="#ff0000", command=self.editWhiteColor)
        self.scaleRed_whitePanel.pack(padx=(0,10), pady=2)
        self.scaleGreen_whitePanel = Scale(self.RGB_whitePanelFrame, length=220, width=8, from_=0, to=255, orient="horizontal", bg="#00ff00", command=self.editWhiteColor)
        self.scaleGreen_whitePanel.pack(padx=(0,10), pady=2)
        self.scaleBlue_whitePanel = Scale(self.RGB_whitePanelFrame, length=220, width=8, from_=0, to=255, orient="horizontal", bg="#0000ff", command=self.editWhiteColor)
        self.scaleBlue_whitePanel.pack(padx=(0,10), pady=2)
        self.RGB_whiteColorFrame = Frame(self.settingImage, width=20, height=100)
        self.RGB_whiteColorFrame.grid(row=3, column=2, sticky=E)
        self.scaleRed_whitePanel.set(self.W_R)
        self.scaleGreen_whitePanel.set(self.W_G)
        self.scaleBlue_whitePanel.set(self.W_B)
        self.RGB_whiteColorFrame.config(bg=rgb_to_hex((self.W_R, self.W_G, self.W_B)))

        # broad black panel
        self.setImgLabel = Label(self.settingImage, text="Màu ô đen", font=theFont)
        self.setImgLabel.grid(row=4, column=0, columnspan=2)
        self.RGB_blackPanelFrame = Frame(self.settingImage, bg="#421A65")
        self.RGB_blackPanelFrame.grid(row=5, column=0, pady=2, columnspan=2)
        self.scaleRed_blackPanel = Scale(self.RGB_blackPanelFrame, length=220, width=8, from_=0, to=255, orient="horizontal", bg="#ff0000", command=self.editBlackColor)
        self.scaleRed_blackPanel.pack(padx=(0,10), pady=2)
        self.scaleGreen_blackPanel = Scale(self.RGB_blackPanelFrame, length=220, width=8, from_=0, to=255, orient="horizontal", bg="#00ff00", command=self.editBlackColor)
        self.scaleGreen_blackPanel.pack(padx=(0,10), pady=2)
        self.scaleBlue_blackPanel = Scale(self.RGB_blackPanelFrame, length=220, width=8, from_=0, to=255, orient="horizontal", bg="#0000ff", command=self.editBlackColor)
        self.scaleBlue_blackPanel.pack(padx=(0,10), pady=2)
        self.RGB_blackColorFrame = Frame(self.settingImage, width=20, height=100)
        self.RGB_blackColorFrame.grid(row=5, column=2, sticky=E)
        self.scaleRed_blackPanel.set(self.B_R)
        self.scaleGreen_blackPanel.set(self.B_G)
        self.scaleBlue_blackPanel.set(self.B_B)
        self.RGB_blackColorFrame.config(bg=rgb_to_hex((self.B_R, self.B_G, self.B_B)))
    # setting music frame    
    def setupSettingMusicFrame(self):
        self.settingMusic = Frame(self.mainFrame, bg="#421A65")
        self.settingMusic.pack(padx=10, pady=10)
        self.btnPause = Button(self.settingMusic, font=theFont, command=self.pauseMusic)
        self.btnPause.pack(padx=10, pady=10)
        self.volMusicLabel = Label(self.settingMusic, text=str(self.musicVol), font=theFont)
        self.volMusicLabel.pack(padx=10, pady=10)
        self.scaleMusic = Scale(self.settingMusic, orient='horizontal', command=self.updateVolume, showvalue=0, width=10, length=250)
        self.scaleMusic.set(self.musicVol)
        self.scaleMusic.pack(padx=10, pady=10)
        if self.pause:
            self.btnPause.config(text="Bật âm thanh")
            self.scaleMusic.configure(state='disabled')
        else:
            self.btnPause.config(text="Tắt âm thanh")
        self.btnPauseSound = Button(self.settingMusic, font=theFont, command=self.pauseSound)
        self.btnPauseSound.pack(padx=10, pady=10)
        self.volSoundLabel = Label(self.settingMusic, text=str(self.soundVol), font=theFont)
        self.volSoundLabel.pack(padx=10, pady=10)
        self.scaleSound = Scale(self.settingMusic, orient='horizontal', command=self.updateSound, showvalue=0, width=10, length=250)
        self.scaleSound.set(self.soundVol)
        self.scaleSound.pack(padx=10, pady=10)
        if self.pauseS:
            self.btnPauseSound.config(text="Bật tiếng")
            self.soundBtn.set_volume(self.soundVol/100)
            self.scaleMusic.configure(state='disabled')
        else:
            self.btnPauseSound.config(text="Tắt tiếng")

    def loadMusic(self):
        mixer.init()
        self.musics = ["music/music1.mp3", "music/music2.mp3", "music/music3.mp3", "music/music4.mp3", "music/music5.mp3"]
        self.playMusic()

    def playMusic(self):
        self.music.unload()
        self.music.load(self.musics[random.randint(0, len(self.musics)-1)])
        self.music.play(-1)
    
    def updateVolume(self, v):
        self.volMusicLabel.config(text=v)
        self.music.set_volume(int(v)/100)

    def updateSound(self, v):
        self.volSoundLabel.config(text=v)
        self.soundBtn.set_volume(int(v)/100)
        self.soundVol = int(v)

    def pauseMusic(self):
        if self.pause:
            self.pause = False
            self.music.unpause()
            try:
                self.scaleMusic.configure(state='normal')
                self.btnPause.config(text="Tắt âm thanh")
            except:
                pass
        else:
            self.pause = True
            self.music.pause()
            try:
                self.scaleMusic.configure(state='disabled')
                self.btnPause.config(text="Bật âm thanh")
            except:
                pass
    
    def pauseSound(self):
        if self.pauseS:
            self.pauseS = False
            self.soundVol = 50
            self.scaleSound.set(50)
            self.scaleSound.configure(state='normal')
            self.btnPauseSound.config(text="Tắt tiếng")
        else:
            self.pauseS = True
            self.soundVol = 0
            self.scaleSound.configure(state='disabled')
            self.scaleSound.set(0)
            self.btnPauseSound.config(text="Bật tiếng")

    def loadImgPawn(self):
        for folder in self.listFolderImage:
            img = Image.open("image/piece/"+folder+"/white_pawn.png")
            photo = ImageTk.PhotoImage(image=img)
            self.imgPawns.append(photo)

    def editImgPawn(self, s):
        self.locateFolder += s
        if self.locateFolder < 0: self.locateFolder = len(self.imgPawns)-1
        if self.locateFolder > len(self.imgPawns)-1: self.locateFolder = 0
        self.setFileImage = self.listFolderImage[self.locateFolder]
        self.imgPawn.config(image=self.imgPawns[self.locateFolder])

    def editWhiteColor(self, v):
        self.W_R = int(self.scaleRed_whitePanel.get())
        self.W_G = int(self.scaleGreen_whitePanel.get())
        self.W_B = int(self.scaleBlue_whitePanel.get())
        self.RGB_whiteColorFrame.config(bg=rgb_to_hex((self.W_R, self.W_G, self.W_B)))

    def editBlackColor(self, v):
        self.B_R = int(self.scaleRed_blackPanel.get())
        self.B_G = int(self.scaleGreen_blackPanel.get())
        self.B_B = int(self.scaleBlue_blackPanel.get())
        self.RGB_blackColorFrame.config(bg=rgb_to_hex((self.B_R, self.B_G, self.B_B)))

    def exit(self):
        answer = tkinter.messagebox.askquestion("Thoát", "Bạn có chắc muốn rời đi?")
        if answer == "yes":
            self.close()

    def close(self):
        if self.finding:
            self.stopSearch()
        if not self.finding:
            if self.pause: 
                self.save["music"]="off" 
            else: self.save["music"]="on"
            if self.pauseS:
                self.save["sound"]="off"
            else: self.save["sound"]="on"
            self.save["musicVol"]=self.musicVol
            self.save["soundVol"]=self.soundVol
            self.save["timeLimit"]=self.setTimeLimit.get()
            self.save["imgFolder"]=self.setFileImage
            self.save["W_R"]=self.W_R
            self.save["W_G"]=self.W_G
            self.save["W_B"]=self.W_B
            self.save["B_R"]=self.B_R
            self.save["B_G"]=self.B_G
            self.save["B_B"]=self.B_B
            with open("setting.txt", "w") as file:
                for key in self.save:
                    file.write(key+":"+str(self.save[key])+"\n")
            try:
                self.client.disconnect()
            except:
                pass
            self.root.destroy()
        
if __name__ == "__main__":
    # test
    with open("setting.txt", "r") as file:
        setting = {}
        lines = file.readlines()
        for line in lines:
            line = line.replace("\n", "")
            line = line.split(":")
            setting.update({line[0]:line[1]})
    client = None
    Menu(client, "Demo", "21", "100", setting)