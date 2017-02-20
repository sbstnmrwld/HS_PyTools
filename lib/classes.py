# -*- coding: utf-8 -*-

from collections import Counter
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

    def save(self, path):
        l = sorted(Counter([item.cname for item in self.cards]).items())
        print("[+] Save deck to %s" % path)
        with open(path, mode='w', encoding='utf-8') as f:
            f.write('\n'.join(['%d %s' % (count, card) for card, count in l]))
