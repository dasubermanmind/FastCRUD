from fastcrud.fastcrud.console.parser import Parser
import argparse

if __name__ == '__main__':
    print('Testing FastCRUD')
    parser = argparse.ArgumentParser()
    
    Parser.add_arguments(parser)
    __args = Parser.parser(parser)
    print(f'Args-->{type(__args)}')
    
    Parser.build_dir_and_models(__args.m)

