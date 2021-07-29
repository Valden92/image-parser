import requests
from bs4 import BeautifulSoup


url = 'https://zastavok.net'
r = requests.get(url, allow_redirects=False)
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

    # Получаем имя файла и сохраняем каждую картинку в папаку image
    file_name = second_soup.find('div', class_="wall_page-speedbar").find('h1').text.strip()
    path = 'image/{}.jpg'.format(file_name)
    file = requests.get(end_img_link, allow_redirects=False).content
    f = open(path, 'wb')
    f.write(file)
    f.close()


