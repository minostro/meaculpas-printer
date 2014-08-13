#-*- encoding: UTF-8 -*-
###############################################
# Todos los derechos reservados a:            #
# CreceLibre Consultores en Tecnologías Ltda. #
#                                             #
# ©Milton Inostroza Aguilera                  #
# minostro@crecelibre.cl                      #
# ©Andrés Otárola Alvarado                    #
# aotarola@crecelibre.cl                      #
# 2014                                        #
###############################################

import os
import argparse

EGG_REPOSITORY = 'http://eggs.axion-ingenieria.cl/'
EGG_FILE = os.path.join(os.path.dirname(__file__), 'EggFile').replace('\\','/')

class EnvironmentException(Exception):
  pass

def _execute_command(command):
  if os.system(command) != 0:
    raise EnvironmentException('Command executed: {0}'.format(command))

def create(**options):
  command = 'virtualenv {0} --no-site-packages --python=python{1}'.format(options['env_name'], options['python_version'])
  _execute_command(command)

def initialize(**options):
  command = './bin/python bin/pip install --find-links={0} -r {1}'.format(options['egg_repository'], options['egg_file'])
  _execute_command(command)

def clean(**options):
  command = 'rm -rf bin build include lib share doc'
  _execute_command(command)

def run(**options):
  if options['create']:
    try:
      clean(**vars(args))
      create(**vars(args))
      initialize(**vars(args))
    except EnvironmentException as e:
      print 'Environment cannot be initialied properly \n'
      print 'Cleaning all the temporary files \n'
      clean(**vars(args))
  elif options['initialize']:
    try:
      initialize(**vars(args))
    except EnvironmentException as e:
      print '\nCannot initialize the environment...\n'


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Initialize the entire environment for this app')

  parser.add_argument(
    '--initialize',
    action='store_true',
    help='Folder name of the new environment',
    default=True
  )

  parser.add_argument(
    '--create',
    action='store_true',
    help='Folder name of the new environment',
    default=False
  )

  parser.add_argument(
    '--env_name',
    type=str,
    help='Folder name of the new environment',
    default='.'
  )

  parser.add_argument(
    '--python_version',
    type=str,
    help='Python version interpreter for the new environment',
    default='2.7'
  )

  parser.add_argument(
    '--egg_repository',
    type=str,
    help='Repository where eggs come from',
    default=EGG_REPOSITORY
  )

  parser.add_argument(
    '--egg_file',
    type=str,
    help='Application dependencies',
    default=EGG_FILE
  )

  args = parser.parse_args()
  run(**vars(args))
