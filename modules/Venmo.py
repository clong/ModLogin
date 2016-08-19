import requests
from lxml import html
from BaseModule import BaseModule


class Venmo(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        headers = {'user-agent': useragent}
        session = requests.Session()
        login_page = session.get(
            'https://venmo.com/account/sign-in/',
            headers=headers)
        login_page_html = html.fromstring(login_page.content)

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'venmo.com',
            'Origin': 'https://venmo.com',
            'Referer': 'https://venmo.com/',
            'User-Agent': useragent,
            'X-Requested-With': 'XMLHttpRequest'
        }
        login_attempt = session.post(
            'https://venmo.com/login',
            data={
                'phoneEmailUsername': username,
                'password': password,
                'csrftoken2': 'eObBxpFOsSgmVLJlCeedFwFi7o8uGnI2'
            },
            headers=headers, cookies=session.cookies, allow_redirects=False
        )
        auth_result = login_attempt.json()

        # Return if Venmo challenges the login
        # Venmo is trying to send SMS codes to the linked phone number
        if login_attempt.status_code == 401 and auth_result["error"][
                "message"] == 'Additional authentication is required':
            return {
                'module': self.__class__.__name__,
                'auth_result': 'CHALLENGE',
                'display_name': '',
                'display_handle': ''
            }
        # If login endpoint returns 200 and zero-length response, login was
        # successful
        elif login_attempt.status_code == 200 and len(login_attempt.text) == 0:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': '',
                'display_handle': ''
            }
        # If login endpoint returns 400 or contains incorrect password message,
        # login failed
        elif (login_attempt.status_code == 400 or
              auth_result["error"]["message"] == 'Your email or password was incorrect'):
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
                f.write(login_attempt.text)
                return {
                    'module': self.__class__.__name__,
                    'auth_result': 'ERROR',
                    'display_name': '',
                    'display_handle': ''
                }

venmo = Venmo()
