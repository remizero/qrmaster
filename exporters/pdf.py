import os

from core.config import Config
from core.logger import Logger
from core.state  import State
from utils.utils import log_step, Utils


class PDF :
  """
  Handles the export of QR code-related information into a PDF format.
  Provides a method for exporting the final QR code and its associated content to a PDF file.
  """


  @log_step ( "PDF::export" )
  def export ( self ) :
    """
    Exports the generated QR code and associated content to a PDF file.

    This method takes the QR code and any additional content (like logo, frame, and information)
    and arranges them into a professionally formatted PDF file, which can then be saved to the
    specified output location.
    """
    project   = Config ().get ( "project" )
    configPdf = project.get ( "pdf", {} )

    output = project.get ( "output", {} )
    base_name = project.get ( "name", "qr" )
    # params = output.get ( "params", {} )
    output_dir = State ().get ( "workspace", base_name )

    if not os.path.exists ( output_dir ) :
      os.makedirs ( output_dir )
      Logger ().info ( f"Directorio de salida creado: {output_dir}" )

    current_file = State ().get ( "current_file", base_name )
    outputFile = os.path.join ( output_dir, f"{base_name}.pdf" )

    try :
      Utils ().createPdf ( configPdf, current_file, outputFile )
      Logger ().success ( f"Archivo PDF generado: {outputFile}" )

      # Actualizar el estado del sistema
      State ().set_pdf ( outputFile )
      State ().add_step ( "PDF::export" )
      State ().save ()

    except Exception as e :
      Logger ().error ( f"PDF export failed: {e}" )
      State ().add_error ( f"PDF export failed: {e}" )
      State ().save ()
      raise



