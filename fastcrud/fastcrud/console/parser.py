import argparse
from os import path, mkdir

from pathlib  import Path

from fastcrud.fastcrud.console.settings.settings import MODEL_PATH

class Parser:

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser):
        parser.add_argument('--m' , type=str, help='Create a Model instance')
        parser.add_argument('--V' , type=str, help='Create a View instance')
        parser.add_argument('--g' , type=str, help='Create a Generator to create everything')

    @staticmethod
    def parser(parser: argparse.ArgumentParser):
        """
        Parser is responsible
        """
        args = parser.parse_args()
        
        return args

    @staticmethod
    def build_dir_and_models(model):
        """
        
        """
        if model != '':
            if path.exists(f'/model/{model}'):
                print('The Model directory already exists')
            else:
                try:
                    mkdir(path.dirname('model/'))
                    with open(f'model/{model}.py', 'w') as StreamWriter:
                        # TODO: Update with Model Factory
                        StreamWriter.write(f'class {model}: pass')
                except OSError as os:
                    print(f'Failed To Create: { os }')

    def instantiate_model_properties(self, model = None):
        pass

    def build_views(self, model=None, controller=None):
        pass