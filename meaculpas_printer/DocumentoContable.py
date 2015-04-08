#!/usr/bin/python

import sys

from epson_printer.document import Document
from settings import ENCODING

class DocumentoContable(Document):
  def __init__(self, *args, **kwargs):
    super(DocumentoContable, self).__init__(*args, **kwargs)
    self.itemQuantity = 0
    self.impuestoQuantity = 0

  def setHeader(self, numeroDocumento):
    self.setData("\n"*7)
    self.setData("{:>60}".format(numeroDocumento))

  def setCliente(self, nombre, rut, direccion, giro, comuna, fechaDocumento):
    self.setData("\n"*8)
    left_margin = " " * 4
    nombre = self.getEncodedString(nombre).upper()
    direccion = self.getEncodedString(direccion).upper()
    giro = self.getEncodedString(giro).upper()
    comuna = self.getEncodedString(comuna).upper()

    self.setData("{:} {:<55} {:}".format(left_margin, nombre[:55], rut))
    self.setData("{:} {:<55} {:}".format(left_margin, direccion[:55], giro))
    self.setData("{:} {:}\n".format(left_margin, comuna))
    self.setData(fechaDocumento)

  def itemSectionInit(self):
    self.setData("\n"*2)

  def setItem(self, codigo, descripcion, cantidad, precio_unitario, precio_total):
    self.itemQuantity += 1
    descripcion = self.getEncodedString(descripcion)
    item = "{:>13} {:<32} {:>9} {:>9} {:>10}".format(codigo[:13], descripcion[:32], cantidad, precio_unitario, precio_total)
    self.setData(item)

  def desgloseImpuestosSectionInit(self):
    self.setData("\n"* (20 - self.itemQuantity))

  def setDesgloseImpuesto(self, descripcionImpuesto):
    self.impuestoQuantity += 1
    descripcionImpuesto = self.getEncodedString(descripcionImpuesto)
    self.setData(descripcionImpuesto)

  def setCantidadPalabras(self, cantidadPalabras):
    self.setData("\n"* (2 - self.impuestoQuantity))
    cantidadPalabras = self.getEncodedString(cantidadPalabras + " pesos.\n")
    self.setData(cantidadPalabras.upper())

  def setTotales(self, totalNeto, iva, impuestos, total):
    leftMargin = " " * 48
    self.setData(leftMargin + "{:>28}".format(totalNeto))
    self.setData(leftMargin + "    19% {:>20}".format(iva))
    for impuesto, monto in impuestos.iteritems():
      self.setData(leftMargin + " {:}% {:>20}".format(impuesto, monto))
    self.setData(leftMargin + "    {:>24}".format(total))

  def getEncodedString(self, text):
    return text.encode(ENCODING)

