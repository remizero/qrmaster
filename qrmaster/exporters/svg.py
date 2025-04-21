import cairosvg
import os

from qrmaster.core.config import Config
from qrmaster.core.logger import Logger
from qrmaster.core.state  import State
from qrmaster.utils.utils import log_step


class SVG :
  """
  Handles the generation and export of QR code data in SVG format.
  Provides utilities for exporting SVG and converting it to PNG format.
  """


  def __init__ ( self, qr ) :
    """
    Initializes the SVG instance with the given QR code data.

    @param qr: The QR code data that will be used to generate the SVG.
    """
    self.qr = qr


  @log_step ( "SVG::export" )
  def export ( self ) :
    """
    Exports the QR code as an SVG file.

    This method generates the SVG representation of the QR code
    and saves it to the defined location.
    """
    project = Config ().get ( "project" )
    output = project.get ( "output", {} )
    base_name = project.get ( "name", "qr" )
    params = output.get ( "params", {} )
    output_dir = State ().get ( "workspace", base_name )

    if not os.path.exists ( output_dir ) :
      os.makedirs ( output_dir )
      Logger ().info ( f"Directorio de salida creado: {output_dir}" )

    filename = f"{base_name}_qr.svg"
    full_path = os.path.join ( output_dir, filename )

    try :
      self.qr.save ( full_path, **params )
      Logger ().success ( f"Archivo SVG generado: {full_path}" )

      # Actualizar el estado del sistema
      State ().set_current_file ( full_path )
      State ().add_generated_file ( full_path )
      State ().add_step ( "SVG::export" )
      State ().save ()

    except Exception as e :
      Logger ().error ( f"Error al guardar el archivo SVG: {e}" )
      State ().add_error ( f"SVG export failed: {e}" )
      raise


  @staticmethod
  @log_step ( "SVG::toPng" )
  def toPng ( input_svg_path, output_png_path, scale = 1.0 ) :
    """
    Converts an SVG file to PNG format.

    @param input_svg_path: Path to the input SVG file.
    @param output_png_path: Path where the output PNG file will be saved.
    @param scale: A scaling factor to adjust the resolution of the output PNG (default is 1.0).
    """
    cairosvg.svg2png ( url = input_svg_path, write_to = output_png_path, scale = scale )
    # Actualizar el estado del sistema
    State ().set_current_file ( output_png_path )
    State ().add_step ( "SVG::toPng" )
    State ().add_generated_file ( output_png_path )
    State ().save ()
