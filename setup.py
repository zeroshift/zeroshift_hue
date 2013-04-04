import sys
import os
from distutils.core import setup

import zeroshift_hue

setup(name='zeroshift_hue',
      version="0.1",
      description='Module for Philips Hue bulbs.',
      long_description="Module for Philips Hue bulbs.",
      author="Nick Prendergast",
      author_email='neprendergast@gmail.com',
      url='https://github.com/zeroshift/zeroshift_hue',
      py_modules=['zeroshift_hue'],
      scripts=['zeroshift_hue.py'],
      license='BSD'
