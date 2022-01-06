import requests
import json
from bs4 import BeautifulSoup
# import xmltodict
# import xmltojson
# import xml.etree.ElementTree as ET
# from requests_html import HTML
from requests_html import AsyncHTMLSession

base_url = 'https://www.kaggle.com/'
username = 'iguyon'
url = base_url+username

asession = AsyncHTMLSession()

async def web_scraper():
    r = await asession.get(url)
    print(dir(r))
    print(r.text)
    r.html.render()
    print(r.text)

web_scraper()