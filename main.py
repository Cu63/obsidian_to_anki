from anki_api import add_card
from obsidian_parser import create_cards
import os


def main():
    try:
        file = open('.config', 'r')
        path = file.readline().strip()
        if not path.startswith('path='):
            print('error: reading .config')
            return
        path = path[5:]
        file.close()
    except:
        path = input('Write path to obsidian cards: ')
        with open('.config', 'w') as f:
            f.write(f'path={path}')

    files = os.listdir(path)
    for file in files:
        if '.md' == file[-3:]:
            print(file)
            cards = create_cards('%s/%s' % (path,file))
            for card in cards:
                add_card(card)


if __name__ == "__main__":
    main()
