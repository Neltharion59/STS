import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)
from util.file_handling import read, write
from json import loads, dumps

search_register_path = os.path.join(root_path, 'resources/searches/search_register_{}.json')


class SearchRegister:
    def __init__(self, name):
        try:
            self.name = name
            self.file_path = search_register_path.format(name)
            self.register = loads(read(self.file_path))
        except FileNotFoundError:
            self.register = {}

    def contains(self, query):
        return query in self.register

    def add(self, query, count):
        if query in self.register:
            return False
        else:
            self.register[query] = {'count': count}
            return True

    def remove(self, query):
        del self.register[query]

    def persist(self):
        write(self.file_path, dumps(self.register))
