import pandoc
import os
import re

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

def convert_md_to_rst():
    doc = pandoc.Document()
    doc.markdown = open('README.md').read()

    filtered = str(doc.rst)
    filtered = re.sub('Table of Contents\n~~~~~~~~~~~~~~~~~.*Installation\n------------', 'Installation\n------------', filtered, flags=re.DOTALL)
    filtered = re.sub('\n`\|Build Status\| <https://travis-ci.org/csu/pyquora>`_ `\|Latest\nVersion\| <https://pypi.python.org/pypi/quora/>`_\n', '', filtered, flags=re.DOTALL)
    filtered = re.sub('`\|Gitter\|.*>`_', '', filtered, flags=re.DOTALL)
    filtered = re.sub('`\|HuBoard\|.*`_', '', filtered, flags=re.DOTALL)
    filtered = re.sub('Contribute\n----------.*', '', filtered, flags=re.DOTALL)

    f = open('README', 'w+')
    f.write(filtered)
    f.close()

convert_md_to_rst()