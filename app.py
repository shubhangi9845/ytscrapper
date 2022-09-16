import os
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import mysql.connector as conn
import pymongo
from urllib import parse
from urllib.request import urlopen as uReq
import base64
import requests

option = Options()
option.add_argument('--no-sandbox')
option.add_argument('disable-dev-shm-usage')
option.headless = True

# Driver local path
DRIVER_PATH = r'/Users/sangrampatil/PycharmProjects/ytscrpper/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)

# Driver server path
# option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# driver = webdriver.Chrome(executable_path=os.environ.get("DRIVER_PATH"), options=option)


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
  database="testdb",
  charset='utf8mb4'
)
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            CHANNEL_URL = request.form['content'].replace(" ","")

            ########## Get video Links ####################
            channel_id = parse.urlparse(CHANNEL_URL).path.split('/')[-1]
            channel_videos_url = CHANNEL_URL + '/videos'
            driver.get(channel_videos_url)
            driver.maximize_window()
            time.sleep(1)
            print("CHANNEL:" + CHANNEL_URL)

            # To scroll page to get first 50 videos
            channel_name = driver.find_element_by_xpath('//*[@id="channel-name"]//yt-formatted-string').text
            print(channel_name)
            first_title = driver.find_element_by_xpath('//*[@id="video-title"]')
            no_of_pagedowns = 8
            while no_of_pagedowns:
                first_title.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
                no_of_pagedowns -= 1

            # Enter number of videos to scrape data
            count = 50
            names = driver.find_elements_by_xpath('//*[@id="video-title"]')
            titles = []
            for name in names[:count]:
                title = name.text
                titles.append(title)
            print('TITLES:{}'.format(titles))
            video_urls = driver.find_elements_by_xpath('//*[@id="video-title"]')
            links = []
            for link in video_urls[:count]:
                url = link.get_attribute('href')
                links.append(url)
            print('LINKS:{}'.format(links))

            ############ Get Video information #################

            videos = []
            for link in links[:1]:
                driver.get(link)
                driver.maximize_window()
                time.sleep(1)
                prev_h = 0
                while True:
                    height = driver.execute_script("""
                                   function getActualHeight() {
                                       return Math.max(
                                           Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                                           Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                                           Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                                       );
                                   }
                                   return getActualHeight();
                               """)
                    driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 200})")
                    # fix the time sleep value according to your network connection
                    time.sleep(0.2)
                    prev_h += 200
                    if prev_h >= height:
                        break
                video_bs = BeautifulSoup(driver.page_source, 'html.parser')
                print(CHANNEL_URL)
                title = video_bs.select_one('#container > h1 > yt-formatted-string').text
                print(title)
                print(link)
                video_id = parse.parse_qs(parse.urlparse(link).query)['v'][0]
                thumbnail = video_bs.select_one('#watch7-content > link:nth-child(11)').get('href')
                print(thumbnail)
                likes_txt = video_bs.select_one('#top-level-buttons-computed > ytd-toggle-button-renderer:nth-child(1) > a > yt-formatted-string').get('aria-label')
                likes = ''.join(i for i in likes_txt if i.isdigit())
                print(likes)
                comment_count = video_bs.select_one('#count > yt-formatted-string > span:nth-child(1)').text
                print(comment_count)
                text_div = video_bs.select("#comment #content #content-text")
                comment_text = []
                for texts in text_div:
                    text = texts.text
                    comment_text.append(text)
                print(comment_text)
                author_div = video_bs.select("#comment #author-text > span")
                comment_by = []
                for auth in author_div:
                    author = auth.text.strip()
                    comment_by.append(author)
                print(comment_by)
                author_thumbs = video_bs.select('#comment #author-thumbnail #img')

                auth_thumbs = []
                for thumb in author_thumbs:
                    thumb_url = thumb.get('src')
                    auth_thumbs.append(thumb_url)
                print(auth_thumbs)
                comment_time_div = video_bs.select('#comment #header-author > yt-formatted-string > a')
                comment_ids = []
                for id in comment_time_div:
                    comment_id_url = id.get('href')
                    url_id = parse.parse_qs(parse.urlparse(comment_id_url).query)['lc'][0]
                    comment_ids.append(url_id)
                print(comment_ids)

                ##### Update in MySQL
                s = "INSERT INTO ChannelVideos (ChannelID, VideoID, ChannelName, VideoLink, Title, ThumbnailURL, Likes, Comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ChannelName=VALUES(ChannelName), Title=VALUES(Title), ThumbnailURL=VALUES(ThumbnailURL), Likes=VALUES(Likes), Comments=VALUES(Comments)"
                s1 = (channel_id, video_id, channel_name, link, title, thumbnail, likes, comment_count)
                mycursor.execute(s, s1)
                mydb.commit()

                #### Update MangoDB Comments
                client = pymongo.MongoClient(
                    "mongodb+srv://shubhangi:sangram123@sangram.jttnwlv.mongodb.net/?retryWrites=true&w=majority")
                database = client['youtube']
                collection = database['comments']
                for (ids, author, text) in zip(comment_ids, comment_by, comment_text):
                    filter = {'_id': ids}
                    cm_data = {"$set":
                                   {'VideoLink': link,
                                    'Author': author,
                                    'Text': text}}
                    collection.update_one(filter, cm_data, upsert=True)
                cursor = collection.find({'VideoLink': link})
                for record in cursor:
                    print(record)

                #### Update MangoDB Thumbnail
                b64_img = base64.b64encode(requests.get(thumbnail).content).decode('utf-8')
                collection = database['thumbnails']
                link1 = parse.parse_qs(parse.urlparse(link).query)['v'][0]
                filter = {'_id': link1}
                thumb_data = {"$set":
                                  {'VideoLink': link,
                                   'Thumbnail': b64_img}}
                collection.update_one(filter, thumb_data, upsert=True)

                mydict = {"Channel": channel_name, "VideoLink": link, "Title": title, "Thumbnail": thumbnail, "Likes": likes,
                          "Comments": comment_count}
                videos.append(mydict)

            driver.quit()
            return render_template('results.html', reviews=videos[0:(len(videos))])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)
    # app.run(debug=True)

