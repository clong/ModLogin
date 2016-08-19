ModLogin
========

ModLogin is a python-based tool that is capable of checking the validity of a given set of credentials against a number of well-known websites. ModLogin modules use the Requests and Mechanize libraries to perform login requests.

![Screenshot (display names redacted)](/img/screenshot.png?raw=true "(display names redacted)")

History
-------
After some of the larger password dumps were released in 2016, I began to take interest in how well (or poorly) websites' automated systems were detecting and responding to anomalous login events. It was an interesting exercise to examine at how different design their login authentication systems and what types of restrictions and countermeasures they have put in place.

Please do not use this tool for malicious purposes or to gain access to accounts that do not belong to you. This tool was not designed to check large numbers of credentials or brute force passwords.

Setup
------
I recommend setting up a virtual environment to install the required dependencies, but it's not required.
```
$ git clone https://github.com/Centurion89/ModLogin.git
$ cd ModLogin/
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Features
--------
* Customize a list of websites to test logins against or choose a pre-created list of email or username-based websites
* Specify a single credential or provide a file containing multiple credentials to check
* Certain modules parse out additional information once logged in such the real name or username for the account
* Captcha/Login challenge detection
* Automated debugging output

Usage
-----
List available website modules:
```
python ModLogin.py -l
```

Check a single credential against a single website:
```
python ModLogin.py -u <email/username> -p <password> -s <website>
```
Check a single credential against a custom selection of websites using a custom useragent:
```
python ModLogin.py -u <email/username> -p <password> -s <website1,website2> -ua "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
```

Check a single credential against all supported websites:
```
python ModLogin.py -u <email/username> -p <password>
```

Check colon-delimited credentials from a file against multiple websites:
```
python ModLogin.py -f /tmp/credentials.txt -s airbnb,etsy,reddit
```

Login Terminology
-----------------
```
SUCCESS = The login using the provided credential was successful.
FAILED = The login using the provided credential was unsuccessful.
CHALLENGE = The website is requiring some form of additional validation (captcha, two-factor, etc).
ERROR = The website responded with something that ModLogin wasn't designed to handle and ModLogin isn't sure which login status is appropriate.
```

Limitations
------------
ModLogin depends on certain webpage elements that may change over time. These changes may cause modules to stop functioning properly. Additionally, many popular websites have implemented Javascript-based login fields or protections which makes building automated login modules for them difficult and/or time consuming. I will actively review pull requests for fixes and additional modules.

TODO
----
Implement asynchronous HTTPS requests using the grequests library. See TODO.txt for websites that do not yet have modules built for them. Please feel free to contribute your own modules.

Credits
-------
This project drew some inspiration and a fair bit of code from [Shard](https://github.com/philwantsfish/shard)
