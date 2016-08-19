import requests
from lxml import html
from BaseModule import BaseModule


class Tumblr(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        headers = {'user-agent': useragent}
        session = requests.Session()
        login_page = session.get(
            'https://www.tumblr.com/login',
            headers=headers)
        login_page_html = html.fromstring(login_page.content)
        try:
            form_key_element = login_page_html.xpath(
                '//*[@id="tumblr_form_key"]/@content'
            )
            form_key = str(form_key_element[0])
        except:
            print "Unable to parse form_key from DOM. Aborting."
            return {
                'module': self.__class__.__name__,
                'auth_result': 'ERROR',
                'display_name': '',
                'display_handle': ''
            }

        headers = {
            'authority': 'www.tumblr.com',
            'method': 'POST',
            'path': '/login',
            'scheme': 'https',
            'cache-control': 'max-age=0',
            'user-agent': useragent,
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.tumblr.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'uupgrade-insecure-requests': '1',
            'referer': 'https://www.tumblr.com/login',
        }
        login_attempt = session.post(
            'https://www.tumblr.com/login',
            data={
                'determine_email': username,
                'user[email]': username,
                'user[password]': password,
                'tumblelog[name]': '',
                'user[age]': '',
                'context': 'other',
                'version': 'STANDARD',
                'follow:': '',
                'http_referer': 'https://www.tumblr.com/logout',
                'form_key': form_key,
                'seen_suggestion': '0',
                'used_suggestion': '0',
                'used_auto_suggestion': '0',
                'about_tumblr_slide': '',
                'random_username_suggestions': '["FreshTurtleTimeMachine","JoyfulFoxKing","TremendouslyFamousTiger","SillyHotTubDelusion","LuckyCrownParadise"]'
            },
            headers=headers, cookies=session.cookies, allow_redirects=False
        )

        # Return if Tumblr challenges the login
        # Captcha will go away if cleared online until next failed login
        # attempt
        if 'Tumblr.RegistrationForm.errors = ["Don\'t forget to fill out the Captcha!"];' in login_attempt.text:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'CHALLENGE',
                'display_name': '',
                'display_handle': ''
            }
        # If login endpoint returns 302 and zero-length response, login was
        # successful
        elif (login_attempt.status_code == 302 and
              len(login_attempt.content) == 0):
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': '',
                'display_handle': ''
            }
        # If login endpoint returns 200 or contains error in response, login
        # failed
        elif (login_attempt.status_code == 200 or
             'Tumblr.RegistrationForm.errors' in auth_results):
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

tumblr = Tumblr()
