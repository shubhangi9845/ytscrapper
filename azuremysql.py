import mysql.connector as conn
from mysql.connector import errorcode
import azure.functions as func

mydb = conn.connect(
  user='shubhangi@projectdemo',
  password='varshu#23',
  host='projectdemo.mysql.database.azure.com',
  ssl_ca=r'/Users/sangrampatil/PycharmProjects/ytscrpper/DigiCertGlobalRootG2.crt.pem',
  database="testdb"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE testdb")

# mycursor.execute("CREATE TABLE ChannelVideos (ChannelURL varchar(255),VideoLink varchar(255),"
#                  "Title varchar(450),ThumbnailURL varchar(450),Likes integer(10),Comments integer(10),"
#                  "Thumbnail varchar(450),Download varchar(450),CommentsList varchar(450))")

# mycursor.execute("ALTER TABLE ChannelVideos ADD PRIMARY KEY(ChannelURL,VideoLink)")

# mycursor.execute("SHOW DATABASES")
# for db in mycursor:
#     print(db)

# mycursor.execute("SHOW TABLES")
# for tb in mycursor:
#     print(tb)