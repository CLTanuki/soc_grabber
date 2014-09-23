import requests

data = {'lang': 'ru', 'user_ids': '66749,13684080', 'fields': 'city, country, timezone, photo'}
resp = requests.get('https://api.vk.com/method/users.get', params=data)
print(resp.json()['response'])
