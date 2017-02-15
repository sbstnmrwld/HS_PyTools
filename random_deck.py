#!/usr/bin/env python2

# import os
# import requests
# import sys

from bs4 import BeautifulSoup
from collections import Counter
import argparse
import json
import random

parser = argparse.ArgumentParser()
parser.add_argument("hclass")
parser.add_argument("-cc", type=float)
parser.add_argument("-w", "--wild", action="store_true")
args = parser.parse_args()

# variables
cards_blacklist = []
cards_collection = []
class_player = args.hclass
cards_player = []


def get_blacklist():
    with open("cards.collectible.json") as c:
	json_request = c.read()
	json_blacklist = json.loads(json_request)
	for item in json_blacklist:
		if (item["set"] == "NAXX") or (item["set"] == "TGT"):
			cards_blacklist.append(item["name"])
	c.close()

def get_collection():
	with open("collection.html") as f:
		collection_raw = f.read()
	f.close()
	return collection_raw

def create_collection(raw_data):
	collection_data = BeautifulSoup(raw_data, 'html.parser')
	collection_items = collection_data.findAll("div", { "class" : "owns-card" })
	for item in collection_items:
		if ((item['data-card-class'] == "NONE") or (item['data-card-class'] == class_player)) and (item['data-card-name'] not in cards_blacklist):
			card_collection_name = item['data-card-name']
			card_collection_count = int(item.findAll("span")[-1]['data-card-count'])
			card_collection_class = item['data-card-class']
			card_collection_rarity = int(item['data-rarity'])
			cards_collection.append([card_collection_name, card_collection_class, card_collection_count, card_collection_rarity])

def create_random_deck():
	number_cards = float(30)
	if args.cc:
		number_class_cards = int(number_cards/100*args.cc)
		number_none_cards = int(number_cards - number_class_cards)
	else:
		number_class_cards = int(number_cards/100*50)
		number_none_cards = int(number_cards - number_class_cards)
	sum_class_cards = 0
	sum_none_cards = 0
	i = 0
	while (i < number_cards):
		rng = random.randrange(0,len(cards_collection))
		random_card = cards_collection[rng]
		if (cards_player.count(random_card[0]) == 2): # eliminate sum up of golden und non-golden cards
			cards_collection.pop(rng)
			pass
		elif (random_card[1] == class_player) and (sum_class_cards < number_class_cards):
			cards_player.append(random_card[0])
			sum_class_cards += 1
			i += 1
		elif (random_card[1] == "NONE") and (sum_none_cards < number_none_cards):
			cards_player.append(random_card[0])
			sum_none_cards += 1
			i += 1
		if (cards_player.count(random_card[0]) == cards_collection[rng][2]) or (random_card[3] == 5):	# maximum number of this card
			cards_collection.pop(rng)
			pass
	deck_player = Counter(cards_player)
	for card, count in deck_player.iteritems():
		print str(count) + " " + card

def main():
	if args.wild is False:
		get_blacklist()
	create_collection(get_collection())
	create_random_deck()

if __name__ == '__main__':
	main()
