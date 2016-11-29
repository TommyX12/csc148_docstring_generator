# CSC148 Docstring Generator
A docstring template generator that adds docstring template to classes
    and functions in your files and insert missing elements into existing ones.

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
    - function: A type contract will be added for every parameter. Doctest
        will be added.
    - class: The generator will scan the constructor (if exists) for any
        self.xxxx or self._xxxx properties.
        Warning: This feature will NOT consider inheritance.
- Newly added docstring will have "[TODO]" as placeholder for the user to
    enter data, such as representation invariants.
- If a docstring already exists, descriptions and doctests will be inserted.
- The original version will be renamed to "[old file name].bak" under the
    same folder. Check the new versions before running the generator again,
    or else the old backup will be overwritten.

# Example:
Before:
```python
def my_function(param1, param2):
    return param1 + param2

class my_class:
    def __init__(self, param1):
        self.attr1 = param1
        self.attr2 = 0
        self._pattr1 = 0
        self._pattr2 = 0

    def my_method(self, param1, param2):
        print(param1, param2)

    def my_method2(self, param1, param2):
        """
        for existing docstrings, parameter descriptions and doctests will be
        inserted.

        @type self: my_class
        @type param1: int
        @type param2: int
            existing descriptions will not be modified.
        """
        return 0
```
After:
```python
"""
[TODO]
"""

def my_function(param1, param2):
    """[TODO]
    
    Preconditions: [TODO]
    
    @type param1: [TODO]
        [TODO]
    @type param2: [TODO]
        [TODO]
    @rtype: [TODO]
    
    >>> [TODO]
    
    """
    return param1 + param2

class my_class:
    """[TODO]
    
    === Attributes ===
    @type attr2: [TODO]
        [TODO]
    @type attr1: [TODO]
        [TODO]
    
    === Private Attributes ===
    @type _pattr1: [TODO]
        [TODO]
    @type _pattr2: [TODO]
        [TODO]
    
    === Representation Invariants ===
    - [TODO]
    """
    def __init__(self, param1):
        """[TODO]
        
        Preconditions: [TODO]
        
        @type self: [TODO]
        @type param1: [TODO]
            [TODO]
        @rtype: None
        
        >>> [TODO]
        
        """
        self.attr1 = param1
        self.attr2 = 0
        self._pattr1 = 0
        self._pattr2 = 0

    def my_method(self, param1, param2):
        """[TODO]
        
        Preconditions: [TODO]
        
        @type self: [TODO]
        @type param1: [TODO]
            [TODO]
        @type param2: [TODO]
            [TODO]
        @rtype: None
        
        >>> [TODO]
        
        """
        print(param1, param2)

    def my_method2(self, param1, param2):
        """
        for existing docstrings, parameter descriptions and doctests will be
        inserted.

        @type self: my_class
        @type param1: int
            [TODO]
        @type param2: int
            existing descriptions will not be modified.
        
        >>> [TODO]
        
        """
        return 0
```

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
