def write_deck_file(deck_path, deck_list):

    print "\n# Exporting deck to " + deck_path + "\n"
    out = open(deck_path, 'w')
    for item in deck_list:
        out.write(item + "\n")
        print item
    out.close()
