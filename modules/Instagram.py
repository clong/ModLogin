import json
import re
import requests
from lxml import html
from BaseModule import BaseModule


class Instagram(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        headers = {'user-agent': useragent}
        session = requests.Session()
        login_page = session.get(
            'https://instagram.com/accounts/login',
            headers=headers)
        login_page_html = html.fromstring(login_page.content)

        # Define new headers to include the parsed-out CSRF token
        headers = {
            'user-agent': useragent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': session.cookies['csrftoken'],
            'Accept': '*/*',
            'Referer': 'https://www.instagram.com'
        }
        login_attempt = session.post(
            'https://www.instagram.com/accounts/login/ajax/',
            data={
                'username': username,
                'password': password
            },
            headers=headers, cookies=session.cookies, allow_redirects=False
        )
        auth_results = login_attempt.json()

        # If 'authenticated' JSON value is True, login was successful
        if auth_results["authenticated"]:
            display_handle = str(auth_results["user"])
            display_name = self.get_name_element(
                session, headers, display_handle)
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': display_name,
                'display_handle': display_handle
            }
        # If 'authenticated' JSON value is False, login failed
        elif auth_results["authenticated"] is False:
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
                f.write(auth_results)
            return {
                'module': self.__class__.__name__,
                'auth_result': 'ERROR',
                'display_name': '',
                'display_handle': ''
            }

    def get_name_element(self, session, headers, handle):
        try:
            display_name_page = session.get('https://instagram.com/' + handle,
                                            headers=headers,
                                            cookies=session.cookies
                                            )
            # Define a regex to parse out the user's full name
            matches = re.search(
                r'\"full_name\"\:\s\"([\w\d\s]+)\"',
                display_name_page.content)
            display_name = str(matches.group(1))
            return display_name
        except Exception as e:
            print "Debug: Unable to successfully parse name element: " + str(e)
            return ''

instagram = Instagram()
