#!/usr/bin/env python2
from bs4 import BeautifulSoup
from collections import Counter
import argparse
import json
import random


class Card(object):

    def __init__(self, cname, cclass, crarity):
        self.cname = cname
        self.cclass = cclass
        self.crarity = crarity

    def __str__(self):
        return '%s, %s, %s' % (self.cname, self.cclass, self.crarity)


class Deck(object):

    def __init__(self):
        self.cards = []

    def __str__(self):
        l = sorted(Counter([item.cname for item in self.cards]).items())
        return '\n'.join(['%d %s' % (count, card) for card, count in l])

    def random(self, cclass=None):
        if cclass:
            cards = [c for c in self.cards if c.cclass == cclass]
        else:
            cards = self.cards
        if cards:
            return random.choice(cards)

    def drop_card(self, card):
        self.cards.remove(card)

    def take_card(self, card):
        self.cards.append(card)

    def count_card(self, card):
        return sum(1 for c in self.cards if c.cname == card)


def create_d_collection(cclass, bl=[]):
    d = Deck()
    with open("collection.html") as f:
        c_raw = f.read()
    c_items = BeautifulSoup(c_raw,
                            'html.parser').findAll("div",
                                                   {"class": "owns-card"})
    for item in c_items:
        ccount = int(item.findAll("span")[-1]['data-card-count'])
        c = Card(item['data-card-name'],
                 item['data-card-class'],
                 int(item['data-rarity']))
        if (d.count_card(c.cname) == 2) or ((d.count_card(c.cname) == 1 and c.crarity == 5)) or (c.cname in bl):
            pass
        elif (c.cclass == "NONE") or (c.cclass == cclass):
            d.take_card(c)
            if ccount == 2:
                d.take_card(c)
    return d


def create_l_blacklist():
    l = []
    w = ("NAXX", "TGT")
    with open("cards.collectible.json") as f:
        j_request = f.read()
    j_bl = json.loads(j_request)
    l = [c["name"] for c in j_bl if c["set"] in w]
    return l


def create_d_random(collection, cclass):
    d = Deck()

    # number_cards = float(30)
    # if args.cc:
    #     number_class_cards = int(number_cards/100*args.cc)
    #     number_none_cards = int(number_cards - number_class_cards)
    # else:
    #     number_class_cards = int(number_cards/100*50)
    #     number_none_cards = int(number_cards - number_class_cards)
    # sum_class_cards = 0
    # sum_none_cards = 0

    sum_class_cards = 0
    i = 0
    while (i < 30):
        c = collection.random()
        if (c.cclass == cclass) and (sum_class_cards < 15):
            d.take_card(c)
            collection.drop_card(c)
            sum_class_cards += 1
            i += 1
        elif (c.cclass == "NONE") and (sum_class_cards < 15):
            d.take_card(c)
            collection.drop_card(c)
            i += 1
    return d


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cclass", type=str)
    args = parser.parse_args()

    cclass = str(args.cclass)

    l_blacklist = create_l_blacklist()
    d_collection = create_d_collection(cclass, l_blacklist)
    d_random = create_d_random(d_collection, cclass)

    print d_random

if __name__ == '__main__':
    main()
