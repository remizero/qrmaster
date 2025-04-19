import json
import os
from datetime import datetime

from core.config import Config
from core.logger import Logger
from utils.utils import log_step


class State () :
  """
  The State class is used to manage and track the current state of the QR code project, including
  information about generated files, errors, and configuration. It provides functionality to load,
  save, and manipulate state data, making it easier to handle the workflow of QR code generation
  and related tasks.

  This class maintains the state in a structured manner, saving relevant project information in
  files for later use.
  """


  _instance = None
  data = {
    "current_file": "",
    "frame": "",
    "pdf": "",
    "last_svg": "",
    "last_run": "",
    "workspace": "",
    "steps_done": [],
    "generated_files": [],
    "errors": []
  }


  def __new__ ( cls ) :
    """
    Creates a new instance of the State class.

    This method initializes the state management system. It ensures that an instance of the class
    is created with the necessary attributes to manage project state.
    """
    if cls._instance is None :
      cls._instance = super ().__new__ ( cls )
    return cls._instance


  def __init__ ( self ) :
    """
    Initializes the state object.

    This method sets up the initial state attributes that will be used to track project progress,
    including the current file, generated files, errors, and other state-specific information.
    """
    root = Config ().get ( "project" )
    project_path = os.path.join ( "projects", root.get ( "name" ) )
    if project_path :
      self.path = os.path.join ( project_path, "state.json" )
      self.log_path = os.path.join ( os.path.dirname ( self.path ), "state._log" )
      self.load ()

    else :
      raise ValueError ( "No project path defined in Config" )


  def _log ( self, message : str ) :
    """
    Logs a message to the state system.

    This method adds a log entry for a given message. It is used internally to keep track of
    important events or actions within the state.

    Args:
        message (str): The message to log.
    """
    timestamp = datetime.now ().isoformat ()
    with open ( self.log_path, 'a', encoding = 'utf-8' ) as f :
      f.write ( f"[{timestamp}] {message}\n" )


  def load ( self ) :
    """
    Loads the saved state data from the file.

    This method retrieves the state information from persistent storage, allowing the project
    to resume from the last saved state.
    """
    if os.path.exists ( self.path ) :
      with open ( self.path, 'r', encoding = 'utf-8' ) as f :
        self.data.update ( json.load ( f ) )
      self._log ( f"Se carga el archivo de estado del proyecto en {self.path}" )
      Logger ().info ( f"Se carga el archivo de estado del proyecto en {self.path}" )


  def save ( self ) :
    """
    Saves the current state data to a file.

    This method writes the current state information to a file so that it can be restored later
    if needed.
    """
    os.makedirs ( os.path.dirname ( self.path ), exist_ok = True )
    with open ( self.path, 'w', encoding = 'utf-8' ) as f :
      json.dump ( self.data, f, indent = 2 )
    self._log ( f"Estado guardado en {self.path}" )
    Logger ().info ( f"Estado guardado en {self.path}" )


  def set_current_file ( self, filename : str ) :
    """
    Sets the current file being processed in the state.

    This method updates the state with the current file, allowing the system to track which file
    is being worked on.

    Args:
        filename (str): The name of the current file.
    """
    self.data [ "current_file" ] = filename
    self.save ()
    self._log ( f"Archivo actual establecido: {filename}" )
    Logger ().info ( f"Archivo actual establecido: {filename}" )


  def set_frame ( self, filename : str ) :
    """
    Sets the frame file in the state.

    This method stores information about the frame file used in the project, helping to manage
    and track its status.

    Args:
        filename (str): The name of the frame file.
    """
    self.data [ "frame" ] = filename
    self.save ()
    self._log ( f"Archivo frame establecido: {filename}" )
    Logger ().info ( f"Archivo frame establecido: {filename}" )


  def set_pdf ( self, path : str ) :
    """
    Sets the path for the generated PDF file in the state.

    This method updates the state with the path to the generated PDF, allowing the system to
    track where the final output file is stored.

    Args:
        path (str): The file path for the generated PDF.
    """
    self.data [ "pdf" ] = path
    self.save ()
    self._log ( f"Último archivo generado: {path}" )
    Logger ().info ( f"Último archivo generado: {path}" )


  def setWorkspace ( self, path : str ) :
    """
    Sets the workspace directory for the project.

    This method updates the state with the location of the workspace, allowing the system to
    track where project-related files are stored.

    Args:
        path (str): The workspace directory path.
    """
    self.data [ "workspace" ] = path
    self.save ()
    self._log ( f"Workspace directory set to {path}" )
    Logger ().info ( f"Workspace directory set to {path}" )


  def add_step ( self, step : str ) :
    """
    Adds a step to the state.

    This method records a step in the project's workflow, helping to track the progress of
    tasks and actions performed.

    Args:
        step (str): A description of the step to add.
    """
    if step not in self.data [ "steps_done" ] :
      self.data [ "steps_done" ].append ( step )
      self.save ()
      self._log ( f"Paso añadido: {step}" )
      Logger ().info ( f"Paso añadido: {step}" )


  def set_last_run_now ( self ) :
    """
    Sets the last run timestamp to the current time.

    This method updates the state to record the current time as the last run time of the project.
    It helps track when the project was last executed.
    """
    self.data [ "last_run" ] = datetime.now ().isoformat ()
    self.save ()
    self._log ( f"Ejecución registrada en: {timestamp}" )
    Logger ().info ( f"Ejecución registrada en: {timestamp}" )


  def add_generated_file ( self, filename : str ) :
    """
    Adds a generated file to the state.

    This method records a file that was generated during the project workflow, helping to keep
    track of the files that were created.

    Args:
        filename (str): The name of the generated file.
    """
    self.data [ "generated_files" ].append ( filename )
    self.save ()
    self._log ( f"Archivo generado registrado: {filename}" )
    Logger ().info ( f"Archivo generado registrado: {filename}" )


  def add_error ( self, error_msg : str ) :
    """
    Adds an error message to the state.

    This method records an error encountered during the project execution, helping to track
    issues that arise during the workflow.

    Args:
        error_msg (str): The error message to log.
    """
    self.data [ "errors" ].append ( error_msg )
    self.save ()
    self._log ( f"Error registrado: {error_msg}" )
    Logger ().info ( f"Error registrado: {error_msg}" )


  def reset_errors ( self ) :
    """
    Resets the error list in the state.

    This method clears all recorded errors, allowing the system to start fresh or ignore previous
    errors if needed.
    """
    self.data [ "errors" ] = []
    self.save ()
    self._log ( "Errores reseteados." )
    Logger ().info ( "Errores reseteados." )


  def get ( self, key : str, default = None ) :
    """
    Retrieves a value from the state.

    This method returns the value associated with the provided key from the state data. If the
    key is not found, it returns the specified default value.

    Args:
        key (str): The key for the value to retrieve.
        default: The default value to return if the key is not found. (default is None)

    Returns:
        The value associated with the key or the default value if the key is not found.
    """
    return self.data.get ( key, default )


  def as_dict ( self ) -> dict :
    """
    Returns the state as a dictionary.

    This method converts the current state into a dictionary format, making it easier to inspect
    or save the state as a serialized object.

    Returns:
        dict: The current state as a dictionary.
    """
    return self.data
