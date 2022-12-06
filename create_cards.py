import os


def read_header(header: str):
    header.replace('')
    lines = header.split('\n')
    if lines[0] != 'Source:':
        print('error: wrong header format')
        return None



def split_file(text: str):
    header_spliter = '## ' + '-' * 30
    text = text.split(header_spliter)
    header = text[0].strip()
    body = text[1].strip()
    return header, body



def create_cards(f_name: str) -> list(dict()):
    cards = []

    file = open(f_name, 'r')
    if file is None:
        print("error: can't open file %s" % file)
        return []

    text = file.readline()
    print(text)
    if text != 'Status: #toanki\n':
        print('Card is already in deck.')
        file.close()
        return cards

    text = file.read()
    file.close()
    header, body = split_file(text)
    decks = read_header(header)

    return cards

def main():
    files = os.listdir('.')
    for file in files:
        if '.md' == file[-3:]:
            print(file)
            create_cards(file)

    
if __name__ == '__main__':
    main()
