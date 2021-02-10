import requests
from bs4 import BeautifulSoup
import os

from urllib.request import urlopen

from sclib import SoundcloudAPI, Track, Playlist


URL = input()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487', 'accept': '*/*'}


api = SoundcloudAPI()
track = api.resolve(URL)

def get_html(URL, params = None):
	r = requests.get(URL, headers=HEADERS, params = params)
	return r

def get_content(html):
	assert type(track) is Track
	filename = f'./{track.artist} - {track.title}.mp3'
	with open(filename, 'wb+') as fp:
		track.write_mp3_to(fp)

	soup = BeautifulSoup(html, 'html.parser')
	img_url = soup.find('meta', property='og:image').get('content')

	r = requests.get(img_url, stream = True)
	with open(f'{filename}.jpg', 'bw') as f:

		for chunk in r.iter_content(8192):
			f.write(chunk)

def parse():
	html = get_html(URL)

	if html.status_code == 200:
		get_content(html.text)
		print('Done.')
	else:
		print('Error')

parse()
