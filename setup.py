from distutils.core import setup
import py2exe

setup(console=['scriptukas.py'],
      zipfile=None,
      options={
          "py2exe": {
              "optimize": 2,
              "bundle_files": 1,
              "compressed": True,
              "dll_excludes": ['msvcr71.dll'],
              "excludes": ['pyreadline', 'difflib', 'doctest', 'locale',
                           'optparse', 'pickle', 'calendar']
          }
      })
