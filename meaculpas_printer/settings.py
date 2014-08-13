#!/usr/bin/python
import os

from ConfigParser import ConfigParser

ROOT = lambda base = '' : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

parser = ConfigParser()
parser.read(ROOT("../config.cfg"))

PRODUCT_ID = int(parser.get('PRINTER', 'PRODUCT_ID', 1), 0)
VENDOR_ID = int(parser.get('PRINTER', 'VENDOR_ID', 1), 0)

ENCODING = parser.get('DOCUMENTO_CONTABLE', 'ENCODING')
