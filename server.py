import socket, threading, pyodbc, random
from client import *

player_waiting_list_30 = []
player_waiting_list_60 = []
player_waiting_list_90 = []
player_waiting_list_120 = []

player_list = []
piece_point = {"pawn": 1, "rook": 5, "bishop": 3, "knight": 3, "queen": 9}

with open("serverSetting.txt", "r") as file:
    serverSetting = {}
    lines = file.readlines()
    for line in lines:
        line = line.replace("\n", "")
        line = line.split(":")
        serverSetting.update({line[0]:line[1]})

class Player:
    def __init__(self, conn):
        self.id = None
        self.conn = conn
        self.name = ""
        self.point = 0
        self.time = 0
        self.inGamePoint = 0
        self.inGameTime = 0
        self.pointMinus = 0
        self.winPoint = 0
        self.searching = False
        self.playing = False

#database
DRIVER = '{SQL Server}'
SERVER_NAME = serverSetting['serverDatabaseName']
DATABASE_NAME = "ChessDB"

db = pyodbc.connect(
    f'DRIVER={DRIVER};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    f'Trusted_Connection=yes;'
)

def loginAccount(db, account, password):
    cursor = db.cursor()
    query = f"SELECT * FROM PlayerData WHERE Account='{account}'"
    cursor.execute(query)
    cursor = cursor.fetchall()
    if (len(cursor) > 0):
        # find account
        query = f"SELECT * FROM PlayerData WHERE Account='{account}' And Password='{password}'"
        cursor = db.cursor()
        cursor.execute(query)
        cursor = cursor.fetchall()
        if len(cursor) == 0:
            return False, "2", None, None
        if cursor[0][3] == 'True ':
            return False, "3", None, None
        return True, cursor[0][1], cursor[0][0], cursor[0][4]
    else:
        # can't find account
        return False, "1", None, None

def addPlayerToWaitingList(player, gameTimeLimit):
    if gameTimeLimit == "30":
        player_waiting_list_30.append(player)
        print(f"[PLAYER WAITING] type:30 {str(len(player_waiting_list_30))} player")
    elif gameTimeLimit == "60":
        player_waiting_list_60.append(player)
        print(f"[PLAYER WAITING] type:60 {str(len(player_waiting_list_60))} player")
    elif gameTimeLimit == "90":
        player_waiting_list_90.append(player)
        print(f"[PLAYER WAITING] type:90 {str(len(player_waiting_list_90))} player")
    elif gameTimeLimit == "120":
        player_waiting_list_120.append(player)
        print(f"[PLAYER WAITING] type:120 {str(len(player_waiting_list_120))} player")

def removeFromWaitingList(id, player_waiting_list):
    for p in player_waiting_list:
        if p.id == id:
            x = p
            x.searching = False
            x.playing = False
            x.conn.send("STOPS".encode(FORMAT))
            player_waiting_list.remove(p)
            break

def removePlayerFromWaitingList(id, gameTimeLimit):
    if gameTimeLimit == "30":
        removeFromWaitingList(id, player_waiting_list_30)
        print(f"[PLAYER WAITING] type:30 {str(len(player_waiting_list_30))} player")
    elif gameTimeLimit == "60":
        removeFromWaitingList(id, player_waiting_list_60)
        print(f"[PLAYER WAITING] type:60 {str(len(player_waiting_list_60))} player")
    elif gameTimeLimit == "90":
        removeFromWaitingList(id, player_waiting_list_90)
        print(f"[PLAYER WAITING] type:90 {str(len(player_waiting_list_90))} player")
    elif gameTimeLimit == "120":
        removeFromWaitingList(id, player_waiting_list_120)
        print(f"[PLAYER WAITING] type:120 {str(len(player_waiting_list_120))} player")

def playerGetPoint(player, piece_name):
    piece_name = piece_name[6:]
    if piece_name in list(piece_point.keys()):
        player.inGamePoint += piece_point[piece_name]

def playerOffline(player):
    cursor = db.cursor()
    query = f"UPDATE PlayerData SET Online='False' WHERE Id={player.id}"
    cursor.execute(query)
    db.commit()
    player_list.remove(player)

def updatePlayerPoint(player):
    if player.point < 0:
        player.point = 0
    cursor = db.cursor()
    query = f"UPDATE PlayerData SET Point={str(player.point)} WHERE Id={player.id}"
    cursor.execute(query)
    db.commit()

def getPlayerInfo(player):
    cursor = db.cursor()
    query = f"with r as (select ROW_NUMBER() over(order by Point desc) as Row,* from PlayerData) select * from r Where Id={player.id};"
    cursor.execute(query)
    cursor = cursor.fetchall()
    return cursor[0]

