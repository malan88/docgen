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
        return result
    return ''


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


def parse_func(func, indents=2):
    """Prints a function stub and it's docstring.

    # args
    - func_node -: the function to be printed
    - indent -int: the number of # to indent by

    @TODO: test todos
    """
    stub = '#' * indents + func_stub(func)
    rawdoc = format_docstring(ast.get_docstring(func)).splitlines()
    todos = []
    doc = []
    for line in rawdoc:
        if '@todo' in line.lower():
            todos.append((func.lineno, line))
        else:
            doc.append(line)
    doc = stub + '\n' + '\n'.join(doc)
    docdict = {'doc': doc, 'todos': todos}
    return docdict


def parse_class(cls):
    """Parses a class definition and all methods"""
    title = class_stub(cls)
    rawdoc = format_docstring(ast.get_docstring(cls)).splitlines()
    todos = []
    clsdoc = []
    for line in rawdoc:
        if '@todo' in line.lower():
            todos.append((cls.lineno, line))
        else:
            clsdoc.append(line)
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
    methoddocs = []
    for method in methods:
        methoddoc = parse_func(method)
        if '@prop' in methoddoc['doc'].lower():
            clsdoc.append(methoddoc['doc'].replace('@prop', '').strip())
        else:
            methoddocs.append(methoddoc['doc'])
        todos.extend(methoddoc['todos'])
    doc = '\n'.join([title, '\n'.join(clsdoc), '\n'.join(methoddocs)])
    return {'doc': doc, 'todos': todos}


def gendoc(f):
    """Generates the docs from a file.

    # args
    - f -str: a filename
    """
    f = f.strip('./')
    with open(f) as file:
        node = ast.parse(file.read())
    fstub = f'# `{f}`'
    rawdoc = format_docstring(ast.get_docstring(node)).splitlines()

    todos = []
    fdoc = []
    for line in rawdoc:
        if '@todo' in line.lower():
            todos.append((f, 0, line))
        else:
            fdoc.append(line)

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    rawtodos = []

    funcdocs = []
    for function in functions:
        funcdoc = parse_func(function)
        funcdocs.append(funcdoc['doc'])
        rawtodos.extend(funcdoc['todos'])

    classdocs = []
    for cls in classes:
        classdoc = parse_class(cls)
        classdocs.append(classdoc['doc'])
        rawtodos.extend(classdoc['todos'])

    rawtodos = [(f, *todo) for todo in rawtodos]
    todos.extend(rawtodos)
    finaltodos = []
    for todo in todos:
        finaltodos.append('- [ ] ' + str(todo))

    fulldocs = '\n\n'.join([fstub, *fdoc, *finaltodos, *funcdocs, *classdocs])
    return fulldocs


def main(files):
    """Main entrypoint for the file,

    # args
    - files -list[str]: a list of file names to parse
    """
    docs = {}
    for f in files:
        docs[f] = gendoc(f)
    for k, v in docs.items():
        print(v)


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    main(args)
