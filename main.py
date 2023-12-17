from tkinter import *
from login_UI import *
from menu_UI import *
from client import *

class Program:
    def __init__(self):
        with open("setting.txt", "r") as file:
            self.setting = {}
            lines = file.readlines()
            for line in lines:
                line = line.replace("\n", "")
                line = line.split(":")
                self.setting.update({line[0]:line[1]})
        self.client = Client(self.setting["server"], int(self.setting["port"])) #"192.168.1.103", 5050
        self.login = Login(self, self.client)

    def allowLogin(self, name, id, point):
        self.menu = Menu(self.client, name, id, point, self.setting)

if __name__ == "__main__":
    Program()