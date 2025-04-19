import argparse
import sys


from core.commands import Commands
from core.config import Config


def main () :

  parser = argparse.ArgumentParser ( description = "QR Code Generator CLI." )
  subparsers = parser.add_subparsers ( dest = "command" )

  # generate command
  generate_parser = subparsers.add_parser ( "generate", help = "Generate QR code." )
  generate_parser.add_argument ( "--config", required = True, help = "Path to options.json." )

  # validate command
  validate_parser = subparsers.add_parser ( "validate", help = "Validates the JSON configuration file." )
  validate_parser.add_argument ( "--config", type = str, required = True, help = "Path to the configuration JSON file." )

  # viewLog command
  view_log_parser = subparsers.add_parser ( "view-log", help = "View the system or project log." )
  view_log_parser.add_argument ( "--path", type = str, default = "logs/global.log", help = "Log file path." )
  view_log_parser.add_argument ( "--tail", type = int, default = 0, help = "Number of final lines to display." )
  view_log_parser.add_argument ( "--paginate", action = "store_true", help = "Display with pagination (less)." )

  # Comando: clear-log
  clear_log_parser = subparsers.add_parser ( "clear-log", help = "Delete the log file." )
  clear_log_parser.add_argument ( "--path", type = str, default = "logs/global.log", help = "Path to the log file." )

  # report command
  generate_parser = subparsers.add_parser ( "report", help = "Generate Technnical Report for QR code." )
  generate_parser.add_argument ( "--config", required = True, help = "Path to options.json." )


  args = parser.parse_args ()


  config = Config ()
  result = config.load ( args.config )

  if not result.get ( "valid", True ) :  # Fallo al cargar (archivo no existe o JSON malformado)

    print ( f"[❌] Error uploading config file: {result['error']}" )
    sys.exit ( 1 )


  if args.command == "generate" :

    Commands.generate ( config )

  elif args.command == "report" :

    Commands.report ( config )

  elif args.command == "validate" :

    Commands.validate ( config )

  elif args.command == "view-log" :

    Commands.viewLog ( path = args.path, tail = args.tail, paginate = args.paginate )

  elif args.command == "clear-log" :

    Commands.clearLog ( args.path )
