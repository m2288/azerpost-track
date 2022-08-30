import json
import time
import urllib
import requests
import mechanize
from flask import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
from fake_useragent import UserAgent
from datetime import datetime, timezone

app = Flask(__name__)

ua = UserAgent()



@app.route("/", methods=['GET'])
def home_page():
    data_set = {'Page': "Home", "Message": 'Home page loaded.',
                "Timestamp": time.time()}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route("/sorgu/", methods=['GET'])
def request_page():
    tracking_code = str(request.args.get('id'))
    netice = start_scraping(tracking_code)
    print(netice)
    user_query = str(request.args.get('id'))
    data_set = {"Cavab": netice}
    #{kod, son_odenis_meblegi, son_odenis_tarixi, yekun_borc}
    json_dump = json.dumps(data_set)

    return json_dump


def start_scraping(code):
    main_url = "http://azerpost.az/az/tracking/"
    track_code = "RA189555341LV"

    try:
        url = main_url + code
        print(url)
        br = mechanize.Browser()
        br.set_handle_equiv(False)
        br.addheaders = [('User-agent', ua.safari), ('Accept', '*/*')]
        br.set_debug_http(True)
        html = br.open(url)
        soup = BeautifulSoup(html)
        pages = []
        pages.append(url)
        i = 0
        Dict = {}
        for item in pages:

            page = requests.get(item)
            soup = BeautifulSoup(page.text, 'html.parser')

            for row in soup.table.find_all('tr')[1:]:
                tarix = row.td.text
                vaxt = row.td.find_next_sibling(
                    "td").text
                status = row.td.find_next_sibling(
                    "td").find_next_sibling("td").text
                menteqe = row.td.find_next_sibling(
                    "td").find_next_sibling("td").find_next_sibling("td").text

                setir = {"tarix": tarix, "vaxt": vaxt,
                         "status": status, "menteqe": menteqe}
                Dict[i] = setir
                i += 1
            print(Dict)
            return Dict

    except:
        Dict[i] = {"netice":"Məlumat tapılmadı"}
        return Dict


if __name__ == '__main__':
    app.run(port=7777)
