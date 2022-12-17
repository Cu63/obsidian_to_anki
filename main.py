from anki_api import add_card, update_card_style
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
    flag = False
    if len(sys.argv) == 2:
        if sys.argv[1].startswith('--path=') or sys.argv[1].startswith('-p='):
            with open('.config', 'w') as f:
                path = sys.argv[1].split("=", maxsplit=1)[1]
                f.write(f'path={path}')
            with open('.gitignore', 'w') as f:
                f.write('__pycache__\n')
                f.write('.config\n')
                update_card_style()
        elif sys.argv[1] in ('--test', '-t'):
            path = './test_cards'
            flag = 't'
        elif sys.argv[1] in ('-u', '--update'):
            flag = 'u'
            path = get_path()
        elif sys.argv[1] in ('--help', '-h'):
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
            cards = create_cards('%s/%s' % (path,file), flag=flag)
            for card in cards:
                add_card(card, flag)


if __name__ == "__main__":
    main()
