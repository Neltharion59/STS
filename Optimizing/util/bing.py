import requests
from bs4 import BeautifulSoup
from html import escape
import re


def search_result_count(search_query):
    encoded_arg = escape(search_query)

    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

    r = requests.get('https://www.bing.com/search',
                     params={'q': encoded_arg},
                     headers={"User-Agent": custom_user_agent}
                     )
    soup = BeautifulSoup(r.text, features="html.parser")

    element_text = soup.find('span', {'class': 'sb_count'}).text
    result_count_s = re.sub('[^0-9]', '', element_text)
    result_count = int(result_count_s)

    return result_count
