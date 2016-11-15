import mechanize
from lxml import html
from BaseModule import BaseModule


class Github(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", useragent)]

        login_page = br.open('https://github.com/login')
        assert br.viewing_html()
        br.select_form(nr=0)
        br["login"] = username
        br["password"] = password
        login_attempt = br.submit()
        login_html_str = str(login_attempt.read())
        # If '/two-factor' in the URL, Github is prompting for MFA code
        if '/two-factor' in login_attempt.geturl():
            return {
                'module': self.__class__.__name__,
                'auth_result': 'CHALLENGE',
                'display_name': '',
                'display_handle': ''
            }
        # If '/login' or '/session' in the URL, the login attempt failed
        if ('/login' in login_attempt.geturl() or
            '/session' in login_attempt.geturl()):
            return {
                'module': self.__class__.__name__,
                'auth_result': 'FAILED',
                'display_name': '',
                'display_handle': ''
            }
        # If redirected to "https://github.com/", login succeeded
        elif login_attempt.geturl() == 'https://github.com/':
            display_handle = self.get_handle_element(login_html_str)
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': '',
                'display_handle': display_handle
            }
        # If neither of the above occur, must be unknown issue
        else:
            # Output a copy of the HTML that was returned for debugging
            debug_filename = str(self.__class__.__name__) + \
                "_" + username + "_debug.html"
            with open("./debug/" + debug_filename, "a+") as f:
                f.write(login_html_str)
            return {
                'module': self.__class__.__name__,
                'auth_result': 'ERROR',
                'display_name': '',
                'display_handle': ''
            }

    def get_handle_element(self, login_html_str):
        try:
            login_attempt_html = html.fromstring(login_html_str)
            # Define a page element that only appears if the login is
            # successful
            logged_in_handle_element = login_attempt_html.xpath(
                '//*[@id="user-links"]/li[3]/div/div/div[1]/strong'
            )
            return str(logged_in_handle_element[0].text_content()).strip()
        except Exception as e:
            print "Debug: Unable to successfully parse handle element: " + \
                  str(e)
        return ''

github = Github()
