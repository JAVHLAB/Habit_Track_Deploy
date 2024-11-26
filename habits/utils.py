import requests

def send_expo_notification(token_push, mensaje):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "to": token_push,
        "sound": "default",
        "title": "Notificación de Hábitos",
        "body": mensaje
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()