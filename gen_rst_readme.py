import pandoc
import os

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

doc = pandoc.Document()
doc.markdown = open('README.md').read()
f = open('README', 'w+')
f.write(doc.rst)
f.close()