import os
from hashlib import md5


# Parse raw commadn list and create json card form from them
def get_cards(cards: list[str]) -> list[str]:
    json_cards = []
    table = cards[0].maketrans({'[': '', ']': '', ' ': '&nbsp;'})
    for card in cards:
        if card.startswith('!'):
            continue
        card = card.strip().translate(table)
        front, *back = card.split('\n', 1)
        if back == []:
            continue
        # задаёт разметку для кода и списков в карточках
        back = back[0].split('\n')
        if back[0].startswith('>'):
            back[0] = "<dl class='code'><br><dt>%s</dt>" % back[0][1:]
        for i in range(1, len(back)):
            if back[i].startswith('>') and not back[i-1].startswith('<d'):
                back[i] = "<dl class='code'><br><dt>%s</dt>" % back[i][1:]
            elif back[i].startswith('>') and back[i-1].startswith('<d'):
                back[i] = "<dt>%s</dt>" % back[i][1:]
            elif not back[i].startswith('>') and back[i-1].startswith('<d'):
                back[i] = "</dl><br>%s" % back[i]
            elif back[i].startswith('- ') and not back[i-1].startswith('<l'):
                back[i] = "<ul class='list'><br><li>%s</li>" % back[i][1:]
            elif back[i].startswith('-') and back[i-1].startswith('<l'):
                back[i] = "<li>%s</li>" % back[i][1:]
            elif not back[i].startswith('-') and back[i-1].startswith('<l'):
                back[i] = "</ul><br>%s" % back[i]
        if back[-1].startswith('<dt>'):
            back[-1] = "%s<br></dt>" % back[-1]
        elif back[-1].startswith('<li>'):
            back[-1] = "%s<br></li>" % back[-1]

        back = '<br>'.join(back)
        back = back.replace('\t', '&nbsp;' * 4)
        
        json_cards.append({"card_front": front, "card_back": back})
    return json_cards


# Check status and return decks names
def read_header(header: str) -> list[str]:
    decks = []
    lines = header.split('\n')
    if 'Source:' not in lines[0]:
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
def create_cards(f_name: str, flag: str) -> list(dict()):
    cards = []

    file = open(f_name, 'r', encoding='utf-8')
    if file is None:
        print("error: can't open file %s" % file)
        return cards

    hash_ = file.readline()[:-1]
    text = file.read()
    calc_hash = md5(text.encode()).hexdigest()
    if hash_ == calc_hash:
        print('File is already in deck.')
        file.close()
        return cards

    file.close()
    header, body = split_file(text)
    decks = read_header(header)
    fields = get_cards(body)

    if flag == 't':
        text = '%s\n%s' % (hash_, text)
    else:
        text = '%s\n%s' % (calc_hash, text)
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
    with open('./test_cards/test_card1.md') as file:
        file.readline()
        text = file.read()
    print(get_cards([text]))

'''
def main():
    files = os.listdir('.')
    for file in files:
        if '.md' == file[-3:]:
            print(file)
            cards = create_cards(file)
            print(cards)
'''

if __name__ == '__main__':
    main()
