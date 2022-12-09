import os


def get_cards(cards: list[str]) -> list[str]:
    json_cards = []
    table = cards[1].maketrans({'\t': '', '[': '', ']': ''})
    for card in cards:
        if card.startswith('!'):
            continue
        card = card.strip().translate(table)
        front, *back = card.split('\n', 1)
        if back == []:
            continue
        back = back[0]
        json_cards.append({"fields": {"Front": front, "Back": back}})
    return json_cards


def read_header(header: str) -> list[str]:
    decks = []
    lines = header.split('\n')
    if lines[0] != 'Source:':
        print('error: wrong header format')
        return None
    table = lines[1].maketrans({'\t': '', '[': '', ']': ''})
    for line in lines[1:]:
        l = line.translate(table)
        l = l.split('#')[0]
        decks.append(l)
    if decks == []:
        decks = ['Default']
    return decks


def split_file(text: str):
    header_spliter = '## '
    text = text.split(header_spliter)
    header = text[0].strip()
    body = text[1:]
    return header, body


def create_cards(f_name: str) -> list(dict()):
    cards = []

    file = open(f_name, 'r')
    if file is None:
        print("error: can't open file %s" % file)
        return cards

    text = file.readline()
    if text != 'Status: #toanki\n':
        print('Card is already in deck.')
        file.close()
        return cards

    text = file.read()
    file.close()
    header, body = split_file(text)
    decks = read_header(header)
    cards = get_cards(body)

    return cards


def main():
    files = os.listdir('.')
    for file in files:
        if '.md' == file[-3:]:
            print(file)
            create_cards(file)

    
if __name__ == '__main__':
    main()
