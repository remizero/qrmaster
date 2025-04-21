import os
from pixels2svg import pixels2svg

from qrmaster.core.config     import Config
from qrmaster.core.logger     import Logger
from qrmaster.core.state      import State
from qrmaster.utils.utils     import log_step, Utils
from qrmaster.utils.svg_utils import SvgUtils


class Logo () :
  """
  Handles the embedding and conversion of logos for QR codes.
  Provides methods for embedding logos into QR codes and converting PNG logos to SVG format.
  """


  @log_step ( "Logo::embed" )
  def embed ( self ) :
    """
    Embeds a logo into the QR code.

    This method inserts the provided logo into the QR code, adjusting its size
    and position based on the QR code's dimensions and the logo's properties.
    """
    project = Config ().get ( "project" )
    logo = project.get ( "logo" )
    logoPath = logo.get ( "path" )
    if not os.path.exists ( logoPath ) :

      raise ValueError ( "PATH must be provided for node 'logo'" )
      # return self.base_svg  # No logo, return original

    base_name = project.get ( "name", "qr" )
    output_dir = State ().get ( "workspace", base_name )

    if not os.path.exists ( output_dir ) :
      os.makedirs ( output_dir )
      Logger ().info ( f"Directorio de salida creado: {output_dir}" )

    qr_svg = State ().get ( "current_file", base_name )

    info = Utils ().fileInfo ( logoPath )
    logo_svg = os.path.join ( output_dir, info [ "name" ] + ".svg" )

    info = Utils ().fileInfo ( State ().get ( "current_file", base_name ) )
    output_svg = os.path.join ( output_dir, info [ "name" ] + "_logo.svg" )

    qr_svg_path = os.path.join ( output_dir, qr_svg )
    Utils ().svgIntoSvg ( qr_svg_path, logo_svg, output_svg )
    State ().set_current_file ( output_svg )
    State ().add_step ( "Logo::embed" )
    State ().add_generated_file ( output_svg )
    State ().save ()


  @log_step ( "Logo::pngToSvg" )
  def pngToSvg ( self ) :
    """
    Converts a PNG logo file to SVG format.

    This method converts a PNG image to SVG format for use in QR code embedding or other applications.
    """
    project = Config ().get ( "project" )
    logo = project.get ( "logo" )
    logoPath = logo.get ( "path" )
    if not os.path.exists ( logoPath ) :

      raise ValueError ( "PATH must be provided for node 'logo'" )

    base_name = project.get ( "name", "qr" )
    output_dir = State ().get ( "workspace", base_name )

    if not os.path.exists ( output_dir ) :
      os.makedirs ( output_dir )
      Logger ().info ( f"Directorio de salida creado: {output_dir}" )

    info = Utils ().fileInfo ( logoPath )
    output_path = os.path.join ( output_dir, info [ "name" ] + ".svg" )

    pixels2svg ( logoPath, output_path )
    Logger ().info ( f"Conversión de Logo a SVG realizada exitosamente: {output_path}" )
    State ().add_step ( "Logo::pngToSvg" )
    State ().add_generated_file ( output_path )
    State ().save ()
