import json
import requests
from lxml import html
from BaseModule import BaseModule


class Pinterest(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        headers = {'user-agent': useragent}
        session = requests.Session()
        login_page = session.get(
            'https://pinterest.com/login',
            headers=headers)
        login_page_html = html.fromstring(login_page.content)

        # Define new headers to include the parsed-out CSRF token
        login_string = json.loads(
            '{"options":{"username_or_email":"' +
            username +
            '","password":"' +
            password +
            '"},"context":{}}')
        # This is probably unneccessary
        login_string = json.dumps(login_string)
        headers = {
            'User-Agent': useragent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken': session.cookies['csrftoken'],
            'X-NEW-APP': '1',
            'X-APP-VERSION': '96e65a2',
            'Origin': 'https://www.pinterest.com',
            'X-Pinterest-AppState': 'Active',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.pinterest.com/'
        }
        login_attempt = session.post(
            'https://www.pinterest.com/resource/UserSessionResource/create/',
            data={
                'source_url': '/login',
                'data': login_string,
                'module_path': 'App>LoginPage>Login>Button(class_name=primary data-test-loginBaseButton, text=Log in, type=submit, size=large, state_badgeValue="", state_accessibilityText=Log in, state_disabled=true)'
            },
            headers=headers, cookies=session.cookies, allow_redirects=False
        )
        auth_results = login_attempt.json()

        # If JSON value for errors is None, login was successful
        if auth_results['resource_response']['error'] is None:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': '',
                'display_handle': ''
            }
        # If JSON value contains error message, login failed
        elif ('password you entered' in
              str(auth_results['resource_response']['error'])):
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

pinterest = Pinterest()
