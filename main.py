from anki_api import add_card, style_check, invoke
from obsidian_parser import create_cards
import os
import sys
import threading
from queue import Queue


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

def add_file_cards(files_queue, flag):
    while not files_queue.empty():
        file = files_queue.get()
        print(file)
        cards = create_cards(file, flag=flag)
        for card in cards:
            add_card(card, flag)


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
                style_check()
        elif sys.argv[1] in ('--test', '-t'):
            path = './test_cards'
            flag = 't'
            style_check()
        elif sys.argv[1] in ('-u', '--update'):
            flag = 'u'
            path = get_path()
            style_check()
        elif sys.argv[1] in ('--help', '-h'):
            print('\t <--test/-t>="test program')
            print('\t <--path/-p>="path to cards"')
            print('\t <--help/-h>="for help"')
            print('\t <--update/-u>="for update cards without reset progres"')
            return
    else:
        path = get_path()

    files = os.listdir(path)
    files_queue = Queue()
    for file in files:
        if '.md' == file[-3:]:
            files_queue.put(f'{path}/{file}')
    for i in range(10):
        print(f'Start thread {i + 1}')
        file_thread = threading.Thread(target=add_file_cards,
                                       args=(files_queue, flag))
        file_thread.start()

    '''
    for file in files:
            print(file)
            cards = create_cards('%s/%s' % (path,file), flag=flag)
            for card in cards:
                add_card(card, flag)
    '''
    invoke('sync')


if __name__ == "__main__":
    main()
