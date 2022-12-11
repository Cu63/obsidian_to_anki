import os


# Parse raw commadn list and create json card form from them
def get_cards(cards: list[str]) -> list[str]:
    json_cards = []
    table = cards[0].maketrans({'\t': '', '[': '', ']': ''})
    for card in cards:
        if card.startswith('!'):
            continue
        card = card.strip().translate(table)
        front, *back = card.split('\n', 1)
        if back == []:
            continue
        back = back[0]
        json_cards.append({"card_front": front, "card_back": back})
    return json_cards


# Check status and return decks names
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
        if l in decks:
            continue
        decks.append(l)
    if decks == []:
        decks = ['Default']
    return decks

# split md file by separator '## '. First block is a header with status
# and decks names
def split_file(text: str):
    header_spliter = '## '
    text = text.split(header_spliter)
    header = text[0].strip()
    body = text[1:]
    return header, body

# Read md file and get cards from it
def create_cards(f_name: str) -> list(dict()):
    cards = []

    file = open(f_name, 'r', encoding='utf-8')
    if file is None:
        print("error: can't open file %s" % file)
        return cards

    text = file.readline()
    if text != 'Status: #toanki \n':
        print('Card is already in deck.')
        file.close()
        return cards

    text = file.read()
    file.close()
    header, body = split_file(text)
    decks = read_header(header)
    fields = get_cards(body)

    text = 'Status: #done \n%s' % text
    file = open(f_name, 'w', encoding='utf-8')
    file.write(text)
    file.close()
    for deck in decks:
        for f in fields:
            cards.append({'card_front': f['card_front'],
                          'card_back': f['card_back'],
                          'deck_name': deck})
    return cards


def main():
    files = os.listdir('.')
    for file in files:
        if '.md' == file[-3:]:
            print(file)
            cards = create_cards(file)
            print(cards)


if __name__ == '__main__':
    main()
