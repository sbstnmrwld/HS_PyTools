#!/usr/bin/env python

from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("hclass")
parser.add_argument("file")
args = parser.parse_args()

cards_collection = []
cards_deck = []
class_player = args.hclass
final_deck = {}


def get_deck(file_name):
    with open(file_name) as f:
        file_lines = f.readlines()
        file_lines = map(lambda s: s.strip(), file_lines)
    return file_lines


def get_collection():
    with open("collection.html") as f:
        collection_raw = f.read()
    f.close()
    return collection_raw


def parse_collection():
    collection_raw_data = get_collection()
    collection_data = BeautifulSoup(collection_raw_data, 'html.parser')
    collection_items = collection_data.findAll("div", {"class": "owns-card"})
    for item in collection_items:
        if (item['data-card-class'] == "NONE") or (item['data-card-class'] == class_player):
            card_collection_name = item['data-card-name']
            card_collection_count = int(item.findAll("span")[-1]['data-card-count'])
            if card_collection_count == 2:
                cards_collection.append(card_collection_name)
            cards_collection.append(card_collection_name)


def parse_deck():
    deck = get_deck(args.file)
    for item in deck:
        if (item[0:1] == "#") or (item == ""):
            break
        elif item[0:1] == "2":
            cards_deck.append(item[2:])
        cards_deck.append(item[2:])


def compare_decks():
    for item in cards_deck:
        if item in cards_collection:
            if (item in final_deck.keys()) and (final_deck[item] == "1"):
                final_deck[item] = "2"
                cards_collection.remove(item)
            else:
                final_deck[item] = "1"
                cards_collection.remove(item)
        elif item in final_deck.keys():
            final_deck[item] = "="
        else:
            final_deck[item] = "-"


def print_deck():
    for card, count in final_deck.iteritems():
        print str(count) + " " + card


def main():
    parse_collection()
    parse_deck()
    compare_decks()
    print_deck()


if __name__ == '__main__':
    main()
