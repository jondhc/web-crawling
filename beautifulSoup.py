import urllib.request
from bs4 import BeautifulSoup

starting_webpage = 'https://en.wikipedia.org/wiki/Web_crawler'
def get_links(url):
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	for link in soup.find_all('a'):
		if link.get('href') is not None:
			if link.get('href').startswith('http'):
				print(link.text)

if __name__ == "__main__":
	get_links(starting_webpage)

