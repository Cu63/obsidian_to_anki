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


def add_card() -> bool:
    desk_name = 'test2'
    if check_desk(desk_name):
        print('%s is exists' % (desk_name))
    else:
        if not create_deck(desk_name):
            print("error: can't creat deck")
            return False
        print('Deck %s was created.' % (desk_name))
    return True


def create_deck(deck_name: str) -> bool:
    try:
        invoke('createDeck', deck=deck_name)
        return True
    except:
        return False


def check_desk(desk_name: str) -> bool:
    result = invoke('deckNames')
    if desk_name in result:
        return True
    return False


def main():
    add_card()


if __name__ == '__main__':
    main()
