from pathlib import Path
from typing import List, Generator
import unittest

from fontTools.ttLib.ttFont import TTFont

from font_finder import FontFinder, FontFinderError

CWD = Path.cwd()
TEST_DATA_DIR = Path.joinpath(CWD, "test_data")
EMPTY_DIR = TEST_DATA_DIR.joinpath("EMPTY_SUBDIR")
ALL_FILES = 14
ALL_FONTS = 13
ALL_TT_SFNT_FONTS = 2
ALL_PS_SFNT_FONTS = 3
ALL_SFNT_FONTS = 5
ALL_STATIC_SFNT_FONTS = 3
ALL_VARIABLE_SFNT_FONTS = 2
ALL_WOFF_FONTS = 4
ALL_WOFF2_FONTS = 4
ALL_WEB_FONTS = 8
ALL_STATIC_FONTS = 7
ALL_VARIABLE_FONTS = 6
FVAR_TABLE = "fvar"


class TTFontSubclass(TTFont):
    def get_file_name(self):
        return Path(self.reader.file.name).name


class TestFontFinder(unittest.TestCase):
    #  Find all fonts in a given directory and its subdirectories returning a list
    def test_find_all_fonts(self):
        expected = ALL_FONTS
        finder = FontFinder(TEST_DATA_DIR, recursive=True)
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsInstance(fonts, List)

    #  Find all fonts in a given directory and its subdirectories returning a generator
    def test_generate_all_fonts(self):
        expected = ALL_FONTS
        finder = FontFinder(TEST_DATA_DIR, recursive=True)
        fonts = finder.generate_fonts()
        self.assertIsInstance(fonts, Generator)
        self.assertEqual(len(list(fonts)), expected)

    #  Find all variable fonts in a given directory and in its subdirectories
    def test_find_all_variable_fonts(self):
        expected = ALL_VARIABLE_FONTS
        finder = FontFinder(TEST_DATA_DIR, recursive=True, filter_out_static=True)
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsNotNone(fonts[0].get(FVAR_TABLE))

    #  Find all static fonts in a given directory and in its subdirectories
    def test_find_all_static_fonts(self):
        expected = ALL_STATIC_FONTS
        finder = FontFinder(TEST_DATA_DIR, recursive=True, filter_out_variable=True)
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsNone(fonts[0].get(FVAR_TABLE))

    #  Find all SFNT fonts in a given directory and its subdirectories
    def test_find_all_sfnt_fonts(self):
        expected = ALL_SFNT_FONTS
        finder = FontFinder(TEST_DATA_DIR, recursive=True, filter_out_woff=True, filter_out_woff2=True)
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsNone(fonts[0].flavor)

    #  Find all SFNT fonts with TrueType outlines in a given directory and in its subdirectory
    def test_find_all_tt_sfnt_fonts(self):
        expected = ALL_TT_SFNT_FONTS
        finder = FontFinder(
            TEST_DATA_DIR, recursive=True, filter_out_woff=True, filter_out_woff2=True, filter_out_ps=True
        )
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsNone(fonts[0].flavor)
        self.assertEqual(fonts[0].sfntVersion, "\x00\x01\x00\x00")

    #  Find all SFNT fonts with PostScript outlines in a given directory and in its subdirectory
    def test_find_all_ps_sfnt_fonts(self):
        expected = ALL_PS_SFNT_FONTS
        finder = FontFinder(
            TEST_DATA_DIR, recursive=True, filter_out_woff=True, filter_out_woff2=True, filter_out_tt=True
        )
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsNone(fonts[0].flavor)
        self.assertEqual(fonts[0].sfntVersion, "OTTO")

    #  Find all static SFNT fonts
    def test_find_all_static_sfnt_fonts(self):
        expected = ALL_STATIC_SFNT_FONTS
        finder = FontFinder(
            TEST_DATA_DIR, recursive=True, filter_out_woff=True, filter_out_woff2=True, filter_out_variable=True
        )
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsNone(fonts[0].flavor)
        self.assertIsNone(fonts[0].get(FVAR_TABLE))

    #  Find all web fonts in a given directory and in its subdirectories
    def test_find_all_web_fonts(self):
        expected = ALL_WEB_FONTS
        finder = FontFinder(TEST_DATA_DIR, recursive=False, filter_out_sfnt=True)
        fonts = finder.find_fonts()
        self.assertEqual(len(fonts), expected)
        self.assertIsNotNone(fonts[0].flavor)

    #  Can return a list of TTFont objects that meet the specified criteria
    def test_return_ttfont_objects(self):
        finder = FontFinder(TEST_DATA_DIR, recursive=True)
        fonts = finder.find_fonts()
        self.assertIsInstance(fonts, List)
        self.assertIsInstance(fonts[0], TTFont)

    #  Search for TTFont subclass
    def test_otf_ttfont_subclass(self):
        file_name = "SourceSans3-Regular.otf"
        font_file = TEST_DATA_DIR.joinpath(file_name)
        finder = FontFinder(font_file, return_cls=TTFontSubclass)
        fonts = finder.find_fonts()
        self.assertIsInstance(fonts, List)
        self.assertIsInstance(fonts[0], TTFontSubclass)
        self.assertEqual(fonts[0].get_file_name(), file_name)

    def test_generate_files(self):
        finder = FontFinder(TEST_DATA_DIR, recursive=True)
        files = finder._generate_files()
        self.assertEqual(len(list(files)), ALL_FILES)

    def test_generate_empty_files(self):
        files = FontFinder(EMPTY_DIR)._generate_files()
        self.assertEqual(len(list(files)), 0)

    #  Raises an exception if the return_cls argument is not a subclass of TTFont
    def test_invalid_cls_argument(self):
        with self.assertRaises(FontFinderError):
            InvalidClass = str
            finder = FontFinder(TEST_DATA_DIR, return_cls=InvalidClass)

    #  Raises an exception if both TrueType and PostScript fonts are filtered out
    def test_filter_out_tt_and_ps(self):
        with self.assertRaises(FontFinderError):
            FontFinder(TEST_DATA_DIR, filter_out_tt=True, filter_out_ps=True)

    #  Raises an exception if both web fonts and SFNT fonts are filtered out
    def test_filter_out_web_and_sfnt(self):
        with self.assertRaises(FontFinderError):
            FontFinder(TEST_DATA_DIR, filter_out_woff=True, filter_out_woff2=True, filter_out_sfnt=True)

    #  Raises and exception if both static and variable fonts are filtered out
    def test_filter_out_static_and_variable(self):
        with self.assertRaises(FontFinderError):
            FontFinder(TEST_DATA_DIR, recursive=True, filter_out_static=True, filter_out_variable=True)

    #  Raises a FontFinderError if the input path is not a file or directory.
    def test_invalid_input_path_type(self):
        input_path = 1
        with self.assertRaises(FontFinderError):
            font_finder = FontFinder(input_path)

    #  Raises a FontFinderError if no fonts are found.
    def test_raise_font_finder_error_empty_generator(self):
        finder = FontFinder(EMPTY_DIR)
        with self.assertRaises(FontFinderError):
            finder._validate_fonts()
