#!/usr/bin/python

import sys

from epson_printer.document import Document
from settings import ENCODING

class DocumentoContable(Document):
  def __init__(self, *args, **kwargs):
    super(DocumentoContable, self).__init__(*args, **kwargs)
    self.itemQuantity = 0

  def setHeader(self, numeroDocumento):
    self.setData("\n"*7)
    self.setData("{:>60}".format(numeroDocumento))

  def setCliente(self, nombre, rut, direccion, giro, comuna, fechaDocumento):
    self.setData("\n"*8)
    left_margin = " " * 4
    nombre = self.getDecodedString(nombre).upper()
    direccion = self.getDecodedString(direccion).upper()
    giro = self.getDecodedString(giro).upper()
    comuna = self.getDecodedString(comuna).upper()

    self.setData("{:} {:<55} {:}".format(left_margin, nombre[:55], rut))
    self.setData("{:} {:<55} {:}".format(left_margin, direccion[:55], giro))
    self.setData("{:} {:}\n".format(left_margin, comuna))
    self.setData(fechaDocumento)

  def itemSectionInit(self):
    self.setData("\n"*2)

  def setItem(self, codigo, descripcion, cantidad, precio_unitario, precio_total):
    self.itemQuantity += 1
    descripcion = self.getDecodedString(descripcion)
    item = "{:>13} {:<32} {:>9} {:>9} {:>10}".format(codigo[:13], descripcion[:32], cantidad, precio_unitario, precio_total)
    self.setData(item)

  def setCantidadPalabras(self, cantidadPalabras):
    self.setData("\n"* (22 - self.itemQuantity))
    cantidadPalabras = self.getDecodedString(cantidadPalabras + " pesos.\n")
    self.setData(cantidadPalabras.upper())

  def setTotales(self, totalNeto, iva, ila13, ila15, ila27, total):
    leftMargin = " " * 48
    self.setData(leftMargin + "{:>28}".format(totalNeto))
    self.setData(leftMargin + "    19% {:>20}".format(iva))
    self.setData(leftMargin + "13% {:>24}".format(ila13))
    self.setData(leftMargin + "15% {:>24}".format(ila15))
    self.setData(leftMargin + "27% {:>24}".format(ila27))
    self.setData(leftMargin + "    {:>24}".format(total))

  def getDecodedString(self, text):
    return text.encode(ENCODING)

