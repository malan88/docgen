"""This module autodocuments a module by using ast and generating a sort of
markdown file of all the class and function stubs in a file. It prints to screen
only, so just redirect output.

Adapted from: https://stackoverflow.com/a/44699395/9691276

```
Format
------
# ./dir/filename
docstring

## function(args)
docstring

## class(base)
docstring
### class function
docstring
```

NOTE: Any leading # in a docstring gets turned to a quadruple ####
"""
import ast
import sys
import re


def format_docstring(docstring):
    """Formats a docstring. Any leading # will be converted to #### for
    formatting consistency.

    # args
    - docstring -str: the dosctring to be formatted.
    """
    if isinstance(docstring, str):
        result = re.sub(r'^#+ ?', '#### ', docstring, flags=re.MULTILINE)
        print("RESULT", result, file=sys.stderr)
        return result
    return None


def class_stub(class_node):
    """Generates a class stub.

    # args
    - class_node -ClassDef: the class node from which to generate the stub.
    """
    stub = '`class ' + class_node.name
    bases = [getattr(n, 'id', 'unnamed') for n in class_node.bases]
    if bases:
        stub += '(' + ', '.join(bases) + ')'
    stub += '`:'
    return stub


def func_stub(func_node):
    """Generates a function stub.

    # args
    - func_node -FuncDef: the function from which to generate the stub
    """
    name = func_node.name
    stub = f'def `{name}('
    args = [arg.arg for arg in func_node.args.args]
    stub += ', '.join(args)
    stub += ')`:'
    return stub


def parse_func(func, indents=1):
    """Prints a function stub and it's docstring.

    # args
    - func_node -: the function to be printed
    - indent -int: the number of # to indent by
    """
    stub = '#' * indents + func_stub(func)
    doc = format_docstring(ast.get_docstring(func))
    docdict = {'doc': stub + '\n' + doc}
    return docdict


def parse_class(cls):
    fulldoc = []
    fulldoc.append(class_stub(cls))
    fulldoc.append(format_docstring(ast.get_docstring(cls)))
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
    for method in methods:
        methdoc = parse_func(method)
        fulldoc.append(parse_func(method))


def gendoc(f):
    """Generates the docs from a file.

    # args
    - f -str: a filename
    """
    with open(f) as file:
        node = ast.parse(file.read())
    fstub = f'# `{f}`'
    fdoc = format_docstring(ast.get_docstring(node))

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]

    funcdocs = []
    for function in functions:
        funcdoc = parse_function(function)
        funcdocs.append(funcdoc['doc'])

    classdocs = []
    for _class in classes:
        classdoc = parse_class(_class)
        classdocs.append(classdoc['doc'])


def main(files):
    """Main entrypoint for the file,

    # args
    - files -list[str]: a list of file names to parse
    """
    docs = {}
    for f in files:
        docs[f] = gendoc(f)
    for k,v in docs.items():
        print(v)


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    main(args)
