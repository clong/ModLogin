import mechanize
from lxml import html
from BaseModule import BaseModule


class Yelp(BaseModule):

    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", useragent)]

        login_page = br.open('https://www.yelp.com/login?return_url=%2F')
        assert br.viewing_html()
        for form in br.forms():
            if form.attrs.get("id") == 'ajax-login':
                br.form = form
        br["email"] = username
        br["password"] = password
        login_attempt = br.submit()
        login_html_str = str(login_attempt.read())
        # Return -2 if Yelp starts throwing a captcha
        if 'word verification below to continue.' in login_html_str:
            return {
                'module': self.__class__.__name__,
                'auth_result': 'CAPTCHA',
                'display_name': '',
                'display_handle': ''
            }
        # If '/login' in the URL, the login attempt failed
        elif '/login' in login_attempt.geturl():
            return {
                'module': self.__class__.__name__,
                'auth_result': 'FAILED',
                'display_name': '',
                'display_handle': ''
            }
        # If no captcha or failed login, assume the login was successful
        elif '-' in login_attempt.geturl():
            display_name = self.get_name_element(login_html_str)
            return {
                'module': self.__class__.__name__,
                'auth_result': 'SUCCESS',
                'display_name': display_name,
                'display_handle': ''
            }
        else:
            # If none of the above occur, must be unknown issue
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
                '''
                //*[@id="super-container"]/div[2]/div[2]/div[2]/div[1]/div[1]/
                div/div[2]/ul[1]/li[1]/a
                '''
            )
            return str(logged_in_name_element[0].text_content())
        except Exception as e:
            print "Debug: Unable to successfully parse name element: " + str(e)
        return ''

yelp = Yelp()
