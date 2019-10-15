import requests
import json
from datetime import datetime as dt

username = input("Введите имя пользователя на GitHub: ")
password = input("Введите пароль к GitHub: ")

user = requests.get("https://api.github.com/user", auth=(username, password))
print(user.text)

user = user.json()
print(user)
with open(f'github_user_{int(dt.now().timestamp())}.json', 'w', encoding="UTF-8") as j_file:
    j_file.write(json.dumps(user))

repos = requests.get('https://api.github.com/user/repos', auth=(username, password))
print(repos.json()[1])

for repo in repos.json():
    if not repo['private']:
        print(repo['html_url'])
        print(repo['full_name'])
