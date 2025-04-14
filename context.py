# context.py
main_output_file = None

def set_main_output_file ( path ) :

  global main_output_file
  main_output_file = path

def get_main_output_file () :

  return main_output_file
