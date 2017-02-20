# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from bs4 import BeautifulSoup
from lib.classes import Card, Deck
from deck_importer import DeckImporter
import argparse
import requests
import sys


class DeckDownloader(object):
    def __init__(self, url, importer=False):
        self.deck = Deck()
        self.filename = url.rsplit('/', 1)[-1]
        self.path = ""
        self.url = url
        self.importer = importer

    def run(self):
        self.check()
        self.deck.save(path="%s%s" % (self.path, self.filename))

        print(self.importer)

        if self.importer:
            importer = DeckImporter(filename="%s%s" % (self.path, self.filename))
            importer.run()

    def check(self):
        websites = ("hearthpwn.com/decks/",
                    "icy-veins.com/hearthstone/")

        if any(item in self.url for item in websites):
            self.download()
        else:
            sys.exit("[-] unknown website: %s" % self.url)

    def download(self):
        print("[+] Downloading deck from %s" % self.url)
        if "hearthpwn" in self.url:
            self.path = "_decks/hearthpwn/"
            data = requests.get(self.url).text
            data = BeautifulSoup(data, 'html.parser')
            data = data.findAll("aside", {"class": "infobox"})
            data = data[0].findAll('a')
            for item in data:
                if item.has_attr('data-count'):
                    c = Card(item.string[7:-6], "", "")
                    self.deck.take_card(c)
                    if int(item["data-count"]) == 2:
                        self.deck.take_card(c)
        elif "icy-veins" in self.url:
            self.path = "_decks/icyveins/"
            data = requests.get(self.url).text
            data = BeautifulSoup(data, 'html.parser')
            data = data.findAll("table", {"class": "deck_card_list"})
            data = data[0].findAll('li')
            for item in data:
                c = Card(item.a.text, "", "")
                self.deck.take_card(c)
                if int(item.text[0]) == 2:
                    self.deck.take_card(c)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("-i", "--importer", action="store_true")
    args = parser.parse_args()

    print(args)

    downloader = DeckDownloader(url=args.url, importer=args.importer)
    downloader.run()


if __name__ == '__main__':
    main()
