import argparse
import os
import sys
from colorama import Fore, Style

from modules.Adobe import adobe
from modules.Airbnb import airbnb
from modules.Etsy import etsy
from modules.Facebook import facebook
from modules.Foursquare import foursquare
from modules.Github import github
from modules.Instagram import instagram
from modules.Klout import klout
from modules.Linkedin import linkedin
from modules.Myspace import myspace
from modules.Netflix import netflix
from modules.Okcupid import okcupid
from modules.Pinterest import pinterest
from modules.Reddit import reddit
from modules.Square import square
from modules.Tumblr import tumblr
from modules.Twitter import twitter
from modules.Venmo import venmo
from modules.Yelp import yelp

"""
Usage Examples:

List available website modules:
$ python ModLogin.py -l

Check a single credential against a single website:
$ python ModLogin.py -u <email/username> -p <password> -s <website>

Check a single credential against a custom selection of websites using a custom useragent:
$ python ModLogin.py -u <email/username> -p <password> -s <website1,website2> -ua "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"

Check a single credential against all supported websites:
$ python ModLogin.py -u <email/username> -p <password>

Check colon-delimited credentials from a file against multiple websites:
$ python ModLogin.py -f /tmp/credentials.txt -s airbnb,etsy,reddit
"""

modules = [
  adobe, airbnb, etsy,
  facebook, foursquare, github,
  instagram, klout, linkedin,
  myspace, netflix, okcupid,
  pinterest, reddit,  square,
  tumblr, twitter, venmo,
  yelp
]

email_modules = [
  adobe, airbnb, etsy,
  foursquare, github, klout,
  linkedin, netflix, okcupid,
  pinterest, square, tumblr,
  twitter, yelp, venmo
]
username_modules = [
  etsy, github, instagram,
  okcupid, pinterest, reddit,
  twitter
]


def print_green(s):
    return Fore.GREEN + str(s) + Style.RESET_ALL


def print_yellow(s):
    return Fore.YELLOW + str(s) + Style.RESET_ALL


def print_red(s):
    return Fore.RED + str(s) + Style.RESET_ALL


def print_selected_modules(module_selection):
    print "\n" + "The following website modules were selected: "
    for module in module_selection:
        print '  - ' + str(module.__class__.__name__)


def print_available_modules():
    print "\nAvailable Modules:"
    for module in modules:
        print ("  - " + module.__class__.__name__)
    print "\nEmail-based Modules:"
    for module in email_modules:
        print ("  - " + module.__class__.__name__)
    print "\nUsername-based Modules:"
    for module in username_modules:
        print ("  - " + module.__class__.__name__)
    sys.exit()


def main():
    global modules
    parser = argparse.ArgumentParser(description='ModLogin: Check credentials \
    against multiple services')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List Supported Modules')
    parser.add_argument('-u', '--username',
                        help='Username/Email Address to be Checked')
    parser.add_argument('-p', '--password',
                        help='Password to be Checked')
    parser.add_argument('-f', '--file',
                        help='File containing colon delimited credentials')
    parser.add_argument('-ua', '--useragent',
                        help='Static user agent to be used in web requests')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--selection',
                       help='Comma separated list of modules to check against \
    - ex: yelp,facebook')
    group.add_argument('-uo', '--usernames-only',
                       help='Only check against username-based modules',
                       action='store_true')
    group.add_argument('-eo', '--emails-only',
                       help='Only check against email-based modules',
                       action='store_true')
    args = parser.parse_args()

    # List available modules
    if args.list:
        print_available_modules()
    # Allow pre-set module groups to be selected
    if args.emails_only:
        modules = email_modules
    if args.usernames_only:
        modules = username_modules
    # Allow a custom user-agent to be specified
    if args.useragent:
        useragent = str(args.useragent)
    else:
        useragent = None

    # Ensure supplied module(s) are supported
    # Generate new module list based on args.selection
    if args.selection:
        selection = str(args.selection).strip().split(',')
        available_modules = [
          module.__class__.__name__.lower() for module in modules
        ]
        for s in selection:
            if s not in available_modules:
                print "Specified module is unsupported: {}".format(s)
                print "Type -l to see supported modules"
                sys.exit()
        modules = [getattr(sys.modules[__name__], s) for s in selection]
        print_selected_modules(modules)

    # User either needs to supply a username/password combination or a file
    if (not args.username or not args.password) and not args.file:
        print "Please specify either a username and password or a file \
containing colon delimited credentials"
        sys.exit()

    if args.file:
        # Ensure file actually exists
        if not os.path.isfile(args.file):
            print "The specified file does not exist: " + str(args.file)
            sys.exit()
        # Count the number of lines in the file that contain a colon
        valid_lines = 0
        with open(args.file) as f:
            for i, l in enumerate(f):
                if ':' in l:
                    valid_lines = i + 1
                pass
            if valid_lines > 0:
                print "\n" + "Running in file mode"
                print str(valid_lines) + ' credentials found in file.'
            else:
                print "No valid colon-delimited credentials found in file"
                sys.exit(1)
        f.close()
        # Check each line to make sure it's well formed. If it is, check
        # the credential against the selected module(s)
        with open(args.file) as f:
            for line in f:
                username = ''
                password = ''
                # Ignore lines that are missing a colon
                if ':' not in line:
                    print "Skipping invalid line (missing delimiter): " + \
                          str(line)
                    continue
                try:
                    username, password = line.strip().split(':')
                except ValueError:
                    print "Skipping invalid line (too many delimiters): " + \
                          str(line)
                    continue
                if not username or not password:
                    print "Skipping invalid line (missing username or \
                    password): " + str(line)
                    continue
                attempt_login(username, password, modules, useragent)
    else:
        # If no file was supplied, run in single credential mode
        attempt_login(args.username, args.password, modules, useragent)


def attempt_login(username, password, module_selection, useragent=None):
    auth_results = []
    for module in module_selection:
        auth_result = module.login(username, password, useragent)
        auth_results.append(auth_result)
        print "\n" + "[*] " + str(module.__class__.__name__) + \
              " - " + username + " : " + password
        if auth_result['auth_result'] == 'SUCCESS':
            print(print_green('  [+] ') + 'Login Attempt: SUCCESS')
        elif auth_result['auth_result'] == 'CHALLENGE':
            print(print_yellow('  [/] ') + 'Login Attempt: CHALLENGE')
        else:
            print(print_red('  [-] ') + 'Login Attempt: FAILED')
        if auth_result['display_handle']:
            print(print_green('  [+] ') + 'Display Handle: ' +
                  auth_result['display_handle'])
        if auth_result['display_name']:
            print(print_green('  [+] ') + 'Display Name: ' +
                  auth_result['display_name'])

if __name__ == "__main__":
    main()
