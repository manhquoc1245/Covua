DRIVER = '{SQL Server}'
SERVER_NAME = "LAPTOP-98D7LRGC\SQLEXPRESS"
DATABASE_NAME = "ChessDB"
import pyodbc
db = pyodbc.connect(
    f'DRIVER={DRIVER};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    f'Trusted_Connection=yes;'
)
cursor = db.cursor()
query = "SELECT * FROM PlayerData Where Account='NgoAn'"
cursor.execute(query)
cursor = cursor.fetchall()
print(cursor)