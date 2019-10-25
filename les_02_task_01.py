import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime as dt

domain_url = 'https://geekbrains.ru'
blog_url = 'https://geekbrains.ru/posts'


def get_page_strict(soup):
    article_list = []
    posts_data = soup.find_all('div', class_='post-item')

    for post in posts_data:
        article_soup = get_soup(f"{domain_url}{post.find('a').attrs.get('href')}")
        try:
            image = post.find('img', class_='col-md-12').attrs.get('srcset')
        except Exception:
            image = ""
        article_dict = {
            'title': article_soup.find(class_='blogpost-title').text,
            'image': image,
            'text': article_soup.find('div', class_='blogpost-content').attrs.get('content'),
            'pub_date': article_soup.find('time', class_='text-md').attrs.get('datetime'),
            'author': article_soup.find('div', class_='text-lg').text
        }
        article_list.append(article_dict)
    return article_list


def get_soup(url):
    page_data = requests.get(url)
    soup_data = BeautifulSoup(page_data.text, 'lxml')
    return soup_data


def parser(url):
    article_list = []
    counter = 1
    while True:
        soup = get_soup(url)
        article_list.extend(get_page_strict(soup))
        try:
            url = soup.find('a', attrs={'rel': 'next'}, text='›').attrs.get('href')
        except AttributeError as e:
            break
        url = f"{domain_url}{url}"
        print(f"Страница {counter}")
        counter += 1
        if counter == 6:    # Долго ждать, да и сервер жалко
            return article_list
        time.sleep(1)
    return article_list


result_data = parser(blog_url)

with open(f'gd_articles_{int(dt.now().timestamp())}.json', 'w', encoding="UTF-8") as j_file:
    j_file.write(json.dumps(result_data))

print("Выполнено")
