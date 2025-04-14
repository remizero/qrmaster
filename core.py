import argparse
import cairosvg
import json
import os
import re
import segno
import json
import os
import svgutils.transform as sg
import sys
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
from PIL import Image
from pixels2svg import pixels2svg
from svgwrite import Drawing
from context import set_main_output_file, get_main_output_file


##
# @brief Añade un logo SVG centrado dentro de un código QR SVG existente.
#
# @param qr_svg_path Ruta del archivo SVG del código QR.
# @param logo_svg_path Ruta del archivo SVG del logo.
# @param output_svg_path Ruta donde se guardará el SVG combinado.
#
def addLogo ( qr_svg_path, logo_svg_path, output_svg_path ) :

  background = sg.fromfile ( qr_svg_path )
  logo = sg.fromfile ( logo_svg_path )

  # Medidas del fondo
  bg_width = convertToPixels ( background.get_size () [ 0 ] )
  bg_height = convertToPixels ( background.get_size () [ 1 ] )

  # Medidas originales del logo
  logo_width = convertToPixels ( logo.get_size () [ 0 ] )
  logo_height = convertToPixels ( logo.get_size () [ 1 ] )

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
  print ( "Se ha agregado el logo al código QR exitosamente." )


##
# @brief Aplica configuraciones específicas al objeto QR generado.
# @param data Datos del objeto QR.
# @param qr_settings Diccionario con configuraciones (escala, colores, etc.).
#
def AddQrSettings ( data, qr_settings ) :

  return segno.make ( data, **qr_settings )


##
# @brief Convierte una medida (str con unidad) a píxeles.
#
# @param measurement Medida con unidad (ej. "10mm", "100px").
# @return Valor numérico en píxeles.
#
def convertToPixels ( measurement ) :

  value = float ( re.search ( r'[0-9\.]+', measurement ).group () )
  if measurement.endswith ( "px" ) :

    return value

  elif measurement.endswith ( "mm" ) :

    return value * 3.7795275591

  else :
    return value # unit not supported


##
# @brief Crea un marco SVG institucional con textos y borde alrededor de un QR.
#
# @param qr_logo_svg_path Ruta del QR con logo en SVG.
# @param output_path Ruta del archivo de salida.
# @param config Diccionario de configuración del marco.
#
def createFrame ( qr_logo_svg_path, output_path, config ) :

  qr_svg = sg.fromfile(qr_logo_svg_path)
  qr_width = convertToPixels(qr_svg.get_size()[0])
  qr_height = convertToPixels(qr_svg.get_size()[1])

  # Configuración
  margin = config.get ( "margin", 10)
  text_height = config.get ( "text_height", 60)
  bg_color = config.get ( "background_color", "white")
  border_color = config.get ( "border_color", "#005baa")
  border_width = config.get ( "border_width", 4)

  title = config.get ( "title", "")
  title_font_size = config.get ( "title_font_size", 16)
  title_font_family = config.get ( "title_font_family", "Arial")
  title_color = config.get ( "title_color", border_color)

  message = config.get ( "message", "Escanea para ver el documento.")
  message_font_size = config.get ( "message_font_size", 12)
  message_color = config.get ( "message_color", "#555")

  svg_width = qr_width + 2 * margin
  svg_height = qr_height + 2 * margin + text_height

  dwg = Drawing(output_path, size=(f"{svg_width}px", f"{svg_height}px"), profile='tiny')

  dwg.add(dwg.rect(insert=(0, 0), size=(f"{svg_width}px", f"{svg_height}px"), fill=bg_color))
  dwg.add(dwg.rect(insert=(margin, margin), size=(f"{svg_width - 2 * margin}px", f"{svg_width - 2 * margin}px"),
                    fill="none", stroke=border_color, stroke_width=border_width))

  # Texto principal
  dwg.add(dwg.text(title,
                    insert=(f"{svg_width / 2}px", f"{svg_width + 30}px"),
                    text_anchor="middle",
                    font_size=f"{title_font_size}px",
                    font_family=title_font_family,
                    font_weight="bold",
                    fill=title_color))

  # Mensaje opcional
  dwg.add(dwg.text(message,
                    insert=(f"{svg_width / 2}px", f"{svg_width + 50}px"),
                    text_anchor="middle",
                    font_size=f"{message_font_size}px",
                    font_family="Arial",
                    fill=message_color))

  dwg.save()
  print(f"✅ Marco generado como: {output_path}")


