import mechanize
from lxml import html
from BaseModule import BaseModule


class Reddit(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", useragent)]

        login_page = br.open('https://reddit.com/login')
        assert br.viewing_html()
        for form in br.forms():
            if form.attrs.get("id") == 'login-form':
                br.form = form
        br["user"] = username
        br["passwd"] = password
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
        # Redirect to https://reddit.com or logout button preset == success
        elif (login_attempt.geturl() == 'https://reddit.com' or
              'logout hover' in login_html_str):
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
                '//*[@id="header-bottom-right"]/span[1]/a'
            )
            return str(logged_in_handle_element[0].text_content())
        except Exception as e:
            print "Debug: Unable to successfully parse handle element: " + \
                  str(e)
        return ''

reddit = Reddit()
