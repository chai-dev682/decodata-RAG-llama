import os
from urllib.parse import urljoin, urlparse
import re
import asyncio
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm
import aiohttp
import ssl
import certifi

# Concurrency settings.
concurrency = 20


def get_links_from_base_url(soup, base_url):
    def is_relative_link(link):
        return not link.startswith('http')

    def is_one_deeper_level(link, base_url):
        parsed_link = urlparse(link)
        parsed_base_url = urlparse(base_url)

        if parsed_link.netloc != parsed_base_url.netloc:
            return False

        url_path = parsed_link.path.rstrip('/')
        base_path = parsed_base_url.path.rstrip('/')

        return url_path.startswith(base_path + '/') and url_path.count('/') == base_path.count('/') + 1

    def extract_links(soup, base_url):
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('tel:'):
                continue
            elif href and href.startswith('mailto:'):
                continue
            elif href and 'javascript' in href:
                continue
            elif href and is_relative_link(href):
                if href.startswith('/'):
                    links.append(urljoin(base_url, href))
                else:
                    links.append(urljoin(base_url + '/', href))
            elif href and is_one_deeper_level(href, base_url):
                links.append(href)
        return list(set(links))  # Remove duplicates

    def filter_one_step_deeper(urls, base_url):
        base = urlparse(base_url)

        def is_valid_url(url):
            try:
                current = urlparse(url)
                if current.hostname != base.hostname:
                    return False
                if any(keyword in current.path for keyword in [
                    'career', 'index', 'contact', 'download',
                    'cookie', 'policy', 'credits', 'privacy',
                    'blog', 'login', 'sitemap', 'faq',
                    'password', 'javascript', 'regist', 'callto',
                    'news', 'terms', 'site-map']):
                    return False
                base_segments = [segment for segment in base.path.split('/') if segment]
                current_segments = [segment for segment in current.path.split('/') if segment]
                return len(current_segments) == len(base_segments) + 1
            except Exception as error:
                print('Error parsing URL:', url, error)
                return False

        return list(filter(is_valid_url, urls))

    def format_and_remove_duplicates(urls):
        formatted_urls = [url if url.endswith('/') else url + '/' for url in urls]
        unique_urls = list(set(formatted_urls))
        return unique_urls

    first_links = extract_links(soup, base_url)
    links = filter_one_step_deeper(first_links, base_url)
    links = format_and_remove_duplicates(links)

    return links


async def scrapfish_gather_links(url, session):
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        async with session.request(
                method="GET",
                url="https://scraping.narf.ai/api/v1/",
                params={
                    "api_key": os.environ["SCRAPING_FISH_API_KEY"],
                    "url": url,
                    "render_js": "true"
                },
                ssl=ssl_context
        ) as response:
            return await response.text()
    except Exception:
        return None


async def fetch_links(url):
    all_links = []

    async with aiohttp.ClientSession() as session:
        response = await scrapfish_gather_links(url, session)
        if response is not None:
            soup = BeautifulSoup(response, 'html.parser')
            linked_urls = get_links_from_base_url(soup, url)
            print(linked_urls)
            all_links.extend(linked_urls)
        if url not in all_links:
            all_links.append(url)
    return all_links


def return_text(soup):
    try:
        # Remove script, style, and other unnecessary elements.
        for tag in ['script', 'style', 'noscript', 'iframe', 'header', 'footer']:
            for element in soup.find_all(tag):
                element.decompose()
        # Extract and clean the text from the body or specific parts of the page.
        text = soup.body.get_text()
        # Using regular expressions to replace multiple spaces, tabs, newlines, etc., with a single space and trim.
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as err:
        return None


async def scrapfish_gather(url, session, semaphore, progress_bar):
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with semaphore:

        try:
            async with session.request(
                    method="GET",
                    url="https://scraping.narf.ai/api/v1/",
                    params={
                        "api_key": os.environ["SCRAPING_FISH_API_KEY"],
                        "url": url,
                        "render_js": "true"
                    },
                    ssl=ssl_context
            ) as response:
                text = await response.text()
                progress_bar.update(1)
                return text

        except Exception:
            progress_bar.update(1)
            return None



async def fetch_content(urls):
    data = {}
    semaphore = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:
        progress_bar = tqdm(total=len(urls), desc="Fetching URLs...")

        tasks_list = [scrapfish_gather(url, session, semaphore, progress_bar) for url in urls]
        results = await asyncio.gather(*tasks_list)

        for index, response in enumerate(results):
            try:
                if response is not None:
                    soup = BeautifulSoup(response, 'html.parser')
                    title = soup.title.string if soup.title else 'XXXX'
                    content = return_text(soup)

                    if content is not None:
                        data[urls[index]] = f"Website Tile: \n{title}\n\nWebsite Content: {content}"
                else:
                    data[urls[index]] = ""
            except Exception:
                data[urls[index]] = ""

    return data
