import json
import requests
from lxml import html
from BaseModule import BaseModule


class Stumbleupon(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        headers = {'user-agent': useragent}
        session = requests.Session()
        login_page = session.get(
            'https://www.stumbleupon.com',
            headers=headers)
        login_page_html = html.fromstring(login_page.content)

        headers = {
            'User-Agent': useragent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://www.stumbleupon.com',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Referer': 'http://www.stumbleupon.com/login',
            # These values can be static for the auth request
            'X-Su-ClientId': '2c2cd658-2bcf-04b7-fa2d-fa8a8bb91a7e',
            'X-Su-ConsumerKey': '35774027dc2f2f64a280e63eafb018505c045655',
            'X-Su-Version': 'spa 3.1 js master_7fc4746 SU'
        }
        login_attempt = session.post(
            'https://www.stumbleupon.com/api/v2_0/auth/login',
            data={
                'username': username,
                'password': password
            },
            headers=headers, cookies=session.cookies, allow_redirects=False
        )
        auth_results = login_attempt.json()

        # If JSON value for '_success' is True, login was successful
        if (auth_results['_error'] is None and
           auth_results['_success']):
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': '',
                'display_handle': ''
            }
        # If JSON value for '_success' is False, login failed
        elif not auth_results['_success']:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'FAILED',
                'display_name': '',
                'display_handle': ''
            }
        else:
            # If none of the above occur, must be unknown issue
            # Output a copy of the HTML that was returned for debugging
            debug_filename = str(self.__class__.__name__) + \
                "_" + username + "_debug.html"
            with open("./debug/" + debug_filename, "a+") as f:
                f.write(json.dumps(auth_results))
                return {
                    'module': self.__class__.__name__,
                    'auth_result': 'ERROR',
                    'display_name': '',
                    'display_handle': ''
                }

stumbleupon = Stumbleupon()
