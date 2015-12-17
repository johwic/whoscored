import re


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def parse_json(raw):
        data = re.sub(r',,', r',null,', raw)
        data = re.sub(r',,', r',null,', data)
        data = re.sub(r'"', r'\"', data)
        data = re.sub(r"\\'", r"'", data)
        data = re.sub(r',]', r',null]', data)
        data = re.sub(r"'(.*?)'(\s*[,\]])", r'"\1"\2', data)

        return data
