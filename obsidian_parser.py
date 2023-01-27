import os
import re
from hashlib import md5


def create_html_list(line_num, lines, card, tag='dl', isFirst=False):
    list_tags = {'ul': '- ', 'ol': '. '}
    if tag == 'dl':
        line_num += 1
        card.append("<dl class='code'>")
        while lines[line_num] != "```":
            line = lines[line_num]
            line = line.replace('\t', '&nbsp;' * 4)
            line = line.replace(' ' * 4, '&nbsp;' * 4)
            card.append(f'<dt>{line}</dt>')
            line_num += 1
        card.append("</dl>")
        line_num += 1
    elif tag in list_tags:
        if isFirst:
            card.append(f"<{tag} class='list'>")
        else:
            card.append(f"<{tag} class='list' style='border: 0px'>")
        shift = lines[line_num].find(list_tags[tag])
        while (line_num < len(lines) and lines[line_num][shift:]
               .startswith(list_tags[tag])):
            line = lines[line_num][shift + 2:]
            line = line.strip().replace('\\', '').replace('\t', '&nbsp;' * 4)
            line = line.replace('    ', 'nbsp;' * 4)
            line = f'<li>{line}'
            card.append(line)
            line_num += 1
            if (line_num < len(lines) and not lines[line_num][shift:]
               .startswith(list_tags[tag])):
                if re.match(r'[ \t]*- ',
                             lines[line_num][shift:]) is not None:
                    line_num = create_html_list(line_num, lines,
                                                card, tag='ul')
                elif re.match(r'[ \t]*[0-9]+\. ',
                               lines[line_num][shift:]) is not None:
                    line_num = create_html_list(line_num, lines,
                                                 card, tag='ol')
            card.append('</li>')
        card.append(f'</{tag}>')

    return line_num


def create_latex(line_num, lines, card):
    line_num += 1
    latex_list = list()
    latex_list.append('\\(')
    while lines[line_num] != '$$':
        latex_list.append(lines[line_num])
        line_num += 1
    latex_list.append('\\)')
    #latex_list = '\n'.join(latex_list)
    latex_list = ' '.join(latex_list)
    card.append(latex_list)
    line_num += 1
    return line_num


def md_to_html(md_text):
    card = []
    back = md_text.split('\n')
    i = 0
    table = back[0].maketrans({'[': '', ']': ''})
    while i < len(back):
        '''
        if len(card) == 0 or card[-1] == '</p>':
            card.append('<p>')
        '''
        if back[i].strip() == '':
            # card.append('</p>')
            i += 1
            continue
        if back[i].strip() == "$$":
            i = create_latex(i, back, card)
            continue
        if back[i].strip() == "```":
            i = create_html_list(i, back, card)
            continue
        back[i] = back[i].translate(table)
        if re.match(r'[ \t]*- ', back[i]) is not None:
            i = create_html_list(i, back, card, tag='ul', isFirst=True)
        elif re.match(r'[ \t]*[0-9]+\. ', back[i]) is not None:
            i = create_html_list(i, back, card, tag='ol', isFirst=True)
        else:
            line = back[i].replace('\t', '&nbsp;' * 4)
            line = line.replace('    ', 'nbsp;' * 4)
            line = line.replace('\\', '')
            card.append(line)
            i += 1

    # card.append('</p>')
    card = '<br>'.join(card)

    return card


# Parse raw command list and create json card form from them
def get_cards(cards: list[str]) -> list[str]:
    json_cards = []
    #table = cards[0].maketrans({'[': '', ']': '', ' ': '&nbsp;'})
    table = cards[0].maketrans({'[': '', ']': ''})
    for card in cards:
        if card.startswith('!'):
            continue
        #card = card.strip().translate(table)
        front, *back = card.split('\n', 1)
        front = front.strip().translate(table)
        if back == []:
            continue
        back = back[0].strip()
        # задаёт разметку для кода и списков в карточках
        back = md_to_html(back)
        if card.startswith('~'):
            front = front[1:]
            json_cards.append({"card_front": back, "card_back": front})
        else:
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
    file.close()
    calc_hash = md5(text.encode()).hexdigest()
    if hash_ == calc_hash and flag not in ('u', 't'):
        print('File is already in deck.')
        return cards

    header, body = split_file(text)
    decks = read_header(header)
    fields = get_cards(body)

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
        _, body = split_file(text)
    print(get_cards(body))


if __name__ == '__main__':
    main()
