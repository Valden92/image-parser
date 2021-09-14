import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import aiofiles


async def download(session, link, soup):
    """Получение ссылки к файлу и его сохранение.
    """
    file_name = soup.find('div', class_="wall_page-speedbar").find('h1').text.strip()
    search_format_file = soup.find('div', class_="main_image").find('img').get('src').strip()
    format_file = search_format_file.split('.')
    path = 'image/{}.{}'.format(file_name, format_file[1])

    async with session.get(link, allow_redirects=False) as file:
        image = await file.content.read()

    async with aiofiles.open(path, 'wb') as out:
        await out.write(image)



async def soup_html(session, url, response):
    """Обработка html.
    """
    soup = BeautifulSoup(response, 'lxml')
    html_list = soup.find_all('div', class_="short_prev")

    for html in html_list:
        href = html.find('a').get('href')
        html_link = url + href

        async with session.get(html_link, allow_redirects=False) as resp:
            resp_text = await resp.text()
            second_soup = BeautifulSoup(resp_text, 'lxml')
            img_link = second_soup.find('div', class_="block_down").find('a').get('href')
            end_img_link = url + img_link
        await download(session, end_img_link, second_soup)


async def main(url):
    """Асинхронная функция исполнения основного тела программы.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=False) as resp:
            # resp_status = resp.status
            resp_text = await resp.text()
        img_links = await soup_html(session, url, resp_text)
        print(img_links)


if __name__ == '__main__':
    url = 'https://zastavok.net'

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url))
