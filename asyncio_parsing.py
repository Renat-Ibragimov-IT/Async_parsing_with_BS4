import asyncio
from pprint import pp

import aiohttp
from bs4 import BeautifulSoup

USER_AGENT = {'user-agent': 'Mozilla/5.0'}


async def get_page_data(session, url):
    """Function to receive information from the website"""
    try:
        async with session.get(url, headers=USER_AGENT, timeout=5) as resp:
            resp_text = await resp.text()
        return {'url': url, 'html': resp_text}
    except aiohttp.ClientConnectorError:
        print(f'{url}: Page not found')
    except asyncio.exceptions.TimeoutError:
        print(f'{url}: Timeout Error')


async def load_site_data(urls):
    """Function to collect the necessary data from all websites"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_page_data(session, url))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def main(urls):
    """This function will run program"""
    async with aiohttp.ClientSession():
        return await load_site_data(urls)


def parser(data):
    """This function will extract required part of info"""
    all_data = []
    for info in data:
        if info:
            soup = BeautifulSoup(info['html'], "html.parser")
            title = soup.find('title')
            all_data.append(f'{info["url"]} - {title.text}')
    return pp(all_data)


if __name__ == '__main__':
    with open("news_sites.txt") as file:
        links = [f'http://{website}' for website in file.read().splitlines()]
    all_info = asyncio.run(main(links))
    parser(all_info)
