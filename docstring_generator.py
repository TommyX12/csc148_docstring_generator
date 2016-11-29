"""
# CSC148 Docstring Generator
A docstring template generator that adds docstring template to classes
    and functions in your files without changing existing ones.

# How to use:
- Write all your code first before running this.
- Place this file inside the folder you want to process.
- Run this file (for example, right click in PyCharm and select 'Run').
    Your files are now processed and backup is made.
- Open your files, press "ctrl + F"(Windows) or "command + F"(Mac) to
    bring up the search bar. Write "[TODO]"(without the quotation marks)
    and press "Enter" once. Press "Esc", then hit "F3" to search for the next
    "[TODO]", write appropriate text then hit "F3" again and repeat until all
    "[TODO]"s are gone.
- Add attributes to class docstrings (if some were missing) and remove
    unnecessary ones (such as inherited attributes in super constructor).
    You may also add descriptions to each property / attribute by yourself.

# What will happen:
- All python files under the same folder as well as files in the sub-folders
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

# Change log:
- Able to insert descriptions and doctests into existing docstrings
- Doctests are now considered
- Provide an example of before and after. Covering document docstring,
    function, class (private + public), and unchanged existing docstrings.
- Minor style changes
- Default return type to None if no "return" statement is present in a function.
    An exception is when the function raises NotImplementedError, or pass.
- Adds description placeholder for every parameter and attribute except self.
- Initial release

# Road-map:
- Able to insert more missing elements into existing docstrings.
- Automatically detect the type of some variables


# License:
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


def match_start_docstring(line):
    line = line.lstrip()
    return line.startswith('\"\"\"') or line.startswith('\'\'\'')


def match_end_docstring(line):
    line = line.lstrip()
    return re.match(r'.*\"\"\"', line) or re.match(r'.*\'\'\'', line)


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
        if i >= len(lines):
            break

        line = lines[i]

        if not document_docstring_exists and not is_empty_line(line):
            if not match_start_docstring(line):
                print('- added document docstring')
                results.append('\"\"\"')
                results.append(todo_label)
                results.append('\"\"\"')
                results.append('')

            document_docstring_exists = True

        results.append(line)

        indentation = get_indentation(line)

        if re.match(r'\s*def\s', line) is not None:
            docstring_indentation = None

            has_return = False

            for j in range(i + 1, len(lines)):
                sub_line = lines[j]

                if is_empty_line(sub_line):
                    continue

                sub_indentation = get_indentation(sub_line)
                if len(sub_indentation) <= len(indentation):
                    break

                if docstring_indentation is None:
                    if match_start_docstring(sub_line):
                        for k in range(j + 1, len(lines)):
                            closing_line = lines[k]
                            if match_end_docstring(closing_line):
                                # augmentation_queue.append((j + 1, k + 1, true))
                                print(
                                    '- augmented function docstring: ' + line.lstrip())
                                results += augment_docstring(
                                    lines[j:k+1], True
                                )
                                for _ in range(k - i):
                                    lines.pop(i)

                                break

                        break

                    docstring_indentation = sub_indentation

                sub_line = sub_line.lstrip() + ' '

                if re.match(r'return\W', sub_line) \
                        is not None or \
                        re.match(r'raise\s+NotImplementedError', sub_line) \
                        is not None or \
                        re.match(r'pass\s', sub_line) \
                        is not None:
                    has_return = True
                    break

            if docstring_indentation is not None:
                print('- added function docstring: ' + line.lstrip())
                results += get_function_docstring(line, has_return,
                                                  docstring_indentation)

            continue

        if re.match(r'\s*class\s', line) is not None:

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
                    if match_start_docstring(ctor_line):
                        for k in range(j + 1, len(lines)):
                            closing_line = lines[k]
                            if match_end_docstring(closing_line):
                                # augmentation_queue.append((j + 1, k + 1, true))
                                print(
                                    '- augmented class docstring: ' + line.lstrip())
                                results += augment_docstring(
                                    lines[j:k+1], False
                                )
                                for _ in range(k - i):
                                    lines.pop(i)

                                break

                        break

                    docstring_indentation = ctor_indentation

                if re.match(r'\s*def\s+__init__', ctor_line) is not None:
                    for k in range(j + 1, len(lines)):
                        sub_line = lines[k]

                        if is_empty_line(sub_line):
                            continue

                        sub_indentation = get_indentation(sub_line)
                        if len(sub_indentation) <= len(ctor_indentation):
                            break

                        sub_line = sub_line.lstrip()

                        attr_match_obj = re.match(r'self\.\w+', sub_line)
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


def augment_docstring(existing_docstring, add_doctest):
    result = []

    indentation = get_indentation(existing_docstring[-1])

    has_doctest = False

    for i in range(len(existing_docstring)):
        line = existing_docstring[i]

        result.append(line)

        stripped_line = line.lstrip()

        if re.match(r'@\s*type.*:', stripped_line):
            description_exists = False
            if i+1 < len(existing_docstring):
                next_line = existing_docstring[i+1]
                if not is_empty_line(next_line) and \
                    len(get_indentation(next_line)) > len(indentation):
                    description_exists = True

            if not description_exists and 'self' not in stripped_line:
                result.append(indentation + '    ' + todo_label)

        if stripped_line.startswith('>>>'):
            has_doctest = True

    if add_doctest and not has_doctest:
        last_line = result.pop()
        result.append(indentation)
        result.append(indentation + '>>> ' + todo_label)
        result.append(indentation)
        result.append(last_line)

    return result


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

    docstring.append('\"\"\"' + todo_label)

    if attributes:
        docstring.append('')
        docstring.append('=== Attributes ===')
        for attr in attributes:
            docstring.append('@type ' + attr + ': ' + todo_label)
            docstring.append('    ' + todo_label)

    if p_attributes:
        docstring.append('')
        docstring.append('=== Private Attributes ===')
        for attr in p_attributes:
            docstring.append('@type ' + attr + ': ' + todo_label)
            docstring.append('    ' + todo_label)

    docstring.append('')
    docstring.append('=== Representation Invariants ===')
    docstring.append('- ' + todo_label)
    docstring.append('\"\"\"')

    for i in range(len(docstring)):
        docstring[i] = indentation + docstring[i]

    return docstring


def get_function_docstring(declaration, has_return, indentation):
    """
    Return the docstring template of a function, in a list of separated lines.

    Preconditions: None

    @type declaration: str
        The line containing "def" for the function. Used to extract parameters.
    @type has_return: bool
        If false, the rtype of that function docstring will be default to None.
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

    docstring.append('\"\"\"' + todo_label)
    docstring.append('')
    docstring.append('Preconditions: ' + todo_label)
    docstring.append('')
    for param in params:
        if len(param) > 0:
            docstring.append('@type ' + param + ': ' + todo_label)
            if param != 'self':
                docstring.append('    ' + todo_label)
    if has_return:
        docstring.append('@rtype: ' + todo_label)
    else:
        docstring.append('@rtype: None')

    docstring.append('')
    docstring.append('>>> ' + todo_label)
    docstring.append('')
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
