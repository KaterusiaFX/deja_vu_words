import requests
from bs4 import BeautifulSoup


def add_word_to_url(word):
    initial_english_url = 'https://www.multitran.com/m.exe?l1=1&l2=2&s='
    final_url = initial_english_url + word
    return final_url


def get_html(url):
    try:
        result = requests.get(url)
        result.encoding = 'utf-8'
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_transcription(word):
    html = get_html(add_word_to_url(word))
    if not html:
        return False
    soup = BeautifulSoup(html, 'html.parser')
    word_info = soup.findAll('table')[1].findAll('td')[1]
    transcription = word_info.find('span').text
    return transcription


if __name__ == "__main__":
    word = input('Введите слово на английском ')
    print(get_transcription(word))
