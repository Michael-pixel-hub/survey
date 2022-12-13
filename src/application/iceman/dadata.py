from application.agent.dadata import Dadata
from preferences.utils import get_setting


def fill_inn_data(store):

    api_key = get_setting('agent_dadataapikey')
    secret_key = get_setting('agent_dadatasecretkey')

    if not api_key:
        raise Exception('No api key')

    if not secret_key:
        raise Exception('No secret key')

    dadata = Dadata(api_key, secret_key)
    data = dadata.find_by_id('party', store.inn)

    if type(data) == str:
        return data

    if data is None:
        return 'No data'

    if len(data) < 1:
        return 'No data'

    try:
        store.inn_name = data[0]['value']
    except:
        pass

    try:
        store.inn_name_1 = data[0]['data']['name']['full_with_opf']
    except:
        pass

    try:
        store.inn_director_title = data[0]['data']['management']['post']
    except:
        pass

    try:
        store.inn_director_name = data[0]['data']['management']['name']
    except:
        pass

    try:
        store.inn_address = data[0]['data']['address']['value']
    except:
        pass

    try:
        store.inn_region = data[0]['data']['address']['data']['region']
    except:
        pass

    try:
        store.inn_kpp = data[0]['data']['kpp']
    except:
        pass

    if not store.inn_director_name:
        try:
            if data[0]['data']['type'] == 'INDIVIDUAL':
                store.inn_director_name = data[0]['data']['name']['full']
                store.inn_director_title = data[0]['data']['opf']['full']
        except:
            pass

    try:
        store.inn_ogrn = data[0]['data']['ogrn']
    except:
        pass

    try:
        store.inn_okved = data[0]['data']['okved']
    except:
        pass

    try:
        store.inn_type = data[0]['data']['opf']['short']
    except:
        pass

    return 'Ok'
