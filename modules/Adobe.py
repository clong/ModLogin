import mechanize
from lxml import html
from BaseModule import BaseModule


class Adobe(BaseModule):
    def login(self, username, password, useragent):
        useragent = BaseModule().define_user_agent(useragent)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", useragent)]

        login_page = br.open('https://adobeid-na1.services.adobe.com/renga-idprovider/pages/login?callback=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fadobeid%2Fadobedotcom2%2FAdobeID%2Ftoken%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.adobe.com%252F%2523from_ims%253Dtrue%2526old_hash%253D%2526api%253Dauthorize&client_id=adobedotcom2&scope=creative_cloud%2CAdobeID%2Copenid%2Cgnav%2Cread_organizations%2Cadditional_info.projectedProductContext%2Csao.ACOM_CLOUD_STORAGE%2Csao.stock%2Csao.cce_private%2Cadditional_info.roles&display=web_v2&denied_callback=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fdenied%2Fadobedotcom2%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.adobe.com%252F%2523from_ims%253Dtrue%2526old_hash%253D%2526api%253Dauthorize%26response_type%3Dtoken&relay=71c17d6f-95bd-4077-9932-1fc4455f0987&locale=en_US&flow_type=token&dc=false&eu=false&client_redirect=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fredirect%2Fadobedotcom2%3Fclient_redirect%3Dhttps%253A%252F%252Fwww.adobe.com%252F%2523from_ims%253Dtrue%2526old_hash%253D%2526api%253Dauthorize&idp_flow_type=login')
        assert br.viewing_html()
        for form in br.forms():
            if form.attrs.get("id") == 'adobeid_signin':
                br.form = form
        br["username"] = username
        br["password"] = password
        login_attempt = br.submit()
        login_html_str = str(login_attempt.read())

        # If 'services.adobe.com' in the URL, the login attempt failed
        if 'services.adobe.com' in login_attempt.geturl():
            return {
              'module': self.__class__.__name__,
              'auth_result': 'FAILED',
              'display_name': '',
              'display_handle': ''
            }
        # If 'index.loggedin.json' present in HTML, login == success
        elif 'index.loggedin.json' in login_html_str:
            return {
              'module': self.__class__.__name__,
              'auth_result': 'SUCCESS',
              'display_name': '',
              'display_handle': ''
            }
        else:
            # Output a copy of the HTML that was returned for debugging
            debug_filename = str(self.__class__.__name__) + "_" + username + \
             "_debug.html"
            with open("./debug/" + debug_filename, "a+") as f:
                f.write(login_html_str)
            return {
              'module': self.__class__.__name__,
              'auth_result': 'ERROR',
              'display_name': '',
              'display_handle': ''
            }

adobe = Adobe()