##
# @brief Genera un archivo PDF con el QR final para impresión profesional.
#
# @param nombre_base Nombre base para el PDF.
# @param config Configuración visual del PDF.
# @param path_project Ruta del proyecto.
# @param nombre_doc Nombre del documento asociado al QR.
#
def createPdf ( nombre_base, config, path_project, nombre_doc = "" ) :

  fecha = datetime.now ().strftime ( config.get ( "date_format", "%d/%m/%Y" ) )
  output_name = config.get ( "output_name", f"{nombre_base}.pdf" )
  output_name = f"{path_project}/{output_name}"

  title = config.get ( "title", "Código QR para visualizar el documento" )
  title_font = config.get ( "title_font", "Arial" )
  title_size = config.get ( "title_size", 16 )
  title_style = config.get ( "title_style", "B" )

  info_font = config.get ( "info_font", "Arial" )
  info_size = config.get ( "info_size", 12 )

  show_date = config.get ( "include_date", True )
  doc_name = config.get ( "document_name", nombre_doc or "Documento sin nombre" )

  image_path = config.get ( "image_path", f"{nombre_base}_qr_logo_institucional_full.png" )
  image_width = config.get ( "image_width", 200 )
  image_x = config.get ( "image_x", 5 )
  image_y = config.get ( "image_y", 60 )

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
  pdf.image ( f"{path_project}/{nombre_base}_{image_path}", x = image_x, y = image_y, w = image_width )

  pdf.output ( output_name )
  print ( f"✅ PDF generado como: '{output_name}'" )


##
# @brief Convierte un archivo SVG a imagen PNG.
#
# @param input_svg_path Ruta del archivo SVG.
# @param output_png_path Ruta de salida para el PNG.
# @param scale Factor de escala para la conversión.
#
def createPng ( input_svg_path, output_png_path, scale = 1.0 ) :

  cairosvg.svg2png ( url = input_svg_path, write_to = output_png_path, scale = scale )
  print ( f"✅ SVG convertido a PNG: {output_png_path}" )


##
# @brief Crea el directorio del proyecto si no existe.
#
# @param projectName Nombre del proyecto.
# @return Ruta del directorio creado.
#
def createProjectDir ( projectName ) :

  path = os.path.join ( "output", projectName )
  if not os.path.exists ( path ) :

    os.makedirs ( path, exist_ok = True )
    print ( f"📁 Directorio creado: {path}" )
    return path

  else :

    print ( f"❌ Error: la carpeta '{path}' ya existe. Elige otro nombre o elimina la existente." )
    sys.exit ( 1 )


##
# @brief Crea un archivo SVG a partir del objeto QR.
#
# @param qr Objeto QR generado.
# @param fileName Nombre del archivo SVG.
# @param kw Configuraciones de exportación.
#
def createSvg ( qr, fileName, kw ) :

  qr.save ( fileName, **kw )
  print ( f"🖼️ Exportando QR a SVG como '{fileName}'." )


##
# @brief Codifica datos bancarios en formato EPC.
#
# @param content Diccionario con los campos necesarios.
# @return Cadena EPC formateada.
#
def dataEpc ( content ) :

  name = content.get ( "name" )
  iban = content.get ( "iban" )
  amount = content.get ( "amount" )
  if not all ( [ name, iban, amount ] ) :

    raise ValueError ( "❌ Los campos 'name', 'iban' y 'amount' son obligatorios para tipo 'epc'." )

  return segno.helpers.make_epc_data ( name = name, iban = iban, amount = amount, text = content.get ( "text", "" ), encoding = content.get ( "encoding", "utf-8" ) )


##
# @brief Codifica coordenadas geográficas.
#
# @param content Diccionario con latitud y longitud.
# @return Cadena geo URL.
#
def dataGeo ( content ) :

  lat = content.get ( "latitude" )
  lon = content.get ( "longitude" )
  if not lat or not lon :

    raise ValueError ( "❌ Los campos 'latitude' y 'longitude' son obligatorios para tipo 'geo'." )

  return segno.helpers.make_geo_data ( lat, lon )


##
# @brief Codifica contacto en formato MeCard.
#
# @param content Diccionario con datos del contacto.
# @return Cadena MeCard.
#
def dataMecard ( content ) :

  name = content.get ( "name" )
  email = content.get ( "email" )
  url = config.get ( "url" )
  phone = content.get ( "phone" )
  if not name or not email or not url or not phone :

    raise ValueError ( "❌ El campo 'name' es obligatorio para tipo 'mecard'." )

  return segno.helpers.make_mecard_data ( name = name, email = email, url = url, phone = phone )


