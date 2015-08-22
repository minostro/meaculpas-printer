#!/usr/bin/python

import sys
import logging

from threading import Thread
from flask import Flask, request, render_template, make_response, json

from epson_printer import printer
from DocumentoContable import DocumentoContable
from settings import PRODUCT_ID, VENDOR_ID, ENCODING

app = Flask(__name__)

def getMain():
  global app
  return app

@app.route('/printer')
def hello_world():
  return "{0}, {1}, {2}".format(PRODUCT_ID, VENDOR_ID, ENCODING)

class Print(Thread):
  def __init__(self, documentos):
    super(Print, self).__init__()
    self.documentos = documentos

  def run(self):
    try:
      epsonPrinter = printer.Printer(VENDOR_ID, PRODUCT_ID)
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
    desglose_impuestos = document['desglose_impuestos']

    documento = DocumentoContable()
    documento.setHeader(orden_compra['numero'])
    documento.setCliente(
        cliente['nombre'],
        cliente['rut'],
        cliente['direccion'],
        cliente['giro'],
        cliente['comuna'],
        document['fecha_emision'],
        document['vendedor']
    )
    documento.itemSectionInit()
    for item in items:
      documento.setItem(
          item['codigo'],
          item['descripcion'],
          item['cantidad'],
          item['precio'],
          item['precio_total_item']
      )
    documento.desgloseImpuestosSectionInit()
    for desglose_impuesto in desglose_impuestos:
      documento.setDesgloseImpuesto(desglose_impuesto)
    documento.setCantidadPalabras(document['total_palabras'])
    documento.setTotales(
        document["neto"],
        document["iva"],
        document["impuestos"],
        document["total"]
    )
    documentos.append(documento)
  doPrint = Print(documentos)
  doPrint.start()
  return make_response("se recibieron %s documentos"%len(documentos), 200)

