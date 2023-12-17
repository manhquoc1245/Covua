from menu_UI import *
import tkinter.messagebox
from PIL import ImageTk, Image

theFont = ("Arial", 12)

class Login:
    def __init__(self, master, client):
        self.master = master
        self.client = client
        self.root = Tk()
        self.account = StringVar()
        self.password = StringVar()
        self.signUp = Toplevel()
        w, h = 400, 500
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        self.root.resizable(False, False)
        self.root.title("Đăng nhập")
        self.root.iconbitmap('image/UI/logo.ico')
        self.root.configure(background = "#606060")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.imgBtnLogin = PhotoImage(file="image/UI/btnSignIn.png")
        self.imgBtnSignUp = PhotoImage(file="image/UI/btnSignUp.png")
        self.imgBtnBack = PhotoImage(file="image/UI/btnBack.png")

        self.CreateSignUp()

        img = ImageTk.PhotoImage(Image.open("image/UI/logo.ico"))
        panel = Label(self.root, image=img)
        panel.pack(padx=20, pady=20)

        label1 = Label(self.root, text="Đăng nhập", font=("Arial", 24))
        label1.pack()

        self.tool = Frame(self.root)
        self.tool.configure(background = "#606060")
        self.tool.columnconfigure(0, weight=1)
        self.tool.columnconfigure(1, weight=1)
        label2 = Label(self.tool, text="Tài khoản", font=("Arial", 15), bg="#E600E6", fg="#ffffff", width=10)
        label2.grid(row=0, column=0, padx=(60, 10), pady=10)
        label3 = Label(self.tool, text="Mật khẩu", font=("Arial", 15), bg="#E600E6", fg="#ffffff", width=10)
        label3.grid(row=1, column=0, padx=(60, 10), pady=10)

        self.entry1 = Entry(self.tool, width=12, font=("Arial", 15), textvariable=self.account)
        self.entry1.grid(row=0, column=1, sticky=W)
        self.entry2 = Entry(self.tool, width=12, font=("Arial", 15), show="*", textvariable=self.password)
        self.entry2.grid(row=1, column=1, sticky=W)

        if self.client.warning != "":
            label4 = Label(self.tool, text=self.client.warning, font=theFont, bg="#FF4D6A")
            label4.grid(row=4, column=0, columnspan=2, pady=10)
            btn3 = Button(self.tool, text="Kết nối lại", font=theFont, command=self.client.connect)
            btn3.grid(row=5, column=0, columnspan=2, pady=10)
        else:
            btn1 = Button(self.tool, text="Đăng nhập", font=("Arial", 18), command=self.login, image=self.imgBtnLogin)
            btn1.grid(row=2, column=0, columnspan=2, pady=(20, 0))
            btn2 = Button(self.tool, text="Đăng ký", font=("Arial", 18), command=self.showSignUp, image=self.imgBtnSignUp)
            btn2.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.tool.pack(fill="x")

        self.root.mainloop()
            

    def login(self):
        self.warning = ""
        account = self.entry1.get()
        password = self.entry2.get()
        mess = encode_message(["ACESS", account, password], [5, 15, 20])
        send_message(self.client.conn, mess)
        mess = self.client.conn.recv(5).decode(FORMAT)
        if mess == "ALLOW":
            mess = recv_message(self.client.conn, [15, 10, 10])
            mess = removeSpace(mess)
            self.root.destroy()
            self.master.allowLogin(mess[0], mess[1], mess[2])
        elif mess == "DENI1":
            tkinter.messagebox.showwarning(title="Thông báo", message="Không tìm thấy tài khoản")
        elif mess == "DENI2":
            tkinter.messagebox.showwarning(title="Thông báo", message="Sai mật khẩu")
        elif mess == "DENI3":
            tkinter.messagebox.showwarning(title="Thông báo", message="Tài khoản đang được sử dụng")

    def showSignUp(self):
        self.account.set("")
        self.password.set("")
        self.signUp.deiconify()

    def CreateSignUp(self):
        w, h = 400, 500
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.signUp.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        self.signUp.resizable(False, False)
        self.signUp.title("Đăng ký")
        self.signUp.configure(background = "#606060")

        label1 = Label(self.signUp, text="Đăng ký", font=("Arial", 24))
        label1.pack(pady=(50, 10))

        tool = Frame(self.signUp)

        tool.columnconfigure(0, weight=1)
        tool.columnconfigure(1, weight=1)
        tool.configure(background = "#606060")
        label2 = Label(tool, text="Tài khoản", font=("Arial", 15), bg="#E600E6", fg="#ffffff", width=10)
        label2.grid(row=0, column=0, padx=(60, 10), pady=10)
        label3 = Label(tool, text="Mật khẩu", font=("Arial", 15), bg="#E600E6", fg="#ffffff", width=10)
        label3.grid(row=1, column=0, padx=(60, 10), pady=10)

        self.signUp.entry1 = Entry(tool, width=12, font=("Arial", 15), textvariable=self.account)
        self.signUp.entry1.grid(row=0, column=1, sticky=W)
        self.signUp.entry2 = Entry(tool, width=12, font=("Arial", 15), textvariable=self.password)
        self.signUp.entry2.grid(row=1, column=1, sticky=W)

        btn1 = Button(tool, text="Đăng ký", font=("Arial", 18), command=self.createAccount, image=self.imgBtnSignUp)
        btn1.grid(row=2, column=0, columnspan=2, pady=(40, 0))
        btn2 = Button(tool, text="Quay lại", font=("Arial", 18), command=self.goBack, image=self.imgBtnBack)
        btn2.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        tool.pack(fill="x")
        self.signUp.withdraw()

    def createAccount(self):
        if len(self.account.get()) == 0:
            tkinter.messagebox.showwarning("Thông báo", "Nhập đầy đủ tên tài khoản")
            self.signUp.deiconify()
        elif len(self.password.get()) == 0:
            tkinter.messagebox.showwarning("Thông báo", "Nhập đầy đủ mật khẩu")
            self.signUp.deiconify()
        elif len(self.account.get()) > 15:
            tkinter.messagebox.showwarning("Thông báo", "Tên tài khoản không nhiều hơn 15 ký tự")
            self.signUp.deiconify()
        elif len(self.password.get()) > 20:
            tkinter.messagebox.showwarning("Thông báo", "Mật khẩu không nhiều hơn 20 ký tự")
            self.signUp.deiconify()
        else:
            send_message(self.client.conn, encode_message(["CREAT", self.account.get(), self.password.get(),], [5, 15, 20]))
            mess = self.client.conn.recv(5).decode(FORMAT)
            if mess == "EXIST":
                tkinter.messagebox.showwarning("Thông báo", "Tài khoản đã được đăng ký, hãy chọn tên tài khoản khác")
                self.signUp.deiconify()
            else:
                self.account.set("")
                self.password.set("")
                tkinter.messagebox.showinfo("Thông báo", "Tài khoản đã được tạo thành công")
                self.signUp.withdraw()

    def goBack(self):
        self.account.set("")
        self.password.set("")
        self.signUp.withdraw()

    def exit(self):
        try:
            self.client.disconnect()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    pass
