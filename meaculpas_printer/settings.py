#!/usr/bin/python
import os

from ConfigParser import ConfigParser

ROOT = lambda base = '' : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

parser = ConfigParser()
parser.read(ROOT("../config.cfg"))

PRODUCT_ID = parser.get('PRINTER', 'PRODUCT_ID', 1)
VENDOR_ID = parser.get('PRINTER', 'VENDOR_ID', 1)

ENCODING = parser.get('DOCUMENTO_CONTABLE', 'ENCODING')
