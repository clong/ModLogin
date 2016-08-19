import mechanize
import re
from lxml import html
from BaseModule import BaseModule


class Okcupid(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", useragent)]

        login_page = br.open('https://www.okcupid.com/login')
        assert br.viewing_html()
        for form in br.forms():
            if form.attrs.get("id") == 'loginbox_form':
                br.form = form
        br["username"] = username
        br["password"] = password
        login_attempt = br.submit()
        login_html_str = str(login_attempt.read())
        # If '/login' in the URL, the login attempt failed
        if '/login' in login_attempt.geturl():
            return {
                'module': self.__class__.__name__,
                'auth_result': 'FAILED',
                'display_name': '',
                'display_handle': ''
            }
        # If redirect to '/home', login succeeded.
        elif '/home' in login_attempt.geturl():
            display_name = self.get_name_element(login_html_str)
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': display_name,
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

    def get_name_element(self, login_html_str):
        try:
            # Define a page element that only appears if the login is
            # successful
            matches = re.search(
                r'\"username\"\s\:\s\"([\w\d\s]+)\"',
                login_html_str)
            display_name = str(matches.group(1))
            return display_name
        except Exception as e:
            print "Debug: Unable to successfully parse name element: " + str(e)
        return ''

okcupid = Okcupid()
