"""

A docstring template generator.

How to use:
- Write all your code first before running this.
- Place this file inside the folder you want to process.
- Run this file (for example, right click in PyCharm and select 'Run')
- Go to your files, press "ctrl + F"(Windows) or "command + F"(Mac) to
    bring up the search bar. Write "[TODO]"(without the quotation marks)
    and press "Enter" once. Press "Esc", then hit "F3" to search for the next
    "[TODO]", write appropriate text then hit "F3" again and repeat until all
    "[TODO]"s are gone.
- You may also add descriptions to each property / attribute by yourself.

What will happen:
- All files under the same folder as well as files in the sub-folders
    will be processed.
- In each file, a docstring will be added for every function and class, as
    well as one for the entire document.
    - function: A type contract will be added for every parameter.
    - class: The generator will scan the constructor (if exists) for any
        self.xxxx or self._xxxx properties.
        Warning: This feature will NOT consider inheritance.
- Newly added docstring will have "[TODO]" as placeholder for the user to
    enter data, such as representation invariants.
- If a docstring already exists, nothing will be added.
- The original version will be renamed to "[old file name].bak" under the
    same folder. Check the new versions before running the generator again,
    or else the old backup will be overwritten.


Road-map:
- Default return type to None if no "return" statement is present in a function.


Copyright (c) 2016 TommyX

Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 of the Software, and to permit persons to whom the Software is furnished to do
 so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import os
import sys
import io
import re

todo_label = '[TODO]'


def get_indentation(line):
    """
    Returns the leading spaces and/or tabs of a line of text.

    Preconditions: None

    @type line: str
    @rtype: str
    """
    ptr = 0
    while ptr < len(line):
        if line[ptr] != ' ' and line[ptr] != '\t':
            break
        ptr += 1
    return line[0:ptr]


def is_empty_line(line):
    """
    Return true iff line contains only whitespaces or is empty.

    Preconditions: None

    @type line: str
    @rtype: bool
    """
    return len(line.lstrip()) == 0


def process_file(txt):
    """
    Return the new version of <txt> with docstrings added.

    Preconditions: <txt> is a valid python file.

    @type txt: str
        The text of the python file to process.
    @rtype: str
    """
    results = []

    lines = txt.split('\n')

    document_docstring_exists = False

    for i in range(len(lines)):
        line = lines[i]

        if not document_docstring_exists and not is_empty_line(line):
            if not line.startswith('\"\"\"'):
                print('- added document docstring')
                results.append('\"\"\"')
                results.append(todo_label)
                results.append('\"\"\"')
                results.append('')

            document_docstring_exists = True

        results.append(line)

        indentation = get_indentation(line)

        function_match_obj = re.match(r'\s*def\s', line)
        if function_match_obj is not None:
            docstring_indentation = None
            for j in range(i + 1, len(lines)):
                sub_line = lines[j]

                if is_empty_line(sub_line):
                    continue

                sub_indentation = get_indentation(sub_line)
                if len(sub_indentation) <= len(indentation):
                    break

                if sub_line.lstrip().startswith('\"\"\"'):
                    break

                docstring_indentation = sub_indentation

            if docstring_indentation is not None:
                print('- added function docstring: ' + line.lstrip())
                results += get_function_docstring(line,
                                                  docstring_indentation)

            continue

        class_match_obj = re.match(r'\s*class\s', line)
        if class_match_obj is not None:

            attributes = {}
            p_attributes = {}

            docstring_indentation = None

            for j in range(i + 1, len(lines)):
                ctor_line = lines[j]

                if is_empty_line(ctor_line):
                    continue

                ctor_indentation = get_indentation(ctor_line)
                if len(ctor_indentation) <= len(indentation):
                    break

                if docstring_indentation is None:
                    if ctor_line.lstrip().startswith('\"\"\"'):
                        break

                    docstring_indentation = ctor_indentation

                ctor_match_obj = re.match(r'\s*def\s+__init__', ctor_line)
                if ctor_match_obj is not None:
                    for k in range(j + 1, len(lines)):
                        sub_line = lines[k]

                        if is_empty_line(sub_line):
                            continue

                        sub_indentation = get_indentation(sub_line)
                        if len(sub_indentation) <= len(ctor_indentation):
                            break

                        sub_line = sub_line.lstrip()

                        attr_match_obj = re.match(r'self\.[a-zA-Z0-9_]+',
                                                  sub_line)
                        if attr_match_obj is not None:
                            attr_match_span = attr_match_obj.span()
                            attr_name = sub_line[5:attr_match_span[1]]
                            if attr_name.startswith('_'):
                                p_attributes[attr_name] = True
                            else:
                                attributes[attr_name] = True

                    break

            if docstring_indentation is not None:
                print('- added class docstring: ' + line.lstrip())
                results += get_class_docstring(attributes, p_attributes,
                                               docstring_indentation)

            continue

    return '\n'.join(results)


def get_class_docstring(attributes, p_attributes, indentation):
    """
    Return the docstring template of a class, in a list of separated lines.

    Preconditions: None

    @type attributes: dict[str, bool]
        The keys of this dictionary are the attributes of the class.
        The values of this dictionary will always be True.
    @type p_attributes: dict[str, bool]
        Similar to the <attributes> parameter, for private attributes.
    @type indentation: str
        The leading whitespace to add to each line, so that the docstring
        is aligned properly.
    @rtype: list[str]
    """
    docstring = []

    docstring.append('\"\"\"')
    docstring.append(todo_label)

    if attributes:
        docstring.append('')
        docstring.append('=== Attributes ===')
        for attr in attributes:
            docstring.append('@type ' + attr + ': ' + todo_label)

    if p_attributes:
        docstring.append('')
        docstring.append('=== Private Attributes ===')
        for attr in p_attributes:
            docstring.append('@type ' + attr + ': ' + todo_label)

    docstring.append('')
    docstring.append('=== Representation Invariants ===')
    docstring.append(todo_label)
    docstring.append('\"\"\"')

    for i in range(len(docstring)):
        docstring[i] = indentation + docstring[i]

    return docstring


def get_function_docstring(declaration, indentation):
    """
    Return the docstring template of a function, in a list of separated lines.

    Preconditions: None

    @type declaration: str
        The line containing "def" for the function. Used to extract parameters.
    @type indentation: str
        The leading whitespace to add to each line, so that the docstring
        is aligned properly.
    @rtype: list[str]
    """
    declaration = declaration.lstrip()

    left = declaration.find('(')
    right = declaration.find(')')

    if left == -1 or right == -1:
        return []

    params = declaration[(left + 1): right].split(',')

    for i in range(len(params)):
        params[i] = params[i].strip()

    docstring = []

    docstring.append('\"\"\"')
    docstring.append(todo_label)
    docstring.append('')
    docstring.append('Preconditions: ' + todo_label)
    docstring.append('')
    for param in params:
        if len(param) > 0:
            docstring.append('@type ' + param + ': ' + todo_label)
    docstring.append('@rtype: ' + todo_label)
    docstring.append('\"\"\"')

    for i in range(len(docstring)):
        docstring[i] = indentation + docstring[i]

    return docstring


if __name__ == '__main__':

    generator_name = os.path.basename(sys.argv[0])
    working_directory = os.getcwd()

    for root, subdirs, files in os.walk(working_directory):
        for file in files:
            if not file.endswith('.py'):
                continue

            if file == generator_name:
                continue

            file_name = root + '\\' + file
            file_bak_extension = '.bak'

            print("processing: " + file_name[len(working_directory)+1:])

            in_file = io.open(file_name, 'r', encoding='utf8')
            in_text = in_file.read()
            in_file.close()

            out_file = io.open(file_name + file_bak_extension, 'w',
                               encoding='utf8')
            out_file.write(in_text)
            out_file.close()

            out_text = process_file(in_text)

            out_file = io.open(root + '\\' + file, 'w', encoding='utf8')
            out_file.write(out_text)
            out_file.close()

            print("done.")
