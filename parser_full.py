import requests
from bs4 import BeautifulSoup
import time  # Важно для паузы между запросами

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'ИИ', 'нейросеть', 'разработка']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


# Функция, которая заходит ВНУТРЬ статьи и ищет слова там
def check_article_content(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup_article = BeautifulSoup(response.text, 'html.parser')
            text = soup_article.text.lower()

            # Ищем совпадения
            found = [kw for kw in KEYWORDS if kw.lower() in text]
            return found
    except Exception as e:
        print(f"Ошибка при проверке {url}: {e}")
    return []


def parse_habr_full():
    url = "https://habr.com/ru/all/"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Ошибка получения страницы")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    print(f"Найдено статей на странице: {len(articles)}")
    print("Начинаем глубокую проверку (это займет время)...")
    print("-" * 50)

    count_found = 0

    for article in articles:
        title_tag = article.find('h2')
        if not title_tag: continue

        title = title_tag.text.strip()
        link_tag = title_tag.find('a')
        if not link_tag: continue

        href = link_tag.get('href')
        link = f"https://habr.com{href}" if href.startswith('/') else href

        date_tag = article.find('time')
        date = date_tag.text.strip() if date_tag else "Дата не указана"

        #  вызываем функцию, которая скачивает саму статью
        found_in_full_text = check_article_content(link)

        if found_in_full_text:
            print(f"{date} – {title}")
            print(f"{link}")
            print(f"Найдено в полном тексте: {', '.join(found_in_full_text)}\n")
            count_found += 1

        # Пауза 0.5 секунды
        time.sleep(0.5)

    print(f"\nИтого найдено подходящих статей: {count_found}")


if __name__ == "__main__":
    parse_habr_full()