import requests
from bs4 import BeautifulSoup
from html import escape
import re
from time import sleep
from random import randint


def search_result_count(search_query, tries=10):
    try:
        encoded_arg = escape(search_query)

        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"

        r = requests.get('https://www.bing.com/search',
                         params={'q': encoded_arg},
                         headers={"User-Agent": custom_user_agent}
                         )
        soup = BeautifulSoup(r.text, features="html.parser")
        element = soup.find('span', {'class': 'sb_count'})

        # This worked first time
        if element is not None:
            element_text = element.text
            result_count_s = re.sub('[^0-9]', '', element_text)
            result_count = int(result_count_s)
            return result_count

        # There might be advertisements. Let us try the next page
        r = requests.get('https://www.bing.com/search',
                         params={'q': encoded_arg, 'first': '11'},
                         headers={"User-Agent": custom_user_agent}
                         )
        soup = BeautifulSoup(r.text, features="html.parser")
        element = soup.find('span', {'class': 'sb_count'})

        if element is not None:
            element_text = element.text
            result_count_s = re.sub('[0-9]+-[0-9]+', '', element_text)
            result_count_s = re.sub('[^0-9]', '', result_count_s)
            result_count = int(result_count_s)
            return result_count

        print('Nothing fetched')
        return 0
    except:
        # There might be advertisements. There may be internet connection issue. Retry
        if tries > 0:
            sleep(randint(500, 3050)/1000)
            return search_result_count(tries - 1)
        else:
            print('Max retries')
            return 0
