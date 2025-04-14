import argparse
from commands import (
  options
)


def main () :

  parser = argparse.ArgumentParser ( description = "Generador de QR y documentación técnica en PDF" )
  parser.add_argument ( '--options', required = True, help = "Path to JSON file with options." )
  args = parser.parse_args ()

  if args.options :
    options ( args.options )


if __name__ == "__main__" :
  main ()
