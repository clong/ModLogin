import requests
from lxml import html
from BaseModule import BaseModule


class Twitter(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        headers = {'user-agent': useragent}
        session = requests.Session()
        login_page = session.get('https://twitter.com/login', headers=headers)
        login_page_html = html.fromstring(login_page.content)

        authenticity_token_element = login_page_html.xpath(
            '''
            //*[@id="doc"]/div[1]/div/div/div/div/ul[1]/li/div[2]/form
            /input[3]/@value
            '''
        )
        authenticity_token = str(authenticity_token_element[0])

        login_attempt = session.post(
            'https://twitter.com/sessions',
            data={
                'session[username_or_email]': username,
                'session[password]': password,
                'authenticity_token': authenticity_token,
                'scribe_log:': '', 'redirect_after_login': '/',
                'authenticity_token': authenticity_token,
                'remember_me': '0'},
            headers=headers
        )
        login_attempt_html = html.fromstring(login_attempt.content)
        # Return if Twitter challenges the login
        if '/login_challenge' in str(login_attempt.url):
            return {
                'module': self.__class__.__name__,
                'auth_result': 'CHALLENGE',
                'display_name': '',
                'display_handle': ''
            }
        # If '/login/error' in the URL, the login attempt failed
        elif '/login/error' in login_attempt.url:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'FAILED',
                'display_name': '',
                'display_handle': ''
            }
        # If no challenge or failed login, assume the login was successful
        elif login_attempt.url == 'https://twitter.com/':
            logged_in_elements = self.get_name_element(login_attempt_html)
            display_name, display_handle = logged_in_elements.split(':')
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': display_name,
                'display_handle': display_handle
            }
        else:
            # If none of the above occur, must be unknown issue
            # Output a copy of the HTML that was returned for debugging
            debug_filename = str(self.__class__.__name__) + \
                "_" + username + "_debug.html"
            with open("./debug/" + debug_filename, "a+") as f:
                f.write(login_attempt.content)
            return {
                'module': self.__class__.__name__,
                'auth_result': 'ERROR',
                'display_name': '',
                'display_handle': ''
            }

    def get_name_element(self, login_attempt_html):
        try:
            # Define a page element that only appears if the login is
            # successful
            logged_in_name_element = login_attempt_html.xpath(
                '//*[@id="page-container"]/div[1]/div[1]/div/div[2]/div/a'
            )
            logged_in_handle_element = login_attempt_html.xpath(
                '''
                //*[@id="page-container"]/div[1]/div[1]/div/div[2]/span/a/span
                '''
            )
            display_name = logged_in_name_element[0].text_content()
            display_handle = logged_in_handle_element[0].text_content()
            return str(display_name + ':' + display_handle)
        except Exception as e:
            print "Debug: Unable to successfully parse name element: " + str(e)
            return ':'

twitter = Twitter()
