import argparse

class AoCBase():
    def __init__(self):
        with open('input.txt', 'rt') as f:
            source_data_raw = f.readlines()
        self.source_data = [ x.strip() for x in source_data_raw ]
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-d', help="Debug output", action="store_true")
        self.parser.add_argument('-p', help="Progress output", action="store_true")

    def parse_args(self):
        self.arguments = self.parser.parse_args()

    def debug(self, *kargs):
        if self.arguments.d:
            print(*kargs)

    def progress(self, *kargs, update=False):
        if self.arguments.p:
            if update:
                print('\r', *kargs, end='', sep='', flush=True)
            else:
                print(*kargs)
