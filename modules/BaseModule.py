from abc import ABCMeta, abstractmethod


class BaseModule:
    __metaclass__ = ABCMeta

    def define_user_agent(self, useragent=None):
        if useragent is not None:
            return str(useragent)
        else:
            return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

    def login(self, username, password, useragent):
        return False
