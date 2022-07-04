import asyncio
import aiohttp

from bs4 import BeautifulSoup

user_agent = {'user-agent': 'Mozilla/5.0'}

all_data = []


async def get_page_data(session, url):
    """Function to receive information from the website"""
    async with session.get(url, headers=user_agent) as resp:
        resp_text = await resp.text()
        soup = BeautifulSoup(resp_text, "lxml")
        title = soup.find('title')
        all_data.append(f'{url} - {title.text}')


async def load_site_data(urls):
    """Function to collect the necessary data from all websites"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            try:
                task = asyncio.create_task(get_page_data(session, url))
                tasks.append(task)
                await asyncio.gather(*tasks)
            except aiohttp.ClientConnectorError:
                pass


if __name__ == '__main__':
    with open("news_sites.txt") as file:
        urls = [f'http://{website}' for website in file.read().split('\n')]
    asyncio.run(load_site_data(urls))
    print("\n".join(all_data))
