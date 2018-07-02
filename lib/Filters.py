import re


class Filters(object):

    config = {}

    def __init__(self, obj):
        self.config = obj


    def is_select_tld(self, domain):
        for tld in self.config['tlds']:
            pattern = '(?:[a-zA-Z0-9-]+\.)%s' % tld
            match = re.match(pattern, domain)
            if match is not None:
                return True
        return False

    def is_proper_length(self, domain, include_tld=False):
        if include_tld is True:
            if len(domain) <= self.config['maxDomainLength']:
                return True
            else:
                return False
        else:
            name = domain.split('.')[0]
            if len(name) <= self.config['maxDomainLength']:
                return True
            else:
                return False

    def number_of_characters(self, domain, include_tld=False):
        if include_tld is True:
            return len(domain)
        else:
            name = domain.split('.')[0]
            return len(name)

    def contains_keyword(self, domain):
        tld = domain.split('.')[1]
        for keyword in self.config['keywords']:
            pattern = '(?:[a-zA-Z0-9-]+)?%s(?:[a-zA-Z0-9-]+)?(?:\.%s)$' % (keyword, tld)
            match = re.match(pattern, domain)
            if match is not None:
                return True
        return False
