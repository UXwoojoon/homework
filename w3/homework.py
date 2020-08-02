import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbMusic

headers = {'User-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers = headers)

soup = BeautifulSoup(data.text, 'html.parser')

musics = soup.select('table.list-wrap > tbody > tr')
GMus = []

for music in musics[0:30]:
    if music is not None:
        rank_raw = music.select_one('td.number').text[0:2]
        title_raw = music.select_one('td.info > a:nth-child(1)').text
        artist_raw = music.select_one('td.info > a:nth-child(2)').text

        rank = rank_raw.strip()
        title = title_raw.lstrip()
        GMus.append({'rank':rank, 'title':title, 'artist_raw':artist_raw})

db.GMS.insert_many(GMus)
print(GMus)