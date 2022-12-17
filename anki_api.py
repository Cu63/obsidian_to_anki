from hashlib import md5
import json
import urllib.request


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def add_card(json_card: dict, flag) -> bool:
    card_front = json_card['card_front']
    card_back = json_card['card_back']
    deck_name = json_card['deck_name']
    # add hash to cards name to avoid dublicates
    card_front = '%s<nobr class="hash">%s</nobr>' % (card_front,
                 md5(deck_name.encode()).hexdigest()[:5])
    # check deck by name in anki
    if check_deck(deck_name):
        # try to find card and get it's id from anki
        card_id = check_card(deck_name, card_front)
        if card_id is None:
            card_id = create_card(card_front, card_back, deck_name)
        else:
            card_id = change_card(card_id, card_front, card_back, flag)
    else:
        if not create_deck(deck_name):
            print("error: can't creat deck")
            return False

        card_id = create_card(card_front, card_back, deck_name)

    if card_id is None:
        print("error: can't creat card")
        return False
    return True


def create_deck(deck_name: str) -> bool:
    try:
        print(f'Create deck {deck_name}')
        invoke('createDeck', deck=deck_name)
        return True
    except Exception as e:
        print(e)
        return False


# Try to find deck in anki decks list
def check_deck(deck_name: str) -> bool:
    result = invoke('deckNames')
    if deck_name in result:
        return True
    return False


# Try to find card id by front field in deck
def check_card(deck_name: str, card_front: str) -> int:
    # get all cards ids from deck
    cardsId = invoke('findCards', query='deck:"%s"' % deck_name)
    for card_id in cardsId:
        # get card info and compare it searching card's fields
        card = invoke('cardsInfo', cards=[card_id])
        card = card[0]['fields']
        if card_front == card['Front']['value']:
            return card_id
    return None


def create_card(card_front: str, card_back: str, deck_name: str) -> int:
    try:
        print('Creating card')
        res = invoke('addNote',
                     note={"deckName": deck_name, "modelName": "1 Basic",
                     "fields": {"Front": card_front, "Back": card_back}})
        return res
    except Exception as e:
        print(e)
        return None



def change_card(card_id: int, card_front: str,
                card_back: str, flag: str) -> int:
    try:
        card = invoke('cardsInfo', cards=[card_id])
        card = card[0]['fields']
        if card_back == card['Back']['value']:
            return card_id
        invoke('updateNoteFields',
                note={"id": card_id,
                      "fields": {"Front": card_front, "Back": card_back}})
        if flag not in ('t', 'u'):
            invoke('relearnCards', cards=[card_id])
        return card_id
    except Exception as e:
        print(e)
        print('error: changing card')
        return None

def update_card_style():
    with open('obsidian.css') as f:
        css = f.read()
    invoke('updateModelStyling', model={'name': '1 Basic', "css": css})


def main():
    cardsId = invoke('findCards', query='deck:"test deck 1"')
    update_card_style()
    print(cardsId)
    card = invoke('cardsInfo', cards=cardsId)[0]
    print(card['answer'])
    for c in card:
        print(c, card[c])

if __name__ == '__main__':
    main()
