from bs4 import BeautifulSoup
from deck_importer import import_cards
from _functions import write_deck_file
import os
import requests
import sys

deck_data = ""


def sort_parameters():
    global args_switch
    global deck_url

    if len(sys.argv) == 2:
        deck_url = sys.argv[1]
    elif len(sys.argv) == 3:
        args_switch = os.path.expanduser(sys.argv[1])
        deck_url = os.path.expanduser(sys.argv[2])
        if "-i" not in args_switch:
            sys.exit('unknown parameter: ' + args_switch)

    if "http" not in deck_url:
            sys.exit('Error: no URL found')


def check_website(deck_url):
    if "hearthpwn.com/decks/" in deck_url:
        hearthpwn_deck(deck_url)
    elif "icy-veins.com/hearthstone/" in deck_url:
        icyveins_deck(deck_url)
    else:
        sys.exit("unknown website: " + deck_url)


def icyveins_deck(deck_url):
    global deck_path
    deck_list = []

    deck_data = requests.get(deck_url).text
    deck_data = BeautifulSoup(deck_data, 'html.parser')
    deck_data = deck_data.findAll("table", {"class": "deck_card_list"})
    deck_data = deck_data[0].findAll('li')

    deck_path = "_decks/icyveins/" + deck_url.rsplit('/', 1)[-1]

    for item in deck_data:
        deck_list.append(item.text[0] + " " + item.a.text)

    deck_list.append("\n# " + deck_url)

    write_deck_file(deck_path, deck_list)


def hearthpwn_deck(deck_url):
    global deck_path
    deck_list = []

    deck_data = requests.get(deck_url).text
    deck_data = BeautifulSoup(deck_data, 'html.parser')
    deck_data = deck_data.findAll("aside", {"class": "infobox"})
    deck_data = deck_data[0].findAll('a')

    deck_path = "_decks/hearthpwn/" + deck_url.rsplit('/', 1)[-1]

    for item in deck_data:
        if item.has_attr('data-count'):     # if link is card
            deck_list.append(item['data-count'] + " " + item.string[7:-6])

    deck_list.append("\n# " + deck_url)

    write_deck_file(deck_path, deck_list)


def main():
    sort_parameters()
    check_website(deck_url)

    if "args_switch" in globals():
        if args_switch == "-i":
            import_cards(deck_path)


if __name__ == '__main__':
    main()