def handle_client_connect(conn, addr):
    print(f"[New connection] {addr}")
    player = Player(conn)
    connected = True
    while connected:
        if player.playing == False:
            try:
                order = conn.recv(5)
                order = order.decode(FORMAT)
                print(f"[Connect] Name:{player.name} Addred:{addr} Order:{order}")
            except:
                print("error")
            if not order:
                if player.id != None:
                    playerOffline(player)
                    print(f"[Number player online] {len(player_list)} player")
                break
            if order == "ACESS":
                # user access account
                lenght_list = [15, 20]
                mess = recv_message(conn, lenght_list)
                mess = removeSpace(mess)
                allow, x, id, point = loginAccount(db, mess[0], mess[1])
                if allow:
                    send_message(conn, encode_message(["ALLOW", x, str(id), str(point)], [5, 15, 10, 10])) # use 10 byte to send id, 10 byte to send point
                    player.name = x
                    player.id = id
                    player.point = point
                    cursor = db.cursor()
                    query = f"UPDATE PlayerData SET Online='True ' WHERE Id={player.id}"
                    cursor.execute(query)
                    db.commit()
                    player_list.append(player)
                    print(f"[Number player online] {len(player_list)} player")
                else:
                    x = "DENI" + x
                    conn.send(x.encode(FORMAT))
            elif order == "CREAT":
                # user make another account
                mess = recv_message(conn, [15, 20])
                account, password = mess
                account = removeSpace([account])[0]
                cursor = db.cursor()
                query = f"SELECT * FROM PlayerData Where Account='{account}'"
                cursor.execute(query)
                cursor = cursor.fetchall()
                if len(cursor) == 0:
                    conn.send("NNNNN".encode(FORMAT))
                    cursor = db.cursor()
                    try:
                        query = "SELECT Max(Id) FROM PlayerData"
                        cursor.execute(query)
                        id = cursor.fetchall()[0][0] + 1
                    except:
                        id = 1
                    cursor = db.cursor()
                    row = (id, account, password, "False", 0)
                    query = "INSERT INTO PlayerData VALUES (?, ?, ?, ?, ?);"
                    cursor.execute(query, row)
                    db.commit()
                    print(f"[ADD ACCOUNT] name:{account}")
                else:
                    conn.send("EXIST".encode(FORMAT))
            elif order == "GAMEB":
                # user begin a game
                player.searching = True
                gameTimeLimit = removeSpace(recv_message(conn, [3]))[0]
                addPlayerToWaitingList(player, gameTimeLimit)
                player.playing = True
            elif order == "SINFO":
                info = getPlayerInfo(player)
                send_message(player.conn, encode_message([str(info[0]), str(info[5])], [10, 10]))
            elif order == "DICON":
                # user disconnect server, 1 time use connection
                if player.id != None:
                    playerOffline(player)
                    print(f"[Number player online] {len(player_list)} player")
                connected = False
            elif order == "USEAR":
                # user stop searching, 1 time use connection
                mess = recv_message(conn, [10, 3])
                mess = removeSpace(mess)
                removePlayerFromWaitingList(int(mess[0]), mess[1])
                connected = False
    conn.close()

def feedbackPlayer(order, player1, player2):
    print(f"[ORDER] {order} from {player1.name} to {player2.name}")
    if order == "ENDGM":
        # player1 lose, player2 win
        player2.conn.send("ENDGM".encode(FORMAT))
        player2.winPoint = 30
        player1.pointMinus = 30
        return False
    elif order == "SURDE":
        # player 1 surrender, player2 win
        player1.conn.send("NNNNN".encode(FORMAT))
        player2.conn.send("SURDE".encode(FORMAT))
        player2.winPoint = 30
        player1.pointMinus = 10
        t = int(removeSpace(recv_message(player1.conn, [3]))[0])
        player1.inGameTime += t
        return False
    elif order == "DRAW1" or order == "DRAW2":
        # draw
        player2.conn.send(order.encode(FORMAT))
        player1.winPoint = 15
        player2.winPoint = 15
        return False
    elif order == "MOVIN":
        cp_mess = mess = recv_message(player1.conn, [12, 12, 1, 1, 1, 1])
        mess = [order] + mess
        mess = encode_message(mess, [5, 12, 12, 1, 1, 1, 1])
        print(mess)
        send_message(player2.conn, mess)
        cp_mess = removeSpace(cp_mess)
        playerGetPoint(player1, piece_name=cp_mess[1])
    elif order == "UPGRA":
        cp_mess = mess = recv_message(player1.conn, [12, 12, 1, 1, 1, 1, 12])
        mess = [order] + mess
        mess = encode_message(mess, [5, 12, 12, 1, 1, 1, 1, 12])
        print(mess)
        send_message(player2.conn, mess)
        cp_mess = removeSpace(cp_mess)
        playerGetPoint(player1, piece_name=cp_mess[1])
    elif order == "ROOKI":
        cp_mess = mess = recv_message(player1.conn, [12, 12, 1, 1, 1, 1, 12, 1, 1, 1, 1])
        mess = [order] + mess
        mess = encode_message(mess, [5, 12, 12, 1, 1, 1, 1, 12, 1, 1, 1, 1])
        print(mess)
        send_message(player2.conn, mess)
        cp_mess = removeSpace(cp_mess)
        playerGetPoint(player1, piece_name=cp_mess[1])
    t = int(removeSpace(recv_message(player1.conn, [3]))[0])
    print(f"Time spend: {t}")
    player1.inGameTime += t
    return True

