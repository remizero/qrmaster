HOW TO INSTALL
==============

The installation process presented here is only applicable to Linux
platforms. It has not been tested on other platforms, but you are free
to port this application to any platform you need and can report and
contribute any modifications to be included in the project.

Requirements
------------

-  Python 3.x
-  pip (Python package installer)
-  cairosvg
-  fpdf
-  jsonschema
-  pixels2svg
-  segno
-  svgutils
-  svgwrite

Via PyPI
--------

.. code:: bash

   pip install qrmaster

Via source
----------

Download
~~~~~~~~

.. code:: bash

    git clone https://github.com/remizero/qrmaster.git

Install
~~~~~~~

Virtual Environment
^^^^^^^^^^^^^^^^^^^

To create the virtual environment.

.. code:: bash

    python3 -m venv venv
    source venv/bin/activate

Install Dependencies
^^^^^^^^^^^^^^^^^^^^

To install the required dependencies, run the following command:

.. code:: bash

   pip install -r requirements.txt
