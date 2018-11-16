import urllib.request
from bs4 import BeautifulSoup

starting_webpage = 'http://lite.cnn.io'
crawled_links = []
dictionary = {}

def get_text(url, title):
	try:
		try:
			page = urllib.request.urlopen(url)
			soup = BeautifulSoup(page, 'html.parser')
			directory = './Docs/'
			f = open(directory + title + '.txt', 'w')
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
			crawled_links.append(link.get('href'))
			if link.get('href').startswith('http'):
				if len(link.text) < 30:
					get_text(link.get('href'), link.text.replace("/", ""))
			else:
				get_text(starting_webpage + link.get('href'), link.text.replace("/", ""))

import sys
import os
import pprint
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict


def tokenize(text):
	tokens = set(word_tokenize(text))
	return tokens


def createDictionary(terms, doc):
	for k in terms:
		dictionary.setdefault(k, []).append(doc)


def showDictionary(arg):
	pp = pprint.PrettyPrinter(indent=2)
	pp.pprint(list(arg.items()))


def getPosting(key):
	return dictionary[key]

def performAndQuery(post1, post2):
	results = []
	for i in post1:
		if i in post2:
			results.append(i)
	return results


def performOrQuery(post1, post2):
	return list(set(post1 + post2))


def performNotQuery(post):
	results = []
	for i in range(1, len(documents)):
		if documents[i] not in post:
			results.append(i)
	return results


def performAndQueryOrQuery(term1, term2, term3):  # and - or
	return list(performOrQuery((performAndQuery(getPosting(term1), getPosting(term2))), getPosting(term3)))


def performAndQueryAndQuery(term1, term2, term3):  # and - and
	return list(performAndQuery((performAndQuery((getPosting(term1)), (getPosting(term2)))), (getPosting(term3))))


def performAndQueryNotQuery(term1, term2):  # not - and
	return list(performAndQuery((term1), (performNotQuery(getPosting(term2)))))


def performOrQueryOrQuery(term1, term2, term3):  # or -or
	return list(performOrQuery((getPosting(term1)), (performOrQuery((getPosting(term2)), (getPosting(term3))))))


def performOrQueryNotQuery(term1, term2):  # not - or
	return list(performOrQuery((getPosting(term1)), (performNotQuery(getPosting(term2)))))


def performOrQueryAndQuery(term1, term2, term3):  # or - and
	return list(performAndQuery((performOrQuery((getPosting(term1)), (getPosting(term2)))), (getPosting(term3))))


def makeQuerys():
	print("What kind of query do you want?: ")
	print("a  ->  Simple AND Query")
	print("o  ->  Simple OR Query")
	print("n  ->  Simple NOT Query")
	print("aa ->  Query with AND - AND")
	print("ao ->  Query with AND - OR")
	print("an ->  Query with AND - NOT")
	print("oa ->  Query with OR - AND")
	print("oo ->  Query with OR - OR")
	print("on ->  Query with OR - NOT")
	print("b ->   Back to the previous menu")
	case = input()
	case.lower()
	showDictionary(dictionary)
	print()
	if case == "a":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		print(performAndQuery((getPosting(term1)), (getPosting(term2))))
		mainOptions()
	elif case == "o":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		print(performOrQuery((getPosting(term1)), (getPosting(term2))))
		mainOptions()
	elif case == "n":
		term1 = input("Termino: ")
		print(performNotQuery((getPosting(term1))))
		mainOptions()
	elif case == "aa":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		term3 = input("Third term: ")
		print(performAndQueryAndQuery(term1, term2, term3))
		mainOptions()
	elif case == "ao":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		term3 = input("Third term: ")
		print(performAndQueryOrQuery(term1, term2, term3))
		mainOptions()
	elif case == "an":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		term3 = input("Third term: ")
		print(performAndQueryNotQuery(term1, term2))
		mainOptions()
	elif case == "oa":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		term3 = input("Third term: ")
		print(performOrQueryAndQuery(term1, term2, term3))
		mainOptions()
	elif case == "oo":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		term3 = input("Third term: ")
		print(performOrQueryOrQuery(term1, term2, term3))
		mainOptions()
	elif case == "on":
		term1 = input("First term: ")
		term2 = input("Second term: ")
		term3 = input("Third term: ")
		print(performOrQueryNotQuery(term1, term2))
		mainOptions()
	elif case == "b":
		os.system("clear")
		mainOptions()
	else:
		os.system("clear")
		print("Your option is invalid. Please try again")
		makeQuerys()


def mainOptions():
	print()
	print("These are the tasks you can do:")
	print("p -> Print the Inverted Index ")
	print("q -> Make a Query")
	print("e -> Exit")
	op = input("Please choose an option to do: ")
	op.lower()

	if op == "p":
		os.system("clear")
		showDictionary(dictionary)
		next = input("Would you like to do anything else? (yes/no): ")
		next.lower()
		if next == "yes":
			print()
			mainOptions()
		else:
			print("Thanks for comming!")
			sys.exit()
	elif op == "q":
		os.system("clear")
		makeQuerys()
	elif op == "e":
		print("Thanks for comming!")
		sys.exit()

def open_docs():
	directory = "./Docs"
	for document in os.listdir(directory):
		try:
			file = open(directory + "/" + document, "r")
			content = file.read()
			createDictionary(tokenize(content), document)
		except:
			print("Error while reading file " + document)

if __name__ == "__main__":
	get_links(starting_webpage)
	for link in crawled_links:
		print("Link: " + link)
	open_docs()
	mainOptions()


