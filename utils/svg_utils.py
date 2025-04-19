import os
from xml.etree import ElementTree as ET


class SvgUtils :
  """
  The SvgUtils class provides utility methods for working with SVG files.
  This includes methods to embed one SVG into another and save the resulting SVG.
  """


  @staticmethod
  def embed_svg ( base_svg_path : str, insert_svg_path : str, output_svg_path : str ) :
    """
    Embeds an SVG file into another SVG file and saves the resulting SVG.

    This method takes two SVG files: a base SVG and an insert SVG. The insert SVG
    will be embedded into the base SVG, and the resulting SVG will be saved to the
    specified output path.

    Args:
        base_svg_path (str): The file path of the base SVG file where the insert SVG will be embedded.
        insert_svg_path (str): The file path of the SVG file to be embedded into the base SVG.
        output_svg_path (str): The file path where the resulting SVG with the embedded insert SVG will be saved.

    Returns:
        None

    This method modifies the base SVG file by embedding the contents of the insert SVG into it.
    """
    base_tree = ET.parse ( base_svg_path )
    base_root = base_tree.getroot ()

    insert_tree = ET.parse ( insert_svg_path )
    insert_root = insert_tree.getroot ()

    # Insert the second SVG content into the first
    for elem in insert_root :
      base_root.append ( elem )

    ET.ElementTree ( base_root ).write ( output_svg_path, encoding = 'utf-8', xml_declaration = True )
