import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.ALRMFinancialCounsellingForm',
      version='0.5.0',
      description=('Automated ALRM-Wyatt Financial Counselling Form'),
      long_description='# Wyatt - ALRM Financial Counselling Consent Form\r\n\r\nA Docassemble interview to automate the preparation of a this form.\r\n\r\nCurrently this app:\r\n\r\n- asks the user the questions on the form\r\n- populates a PDF with the supplied answers\r\n- makes PDF available for download and/or email\r\n\r\nFuture versions will:\r\n\r\n- record interviews in a database for reporting purposes\r\n- allow for bulk imports of data into the database',
      long_description_content_type='text/markdown',
      author='Mark Ferraretto',
      author_email='mark@ferraretto.com',
      license='The MIT License (MIT)',
      url='https://www.alrm.org.au',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/ALRMFinancialCounsellingForm/', package='docassemble.ALRMFinancialCounsellingForm'),
     )

