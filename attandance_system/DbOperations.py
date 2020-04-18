import mysql.connector
import datetime
db_connection = mysql.connector.connect(
  host="localhost",
  user="mysqluser",
  passwd="raspberry",
  database="attandance_db"
)

mycursor = db_connection.cursor()
sql = "SELECT * FROM T_CIHAZ"
mycursor.execute(sql)
myresult = mycursor.fetchall()
deviceId = 0
if len(myresult) > 0:
    deviceId = myresult[0][0]


def checkUserExist(cardId):
    mycursorcheckUserExist = db_connection.cursor()
    sql = "SELECT * FROM T_KULLANICI WHERE KART_ID = %s"
    adr = (cardId, )
    mycursorcheckUserExist.execute(sql, adr)
    myresult = mycursorcheckUserExist.fetchall()
    result = len(myresult)
    return(result)

def getDeviceId():
    global deviceId
    return deviceId

# def getReaderId(readerType):
#     mycursorgetReaderId = db_connection.cursor()
#     sql = "SELECT * FROM T_OKUYUCU WHERE ISLEV = %s"
#     adr = (readerType, )
#     mycursorgetReaderId.execute(sql, adr)
#     myresultgetReaderId = mycursorgetReaderId.fetchall()
#     readerId = 0
#     if len(myresultgetReaderId) > 0:
#         readerId = myresultgetReaderId[0][0]
#     return readerId
    
def insertAuthorize(cardId, readerId, isExisted):
    global deviceId
    mycursor = db_connection.cursor()
    now = datetime.datetime.now()
    #print(cardId, readerId, deviceId, now, isExisted, 0)
    sql = "INSERT INTO T_GECIS (GECIS_ID, KART_ID, OKUYUCU_ID, CIHAZ_ID, GECIS_ZAMANI, YETKILI_MI, AKTARILDI) VALUES  (UUID(), %s, %s, %s, %s, %s, %s)"
    val = (cardId, readerId, deviceId, now, isExisted, 0)
    mycursor.execute(sql, val)

    db_connection.commit()

    #print(mycursor.rowcount, "record inserted.")