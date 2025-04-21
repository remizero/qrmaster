import json
import jsonschema
from jsonschema import validate as validateSchema
from pathlib import Path

from qrmaster.core.schema import schemaObj


class Config () :
  """
  The Config class is responsible for managing the configuration of the QR code generation process.
  It loads, validates, and provides access to the configuration settings defined in a JSON file.

  This class ensures that the configuration is properly structured and contains all necessary fields.
  """


  _instance = None
  _config : dict = {}
  schema = schemaObj


  def __new__ ( cls ) :
    """
    Initializes a new instance of the Config class.

    This method is responsible for setting up the initial state of the configuration object.
    """
    if cls._instance is None :
      cls._instance = super ().__new__ ( cls )
    return cls._instance


  def get ( self, key : str = None ) :
    """
    Retrieves the value associated with the provided key from the configuration.

    Args:
        key (str): The key of the configuration value to retrieve. If no key is provided, the entire configuration is returned.

    Returns:
        The configuration value corresponding to the provided key, or the entire configuration if no key is given.
    """
    if not key :
      return self._config

    else :
      return self._config.get ( key )


  def load ( self, path : str ) -> dict :
    """
    Loads the configuration from a specified file path.

    Args:
        path (str): The file path to the configuration file (typically a JSON file).

    Returns:
        dict: The loaded configuration data.

    Raises:
        FileNotFoundError: If the configuration file is not found at the given path.
        JSONDecodeError: If the configuration file is not a valid JSON file.
    """
    try :

      with open ( path, 'r', encoding = 'utf-8' ) as f :
        self._config = json.load ( f )

    except FileNotFoundError :
      return {
        "valid" : False,
        "error" : f"File not found: {path}"
      }

    except json.JSONDecodeError as jde :
      return {
        "valid" : False,
        "error" : f"JSON malformed in line {jde.lineno}, column {jde.colno}: {jde.msg}"
      }

    return self.validate ()


  def validate ( self ) :
    """
    Validates the loaded configuration to ensure it contains the necessary fields
    and follows the expected structure.

    This method checks that all required settings are present and properly formatted.

    Raises:
        ValueError: If the configuration is missing required fields or contains invalid data.
    """
    try :

      validateSchema ( instance = self._config, schema = self.schema )
      return { "valid" : True, "data" : self._config }

    except jsonschema.exceptions.ValidationError as ve:
      return {
        "valid" : False,
        "error" : f"Validation error in section '{'/'.join(str(p) for p in ve.path)}': {ve.message}"
      }
