from handlers import (
  handle_qr,
  handle_svg,
  handle_logo,
  handle_frame,
  handle_output,
  handle_png,
  handle_pdf,
  create_technical_report
)
from core import (
  createProjectDir,
  load_options
)
from context import set_main_output_file, get_main_output_file


##
# @brief Flujo principal del sistema ajecutando las opciones cargadas desde JSON.
#
# @param json Diccionario con la configuración.
#
def options ( json ) :
  # Se cargan las opciones.
  options = load_options ( json )

  project = options.get ( "project" )
  if not project :
    raise ValueError ( "❌ El nodo 'project' debe estar presente." )

  # Se obtiene el nombre del proyecto.
  project_name = project.get ( "name", "" ).strip ()
  if not project_name :
    raise ValueError ( "❌ El nombre del proyecto ('project.name') no puede estar vacío." )

  # Se crea el directorio del proyecto.
  path_project = createProjectDir ( project_name )
  print ( f"📁 Proyecto '{project_name}' creado en: {path_project}" )

  # Se genera el código QR.
  qr = handle_qr ( project )

  # Se genera un archivo SVG del código QR.
  output = project.get ( "output" )
  if output :
    handle_svg ( qr, project, path_project )

  # Se agrega el Logo indicado al archivo SVG del código QR.
  logo = project.get ( "logo", {} )
  if logo :
    handle_logo ( project, path_project )

  # Se crea un marco para el archivo SVG del código QR.
  frame = project.get ( "frame", {} )
  if frame :
    handle_frame ( project, path_project )

  # Se genera un archivo PNG del código QR.
  output = project.get ( "output" )
  if output :
    handle_png ( project, path_project )

  # Se generan los diferentes archivos de salida del código QR.
  output = project.get ( "output" )
  if output :
    handle_output ( qr, project.get ( "output", {} ), path_project, base_filename = project_name )

  # Se genera un archivo PDF del código QR.
  pdf = project.get ( "pdf" )
  if output :
    handle_pdf ( project, path_project )

  # Se genera un informe técnico en PDF del código QR.
  create_technical_report ( options, path_project )
  print ( "Proceso completado." )
