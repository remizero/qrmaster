import os
from datetime    import datetime
from fpdf        import FPDF

from core.config import Config
from core.logger import Logger
from core.state  import State
from utils.utils import log_step


class QrMasterPdf ( FPDF ) :
  """
  The QrMasterPdf class is a subclass of FPDF that provides custom header and footer functionality
  for generating a QR code-related PDF report. It allows for easy customization of the PDF's header
  and footer sections, specifically tailored for QR code projects.

  Inherits from the FPDF class to leverage basic PDF generation features while adding custom content.
  """


  def header ( self ) :
    """
    Defines the header content for the PDF document.

    This method is called automatically when a new page is added. It can be used to add custom
    header elements such as logos, titles, or page numbers at the top of the PDF.
    This implementation can be customized as needed for the QR code project.
    """
    project = Config ().get ( "project" )
    pdf_config = project.get ( "report", {} )
    logo_path = pdf_config.get ( "header", {} ).get ( "company_logo", "" )
    company_name = pdf_config.get ( "company_name", "Mi Empresa" )
    header_color = pdf_config.get ( "color", ( 50, 50, 50 ) )  # RGB

    self.set_fill_color ( *header_color )
    self.rect ( 0, 0, self.w, 15, 'F' )  # Barra horizontal

    # Logo a la izquierda
    if logo_path and os.path.exists ( logo_path ) :
      self.image ( logo_path, x = 10, y = 2, h = 10 )

    # Nombre empresa centrado
    self.set_text_color ( 255, 255, 255 )
    self.set_font ( "Arial", "B", 12 )
    self.set_y ( 5 )
    self.cell ( 0, 5, company_name, align = "C", ln = False )

    self.set_y ( 20 )


  def footer ( self ) :
    """
    Defines the footer content for the PDF document.

    This method is called automatically when a new page is added. It can be used to add custom
    footer elements such as page numbers or other information at the bottom of the PDF.
    The footer is displayed on every page unless overridden.
    """
    project = Config ().get ( "project" )
    pdf_config = project.get ( "report", {} )
    footer_color = pdf_config.get ( "color", ( 50, 50, 50 ) )
    contact = pdf_config.get ( "contact", "contacto@empresa.com" )
    website = pdf_config.get ( "website", "http:://www.empresa.com" )
    # redes = pdf_config.get ( "social", "@empresa" )

    self.set_y ( -15 )
    self.set_fill_color ( *footer_color )
    self.rect ( 0, self.h - 15, self.w, 15, 'F' )  # Pie de página

    self.set_text_color ( 255, 255, 255 )
    self.set_font ( "Arial", "I", 8 )

    self.cell ( 0, 5, f"© {datetime.now ().year} {project.get ( 'name', '' )} - Todos los derechos reservados", ln = True, align = "C" )
    self.cell ( 0, 5, f"Contacto: {contact} | Website: {website}", ln = False, align = "C" )