##
# @brief Codifica una URL simple.
#
# @param content Diccionario con clave 'url'.
# @return Cadena URL.
#
def dataUrl ( content ) :

  url = content.get ( "url", "" ).strip ()
  if not url:
    raise ValueError ( "❌ El campo 'url' es obligatorio para tipo 'url'." )
  return url


##
# @brief Codifica datos de contacto en formato vCard.
#
# @param content Diccionario con los campos de contacto.
# @return Cadena vCard.
#
def dataVcard ( content ) :

  name = content.get ( "name" )
  displayname = content.get ( "displayname", "" )
  email = content.get ( "email" )
  url = content.get ( "url" )
  phone = content.get ( "phone" )
  if not name or not displayname or not email or not url or not phone :

    raise ValueError ( "❌ El campo 'name' es obligatorio para tipo 'vcard'." )

  return segno.helpers.make_vcard_data ( name = name, displayname = displayname, email = email, url = url, phone = phone )


##
# @brief Codifica información de red WiFi.
#
# @param content Diccionario con SSID, password, etc.
# @return Cadena de configuración WiFi.
#
def dataWifi ( content ) :

  ssid = content.get ( "ssid" )
  password = content.get ( "password", "" )
  security = content.get ( "security", "nopass" )
  if not ssid or not password or not security :

    raise ValueError ( "❌ El campo 'ssid' es obligatorio para tipo 'wifi'." )

  return segno.helpers.make_wifi_data ( ssid = ssid, password = password, security = security )


##
# @brief Genera un objeto QR desde la configuración dada.
#
# @param config Diccionario con la configuración del proyecto.
# @return Objeto QR generado.
#
def generateQr ( config ) :

  content = config.get ( "content", {} )
  if content :
    qr_type = content.get ( "type", "" ).strip ().lower ()
    qr_settings = config.get ( "qr", {} )

    if not qr_type :
      raise ValueError ( "❌ El campo 'type' en 'content' es obligatorio." )

    print ( f"📦 Generando QR tipo '{qr_type}' con parámetros: {qr_settings or 'por defecto'}" )

    qr = None  # Objeto QR

    if qr_type == "url" :

      data = dataUrl ( content )

    elif qr_type == "wifi" :

      data = dataWifi ( content )

    elif qr_type == "geo" :

      data = dataGeo ( content )

    elif qr_type == "mecard" :

      data = dataMecard ( content )

    elif qr_type == "vcard" :

      data = sdataVcard ( content )

    elif qr_type == "epc" :

      data = dataEpc ( content )

    else :

      raise ValueError ( f"❌ Tipo de contenido no soportado: '{qr_type}'" )

    print ( f"✅ Código QR gererado exitosamente." )
    return AddQrSettings ( data, qr_settings )

  else :

    print ( "❌ No existe el nodo \"content\" en el archivo de configuración options.json." )
    exit ( 1 )


##
# @brief Carga la configuración desde un archivo JSON.
#
# @param json_path Ruta al archivo JSON.
# @return Diccionario con la configuración.
#
def load_options ( json_path ) :

  with open ( json_path, "r", encoding = "utf-8" ) as file :
      return json.load ( file )


##
# @brief Convierte una imagen PNG a SVG (logo vectorizado).
#
# @param image_path Ruta al archivo PNG.
# @param output_path Ruta del archivo SVG de salida.
#
def pngToSvg ( image_path, output_path ) :

  pixels2svg ( image_path, output_path )
  print ( "Conversión de Logo a SVG realizada exitosamente." )


##
# @brief Inserta un SVG (QR) dentro de otro SVG (marco).
#
# @param frame_svg_path Ruta al marco SVG.
# @param qr_svg_path Ruta al QR SVG.
# @param output_svg_path Ruta al SVG combinado.
#
def svgIntoSvg ( frame_svg_path, qr_svg_path, output_svg_path ) :

  frame = sg.fromfile ( frame_svg_path )
  qr = sg.fromfile ( qr_svg_path )

  root = qr.getroot ()

  # Mover el logo al centro
  root.moveto ( 10, 10 )

  frame.append ( [ root ] )
  frame.save ( output_svg_path )
  print ( f"✅ SVG final guardado como: {output_svg_path}" )


##
# @brief Carga las opciones desde un archivo JSON.
#
# @param json_path Ruta al archivo JSON.
#
def load_options ( json_path ) :

  with open ( json_path, "r", encoding = "utf-8" ) as file :
    return json.load ( file )
