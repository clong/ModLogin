import mechanize
from lxml import html
from BaseModule import BaseModule


class Myspace(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", useragent)]
        br.set_handle_redirect(True)
        br.set_handle_refresh(
            mechanize._http.HTTPRefreshProcessor(),
            max_time=1)
        login_page = br.open('https://myspace.com/login')
        assert br.viewing_html()
        br.select_form(name="signInForm")
        br["email"] = username
        br["password"] = password

        try:
            login_attempt = br.submit()
            login_html_str = str(login_attempt.read())
        except mechanize.HTTPError as response:
            if 'Error 401' in str(response):
                return {
                    'module': self.__class__.__name__,
                    'auth_result': 'FAILED',
                    'display_name': '',
                    'display_handle': ''
                }
        # If "User Logged In" string present in HTML, login was successful
        if "'User Logged In', 'Yes'" in login_html_str:
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
            login_attempt_html = html.fromstring(login_html_str)
            # Define a page element that only appears if the login is
            # successful
            logged_in_name_element = login_attempt_html.xpath(
                '//*[@id="global"]/nav/ul[1]/li[2]/a/span'
            )
            return str(logged_in_name_element[0].text_content())
        except Exception as e:
            print "Debug: Unable to successfully parse name element: " + str(e)
            return ''

myspace = Myspace()
