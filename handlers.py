# handlers.py
import os
from fpdf import FPDF
from datetime import datetime
from core import (
  generateQr,
  createSvg,
  pngToSvg,
  addLogo,
  createFrame,
  svgIntoSvg,
  createPng,
  createPdf
)
from context import set_main_output_file, get_main_output_file


##
# @brief Crea un informe técnico profesional en PDF.
#
# @param json_data Diccionario con todos los datos del proyecto.
# @param output_path Ruta para guardar el PDF.
#
def create_technical_report ( json_data : dict, output_path : str ) :

  project = json_data.get ( "project", {} )
  pdf = FPDF ()
  pdf.add_page ()

  # Título principal
  pdf.set_font ( "Arial", "B", 18 )
  pdf.cell ( 0, 10, f"Informe técnico del proyecto QR: {project.get('name', 'Sin nombre')}", ln = True, align = "C" )

  # Fecha
  if project.get ( "pdf", {} ).get ( "include_date", True ) :

    date_fmt = project [ "pdf" ].get ( "date_format", "%d/%m/%Y" )
    fecha = datetime.now ().strftime ( date_fmt )
    pdf.set_font ( "Arial", "", 10 )
    pdf.cell ( 0, 10, f"Fecha de generación: {fecha}", ln = True, align = "C" )

  pdf.ln ( 10 )

  # Sección 1: Contenido del QR
  pdf.set_font ( "Arial", "B", 14 )
  pdf.cell ( 0, 10, "1. Contenido del código QR", ln = True )
  pdf.set_font ( "Arial", "", 12 )
  content = project.get ( "content", {} )
  pdf.multi_cell ( 0, 10, f"Tipo de contenido: {content.get ( 'type', 'No definido' )}" )
  for k, v in content.items () :

    if k != "type" :

      pdf.multi_cell ( 0, 10, f"{k.capitalize ()}: {v}" )

  pdf.ln ( 5 )

  # Sección 2: Parámetros de salida
  pdf.set_font ( "Arial", "B", 14 )
  pdf.cell ( 0, 10, "2. Parámetros de salida", ln = True )
  pdf.set_font ( "Arial", "", 12 )
  output = project.get ( "output", {} )
  formats = output.get ( "formats", [] )
  params = output.get ( "params", {} )
  pdf.cell ( 0, 10, f"Formatos generados: {', '.join ( formats )}", ln = True )
  for key, value in params.items () :

    pdf.cell ( 0, 10, f"{key}: {value}", ln = True )

  pdf.ln ( 5 )

  # Sección 3: Logo
  logo = project.get ( "logo", {}).get ( "path" )
  if logo and os.path.exists ( logo ) :

    pdf.set_font ( "Arial", "B", 14)
    pdf.cell ( 0, 10, "3. Logo incorporado", ln = True )
    pdf.image ( logo, x = 80, w = 50 )
    pdf.ln ( 55 )

  # Sección 4: Marco institucional
  pdf.set_font ( "Arial", "B", 14 )
  pdf.cell ( 0, 10, "4. Frame Institucional", ln = True )
  frame = project.get ( "frame", {} )
  pdf.set_font ( "Arial", "", 12 )
  for k, v in frame.items () :

    pdf.cell ( 0, 10, f"{k.replace ( '_', ' ' ).capitalize ()}: {v}", ln = True )

  pdf.ln ( 5 )

  # Sección 5: Visualización del QR final
  pdf.set_font ( "Arial", "B", 14 )
  pdf.cell ( 0, 10, "5. Visualización del código QR final", ln = True )
  image_path = project.get ( "pdf", {} ).get ( "image_path" )
  if image_path and os.path.exists ( image_path ) :

    x = project [ "pdf" ].get ( "image_x", 5 )
    y = project [ "pdf" ].get ( "image_y", pdf.get_y () )
    w = project [ "pdf" ].get ( "image_width", 200 )
    pdf.image ( image_path, x = x, y = y, w = w )
    pdf.ln ( 60 )

  # Sección 6: Observaciones finales
  pdf.set_font ( "Arial", "B", 14 )
  pdf.cell ( 0, 10, "6. Observaciones y comentarios", ln = True )
  pdf.set_font ( "Arial", "", 12 )
  pdf.multi_cell ( 0, 10, "Este informe detalla la generación de un código QR con parámetros personalizados, incluyendo el contenido codificado, el diseño gráfico institucional, y la inclusión de recursos visuales como logotipos. El objetivo es ofrecer una entrega profesional y reutilizable." )

  # Guardar el PDF
  # output_name = project.get ( "pdf", {} ).get ( "output_name", f"{project.get ( 'name', 'qr' )}_informe.pdf" )
  output_name = "Technical_Report.pdf"
  pdf.output ( os.path.join ( output_path, output_name ) )
  print ( f"Informe técnico generado: {output_name}" )


