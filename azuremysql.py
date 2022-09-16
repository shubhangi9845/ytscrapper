import mysql.connector as conn
from mysql.connector import errorcode

# mydb = conn.connect(
#     host="localhost",
#     user="root",
#     passwd="vardhan#23",
#     database="testdb",
#     charset='utf8mb4'
# )
mydb = conn.connect(
  user='shubhangi@projectdemo',
  password='varshu#23',
  host='projectdemo.mysql.database.azure.com',
  ssl_ca=r'/Users/sangrampatil/PycharmProjects/ytscrpper/DigiCertGlobalRootG2.crt.pem',
  database="testdb",
  charset='utf8mb4'
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE testdb")

# mycursor.execute("DROP TABLE ChannelVideos")

mycursor.execute("CREATE TABLE ChannelVideos (ChannelID varchar(255) NOT NULL,VideoID varchar(255) NOT NULL,"
                 "ChannelName varchar(255),VideoLink varchar(255),Title varchar(450) CHARACTER SET utf8mb4,"
                 "ThumbnailURL varchar(450),Likes integer(10),Comments integer(10),Thumbnail varchar(450),"
                 "Download varchar(450),CommentsList varchar(450),PRIMARY KEY (ChannelId, VideoId))")

# mycursor.execute("ALTER TABLE ChannelVideos ADD PRIMARY KEY(ChannelURL,VideoLink)")

#mycursor.execute("ALTER TABLE ChannelVideos MODIFY Title VARCHAR(450) CHARACTER SET utf8mb4")

# mycursor.execute("DELETE FROM ChannelVideos")

# mycursor.execute("SHOW DATABASES")
# for db in mycursor:
#     print(db)

# mycursor.execute("SHOW TABLES")
# for tb in mycursor:
#     print(tb)