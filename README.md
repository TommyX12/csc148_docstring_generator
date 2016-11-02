
# csc148_docstring_generator
A docstring template generator

# How to use:
- Write all your code first before running this.
- Place this file inside the folder you want to process.
- Run this file (for example, right click in PyCharm and select 'Run')
- Go to your files, press "ctrl + F"(Windows) or "command + F"(Mac) to
    bring up the search bar. Write "[TODO]"(without the quotation marks)
    and press "Enter" once. Press "Esc", then hit "F3" to search for the next
    "[TODO]", write appropriate text then hit "F3" again and repeat until all
    "[TODO]"s are gone.
- You may also add descriptions to each property / attribute by yourself.

# What will happen:
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


# Road-map:
- Default return type to None if no "return" statement is present in a function.


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
