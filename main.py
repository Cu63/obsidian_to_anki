from anki_api import add_card
from obsidian_parser import create_cards
import os
import sys


def get_path():
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
    return path



def main():
    test = False
    if len(sys.argv) == 2:
        if sys.argv[1].startswith('--path=') or sys.argv[1].startswith('-p='):
            with open('.config', 'w') as f:
                path = sys.argv[1].split("=", maxsplit=1)[1]
                f.write(f'path={path}')
        elif sys.argv[1] == '--test' or sys.argv[1] == '-t':
            path = './test_cards'
            test = True
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print('\t <--test/-t>="test program')
            print('\t <--path/-p>="path to cards"')
            print('\t <--help/-h>="for help"')
            return
    else:
        path = get_path()

    files = os.listdir(path)
    for file in files:
        if '.md' == file[-3:]:
            print(file)
            cards = create_cards('%s/%s' % (path,file), test=test)
            for card in cards:
                add_card(card)


if __name__ == "__main__":
    main()