def handle_a_game(player1, player2):
    # send mess to player client to begin the game
    send_message(player1.conn, encode_message(["GAMES", player1.name, player2.name, "white"], [5, 15, 15, 5]))
    send_message(player2.conn, encode_message(["GAMES", player2.name, player1.name, "black"], [5, 15, 15, 5]))
    playing = True
    turn = True
    while playing:
        # if game end playing = False
        if turn:
            order = player1.conn.recv(5).decode(FORMAT)
            playing = feedbackPlayer(order=order, player1=player1, player2=player2)
            turn = False
        else:
            order = player2.conn.recv(5).decode(FORMAT)
            playing = feedbackPlayer(order=order, player1=player2, player2=player1)
            turn = True
    # send end game info
    t1 = (player2.inGameTime - player1.inGameTime)//10
    t2 = (player1.inGameTime - player2.inGameTime)//10
    if t1 < 0: t1 = 0
    if t2 < 0: t2 = 0
    send_message(player1.conn, encode_message([str(player1.winPoint), str(player1.inGamePoint), str(t1), str(player1.pointMinus)], [2, 2, 4, 2]))
    send_message(player2.conn, encode_message([str(player2.winPoint), str(player2.inGamePoint), str(t2), str(player2.pointMinus)], [2, 2, 4, 2]))
    player1.point += player1.winPoint + player1.inGamePoint + player1.inGameTime//10 - player1.pointMinus
    player2.point += player2.winPoint + player2.inGamePoint + player2.inGameTime//10 - player2.pointMinus
    updatePlayerPoint(player1)
    updatePlayerPoint(player2)
    print(f"[ENDGAME] Player1:{player1.name} - Player2:{player2.name} Time:{player1.inGameTime}-{player2.inGameTime} Piece_point:{player1.inGamePoint}-{player2.inGamePoint}")
    # reset player info in-game
    player1.inGamePoint = 0
    player2.inGamePoint = 0
    player1.inGameTime = 0
    player2.inGameTime = 0
    player1.winPoint = 0
    player2.winPoint = 0
    player1.pointMinus = 0
    player2.pointMinus = 0
    player1.playing = False
    player2.playing = False

def searchingMatch(player_waiting_list):
    while True:
        l = len(player_waiting_list)
        if 0 != l != 1:
            player1 = random.randint(0, l-1)
            player2 = random.randint(0, l-1)
            if player1 != player2:
                # find a match
                player1 = player_waiting_list[player1]
                player2 = player_waiting_list[player2]
                if -500 < player1.point - player2.point <= 500:
                    player_waiting_list.remove(player1)
                    player_waiting_list.remove(player2)
                    if player1.searching == player2.searching == True:
                        gameThread = threading.Thread(target=handle_a_game, args=(player1, player2))
                        gameThread.start()

def start_server():
    server.listen()
    print(f"[Listen] {SERVER}")
    print(f"[Port] {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client_connect, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    # connect client
    PORT = int(serverSetting['port'])
    if serverSetting['localHost'] == 'yes':
        SERVER = "localhost"
    else:
        SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    cursor = db.cursor()
    query = f"UPDATE PlayerData SET Online='False'"
    cursor.execute(query)
    db.commit()
    print(f"[Server start] {SERVER}")
    searchingMatchThread1 = threading.Thread(target=searchingMatch, args=(player_waiting_list_30, ))
    searchingMatchThread2 = threading.Thread(target=searchingMatch, args=(player_waiting_list_60, ))
    searchingMatchThread3 = threading.Thread(target=searchingMatch, args=(player_waiting_list_90, ))
    searchingMatchThread4 = threading.Thread(target=searchingMatch, args=(player_waiting_list_120, ))
    searchingMatchThread1.start()
    searchingMatchThread2.start()
    searchingMatchThread3.start()
    searchingMatchThread4.start()
    start_server()
    db.close()