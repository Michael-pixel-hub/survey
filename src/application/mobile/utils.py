import json
import requests


def push(key, title, message, category):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAnlNzemQ:APA91bGGTMMnDFXozfhIgg6TuhVGhIQNH2TlMSak_U_ULYPbXTbwzt1pzCoRE74jh2lXT7XoDPwJ'
                         '5WVogQVXYFFvyHPPHrCe-5NEZuq2ts06ffppMEi9Yqp5syeflDSjFlj3SgusNN4p'
    }

    to = key

    if key is None:
        to = '/topics/all'

    data = {
        'to': to,
        'notification': {
            'title': title,
            'body': message,
            'sound': 'default',
            'priority': 'high',
        },
        'data': {
            'click_action': 'FLUTTER_NOTIFICATION_CLICK',
            'category': category,
        },
    }

    try:
        result = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(data))
    except Exception as e:
        return f'Ошибка: {e}'

    return result.text
