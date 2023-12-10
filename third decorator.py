import requests
from fake_headers import Headers
import bs4
from second_decorator import logger


@logger
def _get_response(some_url):
    fake_headers = Headers(os='win').generate()
    response = requests.get(some_url, headers=fake_headers)
    return response


def make_soup(some_url):
    res = _get_response(some_url).text
    return bs4.BeautifulSoup(res, features='html.parser')


def get_article_date(article):
    return article.find('time').attrs.get('title')


def get_article_header(article):
    header_class = 'tm-article-snippet__title tm-article-snippet__title_h1'
    return article.find(class_=header_class).find('span').text


def get_actual_link(article):
    url = 'https://habr.com/ru'
    full_text_link = article.find('h2').find('a').attrs.get('href')
    return f'{url}{full_text_link[3:]}'  # delete a part '/ru' from href


def check_article_body(full_article_soup):
    res_set = set()
    body_class_1 = 'article-formatted-body article-formatted-body article-formatted-body_version-2'
    article_soup = full_article_soup.find(class_=body_class_1)
    if article_soup is None:
        body_class_2 = 'article-formatted-body article-formatted-body article-formatted-body_version-1'
        article_soup = full_article_soup.find(class_=body_class_2)

    temp_list = article_soup.text.split()
    for word in temp_list:
        new_word = word.strip(',.«»!?#*').lower()
        res_set.add(new_word)

    return res_set