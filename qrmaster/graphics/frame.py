import os
import svgutils.transform as sg
from svgwrite import Drawing

from qrmaster.core.config     import Config
from qrmaster.core.logger     import Logger
from qrmaster.core.state      import State
from qrmaster.utils.utils     import log_step, Utils
from qrmaster.utils.svg_utils import SvgUtils


class Frame :
  """
  Handles the creation and embedding of frames around QR codes.
  Provides methods for creating a frame around the QR code and embedding it with specified attributes.
  """


  @log_step ( "Frame::create" )
  def create ( self ) :
    """
    Creates a frame around the QR code.

    This method generates a frame around the QR code, setting the margins, colors, and other styling options
    as specified in the configuration, and positions the QR code within the frame.
    """
    project = Config ().get ( "project" )
    base_name = project.get ( "name", "qr" )
    qr_logo_svg_path = State ().get ( "current_file", base_name )

    qr_svg = sg.fromfile ( qr_logo_svg_path )
    qr_width  = Utils ().convertToPixels ( qr_svg.get_size () [ 0 ] )
    qr_height = Utils ().convertToPixels ( qr_svg.get_size () [ 1 ] )

    frameConfig = project.get ( "frame", {} )

    if frameConfig :
      # Configuración
      margin            = frameConfig.get ( "margin", 10 )
      text_height       = frameConfig.get ( "text_height", 60 )
      bg_color          = frameConfig.get ( "background_color", "white" )
      border_color      = frameConfig.get ( "border_color", "#005baa" )
      border_width      = frameConfig.get ( "border_width", 4 )

      title             = frameConfig.get ( "title", "" )
      title_font_size   = frameConfig.get ( "title_font_size", 16 )
      title_font_family = frameConfig.get ( "title_font_family", "Arial" )
      title_color       = frameConfig.get ( "title_color", border_color )

      message           = frameConfig.get ( "message", "Escanea para ver el documento." )
      message_font_size = frameConfig.get ( "message_font_size", 12 )
      message_color     = frameConfig.get ( "message_color", "#555" )

      svg_width  = qr_width + 2 * margin
      svg_height = qr_height + 2 * margin + text_height

      workspace = State ().get ( "workspace", base_name )
      output_path = os.path.join ( workspace, f"{base_name}_frame.svg" )

      dwg = Drawing (
              output_path,
              size = ( f"{svg_width}px", f"{svg_height}px" ),
              profile = 'tiny'
            )

      dwg.add (
        dwg.rect (
          insert = ( 0, 0 ),
          size   = ( f"{svg_width}px", f"{svg_height}px" ),
          fill   = bg_color
        )
      )
      dwg.add (
        dwg.rect (
          insert       = ( margin, margin ),
          size         = ( f"{svg_width - 2 * margin}px", f"{svg_width - 2 * margin}px" ),
          fill         = "none",
          stroke       = border_color,
          stroke_width = border_width
        )
      )

      # Texto principal
      dwg.add (
        dwg.text (
          title,
          insert      = ( f"{svg_width / 2}px", f"{svg_width + 30}px" ),
          text_anchor = "middle",
          font_size   = f"{title_font_size}px",
          font_family = title_font_family,
          font_weight = "bold",
          fill        = title_color
        )
      )

      # Mensaje opcional
      dwg.add (
        dwg.text (
          message,
          insert      = ( f"{svg_width / 2}px", f"{svg_width + 50}px" ),
          text_anchor = "middle",
          font_size   = f"{message_font_size}px",
          font_family = "Arial",
          fill        = message_color
        )
      )

      dwg.save ()
      State ().set_frame ( output_path )
      State ().add_step ( "Frame::create" )
      State ().add_generated_file ( output_path )
      State ().save ()


  @log_step ( "Frame::embed" )
  def embed ( self ) :
    """
    Embeds the created frame into the QR code.

    This method inserts the previously created frame into the QR code image, ensuring the frame
    is correctly positioned and adjusted to fit the QR code's dimensions.
    """
    project = Config ().get ( "project" )

    base_name = project.get ( "name", "qr" )
    output_dir = State ().get ( "workspace", base_name )

    if not os.path.exists ( output_dir ) :
      os.makedirs ( output_dir )
      Logger ().info ( f"Directorio de salida creado: {output_dir}" )

    frame_svg_path = State ().get ( "frame" )
    if frame_svg_path :
      qr_svg_path = State ().get ( "current_file", base_name )
      info = Utils ().fileInfo ( qr_svg_path )
      output_svg_path = os.path.join ( output_dir, info [ "name" ] + "_frame.svg" )
      Utils ().svgIntoFrame ( frame_svg_path, qr_svg_path, output_svg_path )
      State ().set_current_file ( output_svg_path )
      State ().add_step ( "Frame::embed" )
      State ().add_generated_file ( output_svg_path )
      State ().save ()

    else :
      Logger ().error ( "Imposible incrustar código QR en marco institucional." )
