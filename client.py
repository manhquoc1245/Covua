import socket

FORMAT = 'utf-8'

def encode_message(message, lenght_list):
    encode_list = []
    for m, l in zip(message, lenght_list):
        m = str(m)
        while len(m) < l:
            m += " "
        encode_list.append(m.encode(FORMAT))
    return encode_list

def send_message(conn, message):
    for m in message:
        conn.send(m)

def recv_message(conn, lenght_list):
    mess_list = []
    for i in lenght_list:
        info = conn.recv(i).decode(FORMAT) #info = conn.recv(LENGHT).decode(FORMAT); don't need message input
        mess_list.append(info)
    return mess_list

def removeSpace(mess):
    for x in range(0, len(mess)):
        l = len(mess[x])
        for i in range(0, l):
            if mess[x][i] == " ":
                mess[x] = mess[x][0:i]
                break
    return mess

class Client:
    def __init__(self, server, port):
        self.PORT = port
        self.SERVER = server
        self.connect()

    def connect(self):
        self.warning = ""
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((self.SERVER, self.PORT))
        except Exception as e:
            self.warning += f"Can't connect to server {self.SERVER}"

    def disconnect(self):
        self.conn.send("DICON".encode(FORMAT))
        self.conn.close()

if __name__ == "__main__":
    x = Client("0.tcp.ap.ngrok.io", 17482)
    x.disconnect()
