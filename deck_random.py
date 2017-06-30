# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from bs4 import BeautifulSoup
from lib.classes import Card, Deck
import argparse
import json
import requests
import time


class DeckRandom(object):
    def __init__(self, cclass, hpwn_user):
        self.cclass = cclass.upper()
        self.hpwn_user = hpwn_user
        self.l_blacklist = []
        self.d_collection = Deck()
        self.d_random = Deck()

    def run(self):
        self.blacklist()
        self.download()
        self.collection()
        self.random()
        self.d_random.save(path="_decks/random/%s_%s" % (self.cclass, time.strftime('%Y%m%d-%H%M%S')))
        print(self.d_random)

    def download(self):
        print("[+] Downloading collection")
        collection = requests.get("http://www.hearthpwn.com/members/" + self.hpwn_user + "/collection").text
        with open("collection.html", mode='w', encoding='utf-8') as f:
            f.write(collection)

    def collection(self):
        print("[+] Creating collection deck")
        with open("collection.html") as f:
            data = f.read()
            items = BeautifulSoup(data, 'html.parser').findAll("div", {"class": "owns-card"})
            for item in items:
                ccount = int(item.findAll("span")[-1]['data-card-count'])
                c = Card(item['data-card-name'], item['data-card-class'], int(item['data-rarity']))
                if (self.d_collection.count_card(c.cname) == 2) or ((self.d_collection.count_card(c.cname) == 1 and c.crarity == 5)) or (c.cname in self.l_blacklist):
                    pass
                elif (c.cclass == "NONE") or (c.cclass == self.cclass):
                    self.d_collection.take_card(c)
            if ccount == 2:
                self.d_collection.take_card(c)

    def blacklist(self):
        print("[+] Creating blacklist")
        w = ("BRM", "GVG", "HOF", "LOE", "NAXX", "TGT")
        with open("cards.collectible.json") as f:
            data = f.read()
        data = json.loads(data)
        self.l_blacklist = [c["name"] for c in data if c["set"] in w]

    def random(self):
        print("[+] Creating random deck")

        # number_cards = float(30)
        # if args.cc:
        #     number_class_cards = int(number_cards/100*args.cc)
        #     number_none_cards = int(number_cards - number_class_cards)
        # else:
        #     number_class_cards = int(number_cards/100*50)
        #     number_none_cards = int(number_cards - number_class_cards)
        # sum_class_cards = 0
        # sum_none_cards = 0

        s_cc = 0
        s_nc = 0

        i = 0
        while (i < 30):
            c = self.d_collection.random()
            if (c.cclass == self.cclass) and (s_cc < 15):
                    self.d_random.take_card(c)
                    self.d_collection.drop_card(c)
                    s_cc += 1
                    i += 1
            elif (c.cclass == "NONE") and (s_nc < 15):
                self.d_random.take_card(c)
                self.d_collection.drop_card(c)
                s_nc += 1
                i += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cclass", type=str)
    parser.add_argument("hpwn_user", type=str)
    args = parser.parse_args()

    random = DeckRandom(cclass=args.cclass, hpwn_user=args.hpwn_user)
    random.run()


if __name__ == '__main__':
    main()
