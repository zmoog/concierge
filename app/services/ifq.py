# import logging
import os
import tempfile
import requests

from lxml import html

IFQ_LOGIN_URL = 'https://shop.ilfattoquotidiano.it/login/'
IFQ_ARCHIVE_URL = 'https://shop.ilfattoquotidiano.it/archivio-edizioni/'


# logging.basicConfig(level=logging.DEBUG)

class IFQ(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def download_pdf(self, pub_date):

        login_payload = dict(
            username=self.username,
            password=self.password,
            _wp_http_referer='/login/',
            redirect='/login/',
            login='Accedi')

        edition_payload = dict(
            # edition_date='30/05/2015',
            edition_date=pub_date.strftime('%d/%m/%Y'),
            # edition_date_nonce=edition_date_nonce,
            _wp_http_referer='/abbonati/')

        # logging.debug('login_payload: {}'.format(login_payload))

        with requests.Session() as session:

            resp = session.get(IFQ_LOGIN_URL)
            # print(IFQ_LOGIN_URL) 
            # print(resp.status_code) 
            # print(resp.cookies)
            tree = html.fromstring(resp.text)
            # print('resp.text', resp.text)
            # print('tree', tree)
            nonce = tree.xpath('//input[@id="woocommerce-login-nonce"]')
            # print('woocommerce-login-nonce', nonce)
            login_payload['woocommerce-login-nonce'] = nonce[0].value

            # cookies = dict(cookies_are='working')
            resp = session.post(IFQ_LOGIN_URL, data=login_payload)
            # resp = session.post(TEST_URL, data=payload)  # , cookies=cookies)

            # print(resp.status_code)
            # logging.debug(resp.text)

            resp = session.get(IFQ_ARCHIVE_URL)
            # logging.debug(resp.status_code)
            # logging.debug(resp.text)

            tree = html.fromstring(resp.text)
            nonce = tree.xpath('//input[@name="edition_date_nonce"]')
            # print('nonce', nonce)
            edition_date_nonce = nonce[0].value

            edition_payload['edition_date_nonce'] = edition_date_nonce

            # logging.debug(edition_payload)
            # print(edition_payload)

            resp = session.post(IFQ_ARCHIVE_URL,
                                data=edition_payload,
                                stream=True)

            if resp.status_code != 200:
                # print(resp.text)
                raise IssueNotAvailable()

            file = tempfile.NamedTemporaryFile(delete=False)

            with file as f:
                # with open(local_filename, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    # filter out keep-alive new chunks
                    if chunk:
                        f.write(chunk)
                        f.flush()

            return file.name


class IssueNotAvailable(Exception):
    pass
