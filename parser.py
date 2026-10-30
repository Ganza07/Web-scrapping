import requests
from bs4 import BeautifulSoup

# 1. Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'ИИ', 'IT']

def parse_habr():
    url = "https://habr.com/ru/all/"

    # Притворяемся обычным браузером, чтобы Хабр нас не заблокировал
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # 2. Делаем запрос к странице
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при получении страницы. Код ответа: {response.status_code}")
        return
    # 3. Создаём объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 4. Находим все блоки статей.
    articles = soup.find_all('article')
    print(f"Найдено статей на странице: {len(articles)}\n")
    print("Подходящие статьи:")
    print("-" * 50)

    # 5. Проходимся по каждой статье
    for article in articles:
        # Ищем заголовок
        title_tag = article.find('h2')
        if not title_tag:
            continue

        title = title_tag.text.strip()

        # Ищем ссылку внутри заголовка
        link_tag = title_tag.find('a')
        if not link_tag:
           continue

        # Ссылка часто относительная, добавляем домен
        href = link_tag.get('href')
        link = f"https://habr.com{href}" if href.startswith('/') else href

        # Ищем дату публикации
        date_tag = article.find('time')
        if not date_tag:
            date_tag = article.find('span', class_='tm-article-datetime-published__time')
        date = date_tag.text.strip() if date_tag else "Дата не указана"

        # Берем весь текст из блока статьи (включая превью) и переводим в нижний регистр для поиска
        preview_text = article.text.lower()

        # 6. Проверяем, есть ли хоть одно ключевое слово в тексте
        # Создаем список слов из KEYWORDS, которые нашлись в тексте
        found_keywords = [kw for kw in KEYWORDS if kw.lower() in preview_text]

        # Если список не пустой, значит совпадение есть
        if found_keywords:
            # Выводим в требуемом формате: <дата> – <заголовок> – <ссылка>
            print(f"{date} – {title} – {link}")
            print(f"  ↳ Найдены слова: {', '.join(found_keywords)}\n")

if __name__ == "__main__":
    parse_habr()
