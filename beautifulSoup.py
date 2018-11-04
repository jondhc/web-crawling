import urllib.request
from bs4 import BeautifulSoup

starting_webpage = 'https://en.wikipedia.org/wiki/Web_crawler'

def get_text(url, title):
	try:
		try:
			page = urllib.request.urlopen(url)
			soup = BeautifulSoup(page, 'html.parser')
			f = open(title + '.txt', 'w')
			f.write(soup.get_text())
			f.close()
		except urllib.error.URLError:
			print("Error in page " + url)
	except urllib.error.HTTPError:
		print("Error in page " + url)

def get_links(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	for link in soup.find_all('a'):
		if link.get('href') is not None:
			if link.get('href').startswith('http'):
				if len(link.text) < 30:
					get_text(link.get('href'), link.text.replace("/", ""))

if __name__ == "__main__":
	get_links(starting_webpage)

