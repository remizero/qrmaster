import os

from core.config    import Config
from core.logger    import Logger
from core.project   import Project
from core.qr        import QR
from core.report    import Report
from core.state     import State
from exporters.pdf  import PDF
from exporters.svg  import SVG
from graphics.frame import Frame
from graphics.logo  import Logo
from utils.utils    import log_step, Utils


class Commands () :
  """
  Container class for the main commands of the QRMaster system.

  Each static method represents an action that can be executed from the CLI,
  such as generating a QR code, creating a technical report, validating the configuration,
  or managing log files.
  """


  @staticmethod
  @log_step ( "Command generate" )
  def generate ( config : Config ) :
    """
    Generates QR resources according to the parameters defined in the configuration file.

    :param config: Validated configuration instance of the project.
    :type config: Config
    """

    # The project and working directory is created.
    projectConfig = config.get ( "project" )
    project = Project ( projectConfig )
    projectDir = project.createDir ()

    # The QR code is generated.
    qr = QR ().generate ()

    # The QR code is exported to SVG format.
    output_svg = SVG ( qr )
    output_svg.export ()

    # The logo is processed. It's converted to SVG and then embedded into the SVG QR code.

    if projectConfig.get ( "logo" ) :

      logo = Logo ()
      logo.pngToSvg ()
      logo.embed ()

    # An aesthetic frame is generated for the QR code in SVG format.
    if projectConfig.get ( "frame" ) :

      output_frame = Frame ()
      output_frame.create ()
      output_frame.embed ()

      base_name = projectConfig.get ( "name", "qr" )
      input_svg_path  = State ().get ( "current_file", base_name )
      output_dir = State ().get ( "workspace", base_name )
      info = Utils ().fileInfo ( input_svg_path )
      output_png_path = os.path.join ( output_dir, info [ "name" ] + ".png" )

      SVG.toPng ( input_svg_path, output_png_path )

    # A PDF is generated for the QR code to be printed.
    if projectConfig.get ( "pdf" ) :

      output_pdf = PDF ()
      output_pdf.export ()

    report = Report ()
    report.generate ()


  @staticmethod
  @log_step ( "Command report" )
  def report ( config : Config ) :
    """
    Generates a technical report in PDF format based on project resources.

    :param config: Validated project configuration instance.
    :type config: Config
    """

    report = Report ()
    report.generate ()


  @staticmethod
  @log_step ( "Command validate" )
  def validate ( config : Config ) :
    """
    Validates the structure and content of the JSON configuration file.

    :param config: Configuration instance to validate.
    :type config: Config
    """

    print ( "[✅] Archivo JSON cargado y validado con éxito." )
    print ( config.get () )


  @staticmethod
  @log_step ( "Command veiwLog" )
  def viewLog ( path = "logs/global.log", tail = 0, paginate = False ) :
    """
    Displays the contents of the specified log file.

    :param path: Path to the log file to display.
    :type path: str
    :param tail: Number of trailing lines to display (0 for the entire file).
    :type tail: int
    :param paginate: Indicates whether to paginate the console output.
    :type paginate: bool
    """

    if not os.path.exists ( path ) :
      print ( f"\033[91m❌ El archivo de log no existe: {path}\033[0m" )
      return

    with open ( path, 'r', encoding = 'utf-8' ) as f :
      lines = f.readlines ()

    if tail > 0:
      lines = lines[-tail:]

    if paginate :
      import tempfile
      import subprocess
      with tempfile.NamedTemporaryFile ( mode = 'w+', delete = False, encoding = 'utf-8' ) as tmp :
        tmp.writelines ( lines )
        tmp.flush ()
        subprocess.run ( [ 'less', tmp.name ] )
    else :
      print ( "\n".join ( lines ) )


  @staticmethod
  @log_step ( "Command clearLog" )
  def clearLog ( path = "logs/global.log" ) :
    """
    Clears the contents of the specified log file.

    :param path: Path to the log file to clear.
    :type path: str
    """
    if os.path.exists ( path ) :
      with open ( path, 'w', encoding = 'utf-8' ) as f :
        f.write ( "" )  # Vacía el archivo
      print ( f"\033[92m✅ Log limpiado correctamente: {path}\033[0m" )
    else :
      print ( f"\033[93m⚠️ No se encontró el log. Nada que limpiar: {path}\033[0m" )
