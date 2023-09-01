import argparse
from pathlib  import Path

class Parser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.target_path = '' # Add settings for file path

    # This will in the future also take care of adding migration files, updating schemas etc...
    def add_arguments(self, param: str):
        if param == '--m':
            self.parser.add_argument('--m' ,dest=param, type=str, help='Create a Model instance')
        elif param == '--c':
            self.parser.add_argument('--c' ,dest=param, type=str, help='Create a Controller instance')
        elif param == '--g':
            self.parser.add_argument('--g' ,dest=param, type=str, help='Create a Generator to create everything')


    def parser(self):
        args = self.parser.parse_args()
        return args

    def build_dir_and_models(self, model='', controller='', generator=''):
        if model != '':
            if Path.exists(self.target_path):
                print('The Model directory already exists')
            else:
                pass
                # TODO: Create the file path
                # TODO: Factory pattern. Create the model instance
                