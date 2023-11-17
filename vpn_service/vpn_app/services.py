from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup


def make_internal(request, site, site_name, site_url):
    parsed_url = urlparse(site.url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    response = requests.get(urljoin(base_url, site_url))

    count_data(site, request, response.content)

    soup_obj = BeautifulSoup(response.content, 'html.parser')

    for a_tag in soup_obj.find_all('a', href=True):
        href = a_tag.get('href')
        if href and not href.startswith(('http://', 'https://')):
            new_href = f'/{site_name}{href}/'
            a_tag['href'] = new_href

    for tag in soup_obj.find_all(['img', 'script', 'link'], href=True):
        href = tag.get('href')
        if href and not href.startswith(('http://', 'https://')):
            tag['href'] = base_url + href

    for tag in soup_obj.find_all(['img', 'script', 'link'], src=True):
        src = tag.get('src')
        if src and not src.startswith(('http://', 'https://')):
            tag['src'] = base_url + src

    return soup_obj


def count_data(site, request, content):
    if request.body:
        data_sent = len(request.body)
    else:
        data_sent = len(request.build_absolute_uri().encode('utf-8'))

    site.statistics.hits += 1
    site.statistics.data_sent += data_sent
    site.statistics.data_received += len(content)
    site.statistics.save()
