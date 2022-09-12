import mysql.connector as conn

mydb = conn.connect(
    host="localhost",
    user="root",
    passwd="vardhan#23",
    database="testdb"
)


mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE ChannelVideos (ChannelURL varchar(255),VideoLink varchar(255),"
#                  "Title varchar(450),ThumbnailURL varchar(450),Likes integer(10),Comments integer(10),"
#                  "Thumbnail varchar(450),Download varchar(450),CommentsList varchar(450))")


# mycursor.execute("ALTER TABLE ChannelVideos ADD PRIMARY KEY(ChannelURL,VideoLink)")
