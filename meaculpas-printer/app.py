#!/usr/bin/python
# -*- coding: cp850 -*-

import sys
import os
import logging
from ConfigParser import ConfigParser

from flask import Flask
from flask import request
from flask import render_template, make_response
from flask import json
from threading import Thread

from printer import printer
from DocumentoContable import DocumentoContable

ROOT = lambda base = '' : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

parser = ConfigParser()
parser.read(ROOT("../config.cfg"))

##PRODUCT_ID = parser.get('PRINTER','PRODUCT_ID',1)
##VENDOR_ID = parser.get('PRINTER','VENDOR_ID',1)

PRODUCT_ID = 0x0005
VENDOR_ID = 0x04B8

app = Flask(__name__)

def getOption():
    print ROOT("../config.cfg")
    return (PRODUCT_ID,VENDOR_ID)

def getMain():
    global app
    return app

@app.route('/printer')
def hello_world():
    return 'Hello World!'

class Print(Thread):
  def __init__(self, documentos):
    super(Print, self).__init__()
    self.documentos = documentos

    def run(self):
      try:
        epsonPrinter = printer.Printer(VENDOR_ID, PRODUCT_ID)
        #epsonPrinter = printer.Printer(0x04B8, 0x0005)
        for documento in self.documentos:
          epsonPrinter.printDocument(documento)
      except Exception as ex:
        logging.error(ex)
        logging.error("Error imprimiendo documento contable")
      finally:
        sys.exit(0)

@app.route('/printer/documents', methods=['POST'])
def print_documents():
  documents = json.loads(request.form.get('data'))
  documentos = []
    for document in documents:
      items = document['items']
        cliente = document['cliente']
        orden_compra = document['orden_compra']
        document = document['documento']

        documento = DocumentoContable()
        documento.setHeader(orden_compra['numero'])
        documento.setCliente(
            cliente['nombre'],
            cliente['rut'],
            cliente['direccion'],
            cliente['giro'],
            cliente['comuna'],
            document['fecha_emision']
            )
        documento.itemSectionInit()
        for item in items:
          documento.setItem(
              item['codigo'],
              item['descripcion']
              item['cantidad'],
              item['precio'],
              item['precio_total_item']
              )
          documento.setCantidadPalabras(document['total_palabras'])
        documento.setTotales(
            document["neto"],
            document["iva"],
            document["ila13"],
            document["ila15"],
            document["ila27"],
            document["total"]
            )
        documentos.append(documento)
    doPrint = Print(documentos)
    doPrint.start()
    return make_response("se recibieron %s documentos"%len(documentos), 200)

@app.route('/send/documents', methods=['GET'])
def documents():
  return render_template('documents.html')