##
# @brief Procesa el apartado de arte (no implementado actualmente).
#
# @param config Configuración del proyecto.
# @param path_project Ruta del proyecto.
#
def handle_art ( config, path_project ) :
    print ( "🎭 Aplicando estilo artístico..." )
    # apply_artistic_style(path_project)


##
# @brief Crea el marco institucional para el QR.
#
# @param config Configuración del marco.
# @param path_project Ruta del proyecto.
#
def handle_frame ( config, path_project ) :

  name = config.get ( "name", None )
  frame = config.get ( "frame", {} )
  createFrame ( qr_logo_svg_path = f"{path_project}/{name}_qr_logo.svg", output_path = f"{path_project}/{name}_marco_institucional.svg", config = frame )
  svgIntoSvg ( frame_svg_path = f"{path_project}/{name}_marco_institucional.svg", qr_svg_path = f"{path_project}/{name}_qr_logo.svg", output_svg_path = f"{path_project}/{name}_qr_logo_institucional_full.svg" )
  print ( "🖼️ Agregando marco decorativo..." )


##
# @brief Procesa el logo para incrustarlo en el QR.
#
# @param config Configuración del logo.
# @param path_project Ruta del proyecto.
#
def handle_logo ( config, path_project ) :

  name = config.get ( "name", None )
  logo = config.get ( "logo", {} )
  path = logo.get ( "path", "" )
  if not path :

    raise ValueError("❌ El campo 'path' en el nodo 'logo' es obligatorio.")

  fileName = f"{path_project}/{name}_logo.svg"
  pngToSvg ( image_path = path, output_path = fileName )
  addLogo ( qr_svg_path = f"{path_project}/{name}_qr.svg", logo_svg_path = fileName, output_svg_path = f"{path_project}/{name}_qr_logo.svg" )
  print ( "🎨 Insertando logo en el QR..." )


##
# @brief Genera los archivos de salida adicionales definidos en "output".
#
# @param qr Objeto QR.
# @param config Configuración del output.
# @param path_project Ruta del proyecto.
# @param base_filename Nombre base para los archivos.
#
def handle_output ( qr, config, path_project, base_filename = 'qr' ) :

  if not config :
    print ( "⚠️ No se especificó bloque 'output'. No se guardará el QR." )
    return

  formats = config.get ( "formats", [] )
  params = config.get ( "params", {} )

  for fmt in formats :

    fmt = fmt.lower ()
    if fmt in ( "svg", "pdf", "png" ) :

      print ( f"⚠️ Formato '{fmt}' no soportado directamente por esta función. Será ignorado." )
      continue

    else :

      filename = f"{base_filename}.{fmt}"
      filepath = os.path.join ( path_project, filename )

      try :

        qr.save ( filepath, kind = fmt, **params )
        print ( f"✅ QR exportado como: {filepath}" )

      except Exception as e :

        print ( f"❌ Error al guardar {fmt}: {e}" )


##
# @brief Genera un PDF imprimible con el QR final.
#
# @param config Configuración del PDF.
# @param path_project Ruta del proyecto.
#
def handle_pdf ( config, path_project ) :

  createPdf ( config.get ( "name", "" ).strip (), config.get ( "pdf" ), path_project, nombre_doc = "" )
  print ( "📄 Generando PDF con QR..." )


##
# @brief Genera una imagen PNG desde el SVG del QR.
#
# @param config Configuración de imagen.
# @param path_project Ruta del proyecto.
#
def handle_png ( config, path_project ) :

  name = config.get ( "name", None )
  createPng ( input_svg_path = f"{path_project}/{name}_qr_logo_institucional_full.svg", output_png_path = f"{path_project}/{name}_qr_logo_institucional_full.png" )
  print ( "🖼️ Exportando como PNG..." )


##
# @brief Crea el objeto QR a partir del contenido.
#
# @param config Configuración del proyecto.
# @return Objeto QR generado.
#
def handle_qr ( config ) :

  return generateQr ( config )


##
# @brief Exporta el objeto QR como archivo SVG.
#
# @param qr Objeto QR.
# @param config Configuración del proyecto.
# @param path_project Ruta del proyecto.def handle_svg(qr, config, path_project):    pass
#
def handle_svg ( qr, config, path_project ) :

  name = config.get ( "name", None )
  fileName = f"{path_project}/{name}_qr.svg"
  output = config.get ( "output", {} )
  kw = output.get ( "params", {} )
  createSvg ( qr, fileName, kw )
