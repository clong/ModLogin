import mechanize
from lxml import html
from BaseModule import BaseModule


class Klout(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", useragent)]
        br.set_handle_redirect(True)
        br.set_handle_refresh(
            mechanize._http.HTTPRefreshProcessor(),
            max_time=1)
        login_page = br.open('https://klout.com/login')
        assert br.viewing_html()
        br.select_form(nr=0)
        br["email"] = username
        br["password"] = password
        login_attempt = br.submit()
        login_html_str = str(login_attempt.read())

        # If 'Klout | Sign In' in the URL, the login attempt failed
        if 'Klout | Sign In' in login_html_str:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'FAILED',
                'display_name': '',
                'display_handle': ''
            }
        # If 'Redirecting...' returned, the login was a success
        elif 'Redirecting...' in login_html_str:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': '',
                'display_handle': ''
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

klout = Klout()
