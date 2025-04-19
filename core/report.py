import cairosvg
import tempfile
import os
import segno
from datetime         import datetime
from fpdf             import FPDF
from PIL              import Image

from core.config      import Config
from core.logger      import Logger
from core.qrmasterpdf import QrMasterPdf
from core.state       import State
from utils.utils      import log_step


class Report :
  """
  Generates a technical report for the QR code project, including sections such as title, description,
  and various other detailed sections about the QR code, the generated files, and additional metadata.

  The report is exported to a PDF format, providing a structured and well-organized output.
  """


  def __init__ ( self ) :
    """
    Initializes the Report class, setting up necessary configurations for the report generation.
    """
    self.project = Config ().get ( "project" )
    self.reportConfig = self.project.get ( "report" )
    self.pdf = QrMasterPdf ()

    # Main Title
    title_conf  = self.reportConfig.get ( "title", {} )
    self.title_font  = title_conf.get ( "font", "Arial" )
    self.title_size  = title_conf.get ( "size", 24 )
    self.title_style = title_conf.get ( "style", "B" )

    # Subtitle
    subtitle_conf  = self.reportConfig.get ( "subtitle", {} )
    self.subtitle_font  = subtitle_conf.get ( "font", "Arial" )
    self.subtitle_size  = subtitle_conf.get ( "size", 16 )
    self.subtitle_style = subtitle_conf.get ( "style", "B" )

    # Paragraph
    paragraph_conf  = self.reportConfig.get ( "paragraph", {} )
    self.paragraph_font  = paragraph_conf.get ( "font", "Arial" )
    self.paragraph_size  = paragraph_conf.get ( "size", 12 )
    self.paragraph_style = paragraph_conf.get ( "style", "" )

    self.identation = "        "
    # Creamos una lista de enlaces para más adelante
    self.section_links = []

    # metadata_conf = self.reportConfig.get ( "title", {} )
    # self.pdf.set_title    ( metadata_conf.get ( "title" ) )
    # self.pdf.set_subject  ( metadata_conf.get ( "subject" ) )
    # self.pdf.set_keywords ( metadata_conf.get ( "keywords" ) )
    # self.pdf.set_author   ( metadata_conf.get ( "author" ) )
    # self.pdf.set_creator  ( metadata_conf.get ( "creator" ) )


  @log_step ( "Report::generate" )
  def generate ( self ) :
    """
    Generates the complete technical report in PDF format, including all the sections defined
    in the project configuration. Each section is added in a structured manner, and the report
    is saved to the specified output path.

    The sections included depend on the project's configuration and can be dynamically adjusted.
    """

    self.pdf.add_page ()
    self.pdf.set_y ( 14 )

    especiales = {
      "addDate": {"pre": 0, "post": 2},
      "addTitle": {"pre": 0, "post": 20},
      "addDescription": {"pre": 0, "post": 5},
      "addIndex": {"pre": 10, "post": 5},
    }

    for seccion in [ "addDate", "addTitle", "addDescription", "addIndex" ] :
      if self.sectionToInclude ( seccion ) :
        self.pdf.ln ( especiales [ seccion ] [ "pre" ] )
        getattr ( self, seccion ) ()
        self.pdf.ln ( especiales [ seccion ] [ "post" ] )

    sections = [
      # ( "addDate", lambda: self.project.get ( "report", {} ).get ( "include_date", False ) ),
      # ( "addTitle", lambda: True ),
      # ( "addDescription", lambda: True ),
      # ( "addIndex", lambda: True ),
      ( "addSection_1", lambda: "content" in self.project ),
      ( "addSection_2", lambda: State ().get ( "generated_files" ) != [] ),
      ( "addSection_3", lambda: "output" in self.project ),
      ( "addSection_4", lambda: "logo" in self.project and self.project [ "logo" ].get ( "path" ) ),
      ( "addSection_5", lambda: "frame" in self.project and self.project [ "frame" ] ),
      ( "addSection_6", lambda: os.path.exists ( State ().get ( "current_file", "" ) ) ),
      ( "addSection_7", lambda: State ().get ( "generated_files" ) != [] ),
      ( "addSection_8", lambda: True )
    ]

    for method_name, condition in sections :
      if condition () :
        self.pdf.ln ( 10 )
        getattr ( self, method_name ) ()
        self.pdf.ln ( 5 )

    # --------------------------------------------------------------------------
    # Guardar el PDF
    # output_name = project.get ( "pdf", {} ).get ( "output_name", f"{project.get ( 'name', 'qr' )}_informe.pdf" )
    output_name = "Technical_Report_1.pdf"
    base_name = self.project.get ( 'name', 'Sin nombre' )
    output_path = State ().get ( "workspace", base_name )
    self.pdf.output ( os.path.join ( output_path, output_name ) )
    Logger ().success ( f"Informe técnico generado: {output_name}" )

    # State ().set_current_file ( output_name )
    # State ().add_step ( "Report::generate" )
    # State ().save ()


  def sectionToInclude ( self, method_name : str ) -> bool :
    """
    Determines if a specific section should be included in the report based on the method name.

    Args:
        method_name (str): The name of the method corresponding to the section.

    Returns:
        bool: True if the section should be included, False otherwise.
    """
    project = self.project or {}
    # state = self.state

    # Reglas para secciones estándar
    secciones = {
      "addSection_1": lambda: "content" in project,
      "addSection_2": lambda: bool ( State ().get("generated_files")),
      "addSection_3": lambda: "output" in project,
      "addSection_4": lambda: "logo" in project and os.path.exists(project["logo"].get("path", "")),
      "addSection_5": lambda: "frame" in project and bool(project["frame"]),
      "addSection_6": lambda: State ().get("current_file") and os.path.exists(State ().get("current_file")),
      "addSection_7": lambda: bool(State ().get("generated_files")),
      "addSection_8": lambda: True
    }

    # Reglas para elementos especiales (si quieres añadir lógica condicional, puedes)
    especiales = {
      "addDate": lambda: project.get ( "report", {} ).get ( "include_date", False ),
      "addTitle": lambda: True,
      "addDescription": lambda: True,
      "addIndex": lambda: True
    }

    return secciones.get(method_name, especiales.get(method_name, lambda: False))()


  def addDate ( self ) :
    """
    Adds the current date to the report in the specified format.
    This date is typically included at the top of the report, indicating when the report was generated.
    """
    if self.reportConfig.get ( "include_date", True ) :
      date_fmt = self.reportConfig.get ( "date_format", "%d/%m/%Y" )
      fecha = datetime.now ().strftime ( date_fmt )
      self.pdf.set_font ( "Arial", "", 10 )
      self.pdf.cell ( 0, 10, f"Fecha de generación: {fecha}", ln = True, align = "R" )


  def addTitle ( self ) :
    """
    Adds the title of the report to the PDF, typically at the top of the first page.
    The title is styled according to the configuration defined in the project.
    """
    self.setTitle ()
    self.pdf.cell ( 0, 10, f"Informe técnico del proyecto Código QR.", ln = True, align = "C" )
    self.pdf.cell ( 0, 10, f"{self.project.get ( 'name', 'Sin nombre' )}", ln = True, align = "C" )


  def addDescription ( self ) :
    """
    Adds the introductory description section to the report. This section provides context for the report,
    describing the QR code project and its purpose.
    """
    self.setParagraph ()
    descripcion = (
        f"{self.identation}Este documento presenta un resumen detallado del proceso de generación de un código QR "
        "personalizado, incluyendo el tipo de contenido codificado, los parámetros gráficos aplicados, "
        "y los recursos visuales incorporados. El objetivo es proporcionar una documentación clara, "
        "técnica y visual, así como presentar los usos correctos de los archivos generados."
    )
    # Párrafo justificado
    self.pdf.multi_cell ( 0, 8, descripcion, align = "J" )


  def addIndex ( self ) :
    """
    Adds an index or table of contents to the report. This section lists the available sections of the report
    for easy navigation.
    """
    self.pdf.add_page ()
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "Contenido del documento.", ln = True )
    self.pdf.ln ()
    self.setParagraph ()
    self.pdf.multi_cell ( 0, 8, f"{self.identation}Las secciones listadas a continuación representan la información técnica y visual utilizada para la generación del producto final \"Código QR\". En cada una de las secciones se muestra información detallada de los parámetros claves para cumplir con los objetivos del proyecto.", align = "J" )
    self.pdf.ln ()
    indice = [
      "1-. Contenido del código QR.",
      "2-. Archivos generados.",
      "3-. Parámetros de construcción.",
      "4-. Logo incorporado.",
      "5-. Marco institucional.",
      "6-. Visualización del QR final.",
      "7-. Recomendaciones de uso.",
      "8-. Observaciones y comentarios."
    ]
    for item in indice :
      link = self.pdf.add_link ()
      self.section_links.append ( link )
      self.pdf.cell ( 0, 8, f"{self.identation}{item}", ln = True, link = link )


  def addSection_1 ( self ) :
    """
    Adds the first section to the report, which typically contains details about the QR code content
    and its purpose.
    """
    self.pdf.add_page ()
    self.pdf.ln ()
    # Vincular con el índice (esto enlaza desde el índice al título de la sección)
    self.pdf.set_link ( self.section_links [ 0 ] )  # Índice 0 para la sección 1
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "1. Contenido del código QR", ln = True )
    self.pdf.ln ()
    self.setParagraph ()
    self.pdf.multi_cell ( 0, 8, f"{self.identation}La información presentada a continuación representa el tipo de \"Código QR\" generado, así como tambien los datos y/o documentos a los que permite dar acceso el producto final \"Código QR\".", align = "J" )
    self.pdf.ln ()
    # Contenido dinámico del QR
    content = self.project.get ( "content", {} )
    content_type = content.get ( "type", "No definido" )
    self.pdf.multi_cell ( 0, 8, f"{self.identation}Tipo de contenido: {content_type}" )
    # Iterar los campos dentro de "data", si existen
    data = content.get ( "data", {} )
    for k, v in data.items () :
      self.pdf.multi_cell ( 0, 8, f"{self.identation}{k.capitalize ()}: {v}" )


  def addSection_2 ( self ) :
    """
    Adds the second section to the report, which includes details about the generated files
    and the output formats.
    """
    self.pdf.add_page ()
    self.pdf.ln ()
    # Vincular con el índice
    self.pdf.set_link ( self.section_links [ 1 ] )  # Índice 1 para sección 2
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "2. Archivos generados", ln = True )
    self.pdf.ln ()
    self.setParagraph ()
    self.pdf.multi_cell ( 0, 8, f"{self.identation}Los archivos listados a continuación representan los archivos finales del producto final \"Código QR\", así como también de los archivos intermedios necesarios paso a paso para completar el producto final.", align = "J" )
    self.pdf.ln ()
    # Obtener archivos del state.json
    generated_files = State ().get ( "generated_files", [] )
    if generated_files :
      for file in generated_files :
        self.pdf.multi_cell ( 0, 8, f"{self.identation}- {file}" )
    else :
      self.pdf.multi_cell ( 0, 8, f"{self.identation}No se han registrado archivos generados." )


  def addSection_3 ( self ) :
    """
    Adds the third section, which describes the parameters used to construct the QR code
    and the configuration details.
    """
    self.pdf.add_page ()
    self.pdf.ln ()
    # Vincular con el índice
    self.pdf.set_link ( self.section_links [ 2 ] )  # Sección 3
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "3. Parámetros de construcción", ln = True )
    self.pdf.ln ()
    self.setParagraph ()
    self.pdf.multi_cell ( 0, 8, f"{self.identation}Los datos mostrados a continuación representan la información utilizada para la generación de los distintos tipos de archivos de imágenes utilizados para la generación del producto final \"Código QR\".", align = "J" )
    self.pdf.ln ()
    output = self.project.get ( "output", {} )
    formats = output.get ( "formats", [] )
    params = output.get ( "params", {} )
    self.pdf.multi_cell ( 0, 8, f"{self.identation}Formatos generados: {', '.join ( formats ) if formats else 'Ninguno'}" )
    if params :
      for key, value in params.items () :
        self.pdf.multi_cell ( 0, 8, f"{self.identation}{key}: {value}" )
    else :
      self.pdf.multi_cell ( 0, 8, "No se definieron parámetros de salida." )


  def addSection_4 ( self ) :
    """
    Adds the fourth section, which includes information about the logo embedded within the QR code.
    """
    self.pdf.add_page ()
    self.pdf.ln ()
    self.pdf.set_link ( self.section_links [ 3 ] )  # Enlace del índice
    # Configuración
    MIN_IMG_HEIGHT = 30  # px, para no hacerla demasiado pequeña
    TARGET_WIDTH = 50    # Ancho deseado si hay espacio suficiente
    TOP_PADDING = 5      # Espaciado superior antes del logo
    logo_path = self.project.get ( "logo", {} ).get ( "path" )
    if logo_path and os.path.exists ( logo_path ) :
      self.setSubtitle ()
      self.pdf.cell ( 0, 10, "4. Logo incorporado", ln = True )
      self.pdf.ln ()
      self.setParagraph ()
      self.pdf.multi_cell ( 0, 8, f"{self.identation}La imagen mostrada a continuación representa el logotipo institucional del cliente. Logotipo suministrado para ser utilizado en la construcción del producto final \"Código QR\" permitiendo así personalizar el producto final siendo facilmente identificable para los usuarios del cliente y mantener en todo momento la imagen institucional del cliente.", align = "J" )
      self.pdf.ln ()
      self.pdf.ln ()
      # Obtener tamaño de imagen (en px)
      img = Image.open ( logo_path )
      img_width_px, img_height_px = img.size
      # DPI estándar para conversión: 96dpi ≈ 1in = 25.4mm
      dpi = 96
      img_width_mm = img_width_px * 25.4 / dpi
      img_height_mm = img_height_px * 25.4 / dpi
      # Escalar al TARGET_WIDTH
      scale = TARGET_WIDTH / img_width_mm
      scaled_height = img_height_mm * scale
      # Página y margen actual
      page_height = self.pdf.h - self.pdf.b_margin
      current_y = self.pdf.get_y ()
      remaining_space = page_height - current_y
      # Si no cabe, pasamos a nueva página
      if scaled_height + TOP_PADDING > remaining_space :
        self.pdf.add_page ()
        current_y = self.pdf.get_y ()  # actualizar posición después de nueva página
      # Centrar horizontalmente
      x_pos = ( self.pdf.w - TARGET_WIDTH ) / 2
      # Evitar que sea demasiado pequeña
      if scaled_height < MIN_IMG_HEIGHT:
        scaled_height = MIN_IMG_HEIGHT
        TARGET_WIDTH = img_width_mm * ( MIN_IMG_HEIGHT / img_height_mm )
        x_pos = ( self.pdf.w - TARGET_WIDTH ) / 2
      self.pdf.ln ( TOP_PADDING )
      self.pdf.image ( logo_path, x = x_pos, w = TARGET_WIDTH )
      self.pdf.ln ( scaled_height + 5 )
    else :
      self.setParagraph ()
      self.pdf.multi_cell ( 0, 8, "No se incorporó ningún logo al diseño." )


  def addSection_5 ( self ) :
    """
    Adds the fifth section, which provides details about the institutional frame around the QR code.
    This may include branding or custom frame elements.
    """
    self.pdf.add_page ()
    self.pdf.ln ()
    self.pdf.set_link ( self.section_links [ 4 ] )
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "5. Marco institucional", ln = True )
    self.pdf.ln ()
    self.setParagraph ()
    self.pdf.multi_cell ( 0, 8, f"{self.identation}La imagen mostrada a continuación representa el logotipo institucional del cliente. Logotipo suministrado para ser utilizado en la construcción del producto final \"Código QR\" permitiendo así personalizar el producto final siendo facilmente identificable para los usuarios del cliente y mantener en todo momento la imagen institucional del cliente.", align = "J" )
    self.pdf.ln ()
    # Contenido textual
    frame = self.project.get ( "frame", {})
    self.setParagraph ()
    if frame :
      for k, v in frame.items () :
        label = k.replace ( "_", " " ).capitalize ()
        self.pdf.set_font ( family = self.paragraph_font, style = 'B', size = self.paragraph_size )  # Negrita
        text_width = self.pdf.get_string_width ( f"{self.identation}{label}: " )
        self.pdf.cell ( text_width + 5, 8, f"{self.identation}{label}: ", ln = False )
        self.setParagraph ()
        self.pdf.cell ( 0, 8, f"{v}", ln = True, align = "L" )
    else :
      self.pdf.multi_cell ( 0, 8, "No se definió información institucional en el proyecto." )
    self.pdf.ln ()
    self.setParagraph ()
    self.pdf.cell ( 0, 10, f"{self.identation}Visualización del marco institucional generado:", ln = True )
    # Obtener ruta del marco institucional
    generated = State ().get ( "generated_files", [] )
    project_name = self.project.get ( "name", "" ).replace ( " ", "_" )
    frame_path = None
    for f in generated :
      if f.endswith ( "_frame.svg" ) and project_name in os.path.basename ( f ) :
        frame_path = f
        break
    # Verificar si existe el archivo y procesarlo
    if frame_path and os.path.exists ( frame_path ) :
      # Convertir SVG a PNG temporal (ya que fpdf no soporta SVG directamente)
      with tempfile.NamedTemporaryFile ( suffix = ".png", delete = False ) as tmp_img :
        cairosvg.svg2png ( url = frame_path, write_to = tmp_img.name )
        temp_png = tmp_img.name
      # Cálculo y ajuste de espacio
      page_width = self.pdf.w - 2 * self.pdf.l_margin
      y_space = self.pdf.h - self.pdf.get_y () - self.pdf.b_margin
      img_width = page_width * 0.8  # Usamos el 80% del ancho de la página
      # Abrir imagen para obtener dimensiones
      img = Image.open ( temp_png )
      img_height = img.height * ( img_width / img.width )
      # Verificar si la imagen cabe en el espacio disponible
      if img_height > y_space :
        self.pdf.add_page ()  # Si no cabe, agregamos una nueva página
      # Asegurarnos de que la imagen no es demasiado pequeña
      min_img_height = 30  # Altura mínima visible para la imagen (puedes ajustarlo)
      if img_height < min_img_height :
        img_height = min_img_height
        img_width = img.width * ( img_height / img.height )
      # Insertar imagen escalada en la página
      self.pdf.image ( temp_png, x = self.pdf.l_margin + ( page_width - img_width ) / 2, w = img_width )
      self.pdf.ln ( 10 )
      # Eliminar imagen temporal para limpiar el sistema
      os.remove ( temp_png )
    else :
      self.setParagraph ()
      self.pdf.multi_cell ( 0, 8, "No se encontró un marco institucional generado para mostrar." )


  def addSection_6 ( self ) :
    """
    Adds the sixth section, which shows the final visualization of the QR code generated.
    This is where the actual QR code image is displayed.
    """
    self.pdf.add_page ()
    self.pdf.set_link ( self.section_links [ 5 ] )  # Enlace desde el índice
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "6. Visualización del código QR final", ln = True )
    # Obtener ruta de la imagen del código QR
    image_path = State ().get ( "current_file" )
    # Verificar si la imagen existe
    if image_path and os.path.exists ( image_path ) :
      # Obtener parámetros de configuración para la imagen
      x = self.project [ "pdf" ].get ( "image_x", 5 )
      y = self.project [ "pdf" ].get ( "image_y", self.pdf.get_y () )
      w = self.project [ "pdf" ].get ( "image_width", 200 )
      # Ajustar el desplazamiento vertical
      y_offset = 15  # Ajuste para mover la imagen hacia arriba
      # Cálculo y ajuste de espacio
      page_width = self.pdf.w - 2 * self.pdf.l_margin
      y_space = self.pdf.h - self.pdf.get_y () - self.pdf.b_margin
      img_width = w  # Usamos el ancho especificado
      # Abrir imagen para obtener dimensiones
      img = Image.open ( image_path )
      img_height = img.height * ( img_width / img.width )
      # Verificar si la imagen cabe en el espacio disponible
      if img_height > y_space :
        self.pdf.add_page ()  # Si no cabe, agregamos una nueva página
      # Asegurarnos de que la imagen no es demasiado pequeña
      min_img_height = 30  # Altura mínima visible para la imagen (puedes ajustarlo)
      if img_height < min_img_height :
        img_height = min_img_height
        img_width = img.width * ( img_height / img.height )
      # Insertar imagen escalada en la página
      self.pdf.image ( image_path, x = x, y = y - y_offset, w = img_width )
      text_y = y - y_offset + img_height + 5
      self.pdf.set_y ( text_y )
      self.pdf.ln ()
    else :
      self.setParagraph ()
      self.pdf.multi_cell ( 0, 8, "No se encontró un código QR generado para mostrar." )


  def addSection_7 ( self ) :
    """
    Adds the seventh section, which offers recommendations on how to use the QR code.
    This could include security, accessibility, or functional tips for the user.
    """
    self.pdf.add_page ()
    self.pdf.set_link ( self.section_links [ 6 ] )  # Enlace desde el índice
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "7. Recomendaciones de uso", ln = True )
    # Obtener la lista de archivos generados
    generated_files = State ().get ( "generated_files", [] )
    # Si hay archivos generados, proceder con la sección
    if generated_files :
      # Iterar sobre los archivos generados
      for file in generated_files :
        # Agregar subsección para cada archivo
        self.setParagraph ()
        self.pdf.ln ()
        text_width = self.pdf.get_string_width ( f"{self.identation}Recomendaciones para el archivo: " )
        self.pdf.cell ( text_width, 10, f"{self.identation}Recomendaciones para el archivo: ", ln = False )
        self.pdf.set_font ( family = self.paragraph_font, style = 'B', size = self.paragraph_size )  # Negrita
        self.pdf.cell ( 0, 10, f"{os.path.basename ( file )}", ln = True )
        self.setParagraph ()
        if file.endswith ( ".svg" ) :
          self.pdf.multi_cell ( 0, 8, f"{self.identation}{self.identation}- El archivo {os.path.basename ( file )} es un SVG, que puede ser utilizado en aplicaciones web o impresiones de alta calidad." )
          self.pdf.multi_cell ( 0, 8, f"{self.identation}{self.identation}- Asegúrese de que el diseño del SVG no se distorsione al cambiar de tamaño. Idealmente, debe ser escalado sin pérdida de calidad." )
        elif file.endswith ( ".png" ) :
          self.pdf.multi_cell ( 0, 8, f"{self.identation}{self.identation}- El archivo {os.path.basename ( file )} es una imagen PNG, adecuada para su uso en plataformas digitales." )
          self.pdf.multi_cell ( 0, 8, f"{self.identation}{self.identation}- Mantenga la resolución de la imagen para asegurar que no pierda calidad al ser redimensionada." )
        elif file.endswith ( ".pdf" ) :
          self.pdf.multi_cell ( 0, 8, f"{self.identation}{self.identation}- El archivo {os.path.basename ( file )} es un archivo PDF, que puede ser utilizado para impresión." )
          self.pdf.multi_cell ( 0, 8, f"{self.identation}{self.identation}- Asegúrese de que el archivo esté bien formateado y sin errores antes de enviarlo a la imprenta." )
        else :
          self.pdf.multi_cell ( 0, 8, f"{self.identation}{self.identation}- El archivo {os.path.basename ( file )} es un archivo generado. Consulte la documentación para más detalles sobre cómo utilizarlo." )
        self.pdf.ln ( 5 )
    else :
      self.setParagraph ()
      self.pdf.multi_cell ( 0, 8, "No se han generado archivos que requieran recomendaciones específicas." )


  def addSection_8 ( self ) :
    """
    Adds the eighth and final section, which includes any final observations or additional notes
    regarding the project or the QR code generation process.
    """
    self.pdf.add_page ()
    self.pdf.set_link ( self.section_links [ 7 ] )  # Enlace desde el índice
    self.setSubtitle ()
    self.pdf.cell ( 0, 10, "7. Observaciones y comentarios", ln = True )
    self.setParagraph ()
    self.pdf.multi_cell ( 0, 10, f"{self.identation}Este informe detalla la generación de un código QR con parámetros personalizados, incluyendo el contenido codificado, el diseño gráfico institucional, y la inclusión de recursos visuales como logotipos. El objetivo es ofrecer una entrega profesional y reutilizable." )


  def setTitle ( self ) :
    """
    Sets the title formatting and content for the report, applying the configuration specified
    in the project's settings.
    """
    self.pdf.set_font ( self.title_font, self.title_style, self.title_size )


  def setSubtitle ( self ) :
    """
    Sets the subtitle formatting and content for the report, based on the configuration.
    """
    self.pdf.set_font ( self.subtitle_font, self.subtitle_style, self.subtitle_size )


  def setParagraph ( self ) :
    """
    Sets the paragraph formatting for the report, applying the font and style defined
    in the configuration for the general content of the report.
    """
    self.pdf.set_font ( self.paragraph_font, self.paragraph_style, self.paragraph_size )
