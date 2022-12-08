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
    # Существует ли колода
    if check_deck(deck_name):
        # Если существует
        card_id = check_card(deck_name, card_front)
        if card_id is None:
            print('Creating card')
            # Создать карточку
            card_id = create_card(card_front, card_back, deck_name)
        else:
            print('Changing card')
            # изменить карточку
            card_id = change_card(card_id, card_front, card_back)
    else:
        # В ином случае
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
        invoke('createDeck', deck=deck_name)
        return True
    except:
        return False


def check_deck(deck_name: str) -> bool:
    result = invoke('deckNames')
    if deck_name in result:
        return True
    return False


def check_card(deck_name: str, card_front: str) -> int:
    # Получаем id всех карт из колоды
    cardsId = invoke('findCards', query="deck:%s" % deck_name)
    for card_id in cardsId:
        # Получаем информацию о карте
        card = invoke('cardsInfo', cards=[card_id])
        card = card[0]['fields']
        if card_front == card['Front']['value']:
            return card_id
    return None


def create_card(card_front: str, card_back: str, deck_name: str) -> int:
    try:
        res = invoke('addNotes',
                     notes=[{"deckName": deck_name, "modelName": "1 Basic",
                     "fields": {"Front": card_front,
                     "Back": card_back}})
        return res[0]
    except:
        return None


def change_card(card_id: int, card_front: str,
                card_back: str) -> int:
    try:
        res = invoke('updateNoteFields',
                notes=[{"id": card_id,
                "fields": {"Front": card_front,
                "Back": card_back}}])
         return card_id
    except:
        return None


def main():
    add_card('test card 1234', 'change', 'test3')


if __name__ == '__main__':
    main()
