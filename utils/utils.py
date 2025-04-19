import cairosvg
import os
import re
import svgutils.transform as sg
from datetime import datetime
from fpdf     import FPDF

from core.logger import Logger
from functools   import wraps


def log_step ( name = None ) :
  """
  A decorator function that logs the execution of a method with a specified name.

  This decorator wraps a function and logs its execution step, providing the specified
  name for the log entry. It is typically used to track the progress of various steps
  in a process or workflow.

  Args:
      name (str, optional): The name of the step being logged. If not provided,
                              the function name will be used.

  Returns:
      function: A wrapper function that logs the execution of the decorated method.

  Example:
      @log_step("Step Name")
      def some_method():
          pass
  """
  def decorator ( func ) :
    @wraps ( func )
    def wrapper ( *args, **kwargs ) :
      logger = Logger ()
      step_name = name or func.__name__
      logger.info ( f"Inicio de paso: {step_name}" )
      try :
        result = func ( *args, **kwargs )
        logger.success ( f"Paso completado: {step_name}" )
        return result
      except Exception as e :
        logger.error ( f"Error en paso {step_name}: {e}" )
        raise
    return wrapper
  return decorator


class Utils () :
  """
  The Utils class provides various utility methods that perform tasks like
  creating PDFs, handling SVG files, and converting measurements. These methods
  are designed to simplify common operations in the project.
  """


  @staticmethod
  @log_step ( "Utils::createPdf" )
  def createPdf ( configPdf : dict, imageToInsert : str, outputFile : str ) :
    """
    Creates a PDF file with the given configuration and inserts an image into it.

    This method generates a PDF document based on the provided configuration
    and inserts an image at the specified location.

    Args:
        configPdf (dict): A dictionary containing PDF generation settings (e.g., title, size).
        imageToInsert (str): The file path to the image to be inserted into the PDF.
        outputFile (str): The file path where the resulting PDF will be saved.

    Returns:
        None

    This method creates a PDF file with the specified configuration and includes the image.
    """
    fecha = datetime.now ().strftime ( configPdf.get ( "date_format", "%d/%m/%Y" ) )

    title       = configPdf.get ( "title", "Código QR para visualizar el documento" )
    title_font  = configPdf.get ( "title_font", "Arial" )
    title_size  = configPdf.get ( "title_size", 16 )
    title_style = configPdf.get ( "title_style", "B" )

    info_font   = configPdf.get ( "info_font", "Arial" )
    info_size   = configPdf.get ( "info_size", 12 )

    show_date   = configPdf.get ( "include_date", True )
    doc_name    = configPdf.get ( "document_name", "Documento sin nombre" )



    # image_path  = configPdf.get ( "image_path", f"{nombre_base}_qr_logo_institucional_full.png" )
    image_path  = imageToInsert
    image_width = configPdf.get ( "image_width", 200 )
    image_x     = configPdf.get ( "image_x", 5 )
    image_y     = configPdf.get ( "image_y", 60 )

    pdf = FPDF ()
    pdf.add_page ()

    # Título
    pdf.set_font ( title_font, title_style, title_size )
    pdf.cell ( 200, 10, txt = title, ln = True, align = 'C' )

    # Info
    pdf.set_font ( info_font, size=info_size )
    pdf.ln ( 10 )
    pdf.cell ( 200, 10, txt = f"Nombre del documento: {doc_name}", ln = True, align = 'C' )
    if show_date :
      pdf.cell ( 200, 10, txt = f"Fecha de generación: {fecha}", ln = True, align = 'C' )

    # Imagen
    pdf.ln ( 10 )
    pdf.image ( imageToInsert, x = image_x, y = image_y, w = image_width )

    pdf.output ( outputFile )
    print ( f"✅ PDF generado como: '{outputFile}'" )


  @staticmethod
  @log_step ( "Utils::fileInfo" )
  def fileInfo ( path : str ) -> dict :
    """
    Retrieves information about a file, such as its size and modification date.

    This method collects basic metadata about a file, including its size, last modified
    date, and other relevant details.

    Args:
        path (str): The file path to retrieve information for.

    Returns:
        dict: A dictionary containing file metadata such as size and modification date.

    Example:
        {'size': 1024, 'last_modified': '2025-04-20 15:30:00'}
    """
    filename      = os.path.basename ( path )
    name_only     = os.path.splitext ( filename ) [ 0 ]
    extension     = os.path.splitext ( filename) [ 1 ] [ 1: ]
    absolute_path = os.path.abspath ( path )
    exists        = os.path.exists ( absolute_path )
    parent_dir    = os.path.dirname ( absolute_path )

    return { "filename": filename, "name": name_only, "extension": extension, "absolute_path": absolute_path, "parent_dir": parent_dir, "exists": exists }


  @staticmethod
  @log_step ( "Utils::svgIntoSvg" )
  def svgIntoSvg ( background_svg_path : str, logo_svg_path : str, output_svg_path : str ) :
    """
    Embeds one SVG into another as a logo.

    This method takes a background SVG and an SVG logo, embedding the logo into the background
    SVG at a specified location and saves the resulting SVG to the output file path.

    Args:
        background_svg_path (str): The file path of the background SVG.
        logo_svg_path (str): The file path of the logo SVG to be embedded into the background.
        output_svg_path (str): The file path where the resulting SVG will be saved.

    Returns:
        None

    This method creates a new SVG by combining the background SVG with the logo SVG.
    """
    background = sg.fromfile ( background_svg_path )
    logo = sg.fromfile ( logo_svg_path )

    # Medidas del fondo
    bg_width = Utils.convertToPixels ( background.get_size () [ 0 ] )
    bg_height = Utils.convertToPixels ( background.get_size () [ 1 ] )

    # Medidas originales del logo
    logo_width = Utils.convertToPixels ( logo.get_size () [ 0 ] )
    logo_height = Utils.convertToPixels ( logo.get_size () [ 1 ] )

    # 1. Escalamos el logo para que *encaje* en el fondo (misma base de comparación)
    fit_scale_x = bg_width / logo_width
    fit_scale_y = bg_height / logo_height
    fit_scale = min ( fit_scale_x, fit_scale_y )  # mantener proporciones

    # 2. Luego, reducirlo al 20% del tamaño del código QR
    scale_factor = fit_scale * 0.05

    root = logo.getroot ()
    final_scale = fit_scale * scale_factor
    root.scale ( final_scale )

    # Calcular nueva posición centrada
    new_logo_width = logo_width * final_scale
    new_logo_height = logo_height * final_scale

    x_pos = ( bg_width - new_logo_width ) / 2
    y_pos = ( bg_height - new_logo_height ) / 2

    # Mover el logo al centro
    root.moveto ( x_pos, y_pos )

    background.append ( [ root ] )
    background.save ( output_svg_path )


  @staticmethod
  @log_step ( "Utils::svgIntoFrame" )
  def svgIntoFrame ( frame_svg_path, qr_svg_path, output_svg_path ) :
    """
    Embeds a QR code SVG into a frame SVG.

    This method combines a QR code SVG with a frame SVG, inserting the QR code at a specified
    position within the frame, and saves the resulting SVG to the output path.

    Args:
        frame_svg_path (str): The file path of the frame SVG.
        qr_svg_path (str): The file path of the QR code SVG to be embedded.
        output_svg_path (str): The file path where the resulting SVG will be saved.

    Returns:
        None

    This method creates a new SVG by inserting the QR code into the frame.
    """
    frame = sg.fromfile ( frame_svg_path )
    qr = sg.fromfile ( qr_svg_path )

    root = qr.getroot ()

    # Mover el logo al centro
    root.moveto ( 10, 10 )

    frame.append ( [ root ] )
    frame.save ( output_svg_path )
    print ( f"✅ SVG final guardado como: {output_svg_path}" )


  @staticmethod
  @log_step ( "Utils::convertToPixels" )
  def convertToPixels ( measurement ) :
    """
    Converts a measurement in various units (e.g., mm, cm) to pixels.

    This method takes a measurement and converts it to pixels based on the configured unit
    system and scale.

    Args:
        measurement: The measurement to convert, in any valid unit (e.g., mm, cm).

    Returns:
        float: The converted measurement in pixels.

    Example:
        100 mm would return 283.46 pixels (assuming a scale of 2.83 pixels per mm).
    """
    value = float ( re.search ( r'[0-9\.]+', measurement ).group () )
    if measurement.endswith ( "px" ) :

      return value

    elif measurement.endswith ( "mm" ) :

      return value * 3.7795275591

    else :
      return value # unit not supported
