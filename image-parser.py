import requests
from bs4 import BeautifulSoup


def upload_image(url, page_url):
    """Скачивает изображения со страницы html."""
    r = requests.get(page_url, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'lxml')
    html_list = soup.find_all('div', class_="short_prev")

    for img_html in html_list:
        # Получаем ссылку, которая хранится в href и соединяем с с основным url
        href = img_html.find('a').get('href')
        img_html_link = url + href

        # Выгружаем вторичные html для получения картинок в максимальном разрешении
        second_html = requests.get(img_html_link, allow_redirects=False)
        second_soup = BeautifulSoup(second_html.text, 'lxml')

        # Так же получаем окончание ссылки на картинку из href и соединяем с основным url
        img_link = second_soup.find('div', class_="block_down").find('a').get('href')
        end_img_link = url + img_link

        # Получаем имя файла и формат, и сохраняем каждую картинку в папаку image
        file_name = second_soup.find('div', class_="wall_page-speedbar").find('h1').text.strip()
        search_format_file = second_soup.find('div', class_="main_image").find('img').get('src').strip()
        format_file = search_format_file.split('.')
        path = 'image/{}.{}'.format(file_name, format_file[1])
        file = requests.get(end_img_link, allow_redirects=False).content

        with open(path, 'wb') as out:
            out.write(file)


url = 'https://zastavok.net'

# Добавляем индекс страницы (с какой и по какую качать)
link_start = 1
link_end = 2
if link_start == link_end:
    new_url = '{}/{}/'.format(url, str(link_end))
    upload_image(url, new_url)

else:
    for i in range(link_start, link_end + 1):
        new_url = '{}/{}/'.format(url, str(i))
        print(new_url)
        upload_image(url, new_url)
