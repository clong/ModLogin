import requests
import json
from lxml import html
from BaseModule import BaseModule


class Square(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        headers = {'user-agent': useragent}
        session = requests.Session()
        login_page = session.get(
            'https://www.squareup.com/login',
            headers=headers)
        login_page_html = html.fromstring(login_page.content)

        # Load up CSRF token from cookies
        csrf_token = session.cookies["_js_csrf"]
        # Set POST payload
        payload = {'email': username, 'password': password}

        headers = {
            'User-Agent': useragent,
            'Host': 'api.squareup.com',
            'Content-Type': 'application/json',
            'Origin': 'https://squareup.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Referer': 'https://squareup.com/login',
            'X-Csrf-Token': csrf_token
        }
        login_attempt = session.post(
            'https://api.squareup.com/mp/login',
            data=json.dumps(payload),
            headers=headers, cookies=session.cookies, allow_redirects=False
        )

        auth_results = login_attempt.json()

        # If API returns 200 and JSON key with "trusted_devices", login was
        # successful
        if (login_attempt.status_code == 200 and
           'trusted_device' in auth_results):
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': '',
                'display_handle': ''
            }
        # If JSON value contains error message, login failed
        elif login_attempt.status_code == 401 or 'error' in auth_results:
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

square = Square()
