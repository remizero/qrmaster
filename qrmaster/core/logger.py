import os
from datetime import datetime
from threading import Lock


class Logger :
  """
  Logger class for managing the logging of system messages at different levels,
  such as information, warnings, errors, and success messages. It uses a log file
  to persist messages, allowing traceability of the execution flow.
  """

  _instance = None
  _lock = Lock ()
  COLORS = {
    "INFO": "\033[94m",     # Azul
    "WARNING": "\033[93m",  # Amarillo
    "ERROR": "\033[91m",    # Rojo
    "SUCCESS": "\033[92m",  # Verde
    "ENDC": "\033[0m",      # Reset
  }


  def __new__ ( cls, log_path = "logs/global.log" ) :
    """
    Special method that ensures the singleton pattern is implemented.

    Args:
    log_path (str): Path to the log file where messages will be stored.

    Returns:
    Logger: Single instance of the Logger class.
    """
    with cls._lock :
      if cls._instance is None :
        cls._instance = super ( Logger, cls ).__new__( cls )
        cls._instance._init ( log_path )
      return cls._instance


  def _init ( self, log_path ) :
    """
    Initializes the logger instance by setting the log file.

    Args:
    log_path (str): Path to the log file where messages will be stored.
    """
    home = os.path.expanduser ( "~" )
    self.log_path = os.path.join ( home, log_path )
    os.makedirs ( os.path.dirname ( self.log_path ), exist_ok = True )


  def _log ( self, message : str, level : str ) :
    """
    Internal method to log a message with a specific level to the log file.

    Args:
    message (str): The message to log.
    level (str): Message level (INFO, WARNING, ERROR, SUCCESS).
    """
    timestamp = datetime.now ().isoformat ()
    log_line = f"[{timestamp}] [{level.upper ()}] {message}"
    color = self.COLORS.get ( level.upper (), "" )
    endc = self.COLORS [ "ENDC" ]
    print ( f"{color}{log_line}{endc}" )
    with open ( self.log_path, 'a', encoding = 'utf-8' ) as f :
      f.write ( f"[{timestamp}] [{level.upper ()}] {message}\n" )


  def info ( self, message : str ) :
    """
    Logs an informational message to the log file.

    Args:
    message (str): The informational message to log.
    """
    self._log ( message, "INFO" )


  def warning ( self, message : str ) :
    """
    Logs a warning to the log file.

    Args:
    message (str): The warning message to log.
    """
    self._log ( message, "WARNING" )


  def error ( self, message : str ) :
    """
    Logs an error message to the log file.

    Args:
    message (str): The error message to log.
    """
    self._log ( message, "ERROR" )


  def success ( self, message : str ) :
    """
    Logs a success message to the log file.

    Args:
    message (str): The success message to log.
    """
    self._log ( message, "SUCCESS" )
