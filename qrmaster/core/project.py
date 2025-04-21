import os
import json

from qrmaster.core.config import Config
from qrmaster.core.state  import State
from qrmaster.utils.utils import log_step


class Project :
  """
  Manages the creation and configuration of the project workspace
  based on the provided configuration dictionary.
  """


  def __init__ ( self, config : dict ) :
    """
    Initializes the Project instance with the given configuration.

    @param config: A dictionary containing the project configuration.
    """
    self.project_name = config.get ( "name" )
    home = os.path.expanduser ( "~" )
    self.project_path = os.path.join ( f"{home}/qrmaster/projects", self.project_name )
    self.state_path = os.path.join ( self.project_path, "state.json" )


  @log_step ( "Project::createDir" )
  def createDir ( self ) -> str :
    """
    Creates the workspace directory for the project inside the user's home directory.

    @return: The absolute path to the created workspace directory.
    """
    os.makedirs ( self.project_path, exist_ok = True )
    State ().setWorkspace ( self.project_path )
    State ().add_step ( "Project::createDir" )
    State ().save ()
    return self.project_path
