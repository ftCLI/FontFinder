# FontFinder
## Description
``FontFinder`` is a helper class that finds fonts in a given path. It can search for fonts in a directory and its
subdirectories, and can also handle a single font file.

The class allows for filtering based on various criteria such as outline format (TrueType or PostScript), font
variations (static or variable), and font flavor ('woff', 'woff2' or ``None``).

The class returns a list or a generator of [FontTools](https://github.com/fonttools/fonttools) TTFont objects, or of
TTFont subclass objects, that meet the specified criteria.

## Attributes
The ``FontFinder`` class has the following attributes:
  * ``input_path``: the path to the directory or file
  * ``recursive``: if ``True`` and ``input_path`` is a directory, search for fonts in the directory and its subdirectories
  * ``return_cls``: the class to use for returned objects can be specified by passing a subclass of ``TTFont`` to the
  ``return_cls`` argument. If ``return_cls`` is ``None``, ``TTFont`` is used
  * ``recalc_timestamp``: if ``True``, recalculate the font's ``modified`` timestamp on save
  * ``recalc_bboxes``: if ``True``, recalculate the font's bounding boxes on save
  * ``filter_out_sfnt``: if ``True``, filter out SFNT fonts
  * ``filter_out_woff``: if ``True``, filter out WOFF fonts
  * ``filter_out_woff2``: if ``True``, filter out WOFF2 fonts
  * ``filter_out_tt``: if ``True``, filter fonts with TrueType outlines
  * ``filter_out_ps``: if ``True``, filter fonts with PostScript outlines
  * ``filter_out_static``: if ``True``, filter out static fonts
  * ``filter_out_variable``: if ``True``, filter out variable fonts

## Usage examples
### List or Generator
Depending on the method used, ``FontFinder`` returns a list or a generator of
[FontTools](https://github.com/fonttools/fonttools) TTFont objects (or of TTFont subclasses objects).

The `find_fonts()` method returns a list of TTFont objects, while the `generate_fonts()` method returns a generator of
TTFont objects.

To get a list of TTFont objects, use the `find_fonts()` method:

```python
from font_finder import FontFinder

# return a list of all fonts in a directory
finder = FontFinder("/path/to/directory")
fonts = finder.find_fonts()
```

To get a generator of TTFont objects, use the `generate_fonts()` method:

```python
from font_finder import FontFinder

# return a generator of all fonts in a directory
finder = FontFinder("/path/to/directory")
fonts = finder.generate_fonts()
```

### File or directory
``FontFinder`` can handle a single font file or a directory. If a directory is passed, ``FontFinder`` can search for
fonts in the directory and its subdirectories. If a file is passed, ``FontFinder`` will return a list or a generator
with a single TTFont object.

#### Single file

```python
from font_finder import FontFinder

# return a list with a single font
finder = FontFinder("/path/to/file.ttf")
fonts = finder.find_fonts()
```

#### Directory

```python
from font_finder import FontFinder

# return a list of all fonts in a directory
finder = FontFinder("/path/to/directory")
fonts = finder.find_fonts()
```

### Recursive search

```python
from font_finder import FontFinder

# return a list of all fonts in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
fonts = finder.find_fonts()
```

### Return class
By default, ``FontFinder`` returns a list or a generator of [FontTools](https://github.com/fonttools/fonttools) TTFont
objects. The class to use for returned objects can be specified by passing a subclass of ``TTFont`` to the
``return_cls`` argument. If ``return_cls`` is ``None``, ``TTFont`` objects are returned.

### Using filters
#### Find all fonts with PostScript outlines in a directory and its subdirectories

```python
from font_finder import FontFinder

# find all fonts with PostScript outlines in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
finder.filter_out_tt = True  # filter fonts with TrueType outlines
fonts = finder.find_fonts()
```

#### Find all fonts with TrueType outlines in a directory and its subdirectories
```python
from font_finder import FontFinder

# find all web fonts in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
finder.filter_out_sfnt = True  # filter out SFNT fonts
fonts = finder.find_fonts()
```

#### Find all static fonts in a directory and its subdirectories
```python
from font_finder import FontFinder

# find all static fonts in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
finder.filter_out_variable = True  # filter out variable fonts
fonts = finder.find_fonts()
```

#### Find all variable fonts in a directory and its subdirectories
```python
from font_finder import FontFinder

# find all variable fonts in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
finder.filter_out_static = True  # filter out static fonts
fonts = finder.find_fonts()
```

#### Find all web fonts in a directory and its subdirectories
```python
from font_finder import FontFinder

# find all WOFF and WOFF2 fonts in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
finder.filter_out_sfnt = True  # filter out SFNT fonts
fonts = finder.find_fonts()
```

#### Find all WOFF fonts in a directory and its subdirectories
```python
from font_finder import FontFinder

# find all WOFF fonts in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
finder.filter_out_sfnt = True  # filter out SFNT fonts
finder.filter_out_woff2 = True  # filter out WOFF2 fonts
fonts = finder.find_fonts()
```

#### Find all WOFF2 fonts with TrueType outlines in a directory and its subdirectories
```python
from font_finder import FontFinder

# find all WOFF fonts with TrueType outlines in a directory and its subdirectories
finder = FontFinder("/path/to/directory", recursive=True)
finder.filter_out_sfnt = True  # filter out SFNT fonts
finder.filter_out_woff2 = True  # filter out WOFF2 fonts
finder.filter_out_ps = True  # filter out fonts with PostScript outlines
fonts = finder.find_fonts()
```
