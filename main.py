from anki_api import add_card
from obsidian_parser import create_cards
import os


def main():
    files = os.listdir('.')
    for file in files:
        if '.md' == file[-3:]:
            print(file)
            cards = create_cards(file)
            for card in cards:
                add_card(card)


if __name__ == "__main__":
    main()
