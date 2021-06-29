"""This module autodocuments a module by using ast and generating a sort of
markdown file of all the class and function stubs in a file. It prints to screen
only, so just redirect output.

Adapted from: https://stackoverflow.com/a/44699395/9691276
"""
import ast
import sys
import re

def show_info(functionNode, indent=False):
    stub = '##'
    if indent:
        stub += '#'
    name = functionNode.name
    stub += f' def `{name}('
    args = [arg.arg for arg in functionNode.args.args]
    stub += ', '.join(args)
    stub += ')`:'
    print(stub)
    print(ast.get_docstring(functionNode))
    if not indent:
        print('***')
    print('\n')

def gendoc(f):
    with open(f) as file:
        node = ast.parse(file.read())

    print(f'# `{f}`')
    print(ast.get_docstring(node))
    print('\n')

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]

    for function in functions:
        show_info(function)

    for class_ in classes:
        stub = '## class '
        stub += '`' + class_.name
        bases = [n.id for n in class_.bases]
        if bases:
            stub += '(' + ', '.join(bases) + ')'
        stub += '`:'
        print(stub)
        print(ast.get_docstring(class_))
        print('\n')
        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        for method in methods:
            show_info(method, True)
        print('***')

def main(files):
    for file in files:
        gendoc(file)

if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    main(args)
