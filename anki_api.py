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


def add_card(card_front: str, card_back: str, deck_name: str) -> bool:
    # add hash to cards name to avoid dublicates
    card_front = '%s %s' % (card_front,
                 md5(deck_name.encode()).hexdigest()[:5])
    # check deck by name in anki
    if check_deck(deck_name):
        # try to find card and get it's id from anki
        card_id = check_card(deck_name, card_front)
        if card_id is None:
            print('Creating card')
            card_id = create_card(card_front, card_back, deck_name)
        else:
            print('Changing card')
            card_id = change_card(json_card, card_id)
    else:
        if not create_deck(deck_name):
            print("error: can't creat deck")
            return False

        card_id = create_card(json_card)

    if card_id is None:
        print("error: can't creat card")
        return False
    return True


def create_deck(deck_name: str) -> bool:
    try:
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
    cardsId = invoke('findCards', query="deck:%s" % deck_name)
    for card_id in cardsId:
        # get card info and compare it searching card's fields
        card = invoke('cardsInfo', cards=[card_id])
        card = card[0]['fields']
        if card_front == card['Front']['value']:
            return card_id
    return None


def create_card(json_card: dict) -> int:
    deck_name = json_card['deckName']
    card_front = json_card['Front']
    card_back = json_card['Back']
    try:
        print('Creating card')
        res = invoke('addNote',
                     note={"deckName": deck_name, "modelName": "1 Basic",
                     "fields": {"Front": card_front,
                     "Back": card_back}})
        return res
    except Exception as e:
        print(e)
        print('error: creat card')
        return None


def change_card(json_card: dict, card_id: int) -> int:
    try:
        invoke('updateNoteFields', note={"id": card_id, "fields": json_card['fields']}
        return card_id
    except Exception as e:
        print(e)
        print('error: changing card')
        return None


def main():
    add_card('new card', 'caard', 'test1')
    add_card('card', 'new field', 'test2')


if __name__ == '__main__':
    main()
